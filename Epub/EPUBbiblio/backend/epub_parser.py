import os
import zipfile
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
from database import SessionLocal, Book, BookLibrary, Library
from paths import COVERS_DIR
import logging
import hashlib
import pymupdf

import re

def extract_isbn_from_text(raw_text: str) -> str:
    """Extrae un código ISBN-10 o ISBN-13 limpio si está presente en el texto."""
    if not raw_text:
        return ""
    # Quitar guiones y espacios para la validación numérica
    clean = re.sub(r'[^0-9X-]', '', str(raw_text).upper())
    digits_only = clean.replace('-', '')
    if len(digits_only) == 13 and digits_only.startswith(('978', '979')):
        return digits_only
    if len(digits_only) == 10:
        return digits_only
    # Buscar patrón ISBN dentro de cadenas compuestas (urn:isbn:978..., etc.)
    m13 = re.search(r'(97[89][-\s]?[0-9]{1,5}[-\s]?[0-9]+[-\s]?[0-9]+[-\s]?[0-9])', raw_text)
    if m13:
        found = re.sub(r'[^0-9]', '', m13.group(1))
        if len(found) == 13:
            return found
    m10 = re.search(r'([0-9]{1,5}[-\s]?[0-9]+[-\s]?[0-9]+[-\s]?[0-9X])', raw_text, re.IGNORECASE)
    if m10:
        found = re.sub(r'[^0-9X]', '', m10.group(1).upper())
        if len(found) == 10:
            return found
    return ""

def parse_filename_metadata(filename: str):
    """Extrae título y autor a partir de patrones estándar de nombre de archivo."""
    base = os.path.splitext(filename)[0].strip()
    parts = [p.strip() for p in base.split(' - ') if p.strip()]
    if len(parts) >= 3:
        # Ejemplo: 1991 - Mendoza, Eduardo - Sin Noticias De Gurb
        # O: Coleccion - Autor - Titulo
        author = parts[1]
        title = " - ".join(parts[2:])
        return title, author
    elif len(parts) == 2:
        # Ejemplo: Autor - Titulo
        return parts[1], parts[0]
    return base, "Autor Desconocido"

def extract_metadata_fallback(file_path: str):
    """Parser de rescate directo vía zipfile si ebooklib falla por BOM, XML o namespaces corruptos."""
    try:
        with zipfile.ZipFile(file_path, 'r') as z:
            opf_content = None
            for name in z.namelist():
                if name.lower().endswith('.opf'):
                    opf_content = z.read(name).decode('utf-8-sig', errors='ignore')
                    break
            
            title = None
            author = None
            description = ""
            cover_path = ""
            isbn = ""
            
            if opf_content:
                try:
                    soup = BeautifulSoup(opf_content, "xml")
                    title_tag = soup.find(['dc:title', 'title'])
                    if title_tag and title_tag.get_text().strip():
                        title = title_tag.get_text().strip()
                        
                    creator_tag = soup.find(['dc:creator', 'creator'])
                    if creator_tag and creator_tag.get_text().strip():
                        author = creator_tag.get_text().strip()
                        
                    desc_tag = soup.find(['dc:description', 'description'])
                    if desc_tag and desc_tag.get_text().strip():
                        soup_desc = BeautifulSoup(desc_tag.get_text(), "html.parser")
                        description = soup_desc.get_text(separator="\n").strip()

                    # Buscar identificadores de tipo ISBN
                    for id_tag in soup.find_all(['dc:identifier', 'identifier']):
                        cand = extract_isbn_from_text(id_tag.get_text())
                        if cand:
                            isbn = cand
                            break
                except Exception:
                    pass
            
            filename = os.path.basename(file_path)
            fn_title, fn_author = parse_filename_metadata(filename)
            if not title:
                title = fn_title
            if not author or author == "Autor Desconocido":
                author = fn_author
                
            # Extraer portada si existe en el zip
            for name in z.namelist():
                low = name.lower()
                if any(k in low for k in ['cover', 'portada']) and any(low.endswith(ext) for ext in ['.jpg', '.jpeg', '.png']):
                    ext = ".png" if low.endswith('.png') else ".jpg"
                    path_hash = hashlib.md5(file_path.encode()).hexdigest()
                    cover_filename = f"cover_{path_hash}{ext}"
                    disk_cover_path = os.path.join(COVERS_DIR, cover_filename)
                    if not os.path.exists(disk_cover_path):
                        try:
                            with open(disk_cover_path, "wb") as f:
                                f.write(z.read(name))
                        except Exception:
                            pass
                    cover_path = f"/static/covers/{cover_filename}"
                    break
                    
            return {
                "title": title or filename,
                "author": author or "Autor Desconocido",
                "description": description or "Sin descripción disponible.",
                "cover_path": cover_path,
                "file_path": file_path,
                "isbn": isbn,
                "format": "epub"
            }
    except Exception as e:
        logging.warning(f"Fallback estándar para {file_path}: {e}")
        filename = os.path.basename(file_path)
        fn_title, fn_author = parse_filename_metadata(filename)
        return {
            "title": fn_title,
            "author": fn_author,
            "description": "Sin descripción disponible.",
            "cover_path": "",
            "file_path": file_path,
            "isbn": "",
            "format": "epub"
        }

