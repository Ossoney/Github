import os

# Carpeta centralizada en Documentos del usuario actual (compatible con cualquier PC)
DOCUMENTS_DIR = os.path.join(os.path.expanduser("~"), "Documents", "Epubbiblio")
os.makedirs(DOCUMENTS_DIR, exist_ok=True)

# Rutas de archivos de datos
DB_PATH = os.path.join(DOCUMENTS_DIR, "biblio.db")
COVERS_DIR = os.path.join(DOCUMENTS_DIR, "covers")
LOG_PATH = os.path.join(DOCUMENTS_DIR, "epub_biblio.log")
SETTINGS_PATH = os.path.join(DOCUMENTS_DIR, "settings.json")

# Asegurar que existe la carpeta de portadas
os.makedirs(COVERS_DIR, exist_ok=True)
