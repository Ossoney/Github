from fastapi import FastAPI, BackgroundTasks, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import SessionLocal, Book
from epub_parser import scan_directory
from watcher import watcher
from paths import LOG_PATH, COVERS_DIR, SETTINGS_PATH
import os
import json
import logging
import subprocess
import platform

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

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs(COVERS_DIR, exist_ok=True)
app.mount("/static/covers", StaticFiles(directory=COVERS_DIR), name="covers")

def get_settings():
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, 'r') as f:
                return json.load(f)
        except:
            pass
    return {"watch_path": None}

def save_settings(settings):
    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f)

@app.on_event("startup")
async def startup_event():
    settings = get_settings()
    path = settings.get("watch_path")
    if path and os.path.exists(path):
        logging.info(f"Iniciando vigía automático en: {path}")
        try:
            watcher.start_watching(path)
        except Exception as e:
            logging.error(f"Error al iniciar vigía automático: {e}")

@app.get("/api/settings")
def read_settings():
    return get_settings()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/books")
def read_books(skip: int = 0, limit: int = 500, search: str = None, db: Session = Depends(get_db)):
    logging.info(f"Petición de lectura de libros recibida (skip={skip}, limit={limit}, search={search})")
    query = db.query(Book)
    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            (Book.title.ilike(search_filter)) | 
            (Book.author.ilike(search_filter))
        )
    books = query.offset(skip).limit(limit).all()
    return books

@app.get("/api/stats")
def read_stats(db: Session = Depends(get_db)):
    total = db.query(Book).count()
    total_authors = db.query(func.count(func.distinct(Book.author))).scalar() or 0
    top_author_row = (
        db.query(Book.author, func.count(Book.id).label('cnt'))
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

@app.post("/api/scan")
def scan_library(directory: str, background_tasks: BackgroundTasks):
    logging.info(f"Iniciando escaneo del directorio: {directory}")
    background_tasks.add_task(scan_directory, directory)
    try:
        watcher.start_watching(directory)
    except Exception as e:
        logging.error(f"No se pudo iniciar la autodetección en {directory}: {e}")
    # Guardar persistencia
    save_settings({"watch_path": directory})
    
    return {"message": "Scanning and watching started in background."}

@app.delete("/api/library")
def clear_library(db: Session = Depends(get_db)):
    logging.info("Limpiando biblioteca y borrando portadas...")
    db.query(Book).delete()
    db.commit()

    # Fix: usar COVERS_DIR de paths.py (ruta absoluta) en vez de ruta relativa
    if os.path.exists(COVERS_DIR):
        for filename in os.listdir(COVERS_DIR):
            file_path = os.path.join(COVERS_DIR, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                logging.error(f"Error borrando {file_path}: {e}")

    return {"message": "Biblioteca limpiada correctamente."}

@app.post("/api/books/{book_id}/progress")
def save_progress(book_id: int, progress: str, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        return {"error": "Libro no encontrado.", "status": 404}
    
    book.progress = progress
    db.commit()
    return {"message": "Progreso guardado correctamente."}

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

@app.get("/api/download/{book_id}")
def download_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        return {"error": "Libro no encontrado en la base de datos.", "status": 404}
    
    file_path = book.file_path
    if not os.path.exists(file_path):
        return {"error": "El archivo físico ya no existe en la ruta original.", "status": 404}
    
    return FileResponse(path=file_path, filename=f"{book.title}.epub", media_type="application/epub+zip")