def extract_pdf_metadata(file_path: str):
    """Extrae metadatos y genera la portada de la primera página de un archivo PDF usando PyMuPDF."""
    try:
        doc = pymupdf.open(file_path)
        meta = doc.metadata or {}

        pdf_title = (meta.get("title") or "").strip()
        pdf_author = (meta.get("author") or "").strip()
        pdf_subject = (meta.get("subject") or "").strip()
        pdf_keywords = (meta.get("keywords") or "").strip()

        # Descripción uniendo subject y keywords si existen
        desc_parts = [p for p in [pdf_subject, pdf_keywords] if p]
        description = " - ".join(desc_parts) if desc_parts else "Documento en formato PDF."

        filename = os.path.basename(file_path)
        fn_title, fn_author = parse_filename_metadata(filename)

        # Si el título del PDF está vacío, parece un UUID o el nombre de un software
        if not pdf_title or len(pdf_title) < 2 or pdf_title.lower().startswith(("untitled", "microsoft word", "adobe", "scan")):
            pdf_title = fn_title

        if not pdf_author or pdf_author == "Autor Desconocido" or len(pdf_author) < 2 or pdf_author.lower().startswith(("canon", "hp", "epson", "adobe", "user", "admin")):
            pdf_author = fn_author

        # Generar miniatura/portada a partir de la primera página del PDF
        cover_path = ""
        if len(doc) > 0:
            try:
                page0 = doc[0]
                path_hash = hashlib.md5(file_path.encode()).hexdigest()
                cover_filename = f"cover_pdf_{path_hash}.jpg"
                disk_cover_path = os.path.join(COVERS_DIR, cover_filename)

                if not os.path.exists(disk_cover_path):
                    pix = page0.get_pixmap(dpi=150)
                    pix.save(disk_cover_path)

                cover_path = f"/static/covers/{cover_filename}"
            except Exception as e:
                logging.error(f"Error generando miniatura de portada para PDF {filename}: {e}")

        # Intentar extraer ISBN de la primera página de texto si está presente
        isbn = ""
        try:
            if len(doc) > 0:
                p0_text = doc[0].get_text() or ""
                isbn = extract_isbn_from_text(p0_text)
                if not isbn and len(doc) > 1:
                    p1_text = doc[1].get_text() or ""
                    isbn = extract_isbn_from_text(p1_text)
        except Exception:
            pass

        doc.close()

        return {
            "title": pdf_title or fn_title,
            "author": pdf_author or fn_author or "Autor Desconocido",
            "description": description,
            "cover_path": cover_path,
            "file_path": file_path,
            "isbn": isbn,
            "format": "pdf"
        }
    except Exception as e:
        logging.error(f"Error leyendo PDF {file_path}: {e}")
        fn_title, fn_author = parse_filename_metadata(os.path.basename(file_path))
        return {
            "title": fn_title,
            "author": fn_author or "Autor Desconocido",
            "description": "Documento en formato PDF.",
            "cover_path": "",
            "file_path": file_path,
            "isbn": "",
            "format": "pdf"
        }

def extract_metadata(file_path: str):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return extract_pdf_metadata(file_path)
    return extract_epub_metadata(file_path)

