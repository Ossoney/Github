import os
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
from database import SessionLocal, Book
from paths import COVERS_DIR
import logging
import hashlib

def extract_metadata(file_path: str):
    """Extrae metadatos y guarda la carátula físicamente. No toca la DB."""
    try:
        # ebooklib extrae todo el archivo, lo que es lento para 74k libros.
        # Sin embargo, optimizamos la parte de la base de datos para compensar.
        book = epub.read_epub(file_path)
    except Exception as e:
        logging.error(f"Error procesando {file_path}: {e}")
        return None

    title_meta = book.get_metadata('DC', 'title')
    title = title_meta[0][0] if title_meta else "Título Desconocido"
    
    creator = book.get_metadata('DC', 'creator')
    author = creator[0][0] if creator else "Autor Desconocido"
    
    desc_data = book.get_metadata('DC', 'description')
    description = ""
    if desc_data:
        try:
            raw_desc = desc_data[0][0]
            soup = BeautifulSoup(raw_desc, "html.parser")
            description = soup.get_text(separator="\n").strip()
        except:
            description = "Error procesando descripción."
    else:
        description = "Sin descripción disponible."

    cover_path = ""
    # Buscar imagen de portada
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_COVER or (item.get_type() == ebooklib.ITEM_IMAGE and "cover" in item.id.lower()):
            ext = ".png" if item.file_name.lower().endswith(".png") else ".jpg"
            # Nombre determinista basado en el path para evitar duplicados
            path_hash = hashlib.md5(file_path.encode()).hexdigest()
            cover_filename = f"cover_{path_hash}{ext}"
            cover_path = os.path.join(COVERS_DIR, cover_filename)
            
            if not os.path.exists(cover_path):
                try:
                    with open(cover_path, "wb") as f:
                        f.write(item.get_content())
                except Exception as e:
                    logging.error(f"No se pudo escribir la portada para {title}: {e}")
            break
            
    return {
        "title": title,
        "author": author,
        "description": description,
        "cover_path": "/" + cover_path.replace('\\', '/') if cover_path else "",
        "file_path": file_path
    }

def scan_directory(directory: str):
    logging.info(f"INICIANDO ESCANEO MASIVO: {directory}")
    db = SessionLocal()
    
    batch_size = 50  # Guardar cada 50 libros para máxima velocidad
    processed_count = 0
    new_books_count = 0
    
    try:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.lower().endswith(".epub"):
                    processed_count += 1
                    file_path = os.path.abspath(os.path.join(root, file))
                    
                    # Comprobación ultra rápida gracias al índice en DB
                    existing = db.query(Book.id).filter(Book.file_path == file_path).first()
                    
                    if not existing:
                        metadata = extract_metadata(file_path)
                        if metadata:
                            new_book = Book(**metadata)
                            db.add(new_book)
                            new_books_count += 1
                            
                            # Commit por lotes: esto reduce drásticamente el uso de disco
                            if new_books_count % batch_size == 0:
                                db.commit()
                                logging.info(f"Progreso: {processed_count} archivos analizados | {new_books_count} nuevos en DB")

        db.commit() # Asegurar los últimos libros
    except Exception as e:
        logging.error(f"Error crítico en escaneo: {e}")
        db.rollback()
    finally:
        db.close()
        
    logging.info(f"Escaneo finalizado. Analizados: {processed_count}, Nuevos: {new_books_count}")

def parse_and_save_epub(file_path: str):
    """Mantenemos esta para compatibilidad con el Watcher (autodetección)."""
    db = SessionLocal()
    try:
        file_path = os.path.abspath(file_path)
        existing = db.query(Book).filter(Book.file_path == file_path).first()
        if existing:
            return existing
        
        metadata = extract_metadata(file_path)
        if metadata:
            new_book = Book(**metadata)
            db.add(new_book)
            db.commit()
            db.refresh(new_book)
            return new_book
    finally:
        db.close()
    return None
