import os
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from epub_parser import parse_and_save_epub

class EpubHandler(FileSystemEventHandler):
    def process(self, event):
        if event.is_directory:
            return

        if event.src_path.lower().endswith(".epub"):
            # Pequeña pausa por si el archivo sigue descargándose o escribiéndose
            time.sleep(1.5)
            logging.info(f"Nuevo EPUB detectado: {event.src_path}")
            parse_and_save_epub(event.src_path)

    def on_created(self, event):
        self.process(event)

    # on_modified eliminado: causaba log spam al detectar modificaciones de metadatos
    # de archivos ya registrados en la base de datos.

class LibraryWatcher:
    def __init__(self):
        self.observer = None
        self.watch_path = None
        
    def start_watching(self, path):
        if not os.path.exists(path):
            logging.error(f"El directorio no existe, no se puede vigilar: {path}")
            return

        if self.watch_path == path and self.observer is not None:
            return # Already watching this path
            
        if self.observer:
            self.observer.stop()
            self.observer.join()
            
        self.watch_path = path
        self.observer = Observer()
        event_handler = EpubHandler()
        self.observer.schedule(event_handler, path, recursive=True)
        self.observer.start()
        logging.info(f"Autodetección (Watchdog) iniciada en: {path}")

# Instancia global
watcher = LibraryWatcher()