def extract_epub_metadata(file_path: str):
    """Extrae metadatos y guarda la carátula físicamente con fallback de robustez."""
    try:
        book = epub.read_epub(file_path)
        
        title_meta = book.get_metadata('DC', 'title')
        title = title_meta[0][0] if title_meta else None
        
        creator = book.get_metadata('DC', 'creator')
        author = creator[0][0] if creator else None
        
        desc_data = book.get_metadata('DC', 'description')
        description = ""
        if desc_data:
            try:
                raw_desc = desc_data[0][0]
                soup = BeautifulSoup(raw_desc, "html.parser")
                description = soup.get_text(separator="\n").strip()
            except:
                description = "Sin descripción disponible."
        else:
            description = "Sin descripción disponible."

        cover_path = ""
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_COVER or (item.get_type() == ebooklib.ITEM_IMAGE and "cover" in item.id.lower()):
                ext = ".png" if item.file_name.lower().endswith(".png") else ".jpg"
                path_hash = hashlib.md5(file_path.encode()).hexdigest()
                cover_filename = f"cover_{path_hash}{ext}"
                disk_cover_path = os.path.join(COVERS_DIR, cover_filename)
                
                if not os.path.exists(disk_cover_path):
                    try:
                        with open(disk_cover_path, "wb") as f:
                            f.write(item.get_content())
                    except Exception as e:
                        logging.error(f"No se pudo escribir la portada: {e}")
                cover_path = f"/static/covers/{cover_filename}"
                break
                
        # Si no había imagen marcada como portada, buscar la primera imagen del libro
        if not cover_path:
            for item in book.get_items():
                if item.get_type() == ebooklib.ITEM_IMAGE:
                    ext = ".png" if item.file_name.lower().endswith(".png") else ".jpg"
                    path_hash = hashlib.md5(file_path.encode()).hexdigest()
                    cover_filename = f"cover_{path_hash}{ext}"
                    disk_cover_path = os.path.join(COVERS_DIR, cover_filename)
                    if not os.path.exists(disk_cover_path):
                        try:
                            with open(disk_cover_path, "wb") as f:
                                f.write(item.get_content())
                        except Exception as e:
                            logging.error(f"No se pudo escribir la imagen: {e}")
                    cover_path = f"/static/covers/{cover_filename}"
                    break
                
        isbn = ""
        try:
            identifiers = book.get_metadata('DC', 'identifier')
            if identifiers:
                for id_entry in identifiers:
                    val = id_entry[0] if isinstance(id_entry, (list, tuple)) else str(id_entry)
                    cand = extract_isbn_from_text(val)
                    if cand:
                        isbn = cand
                        break
        except Exception:
            pass

        if not title:
            fn_title, fn_author = parse_filename_metadata(os.path.basename(file_path))
            title = fn_title
            if not author:
                author = fn_author

        return {
            "title": title,
            "author": author or "Autor Desconocido",
            "description": description,
            "cover_path": cover_path,
            "file_path": file_path,
            "isbn": isbn,
            "format": "epub"
        }
    except Exception as e:
        logging.info(f"Usando parser de rescate para {os.path.basename(file_path)}: {e}")
        return extract_metadata_fallback(file_path)

scan_state = {
    "running": False,
    "library_id": 1,
    "library_name": "",
    "total_files": 0,
    "processed": 0,
    "new_books": 0,
    "current_file": "",
    "stop_requested": False,
    "last_result": None
}

