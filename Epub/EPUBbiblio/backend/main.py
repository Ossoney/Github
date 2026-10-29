from fastapi import FastAPI, BackgroundTasks, Depends, HTTPException, status, Query, Header
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import func, or_, text
from datetime import datetime

from database import SessionLocal, Book, User, UserSession, UserProgress, BookReview, BookReport, Library, UserLibrary, BookLibrary, UserDownload
from epub_parser import scan_directory, scan_state
from watcher import watcher
from paths import LOG_PATH, COVERS_DIR, SETTINGS_PATH, get_or_create_recovery_key, RECOVERY_KEY_PATH
from auth import (
    get_db, hash_password, verify_password, create_user_session,
    get_optional_user, get_current_user, require_master, get_token_from_request
)

import os
import json
import logging
import subprocess
import platform
import secrets
import zipfile
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import time
import re

logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

PROMO_TEXT = """
Epub Biblio es un programa freeware que organiza visualmente tus archivos EPUB.
En resumen: extrae portadas y metadatos para armar una biblioteca visual elegante.
No te preocupes, los archivos originales se mantienen intactos.
---------------------------------------------------------------
Si el programa te ha sido útil invítame a un café en paypal.me/ossoney.
Envíame 1$ - 2$ - 3$ o lo que te apetezca.
"""
print(PROMO_TEXT)
logging.info("Iniciando EPUB Biblio...")

app = FastAPI(title="EPUB Biblio API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_cache_control_header(request, call_next):
    response = await call_next(request)
    path = request.url.path
    if path == "/" or path.endswith(".html"):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
    return response

os.makedirs(COVERS_DIR, exist_ok=True)
app.mount("/static/covers", StaticFiles(directory=COVERS_DIR), name="covers")

def get_settings():
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, 'r') as f:
                return json.load(f)
        except Exception:
            pass
    return {"watch_path": None}

def save_settings(settings):
    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f)

@app.on_event("startup")
async def startup_event():
    db = SessionLocal()
    try:
        settings = get_settings()
        fallback_path = settings.get("watch_path")
        logging.info("Iniciando vigía automático (Watchdog) para todas las bibliotecas...")
        watcher.update_watches_from_db(db, fallback_path=fallback_path)
    except Exception as e:
        logging.error(f"Error al iniciar vigía automático: {e}")
    finally:
        db.close()

    # Reconciliación no bloqueante en hilo background al arrancar
    try:
        from reconcile import start_reconciliation_thread
        start_reconciliation_thread()
    except Exception as e:
        logging.error(f"Error iniciando reconciliación al arranque: {e}")

# ==========================================
# PYDANTIC SCHEMAS
# ==========================================
class UserAuthRequest(BaseModel):
    username: str
    password: str

class ReviewRequest(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = ""

class ProgressRequest(BaseModel):
    progress: str
    percentage: Optional[int] = 0

class RoleUpdateRequest(BaseModel):
    role: str

class UserDownloadLimitRequest(BaseModel):
    daily_limit: Optional[int] = 1  # None o -1 para ilimitado, o número entero (0, 1, 2, etc.)
    # Compatibilidad hacia atrás si frontend enviara weekly_limit:
    weekly_limit: Optional[int] = None

class LibraryCreateRequest(BaseModel):
    name: str
    path: Optional[str] = ""
    library_type: Optional[str] = "all"  # "all", "epub", "pdf"

class LibraryUpdateRequest(BaseModel):
    name: str
    path: Optional[str] = ""
    library_type: Optional[str] = "all"

class UserLibrariesUpdateRequest(BaseModel):
    library_ids: List[int]

class PasswordResetWithKeyRequest(BaseModel):
    username: str
    recovery_key: str
    new_password: str

class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str

class AdminPasswordResetRequest(BaseModel):
    new_password: str

class BookReportRequest(BaseModel):
    report_type: str = "other"   # 'wrong_genre' | 'other'
    message: str

# ==========================================
# AUTENTICACIÓN Y REGISTRO (Puntos 2 y 3)
# ==========================================

@app.get("/api/auth/status")
def auth_status(
    db: Session = Depends(get_db),
    optional_user: Optional[User] = Depends(get_optional_user)
):
    master_count = db.query(User).filter(User.role == "master").count()
    has_master = master_count > 0

    if optional_user:
        return {
            "authenticated": True,
            "has_master": has_master,
            "user": {
                "id": optional_user.id,
                "username": optional_user.username,
                "role": optional_user.role,
                "status": optional_user.status
            }
        }
    return {
        "authenticated": False,
        "has_master": has_master,
        "user": None
    }

@app.post("/api/auth/register-master")
def register_master(payload: UserAuthRequest, db: Session = Depends(get_db)):
    """Crea la cuenta del Administrador Master inicial si aún no existe ninguno."""
    existing_master = db.query(User).filter(User.role == "master").first()
    if existing_master:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un usuario Administrador Master configurado."
        )

    clean_username = payload.username.strip()
    if len(clean_username) < 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de usuario debe tener al menos 3 caracteres."
        )
    if len(payload.password) < 4:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña debe tener al menos 4 caracteres."
        )

    existing_user = db.query(User).filter(User.username == clean_username).first()
    if existing_user:
        existing_user.password_hash = hash_password(payload.password)
        existing_user.role = "master"
        existing_user.status = "active"
        db.commit()
        master_user = existing_user
    else:
        master_user = User(
            username=clean_username,
            password_hash=hash_password(payload.password),
            role="master",
            status="active"
        )
        db.add(master_user)
        db.commit()
        db.refresh(master_user)

    session = create_user_session(db, master_user.id)
    logging.info(f"Usuario Master creado con éxito: {master_user.username}")
    return {
        "message": "Administrador Master creado con éxito.",
        "token": session.token,
        "user": {
            "id": master_user.id,
            "username": master_user.username,
            "role": master_user.role,
            "status": master_user.status
        }
    }

@app.post("/api/auth/register")
def register_user(payload: UserAuthRequest, db: Session = Depends(get_db)):
    """Auto-registro de usuarios en modo 'pending' (a la espera de aprobación por el Master)."""
    clean_username = payload.username.strip()
    if len(clean_username) < 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de usuario debe tener al menos 3 caracteres."
        )
    if len(payload.password) < 4:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña debe tener al menos 4 caracteres."
        )

    existing = db.query(User).filter(User.username == clean_username).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de usuario ya está registrado."
        )

    new_user = User(
        username=clean_username,
        password_hash=hash_password(payload.password),
        role="reader",
        status="pending"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    logging.info(f"Nuevo usuario auto-registrado (pendiente): {new_user.username}")
    return {
        "message": "Cuenta creada con éxito. Está pendiente de aprobación por el administrador.",
        "status": "pending"
    }

@app.post("/api/auth/login")
def login_user(payload: UserAuthRequest, db: Session = Depends(get_db)):
    clean_username = payload.username.strip()
    user = db.query(User).filter(User.username == clean_username).first()

    if not user or not verify_password(user.password_hash, payload.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nombre de usuario o contraseña incorrectos."
        )

    if user.status == "pending":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tu cuenta está pendiente de aprobación por el administrador."
        )

    if user.status == "rejected":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tu solicitud de cuenta ha sido rechazada por el administrador."
        )

    session = create_user_session(db, user.id)
    logging.info(f"Inicio de sesión exitoso: {user.username} ({user.role})")
    return {
        "message": "Inicio de sesión correcto.",
        "token": session.token,
        "user": {
            "id": user.id,
            "username": user.username,
            "role": user.role,
            "status": user.status
        }
    }

@app.post("/api/auth/logout")
def logout_user(
    db: Session = Depends(get_db),
    auth_token: Optional[str] = Depends(get_token_from_request)
):
    if auth_token:
        db.query(UserSession).filter(UserSession.token == auth_token).delete()
        db.commit()
    return {"message": "Sesión cerrada correctamente."}

