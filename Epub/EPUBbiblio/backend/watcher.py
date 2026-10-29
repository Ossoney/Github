import os
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from epub_parser import parse_and_save_epub, remove_book_by_path

class EpubHandler(FileSystemEventHandler):
    def process(self, event):
        if event.is_directory:
            return

        ext = os.path.splitext(event.src_path)[1].lower()
        if ext in (".epub", ".pdf"):
            # Pequeña pausa por si el archivo sigue descargándose o escribiéndose
            time.sleep(1.5)
            logging.info(f"Nuevo libro detectado ({ext.upper()}): {event.src_path}")
            parse_and_save_epub(event.src_path)

    def on_created(self, event):
        self.process(event)

    def on_deleted(self, event):
        if event.is_directory:
            return
        ext = os.path.splitext(event.src_path)[1].lower()
        if ext in (".epub", ".pdf"):
            logging.info(f"Libro eliminado del disco ({ext.upper()}): {event.src_path}")
            remove_book_by_path(event.src_path)

    # on_modified eliminado: causaba log spam al detectar modificaciones de metadatos
    # de archivos ya registrados en la base de datos.

class LibraryWatcher:
    def __init__(self):
        self.observer = None
        self.watched_paths = set()
        
    def start_watching(self, paths):
        """Acepta una ruta individual (str) o una lista/conjunto de rutas para vigilar."""
        if isinstance(paths, str):
            paths = [paths]

        valid_paths = set()
        for p in paths:
            if p and os.path.exists(p):
                valid_paths.add(os.path.abspath(p))
            elif p:
                logging.warning(f"Ruta para vigilar no encontrada: {p}")

        if not valid_paths:
            logging.info("No hay rutas válidas para vigilar con Watchdog.")
            return

        if self.observer and self.watched_paths == valid_paths:
            return  # Ya vigila exactamente estas rutas

        if self.observer:
            try:
                self.observer.stop()
                self.observer.join(timeout=2)
            except Exception as e:
                logging.warning(f"Error al detener vigía anterior: {e}")

        self.watched_paths = valid_paths
        self.observer = Observer()
        event_handler = EpubHandler()

        for p in valid_paths:
            self.observer.schedule(event_handler, p, recursive=True)
            logging.info(f"Autodetección (Watchdog) iniciada en: {p}")

        self.observer.start()

    def update_watches_from_db(self, db_session, fallback_path: str = None):
        """Lee todas las rutas configuradas en las bibliotecas de la DB e inicia la vigilancia."""
        try:
            from database import Library
            paths = set()
            if fallback_path and os.path.exists(fallback_path):
                paths.add(os.path.abspath(fallback_path))
            libs = db_session.query(Library).all()
            for lib in libs:
                if lib.path and os.path.exists(lib.path):
                    paths.add(os.path.abspath(lib.path))
            if paths:
                self.start_watching(paths)
        except Exception as e:
            logging.error(f"Error al actualizar rutas de vigilancia desde la DB: {e}")

# Instancia global
watcher = LibraryWatcher()