def scan_directory(directory: str, library_id: int = 1, library_name: str = ""):
    global scan_state
    logging.info(f"INICIANDO ESCANEO MASIVO (Biblioteca ID: {library_id}): {directory}")
    
    # Reiniciar estado
    scan_state["running"] = True
    scan_state["library_id"] = library_id
    scan_state["library_name"] = library_name or f"Biblioteca #{library_id}"
    scan_state["processed"] = 0
    scan_state["new_books"] = 0
    scan_state["current_file"] = "Contando archivos..."
    scan_state["stop_requested"] = False
    scan_state["last_result"] = None

    # Determinar qué tipos de archivos buscar según la biblioteca
    db_check = SessionLocal()
    target_lib = db_check.query(Library).filter(Library.id == library_id).first()
    lib_type = (target_lib.library_type if target_lib and target_lib.library_type else "all").lower()
    db_check.close()

    if lib_type == "pdf":
        allowed_exts = (".pdf",)
    elif lib_type == "epub":
        allowed_exts = (".epub",)
    else:
        allowed_exts = (".epub", ".pdf")

    # Conteo rápido de archivos
    book_files = []
    try:
        for root, dirs, files in os.walk(directory):
            if scan_state["stop_requested"]:
                break
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in allowed_exts:
                    book_files.append(os.path.abspath(os.path.join(root, file)))
    except Exception as e:
        logging.error(f"Error explorando directorio: {e}")

    scan_state["total_files"] = len(book_files)
    db = SessionLocal()
    batch_size = 50
    lib_map = {l.name: l.id for l in db.query(Library).all()}

    try:
        for file_path in book_files:
            if scan_state["stop_requested"]:
                logging.info("Detención de escaneo solicitada por el usuario.")
                break

            scan_state["processed"] += 1
            filename = os.path.basename(file_path)
            scan_state["current_file"] = filename

            existing = db.query(Book.id).filter(Book.file_path == file_path).first()
            if not existing:
                metadata = extract_metadata(file_path)
                if metadata:
                    new_book = Book(**metadata, library_id=library_id)
                    db.add(new_book)
                    db.flush()  # Obtener new_book.id

                    # 1. Vincular a la biblioteca de destino
                    db.add(BookLibrary(book_id=new_book.id, library_id=library_id))
                    # Si no es la principal (id=1), vincular también a la principal
                    if library_id != 1:
                        db.add(BookLibrary(book_id=new_book.id, library_id=1))

                    # 2. Auto-clasificación en géneros temáticos
                    try:
                        from classify_thematic_libraries import classify_book, extract_subjects_from_epub
                        tags = []
                        if file_path.lower().endswith(".epub"):
                            tags = extract_subjects_from_epub(file_path)
                            if tags:
                                new_book.tags = ", ".join(tags)
                        categories = classify_book(tags, new_book.title, new_book.description)
                        for cat_name in categories:
                            cat_id = lib_map.get(cat_name)
                            if cat_id:
                                db.add(BookLibrary(book_id=new_book.id, library_id=cat_id))
                    except Exception:
                        pass

                    scan_state["new_books"] += 1

                    if scan_state["new_books"] % batch_size == 0:
                        db.commit()
                        logging.info(f"Progreso: {scan_state['processed']}/{scan_state['total_files']} archivos analizados | {scan_state['new_books']} nuevos en DB")

        db.commit()
    except Exception as e:
        logging.error(f"Error crítico en escaneo: {e}")
        db.rollback()
    finally:
        db.close()
        scan_state["last_result"] = {
            "processed": scan_state["processed"],
            "new_books": scan_state["new_books"],
            "total_files": scan_state["total_files"],
            "stopped": scan_state["stop_requested"]
        }
        scan_state["running"] = False
        scan_state["current_file"] = ""
        scan_state["stop_requested"] = False

    logging.info(f"Escaneo finalizado. Analizados: {scan_state['last_result']['processed']}, Nuevos: {scan_state['last_result']['new_books']} en Biblioteca {library_id}")

def parse_and_save_epub(file_path: str, library_id: int = 1):
    db = SessionLocal()
    try:
        file_path = os.path.abspath(file_path)
        existing = db.query(Book).filter(Book.file_path == file_path).first()
        if existing:
            return existing
        
        metadata = extract_metadata(file_path)
        if metadata:
            new_book = Book(**metadata, library_id=library_id)
            db.add(new_book)
            db.flush()

            # Vincular a la biblioteca física
            db.add(BookLibrary(book_id=new_book.id, library_id=library_id))
            if library_id != 1:
                db.add(BookLibrary(book_id=new_book.id, library_id=1))

            # Auto-clasificación en géneros temáticos (solo si es epub o si tiene descripción/tags)
            try:
                from classify_thematic_libraries import classify_book, extract_subjects_from_epub
                lib_map = {l.name: l.id for l in db.query(Library).all()}
                tags = []
                if file_path.lower().endswith(".epub"):
                    tags = extract_subjects_from_epub(file_path)
                    if tags:
                        new_book.tags = ", ".join(tags)
                categories = classify_book(tags, new_book.title, new_book.description)
                for cat_name in categories:
                    cat_id = lib_map.get(cat_name)
                    if cat_id:
                        db.add(BookLibrary(book_id=new_book.id, library_id=cat_id))
            except Exception:
                pass

            db.commit()
            db.refresh(new_book)
            return new_book
    finally:
        db.close()
    return None

def remove_book_by_path(file_path: str):
    """Elimina un libro de la base de datos si su archivo EPUB ha sido borrado físicamente del disco."""
    db = SessionLocal()
    try:
        abs_path = os.path.abspath(file_path)
        book = db.query(Book).filter(Book.file_path == abs_path).first()
        if book:
            book_title = book.title
            db.delete(book)
            db.commit()
            logging.info(f"Libro eliminado de la base de datos por eliminación de archivo: '{book_title}' ({abs_path})")
            return True
    except Exception as e:
        logging.error(f"Error al eliminar libro por borrado de archivo: {e}")
        db.rollback()
    finally:
        db.close()
    return False