@app.post("/api/auth/reset-with-recovery-key")
def reset_with_recovery_key(payload: PasswordResetWithKeyRequest, db: Session = Depends(get_db)):
    """Restablece la contraseña de cualquier usuario usando la clave maestra de recuperación del servidor."""
    server_key = get_or_create_recovery_key().strip().upper()
    provided_key = payload.recovery_key.strip().upper()

    if not secrets.compare_digest(server_key, provided_key):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="La clave de recuperación del servidor no es válida. Revisa el archivo 'recovery_key.txt' en tu carpeta Documents/Epubbiblio."
        )

    clean_username = payload.username.strip()
    user = db.query(User).filter(User.username == clean_username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró ningún usuario con el identificador '{clean_username}'."
        )

    if len(payload.new_password) < 4:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La nueva contraseña debe tener al menos 4 caracteres."
        )

    user.password_hash = hash_password(payload.new_password)
    # Invalidar sesiones activas
    db.query(UserSession).filter(UserSession.user_id == user.id).delete()
    db.commit()
    logging.info(f"Contraseña de {user.username} restablecida con clave de recuperación del servidor.")
    return {"message": f"Contraseña restablecida con éxito para {user.username}. Ya puedes iniciar sesión con tu nueva contraseña."}

@app.post("/api/auth/change-password")
def change_my_password(
    payload: PasswordChangeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Permite al usuario autenticado actual cambiar su propia contraseña."""
    if not verify_password(current_user.password_hash, payload.current_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña actual no es correcta."
        )
    if len(payload.new_password) < 4:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La nueva contraseña debe tener al menos 4 caracteres."
        )
    current_user.password_hash = hash_password(payload.new_password)
    db.commit()
    logging.info(f"El usuario {current_user.username} ha actualizado su contraseña.")
    return {"message": "Contraseña actualizada correctamente."}

# ==========================================
# GESTIÓN DE BIBLIOTECAS (MULTI-LIBRARY)
# ==========================================

# Grupos y orden de afinidad literaria para bibliotecas y géneros
LITERARY_GROUPS = [
    {"group": "General", "items": ["Biblioteca Principal"]},
    {"group": "Narrativa e Historia", "items": ["Novela y Narrativa", "Novela Histórica", "Aventuras y Acción", "Sagas Familiares y Generacionales", "Narrativa Intimista y Psicológica", "Historia Militar y Bélica", "Viajes, Expediciones y Rutas"]},
    {"group": "Misterio y Suspense", "items": ["Policial y Novela Negra", "Intriga, Suspense", "Terror", "True Crime y Crónica Negra"]},
    {"group": "Ficción Especulativa", "items": ["Ciencia Ficción", "Ciencia Ficción (VIP)", "Ciencia Ficción (Exclusiva)", "Ciencia Ficción Distópica", "Fantasía", "Mitología, Esoterismo y Ocultismo"]},
    {"group": "Romance y Adultos", "items": ["Novela Romántica", "Romance Histórico (Regencia y Época)", "Romance Contemporáneo y Comedia", "Romance Paranormal y Fantástico", "Erótica y Adultos"]},
    {"group": "Cuentos, Arte y Humor", "items": ["Relatos y Cuentos", "Poesía", "Teatro", "Humor y Sátira", "Cómics, Novela Gráfica y Guiones"]},
    {"group": "Infantil y Juvenil", "items": ["Infantil y Juvenil"]},
    {"group": "Desarrollo y Bienestar", "items": ["Autoayuda y Crecimiento Personal", "Salud, Nutrición y Bienestar", "Cocina y Gastronomía"]},
    {"group": "Sociedad, Ciencia y Tecnología", "items": ["Economía, Negocios y Finanzas", "Informática y Tecnología Digital", "Divulgación y Ciencia", "Biografías, Memorias", "Ensayo, Filosofía"]}
]

LITERARY_ORDER = [
    "Biblioteca Principal",
    "Novela y Narrativa",
    "Sagas Familiares y Generacionales",
    "Narrativa Intimista y Psicológica",
    "Novela Histórica",
    "Aventuras y Acción",
    "Historia Militar y Bélica",
    "Viajes, Expediciones y Rutas",
    "Policial y Novela Negra",
    "Intriga, Suspense",
    "Terror",
    "True Crime y Crónica Negra",
    "Ciencia Ficción_NORMAL",
    "Ciencia Ficción_VIP",
    "Ciencia Ficción Distópica",
    "Fantasía",
    "Mitología, Esoterismo y Ocultismo",
    "Novela Romántica",
    "Romance Histórico (Regencia y Época)",
    "Romance Contemporáneo y Comedia",
    "Romance Paranormal y Fantástico",
    "Erótica y Adultos",
    "Relatos y Cuentos",
    "Poesía",
    "Teatro",
    "Humor y Sátira",
    "Cómics, Novela Gráfica y Guiones",
    "Infantil y Juvenil",
    "Autoayuda y Crecimiento Personal",
    "Salud, Nutrición y Bienestar",
    "Cocina y Gastronomía",
    "Economía, Negocios y Finanzas",
    "Informática y Tecnología Digital",
    "Divulgación y Ciencia",
    "Biografías, Memorias",
    "Ensayo, Filosofía"
]

def get_literary_sort_key(lib_name: str) -> int:
    from database import normalize_for_search
    name_clean = normalize_for_search(lib_name).lower()
    is_vip = "vip" in name_clean or "exclusiva" in name_clean

    for idx, target in enumerate(LITERARY_ORDER):
        if target == "Ciencia Ficción_NORMAL":
            if "ciencia ficcion" in name_clean and not is_vip:
                return idx
        elif target == "Ciencia Ficción_VIP":
            if is_vip:
                return idx
        else:
            target_clean = normalize_for_search(target).lower()
            if target_clean in name_clean:
                return idx
    return len(LITERARY_ORDER)

def get_literary_group(lib_name: str) -> str:
    from database import normalize_for_search
    name_clean = normalize_for_search(lib_name).lower()
    for g in LITERARY_GROUPS:
        for item in g["items"]:
            if normalize_for_search(item).lower() in name_clean:
                return g["group"]
    return "Otros"

@app.get("/api/libraries")
def get_libraries(
    db: Session = Depends(get_db),
    optional_user: Optional[User] = Depends(get_optional_user)
):
    """Devuelve las bibliotecas accesibles para el usuario actual ordenadas por sentido literario."""
    is_master = optional_user and optional_user.role == "master"

    if not optional_user or is_master:
        libs = db.query(Library).all()
        if not is_master:
            # Usuarios anónimos no ven bibliotecas exclusivas de PDF
            libs = [l for l in libs if (l.library_type or "all") != "pdf"]
    else:
        allowed_ids = [ul.library_id for ul in optional_user.libraries]
        libs = db.query(Library).filter(Library.id.in_(allowed_ids)).all()
        # Lectores regulares no ven bibliotecas de tipo 'pdf'
        libs = [l for l in libs if (l.library_type or "all") != "pdf"]

    libs.sort(key=lambda l: (get_literary_sort_key(l.name), l.name))

    result = []
    for lib in libs:
        book_count = db.query(BookLibrary).filter(BookLibrary.library_id == lib.id).count()
        result.append({
            "id": lib.id,
            "name": lib.name,
            "path": lib.path or "",
            "library_type": lib.library_type or "all",
            "book_count": book_count,
            "group": get_literary_group(lib.name),
            "created_at": lib.created_at.strftime("%Y-%m-%d %H:%M") if lib.created_at else None
        })
    return result

@app.post("/api/admin/libraries")
def create_library(
    payload: LibraryCreateRequest,
    db: Session = Depends(get_db),
    master_user: User = Depends(require_master)
):
    name = payload.name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="El nombre de la biblioteca no puede estar vacío.")
    
    existing = db.query(Library).filter(Library.name == name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Ya existe una biblioteca con este nombre.")
        
    lib = Library(
        name=name, 
        path=payload.path.strip() if payload.path else "",
        library_type=payload.library_type if payload.library_type else "all"
    )
    db.add(lib)
    db.commit()
    db.refresh(lib)
    logging.info(f"Biblioteca creada por {master_user.username}: {lib.name} (ID: {lib.id}, Tipo: {lib.library_type})")
    return {"id": lib.id, "name": lib.name, "path": lib.path, "library_type": lib.library_type, "book_count": 0}

@app.put("/api/admin/libraries/{library_id}")
def update_library(
    library_id: int,
    payload: LibraryUpdateRequest,
    db: Session = Depends(get_db),
    master_user: User = Depends(require_master)
):
    lib = db.query(Library).filter(Library.id == library_id).first()
    if not lib:
        raise HTTPException(status_code=404, detail="Biblioteca no encontrada.")
        
    name = payload.name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="El nombre no puede estar vacío.")
        
    existing = db.query(Library).filter(Library.name == name, Library.id != library_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Ya existe otra biblioteca con este nombre.")
        
    lib.name = name
    if payload.path is not None:
        lib.path = payload.path.strip()
    if payload.library_type is not None:
        lib.library_type = payload.library_type
    db.commit()
    return {"message": f"Biblioteca '{lib.name}' actualizada."}

@app.delete("/api/admin/libraries/{library_id}")
def delete_library(
    library_id: int,
    db: Session = Depends(get_db),
    master_user: User = Depends(require_master)
):
    if library_id in [1, 2]:
        raise HTTPException(status_code=400, detail="No se pueden eliminar las bibliotecas protegidas de sistema (IDs 1 y 2).")
        
    lib = db.query(Library).filter(Library.id == library_id).first()
    if not lib:
        raise HTTPException(status_code=404, detail="Biblioteca no encontrada.")
        
    name = lib.name
    # Eliminar vínculos temáticos
    db.query(BookLibrary).filter(BookLibrary.library_id == library_id).delete()
    db.query(UserLibrary).filter(UserLibrary.library_id == library_id).delete()
    db.delete(lib)
    db.commit()
    logging.info(f"Biblioteca temática {name} eliminada por {master_user.username}")
    return {"message": f"Biblioteca '{name}' eliminada correctamente."}

@app.post("/api/admin/libraries/{library_id}/scan")
def scan_specific_library(
    library_id: int,
    background_tasks: BackgroundTasks,
    directory: Optional[str] = None,
    db: Session = Depends(get_db),
    master_user: User = Depends(require_master)
):
    lib = db.query(Library).filter(Library.id == library_id).first()
    if not lib:
        raise HTTPException(status_code=404, detail="Biblioteca no encontrada.")
        
    if scan_state["running"]:
        return {"message": "Ya hay un escaneo en curso. Puedes ver su progreso en Mantenimiento.", "status": scan_state}

    dir_to_scan = directory if directory else lib.path
    if not dir_to_scan or not os.path.exists(dir_to_scan):
        raise HTTPException(status_code=400, detail=f"Ruta inválida o inexistente: '{dir_to_scan}'")
        
    lib.path = dir_to_scan
    db.commit()
    try:
        watcher.update_watches_from_db(db)
    except Exception as e:
        logging.error(f"Error actualizando vigía de bibliotecas: {e}")
    
    background_tasks.add_task(scan_directory, dir_to_scan, library_id, lib.name)
    return {"message": f"Escaneo de '{lib.name}' iniciado en segundo plano en: {dir_to_scan}"}

@app.get("/api/admin/users/{user_id}/libraries")
def get_user_libraries(
    user_id: int,
    db: Session = Depends(get_db),
    master_user: User = Depends(require_master)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    return [ul.library_id for ul in user.libraries]

@app.post("/api/admin/users/{user_id}/libraries")
def set_user_libraries(
    user_id: int,
    payload: UserLibrariesUpdateRequest,
    db: Session = Depends(get_db),
    master_user: User = Depends(require_master)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
        
    db.query(UserLibrary).filter(UserLibrary.user_id == user_id).delete()
    
    for lib_id in payload.library_ids:
        lib_exists = db.query(Library.id).filter(Library.id == lib_id).first()
        if lib_exists:
            db.add(UserLibrary(user_id=user_id, library_id=lib_id))
            
    db.commit()
    logging.info(f"Bibliotecas actualizadas para {user.username}: {payload.library_ids}")
    return {"message": f"Bibliotecas asignadas a {user.username} correctamente."}

# ==========================================
# SINCRONIZACIÓN DE VALORACIONES OPEN LIBRARY
# ==========================================

ratings_sync_state = {
    "running": False,
    "total": 0,
    "processed": 0,
    "found": 0,
    "current_book": "",
    "stop_requested": False
}

def download_cover_from_openlibrary(doc: dict, book: Book, db: Session) -> bool:
    """
    Descarga la portada desde Open Library si el libro no tiene una portada asignada aún.
    Verifica que la imagen sea real (más de 500 bytes para ignorar el píxel en blanco 1x1 de Open Library).
    """
    try:
        cover_id = doc.get("cover_i")
        cover_url = None
        if cover_id:
            cover_url = f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"
        elif doc.get("cover_edition_key"):
            cover_url = f"https://covers.openlibrary.org/b/olid/{doc['cover_edition_key']}-M.jpg"
        elif getattr(book, 'isbn', None):
            clean_isbn = re.sub(r'[^0-9X]', '', str(book.isbn).upper())
            if len(clean_isbn) in (10, 13):
                cover_url = f"https://covers.openlibrary.org/b/isbn/{clean_isbn}-M.jpg"

        if not cover_url:
            return False

        req = urllib.request.Request(cover_url, headers={'User-Agent': 'EpubBiblio/1.0'})
        with urllib.request.urlopen(req, timeout=4) as resp:
            data = resp.read()
            # Open Library devuelve una imagen en blanco de 43 bytes si no tiene portada
            if len(data) > 500:
                path_hash = hashlib.md5((book.file_path or book.title).encode()).hexdigest()
                cover_filename = f"ol_cover_{path_hash}.jpg"
                disk_cover_path = os.path.join(COVERS_DIR, cover_filename)
                with open(disk_cover_path, "wb") as f:
                    f.write(data)
                book.cover_path = f"/static/covers/{cover_filename}"
                db.commit()
                logging.info(f"Open Library: Portada descargada con éxito para '{book.title}'")
                return True
    except Exception as e:
        logging.info(f"No se pudo descargar portada de Open Library para '{book.title}': {e}")
    return False

def fetch_openlibrary_rating_for_book(book: Book, db: Session, force: bool = False) -> tuple[str, str]:
    """
    Consulta en tiempo real la valoración de un libro en Open Library y actualiza la base de datos.
    Devuelve (status, mensaje):
      - status: 'found' | 'unrated' | 'not_found' | 'cached' | 'error'
    """
    if not force and book.external_rating_synced == 1 and book.external_rating is not None:
        if book.external_rating > 0:
            return "cached", f"Valoración cargada desde caché local ({book.external_rating} ⭐)."
        else:
            return "unrated", "El libro ya fue consultado anteriormente y no tenía valoraciones registradas en Open Library."

    try:
        # 1. Quitar corchetes, paréntesis y su contenido
        raw_title = re.sub(r'[\(\[\{].*?[\)\]\}]', ' ', book.title or '')
        # 2. Reemplazar cualquier puntuación con espacio para no romper la sintaxis Lucene de Open Library
        clean_title = re.sub(r'[^a-zA-Z0-9áéíóúÁÉÍÓÚñÑüÜ\s]', ' ', raw_title)
        clean_title = ' '.join(clean_title.split())

        raw_author = re.sub(r'[\(\[\{].*?[\)\]\}]', ' ', book.author or '')
        clean_author = re.sub(r'[^a-zA-Z0-9áéíóúÁÉÍÓÚñÑüÜ\s]', ' ', raw_author)
        clean_author = ' '.join(clean_author.split())

        if not clean_title:
            book.external_rating_synced = 1
            db.commit()
            return "not_found", "Título no válido para búsqueda."

        docs = []

        # -------------------------------------------------------------
        # ESTRATEGIA 1: Búsqueda exacta por ISBN si el EPUB lo incluye
        # -------------------------------------------------------------
        raw_isbn = getattr(book, 'isbn', '') or ''
        # Si el libro aún no tiene el campo isbn en memoria o BD, intentar leerlo del archivo si existe
        if not raw_isbn and book.file_path and os.path.exists(book.file_path):
            try:
                from epub_parser import extract_isbn_from_text
                with zipfile.ZipFile(book.file_path, 'r') as z:
                    for name in z.namelist():
                        if name.lower().endswith('.opf'):
                            soup = BeautifulSoup(z.read(name).decode('utf-8-sig', errors='ignore'), "xml")
                            for id_tag in soup.find_all(['dc:identifier', 'identifier']):
                                cand = extract_isbn_from_text(id_tag.get_text())
                                if cand:
                                    raw_isbn = cand
                                    book.isbn = cand
                                    db.commit()
                                    break
                            break
            except Exception:
                pass

        if raw_isbn:
            clean_isbn = re.sub(r'[^0-9X]', '', str(raw_isbn).upper())
            if len(clean_isbn) in (10, 13):
                try:
                    url_isbn = f"https://openlibrary.org/search.json?isbn={clean_isbn}&limit=2"
                    req_isbn = urllib.request.Request(url_isbn, headers={'User-Agent': 'EpubBiblio/1.0'})
                    with urllib.request.urlopen(req_isbn, timeout=4) as resp_isbn:
                        data_isbn = json.loads(resp_isbn.read().decode('utf-8'))
                        docs = data_isbn.get('docs', [])
                        if docs:
                            logging.info(f"Open Library: Libro localizado exactamente por ISBN ({clean_isbn}) para '{book.title}'")
                except Exception as e_isbn:
                    logging.info(f"Fallo consulta por ISBN {clean_isbn}: {e_isbn}")

        # -------------------------------------------------------------
        # ESTRATEGIA ESTÁNDAR: Búsqueda combinada Título + Autor
        # -------------------------------------------------------------
        if not docs:
            q = urllib.parse.quote(f"{clean_title} {clean_author}".strip())
            url = f"https://openlibrary.org/search.json?q={q}&limit=2"
            req = urllib.request.Request(url, headers={'User-Agent': 'EpubBiblio/1.0 (contact@epubbiblio.local)'})
            try:
                with urllib.request.urlopen(req, timeout=5) as resp:
                    data = json.loads(resp.read().decode('utf-8'))
                    docs = data.get('docs', [])
            except Exception:
                docs = []

        # -------------------------------------------------------------
        # FALLBACK A: Búsqueda solo por Título limpio
        # -------------------------------------------------------------
        if not docs and len(clean_title.split()) >= 2:
            q_title = urllib.parse.quote(clean_title)
            url_t = f"https://openlibrary.org/search.json?title={q_title}&limit=2"
            req_t = urllib.request.Request(url_t, headers={'User-Agent': 'EpubBiblio/1.0'})
            try:
                with urllib.request.urlopen(req_t, timeout=4) as resp_t:
                    data_t = json.loads(resp_t.read().decode('utf-8'))
                    docs = data_t.get('docs', [])
            except Exception:
                pass

        # -------------------------------------------------------------
        # ESTRATEGIA 2: Búsqueda por palabras clave esenciales + apellido
        # (Si el título original tenía subtítulos largos o nombres compuestos)
        # -------------------------------------------------------------
        if not docs:
            stopwords = {'de', 'del', 'la', 'las', 'el', 'los', 'en', 'un', 'una', 'unos', 'unas', 'y', 'e', 'o', 'u', 'a', 'al', 'con', 'por', 'para', 'lo', 'se', 'su', 'sus'}
            title_words = [w for w in clean_title.split() if w.lower() not in stopwords and len(w) > 2]
            key_title_words = title_words[:3]
            if key_title_words:
                # Extraer apellido significativo del autor
                raw_auth_parts = (book.author or '').replace(',', ' ').split()
                auth_part = raw_auth_parts[0] if (',' in (book.author or '')) else (raw_auth_parts[-1] if raw_auth_parts else '')
                clean_auth_kw = re.sub(r'[^a-zA-Z0-9áéíóúÁÉÍÓÚñÑüÜ]', '', auth_part)

                kw_query = ' '.join(key_title_words)
                if clean_auth_kw and len(clean_auth_kw) > 2:
                    kw_query += f" {clean_auth_kw}"

                if kw_query.strip() and kw_query != f"{clean_title} {clean_author}":
                    try:
                        q_kw = urllib.parse.quote(kw_query.strip())
                        url_kw = f"https://openlibrary.org/search.json?q={q_kw}&limit=2"
                        req_kw = urllib.request.Request(url_kw, headers={'User-Agent': 'EpubBiblio/1.0'})
                        with urllib.request.urlopen(req_kw, timeout=4) as resp_kw:
                            data_kw = json.loads(resp_kw.read().decode('utf-8'))
                            docs = data_kw.get('docs', [])
                            if docs:
                                logging.info(f"Open Library: Libro rescatado por palabras clave ('{kw_query}') para '{book.title}'")
                    except Exception:
                        pass

        if docs and 'key' in docs[0]:
            # Si el libro no tiene portada, intentar descargarla de Open Library
            if not book.cover_path or book.cover_path.strip() == "":
                download_cover_from_openlibrary(docs[0], book, db)

            work_key = docs[0]['key']
            r_url = f"https://openlibrary.org{work_key}/ratings.json"
            r_req = urllib.request.Request(r_url, headers={'User-Agent': 'EpubBiblio/1.0'})
            with urllib.request.urlopen(r_req, timeout=4) as r_resp:
                r_data = json.loads(r_resp.read().decode('utf-8'))
                avg = r_data.get('summary', {}).get('average')
                count = r_data.get('summary', {}).get('count')
                if avg is not None and avg > 0:
                    book.external_rating = round(float(avg), 1)
                    book.external_reviews_count = int(count or 1)
                    book.external_rating_synced = 1
                    db.commit()
                    return "found", f"¡Valoración encontrada en Open Library: {book.external_rating} ⭐ ({book.external_reviews_count} opiniones)!"
                else:
                    book.external_rating = 0.0
                    book.external_reviews_count = 0
                    book.external_rating_synced = 1
                    db.commit()
                    return "unrated", "Libro localizado en Open Library, pero aún ningún lector lo ha puntuado allí."
        else:
            book.external_rating = 0.0
            book.external_reviews_count = 0
            book.external_rating_synced = 1
            db.commit()
            return "not_found", "No se encontró este libro ni edición en el catálogo de Open Library."
    except Exception as e:
        logging.warning(f"Error consultando Open Library para '{book.title}': {e}")
        return "error", f"Error de conexión con Open Library: {e}"

def sync_openlibrary_ratings_worker():
    global ratings_sync_state
    ratings_sync_state["running"] = True
    ratings_sync_state["stop_requested"] = False
    
    db = SessionLocal()
    try:
        unsynced_books = (
            db.query(Book)
            .filter((Book.external_rating_synced == 0) | (Book.external_rating_synced.is_(None)))
            .all()
        )
        ratings_sync_state["total"] = len(unsynced_books)
        ratings_sync_state["processed"] = 0
        ratings_sync_state["found"] = 0
        logging.info(f"Iniciando sincronización de valoraciones con Open Library para {len(unsynced_books)} libros.")

        for idx, book in enumerate(unsynced_books):
            if ratings_sync_state.get("stop_requested"):
                logging.info("Sincronización de valoraciones detenida por el usuario.")
                break

            ratings_sync_state["current_book"] = f"{book.title} ({book.author})"
            status, _ = fetch_openlibrary_rating_for_book(book, db)
            if status == "found":
                ratings_sync_state["found"] += 1
            ratings_sync_state["processed"] += 1

            time.sleep(0.5)

        db.commit()
    except Exception as e:
        logging.error(f"Error en tarea de sincronización de Open Library: {e}")
    finally:
        ratings_sync_state["running"] = False
        ratings_sync_state["current_book"] = ""
        db.close()

@app.post("/api/admin/sync-ratings/start")
def start_sync_ratings(
    background_tasks: BackgroundTasks,
    master_user: User = Depends(require_master)
):
    global ratings_sync_state
    if ratings_sync_state["running"]:
        return {"message": "La sincronización ya está en curso.", "status": ratings_sync_state}
    background_tasks.add_task(sync_openlibrary_ratings_worker)
    return {"message": "Sincronización desde Open Library iniciada en segundo plano."}

@app.post("/api/admin/sync-ratings/stop")
def stop_sync_ratings(
    master_user: User = Depends(require_master)
):
    global ratings_sync_state
    if ratings_sync_state["running"]:
        ratings_sync_state["stop_requested"] = True
        return {"message": "Detención solicitada. Se detendrá en breve."}
    return {"message": "No hay sincronización activa."}

@app.get("/api/admin/sync-ratings/status")
def get_sync_ratings_status(
    master_user: User = Depends(require_master)
):
    global ratings_sync_state
    return ratings_sync_state

@app.post("/api/admin/reconcile/start")
def start_reconciliation_api(
    master_user: User = Depends(require_master)
):
    from reconcile import start_reconciliation_thread, reconciliation_state
    if reconciliation_state["running"]:
        return {"message": "La reconciliación ya está en curso.", "status": reconciliation_state}
    start_reconciliation_thread()
    return {"message": "Reconciliación de catálogo con disco iniciada en segundo plano.", "status": reconciliation_state}

@app.get("/api/admin/reconcile/status")
def get_reconciliation_status(
    master_user: User = Depends(require_master)
):
    from reconcile import reconciliation_state
    return reconciliation_state

# ==========================================
# PANEL DE ADMINISTRACIÓN MASTER (Puntos 1 y 3)
# ==========================================

@app.get("/api/admin/users")
def get_admin_users(
    db: Session = Depends(get_db),
    master_user: User = Depends(require_master)
):
    from datetime import timedelta
    one_day_ago = datetime.utcnow() - timedelta(days=1)
    users = db.query(User).order_by(User.created_at.desc()).all()

    result = []
    for u in users:
        recent_dl = db.query(UserDownload).filter(
            UserDownload.user_id == u.id,
            UserDownload.downloaded_at >= one_day_ago
        ).count()

        result.append({
            "id": u.id,
            "username": u.username,
            "role": u.role,
            "status": u.status,
            "assigned_libraries": [ul.library_id for ul in u.libraries],
            "daily_download_limit": u.daily_download_limit,
            "weekly_download_limit": u.daily_download_limit, # compatibilidad
            "downloads_today": recent_dl,
            "downloads_this_week": recent_dl, # compatibilidad
            "created_at": u.created_at.strftime("%Y-%m-%d %H:%M") if u.created_at else None
        })
    return result

@app.post("/api/admin/users/{user_id}/approve")
def approve_user(
    user_id: int,
    db: Session = Depends(get_db),
    master_user: User = Depends(require_master)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    user.status = "active"
    
    # Asignar la Biblioteca Principal por defecto si no tiene asignada ninguna
    if not user.libraries:
        main_lib = db.query(Library).filter(Library.id == 1).first()
        if main_lib:
            db.add(UserLibrary(user_id=user.id, library_id=main_lib.id))

    db.commit()
    logging.info(f"Usuario {user.username} aprobado por {master_user.username}")
    return {"message": f"Usuario {user.username} aprobado y activado."}

@app.post("/api/admin/users/{user_id}/reject")
def reject_user(
    user_id: int,
    db: Session = Depends(get_db),
    master_user: User = Depends(require_master)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    if user.id == master_user.id:
        raise HTTPException(status_code=400, detail="No puedes rechazar tu propia cuenta.")
    user.status = "rejected"
    db.query(UserSession).filter(UserSession.user_id == user.id).delete()
    db.commit()
    logging.info(f"Usuario {user.username} rechazado por {master_user.username}")
    return {"message": f"Usuario {user.username} rechazado."}

@app.post("/api/admin/users/{user_id}/logout")
def force_logout_user(
    user_id: int,
    db: Session = Depends(get_db),
    master_user: User = Depends(require_master)
):
    """Cierra forzosamente todas las sesiones activas del usuario indicado."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    deleted_count = db.query(UserSession).filter(UserSession.user_id == user.id).delete()
    db.commit()
    logging.info(f"Sesiones de {user.username} cerradas por el Master {master_user.username} (total: {deleted_count})")
    return {"message": f"Se ha cerrado la sesión de {user.username} correctamente.", "closed_sessions": deleted_count}

@app.delete("/api/admin/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    master_user: User = Depends(require_master)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    if user.id == master_user.id:
        raise HTTPException(status_code=400, detail="No puedes eliminar tu propia cuenta.")
    username = user.username
    db.delete(user)
    db.commit()
    logging.info(f"Usuario {username} eliminado por {master_user.username}")
    return {"message": f"Usuario {username} eliminado."}

@app.post("/api/admin/users/{user_id}/role")
def change_user_role(
    user_id: int,
    payload: RoleUpdateRequest,
    db: Session = Depends(get_db),
    master_user: User = Depends(require_master)
):
    if payload.role not in ["master", "reader"]:
        raise HTTPException(status_code=400, detail="Rol inválido. Debe ser 'master' o 'reader'.")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    user.role = payload.role
    db.commit()
    return {"message": f"Rol de {user.username} actualizado a {payload.role}."}

@app.post("/api/admin/users/{user_id}/download-limit")
def change_user_download_limit(
    user_id: int,
    payload: UserDownloadLimitRequest,
    db: Session = Depends(get_db),
    master_user: User = Depends(require_master)
):
    """Permite al Administrador Master ajustar o retirar el límite diario de descargas de un usuario."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")

    effective_limit = payload.daily_limit if payload.daily_limit is not None else payload.weekly_limit

    # Si se pasa None o -1, significa Ilimitado (sin límite)
    if effective_limit is None or effective_limit < 0:
        user.daily_download_limit = None
    else:
        user.daily_download_limit = effective_limit

    db.commit()
    limit_str = "Ilimitado" if user.daily_download_limit is None else f"{user.daily_download_limit} libros/día"
    logging.info(f"Límite de descargas de {user.username} actualizado a {limit_str} por {master_user.username}")
    return {
        "message": f"Límite de {user.username} configurado en: {limit_str}",
        "daily_download_limit": user.daily_download_limit,
        "weekly_download_limit": user.daily_download_limit
    }

@app.post("/api/admin/users/{user_id}/reset-password")
def admin_reset_user_password(
    user_id: int,
    payload: AdminPasswordResetRequest,
    db: Session = Depends(get_db),
    master_user: User = Depends(require_master)
):
    """Permite al Administrador Master cambiar directamente la contraseña de cualquier usuario."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    if len(payload.new_password) < 4:
        raise HTTPException(status_code=400, detail="La contraseña debe tener al menos 4 caracteres.")

    user.password_hash = hash_password(payload.new_password)
    db.query(UserSession).filter(UserSession.user_id == user.id).delete()
    db.commit()
    logging.info(f"Master {master_user.username} restableció la contraseña del usuario {user.username}")
    return {"message": f"Contraseña actualizada para {user.username}."}

# ==========================================
# RUTAS DE AJUSTES Y BIBLIOTECA GLOBAL
# ==========================================

@app.get("/api/settings")
def read_settings():
    return get_settings()

@app.post("/api/scan")
def scan_library(
    directory: str,
    background_tasks: BackgroundTasks,
    library_id: int = 1,
    db: Session = Depends(get_db),
    master_user: User = Depends(require_master)
):
    if scan_state["running"]:
        return {"message": "Ya hay un escaneo en curso. Puedes ver su progreso en Mantenimiento.", "status": scan_state}

    lib = db.query(Library).filter(Library.id == library_id).first()
    lib_name = lib.name if lib else f"Biblioteca #{library_id}"

    logging.info(f"Escaneo solicitado por Master ({master_user.username}) en: {directory} (Lib: {library_id})")
    background_tasks.add_task(scan_directory, directory, library_id, lib_name)
    save_settings({"watch_path": directory})
    if lib:
        lib.path = directory
        db.commit()
    try:
        watcher.update_watches_from_db(db, fallback_path=directory)
    except Exception as e:
        logging.error(f"No se pudo actualizar la autodetección de carpetas: {e}")
    return {"message": "Escaneo y vigía iniciados en segundo plano."}

@app.get("/api/admin/scan/status")
def get_scan_status(
    master_user: User = Depends(require_master)
):
    """Devuelve el progreso en vivo del escaneo de carpetas."""
    return scan_state

@app.post("/api/admin/scan/stop")
def stop_scan(
    master_user: User = Depends(require_master)
):
    """Solicita la detención del escaneo en curso."""
    if scan_state["running"]:
        scan_state["stop_requested"] = True
        return {"message": "Detención solicitada. El escaneo finalizará el lote actual y se detendrá."}
    return {"message": "No hay ningún escaneo activo en este momento."}

@app.delete("/api/library")
def clear_library(
    library_id: Optional[int] = None,
    db: Session = Depends(get_db),
    master_user: User = Depends(require_master)
):
    logging.info(f"Limpieza solicitada por Master ({master_user.username}) para Lib: {library_id}...")
    if library_id:
        db.query(Book).filter(Book.library_id == library_id).delete()
    else:
        db.query(Book).delete()
        if os.path.exists(COVERS_DIR):
            for filename in os.listdir(COVERS_DIR):
                file_path = os.path.join(COVERS_DIR, filename)
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                except Exception as e:
                    logging.error(f"Error borrando {file_path}: {e}")
    db.commit()
    return {"message": "Biblioteca limpiada correctamente."}

# ==========================================
# CONSULTA DE LIBROS Y ESTADÍSTICAS
# ==========================================

@app.get("/api/books")
def read_books(
    skip: int = 0,
    limit: int = 500,
    search: str = None,
    library_id: Optional[int] = None,
    formats: Optional[str] = None,  # Lista separada por comas ej: "epub", "pdf" o "epub,pdf"
    sort_by: str = "recent",
    db: Session = Depends(get_db),
    optional_user: Optional[User] = Depends(get_optional_user)
):
    logging.info(f"Petición de libros (skip={skip}, limit={limit}, search={search}, lib={library_id}, formats={formats}, sort={sort_by})")
    query = db.query(Book)

    is_master = optional_user and optional_user.role == "master"

    # Si NO es master, filtrar SIEMPRE para excluir documentos PDF
    if not is_master:
        query = query.filter((Book.format == "epub") | (Book.format == None))
        query = query.filter(~Book.file_path.ilike("%.pdf"))
    elif formats:
        # Solo el master puede filtrar por formatos específicos
        fmt_list = [f.strip().lower() for f in formats.split(',') if f.strip()]
        if fmt_list:
            conds = []
            if "pdf" in fmt_list:
                conds.append(Book.format == "pdf")
                conds.append(Book.file_path.ilike("%.pdf"))
            if "epub" in fmt_list:
                conds.append(Book.format == "epub")
                conds.append(Book.format == None)
                conds.append(Book.file_path.ilike("%.epub"))
            if conds:
                from sqlalchemy import or_
                query = query.filter(or_(*conds))

    # Filtrar por permisos de biblioteca
    if optional_user and optional_user.role == "reader":
        allowed_lib_ids = [ul.library_id for ul in optional_user.libraries]
        if not allowed_lib_ids:
            return []  # El lector no tiene acceso a ninguna biblioteca aún
            
        if library_id is not None:
            if library_id not in allowed_lib_ids:
                raise HTTPException(
                    status_code=403, 
                    detail="No tienes permiso para acceder a esta biblioteca."
                )
            query = query.join(BookLibrary, BookLibrary.book_id == Book.id).filter(BookLibrary.library_id == library_id)
        else:
            query = query.join(BookLibrary, BookLibrary.book_id == Book.id).filter(BookLibrary.library_id.in_(allowed_lib_ids)).distinct()
    else:
        # Master o sin usuario
        if library_id is not None:
            query = query.join(BookLibrary, BookLibrary.book_id == Book.id).filter(BookLibrary.library_id == library_id)

    # Búsqueda ultra-rápida FTS5 con fallback
    if search and search.strip():
        from database import normalize_for_search
        norm_search = normalize_for_search(search)
        raw_words = [w for w in re.sub(r'[^a-zA-Z0-9áéíóúÁÉÍÓÚñÑüÜ]', ' ', norm_search).split() if len(w) > 0]
        if raw_words:
            try:
                fts_query_str = " ".join(f"{w}*" for w in raw_words)
                fts_matched_ids = [
                    r[0] for r in db.execute(
                        text("SELECT rowid FROM books_fts WHERE books_fts MATCH :match_q LIMIT 2000"),
                        {"match_q": fts_query_str}
                    ).fetchall()
                ]
                if fts_matched_ids:
                    query = query.filter(Book.id.in_(fts_matched_ids))
                else:
                    # Sin coincidencias en FTS
                    query = query.filter(Book.id == -1)
            except Exception as fts_err:
                logging.warning(f"Fallback FTS5 a NORM_SEARCH: {fts_err}")
                for word in raw_words:
                    pattern = f"%{word}%"
                    query = query.filter(
                        func.NORM_SEARCH(Book.title).like(pattern) | 
                        func.NORM_SEARCH(Book.author).like(pattern)
                    )

    review_subq = (
        db.query(
            BookReview.book_id,
            func.round(func.avg(BookReview.rating), 1).label("rating"),
            func.count(BookReview.id).label("reviews_count")
        )
        .group_by(BookReview.book_id)
        .subquery()
    )

    query = query.outerjoin(review_subq, Book.id == review_subq.c.book_id)

    # Ordenación aplicada en base de datos sobre la totalidad del catálogo
    eff_rating_col = func.coalesce(review_subq.c.rating, Book.external_rating, 0.0)
    if sort_by == "ratingDesc":
        query = query.order_by(eff_rating_col.desc(), Book.id.desc())
    elif sort_by == "titleAsc":
        query = query.order_by(Book.title.asc(), Book.id.desc())
    elif sort_by == "authorAsc":
        query = query.order_by(Book.author.asc(), Book.id.desc())
    elif sort_by == "dateAsc":
        query = query.order_by(Book.id.asc())
    else:  # "recent" o por defecto
        query = query.order_by(Book.id.desc())

    results = query.with_entities(Book, review_subq.c.rating, review_subq.c.reviews_count).offset(skip).limit(limit).all()
    book_list = []
    for b, rat, rev_cnt in results:
        effective_rating = float(rat) if rat is not None and rat > 0 else (float(b.external_rating) if b.external_rating else 0.0)
        effective_count = rev_cnt if rev_cnt is not None and rev_cnt > 0 else (b.external_reviews_count if b.external_reviews_count else 0)
        book_list.append({
            "id": b.id,
            "title": b.title,
            "author": b.author,
            "description": b.description,
            "cover_path": b.cover_path,
            "file_path": b.file_path,
            "format": b.format or ("pdf" if (b.file_path and b.file_path.lower().endswith(".pdf")) else "epub"),
            "tags": b.tags,
            "library_id": b.library_id,
            "rating": round(effective_rating, 1),
            "reviews_count": effective_count
        })
    return book_list

@app.get("/api/stats")
def read_stats(
    library_id: Optional[int] = None,
    formats: Optional[str] = None,
    db: Session = Depends(get_db),
    optional_user: Optional[User] = Depends(get_optional_user)
):
    query = db.query(Book)
    is_master = optional_user and optional_user.role == "master"

    if not is_master:
        query = query.filter((Book.format == "epub") | (Book.format == None))
        query = query.filter(~Book.file_path.ilike("%.pdf"))
    elif formats:
        fmt_list = [f.strip().lower() for f in formats.split(',') if f.strip()]
        if fmt_list:
            conds = []
            if "pdf" in fmt_list:
                conds.append(Book.format == "pdf")
                conds.append(Book.file_path.ilike("%.pdf"))
            if "epub" in fmt_list:
                conds.append(Book.format == "epub")
                conds.append(Book.format == None)
                conds.append(Book.file_path.ilike("%.epub"))
            if conds:
                from sqlalchemy import or_
                query = query.filter(or_(*conds))
    if optional_user and optional_user.role == "reader":
        allowed_lib_ids = [ul.library_id for ul in optional_user.libraries]
        if not allowed_lib_ids:
            return {"total": 0, "totalAuthors": 0, "topAuthor": "-"}
        if library_id is not None:
            if library_id in allowed_lib_ids:
                query = query.join(BookLibrary, BookLibrary.book_id == Book.id).filter(BookLibrary.library_id == library_id)
            else:
                return {"total": 0, "totalAuthors": 0, "topAuthor": "-"}
        else:
            query = query.join(BookLibrary, BookLibrary.book_id == Book.id).filter(BookLibrary.library_id.in_(allowed_lib_ids)).distinct()
    else:
        if library_id is not None:
            query = query.join(BookLibrary, BookLibrary.book_id == Book.id).filter(BookLibrary.library_id == library_id)

    total = query.count()
    total_authors = query.with_entities(func.count(func.distinct(Book.author))).scalar() or 0
    top_author_row = (
        query.with_entities(Book.author, func.count(Book.id).label('cnt'))
        .group_by(Book.author)
        .order_by(func.count(Book.id).desc())
        .first()
    )
    top_author = top_author_row[0] if top_author_row else "-"
    return {
        "total": total,
        "totalAuthors": total_authors,
        "topAuthor": top_author
    }

# ==========================================
# HISTORIAL INDIVIDUAL Y PROGRESO (Punto 3)
# ==========================================

@app.get("/api/books/{book_id}/my-progress")
def get_my_book_progress(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user)
):
    if not current_user:
        book = db.query(Book).filter(Book.id == book_id).first()
        return {"progress": book.progress if book else None}

    user_prog = db.query(UserProgress).filter(
        UserProgress.user_id == current_user.id,
        UserProgress.book_id == book_id
    ).first()

    if user_prog:
        return {"progress": user_prog.progress, "percentage": user_prog.percentage}
    
    book = db.query(Book).filter(Book.id == book_id).first()
    return {"progress": book.progress if book else None, "percentage": 0}

@app.post("/api/books/{book_id}/progress")
def save_progress(
    book_id: int,
    progress: Optional[str] = None,
    payload: Optional[ProgressRequest] = None,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user)
):
    cfi_value = payload.progress if payload else progress
    if not cfi_value:
        raise HTTPException(status_code=400, detail="Progreso CFI no proporcionado.")

    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        return {"error": "Libro no encontrado.", "status": 404}
    
    if current_user:
        user_prog = db.query(UserProgress).filter(
            UserProgress.user_id == current_user.id,
            UserProgress.book_id == book_id
        ).first()

        percentage = payload.percentage if payload else 0

        if user_prog:
            user_prog.progress = cfi_value
            user_prog.percentage = percentage
            user_prog.updated_at = datetime.utcnow()
        else:
            user_prog = UserProgress(
                user_id=current_user.id,
                book_id=book_id,
                progress=cfi_value,
                percentage=percentage
            )
            db.add(user_prog)

    book.progress = cfi_value
    db.commit()
    return {"message": "Progreso guardado correctamente."}

@app.get("/api/my-readings")
def get_my_readings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    review_subq = (
        db.query(
            BookReview.book_id,
            func.round(func.avg(BookReview.rating), 1).label("rating"),
            func.count(BookReview.id).label("reviews_count")
        )
        .group_by(BookReview.book_id)
        .subquery()
    )

    readings = (
        db.query(Book, UserProgress, review_subq.c.rating, review_subq.c.reviews_count)
        .join(UserProgress, Book.id == UserProgress.book_id)
        .outerjoin(review_subq, Book.id == review_subq.c.book_id)
        .filter(UserProgress.user_id == current_user.id)
        .order_by(UserProgress.updated_at.desc())
        .limit(100)
        .all()
    )
    result = []
    for book, prog, rat, rev_cnt in readings:
        effective_rating = float(rat) if rat is not None and rat > 0 else (float(book.external_rating) if book.external_rating else 0.0)
        effective_count = rev_cnt if rev_cnt is not None and rev_cnt > 0 else (book.external_reviews_count if book.external_reviews_count else 0)
        result.append({
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "cover_path": book.cover_path,
            "description": book.description,
            "format": book.format or ("pdf" if (book.file_path and book.file_path.lower().endswith(".pdf")) else "epub"),
            "tags": book.tags,
            "progress": prog.progress,
            "percentage": prog.percentage,
            "updated_at": prog.updated_at.strftime("%Y-%m-%d %H:%M") if prog.updated_at else None,
            "rating": round(effective_rating, 1),
            "reviews_count": effective_count
        })
    return result

# ==========================================
# OPINIONES Y VALORACIONES (Punto 3)
# ==========================================

@app.get("/api/books/{book_id}/reviews")
def get_book_reviews(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    reviews = (
        db.query(BookReview, User.username)
        .join(User, BookReview.user_id == User.id)
        .filter(BookReview.book_id == book_id)
        .order_by(BookReview.updated_at.desc())
        .all()
    )

    review_list = []
    total_rating = 0
    for rev, username in reviews:
        total_rating += rev.rating
        review_list.append({
            "id": rev.id,
            "user_id": rev.user_id,
            "username": username,
            "rating": rev.rating,
            "comment": rev.comment,
            "updated_at": rev.updated_at.strftime("%Y-%m-%d %H:%M") if rev.updated_at else None
        })

    # Si aún no tiene opiniones de lectores y no ha sido consultado en Open Library, consultar en vivo
    if not review_list and (book.external_rating_synced != 1 or book.external_rating is None):
        fetch_openlibrary_rating_for_book(book, db)

    if review_list:
        avg_rating = round(total_rating / len(review_list), 1)
        total_count = len(review_list)
        source = "Comunidad"
    elif book and book.external_rating and book.external_rating > 0:
        avg_rating = round(book.external_rating, 1)
        total_count = book.external_reviews_count or 1
        source = "Open Library"
    else:
        avg_rating = 0.0
        total_count = 0
        source = "Sin valorar"

    return {
        "book_id": book_id,
        "average_rating": avg_rating,
        "total_reviews": total_count,
        "source": source,
        "cover_path": book.cover_path if book else "",
        "reviews": review_list
    }

@app.post("/api/books/{book_id}/sync-external-rating")
def sync_book_external_rating(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Libro no encontrado.")
    status, message = fetch_openlibrary_rating_for_book(book, db, force=True)
    return {
        "book_id": book.id,
        "average_rating": book.external_rating or 0.0,
        "total_reviews": book.external_reviews_count or 0,
        "source": "Open Library" if (book.external_rating and book.external_rating > 0) else "Sin valorar",
        "cover_path": book.cover_path or "",
        "status": status,
        "message": message
    }

@app.post("/api/books/{book_id}/reviews")
def create_or_update_review(
    book_id: int,
    payload: ReviewRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Libro no encontrado.")

    existing_review = db.query(BookReview).filter(
        BookReview.book_id == book_id,
        BookReview.user_id == current_user.id
    ).first()

    if existing_review:
        existing_review.rating = payload.rating
        existing_review.comment = payload.comment.strip()
        existing_review.updated_at = datetime.utcnow()
        db.commit()
        return {"message": "Opinión actualizada con éxito."}
    else:
        new_review = BookReview(
            user_id=current_user.id,
            book_id=book_id,
            rating=payload.rating,
            comment=payload.comment.strip()
        )
        db.add(new_review)
        db.commit()
        return {"message": "Opinión publicada con éxito."}

@app.delete("/api/books/{book_id}/reviews")
def delete_review(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    review = db.query(BookReview).filter(
        BookReview.book_id == book_id,
        BookReview.user_id == current_user.id
    ).first()

    if not review:
        raise HTTPException(status_code=404, detail="No tienes una opinión para este libro.")

    db.delete(review)
    db.commit()
    return {"message": "Opinión eliminada correctamente."}

# ==========================================
# REPORTES DE INCIDENCIAS (lectores → admin)
# ==========================================

@app.post("/api/books/{book_id}/report")
def report_book_issue(
    book_id: int,
    payload: BookReportRequest,
    db: Session = Depends(get_db),
    optional_user: Optional[User] = Depends(get_optional_user)
):
    """Cualquier visitante (autenticado o no) puede reportar una incidencia sobre un libro."""
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Libro no encontrado.")

    if not payload.message or not payload.message.strip():
        raise HTTPException(status_code=422, detail="El mensaje no puede estar vacío.")

    new_report = BookReport(
        book_id=book_id,
        user_id=optional_user.id if optional_user else None,
        report_type=payload.report_type,
        message=payload.message.strip()
    )
    db.add(new_report)
    db.commit()
    return {"message": "Incidencia enviada al administrador. ¡Gracias por tu colaboración!"}


@app.get("/api/admin/reports")
def list_reports(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Solo para master: lista todos los reportes pendientes."""
    if current_user.role != "master":
        raise HTTPException(status_code=403, detail="Acceso restringido.")

    reports = (
        db.query(BookReport)
        .filter(BookReport.status == "pending")
        .order_by(BookReport.created_at.desc())
        .all()
    )

    result = []
    for r in reports:
        book = db.query(Book).filter(Book.id == r.book_id).first()
        reporter = db.query(User).filter(User.id == r.user_id).first() if r.user_id else None
        result.append({
            "id": r.id,
            "book_id": r.book_id,
            "book_title": book.title if book else "Libro eliminado",
            "book_author": book.author if book else "",
            "report_type": r.report_type,
            "message": r.message,
            "status": r.status,
            "reporter": reporter.username if reporter else "Anónimo",
            "created_at": r.created_at.strftime("%d/%m/%Y %H:%M") if r.created_at else ""
        })
    return result


@app.post("/api/admin/reports/{report_id}/mark-reviewed")
def mark_report_reviewed(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Solo para master: cierra un reporte marcándolo como revisado."""
    if current_user.role != "master":
        raise HTTPException(status_code=403, detail="Acceso restringido.")

    report = db.query(BookReport).filter(BookReport.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Reporte no encontrado.")

    report.status = "reviewed"
    report.reviewed_at = datetime.utcnow()
    db.commit()
    return {"message": "Reporte marcado como revisado."}


# ==========================================
# APERTURA Y DESCARGA DE LIBROS
# ==========================================

@app.get("/api/open/{book_id}")
def open_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        return {"error": "Libro no encontrado en la base de datos.", "status": 404}
    
    file_path = book.file_path
    if not os.path.exists(file_path):
        return {"error": "El archivo físico ya no existe en la ruta original.", "status": 404}
    
    try:
        if platform.system() == "Windows":
            os.startfile(file_path)
        elif platform.system() == "Darwin":
            subprocess.call(["open", file_path])
        else:
            subprocess.call(["xdg-open", file_path])
        return {"message": "Libro abierto exitosamente."}
    except Exception as e:
        return {"error": str(e), "status": 500}

class SendKindleRequest(BaseModel):
    kindle_email: str
    smtp_server: Optional[str] = "smtp.gmail.com"
    smtp_port: Optional[int] = 587
    smtp_user: Optional[str] = ""
    smtp_password: Optional[str] = ""

DAILY_DOWNLOAD_LIMIT = 1

@app.get("/api/download/status")
def get_download_status(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Devuelve el contador de descargas realizadas en las últimas 24 horas y el cupo restante."""
    if current_user.role == "master" or current_user.daily_download_limit is None:
        return {
            "daily_limit": None,
            "weekly_limit": None,
            "downloads_used": 0,
            "downloads_remaining": 9999,
            "is_unlimited": True
        }
    
    user_limit = current_user.daily_download_limit
    from datetime import timedelta
    one_day_ago = datetime.utcnow() - timedelta(days=1)
    recent_count = db.query(UserDownload).filter(
        UserDownload.user_id == current_user.id,
        UserDownload.downloaded_at >= one_day_ago
    ).count()

    return {
        "daily_limit": user_limit,
        "weekly_limit": user_limit, # compatibilidad
        "downloads_used": recent_count,
        "downloads_remaining": max(0, user_limit - recent_count),
        "is_unlimited": False
    }

@app.get("/api/download/{book_id}")
def download_book(
    book_id: int, 
    db: Session = Depends(get_db),
    optional_user: Optional[User] = Depends(get_optional_user),
    is_download: Optional[int] = Query(0)
):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Libro no encontrado en la base de datos.")
    
    file_path = book.file_path
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="El archivo físico ya no existe en la ruta original.")
    
    # Determinar extensión y media_type según el formato del libro
    orig_ext = os.path.splitext(file_path)[1].lower()
    is_pdf = (getattr(book, 'format', None) == "pdf") or orig_ext == ".pdf"

    # Si es PDF, restringir exclusivamente al usuario Master
    if is_pdf:
        if not optional_user or optional_user.role != "master":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="El acceso a documentos en formato PDF está restringido al Administrador Master."
            )

    file_ext = ".pdf" if is_pdf else ".epub"
    media_type = "application/pdf" if is_pdf else "application/epub+zip"

    # Nombre de descarga limpio y seguro: "Autor - Título.ext"
    safe_title = re.sub(r'[\\/*?:"<>|]', '', (book.title or 'libro').strip())
    safe_author = re.sub(r'[\\/*?:"<>|]', '', (book.author or '').strip())
    clean_filename = f"{safe_author} - {safe_title}{file_ext}" if safe_author else f"{safe_title}{file_ext}"
    if not clean_filename.endswith(file_ext):
        clean_filename += file_ext

    # Si es una petición de descarga física directa (botón de descarga):
    if is_download == 1:
        if not optional_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Debes iniciar sesión con tu cuenta de lector para descargar libros."
            )
        
        # El Administrador Master o usuarios con límite None tienen descargas ilimitadas
        user_limit = optional_user.daily_download_limit
        if optional_user.role != "master" and user_limit is not None:
            from datetime import timedelta
            one_day_ago = datetime.utcnow() - timedelta(days=1)
            recent_downloads = db.query(UserDownload).filter(
                UserDownload.user_id == optional_user.id,
                UserDownload.downloaded_at >= one_day_ago
            ).order_by(UserDownload.downloaded_at.asc()).all()

            if len(recent_downloads) >= user_limit:
                first_dl = recent_downloads[0]
                available_again = first_dl.downloaded_at + timedelta(days=1)
                diff = available_again - datetime.utcnow()
                total_minutes_left = max(1, int(diff.total_seconds() // 60))
                hours_left = total_minutes_left // 60
                mins_left = total_minutes_left % 60

                if hours_left >= 1 and mins_left > 0:
                    time_hint = f"{hours_left} hora(s) y {mins_left} minuto(s)"
                elif hours_left >= 1:
                    time_hint = f"{hours_left} hora(s)"
                else:
                    time_hint = f"{mins_left} minuto(s)"

                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail=f"⚠️ Has alcanzado tu límite diario de {user_limit} libro(s) al día. Podrás descargar un nuevo libro en aproximadamente {time_hint}."
                )

            # Registrar la descarga en el historial del usuario
            new_record = UserDownload(user_id=optional_user.id, book_id=book.id)
            db.add(new_record)
            db.commit()

    return FileResponse(
        path=file_path,
        filename=clean_filename,
        media_type=media_type,
        headers={"Content-Disposition": f'inline; filename="{clean_filename}"' if is_download != 1 else f'attachment; filename="{clean_filename}"'}
    )

@app.post("/api/books/{book_id}/send-kindle")
def send_to_kindle(
    book_id: int,
    payload: SendKindleRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.base import MIMEBase
    from email.mime.text import MIMEText
    from email import encoders

    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Libro no encontrado.")
    if not os.path.exists(book.file_path):
        raise HTTPException(status_code=404, detail="El archivo físico del libro no existe en disco.")

    # Guardar preferencia de email Kindle en ajustes si se proporciona
    settings = get_settings()
    settings["last_kindle_email"] = payload.kindle_email
    if payload.smtp_server: settings["smtp_server"] = payload.smtp_server
    if payload.smtp_port: settings["smtp_port"] = payload.smtp_port
    if payload.smtp_user: settings["smtp_user"] = payload.smtp_user
    save_settings(settings)

    # Si no se han configurado credenciales SMTP
    if not payload.smtp_user or not payload.smtp_password:
        return {
            "status": "config_needed",
            "message": "Para enviar directamente por email a tu Kindle se requiere una cuenta emisora (servidor SMTP, usuario y clave de aplicación).",
            "saved_email": payload.kindle_email
        }

    try:
        msg = MIMEMultipart()
        msg['From'] = payload.smtp_user
        msg['To'] = payload.kindle_email
        msg['Subject'] = f"Libro: {book.title}"

        body = f"Adjunto el libro '{book.title}' de {book.author} enviado desde EPUB Biblio."
        msg.attach(MIMEText(body, 'plain'))

        safe_title = re.sub(r'[\\/*?:"<>|]', '', (book.title or 'libro').strip())
        attachment_name = f"{safe_title}.epub"

        with open(book.file_path, "rb") as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename="{attachment_name}"')
            msg.attach(part)

        server = smtplib.SMTP(payload.smtp_server, payload.smtp_port)
        server.starttls()
        server.login(payload.smtp_user, payload.smtp_password)
        server.send_message(msg)
        server.quit()

        return {"status": "success", "message": f"Libro enviado exitosamente a {payload.kindle_email}"}
    except Exception as e:
        logging.error(f"Error enviando libro por email a Kindle: {e}")
        raise HTTPException(status_code=500, detail=f"Fallo al enviar correo: {str(e)}")

# ==========================================
# SERVIR FRONTEND WEB COMPILADO
# ==========================================
FRONTEND_DIST = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "dist"))
if os.path.exists(FRONTEND_DIST):
    app.mount("/", StaticFiles(directory=FRONTEND_DIST, html=True), name="frontend")
