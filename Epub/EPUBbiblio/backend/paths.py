import os

# Carpeta raíz del programa
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Carpeta centralizada en Documentos del usuario actual (compatible con cualquier PC)
DOCUMENTS_DIR = os.path.join(os.path.expanduser("~"), "Documents", "Epubbiblio")
os.makedirs(DOCUMENTS_DIR, exist_ok=True)

# Rutas de archivos de datos
DB_PATH = os.path.join(DOCUMENTS_DIR, "biblio.db")
COVERS_DIR = os.path.join(DOCUMENTS_DIR, "covers")
LOG_PATH = os.path.join(BASE_DIR, "epub_biblio.log")
SETTINGS_PATH = os.path.join(DOCUMENTS_DIR, "settings.json")

# Asegurar que existe la carpeta de portadas
os.makedirs(COVERS_DIR, exist_ok=True)

RECOVERY_KEY_PATH = os.path.join(DOCUMENTS_DIR, "recovery_key.txt")

def get_or_create_recovery_key() -> str:
    """Obtiene o genera una clave maestra de recuperación guardada en el disco local."""
    import secrets
    import string
    if os.path.exists(RECOVERY_KEY_PATH):
        try:
            with open(RECOVERY_KEY_PATH, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        return line
        except Exception:
            pass

    # Generar una nueva clave con formato EPUB-XXXX-XXXX-XXXX
    chars = string.ascii_uppercase + string.digits
    part1 = "".join(secrets.choice(chars) for _ in range(4))
    part2 = "".join(secrets.choice(chars) for _ in range(4))
    part3 = "".join(secrets.choice(chars) for _ in range(4))
    key = f"EPUB-{part1}-{part2}-{part3}"

    content = (
        "# ================================================================\n"
        "# CLAVE DE RECUPERACIÓN MAESTRA DE EPUB BIBLIO\n"
        "# ================================================================\n"
        "# Si olvidas la contraseña del usuario Master, puedes utilizar este\n"
        "# código en la pantalla web de '¿Olvidaste tu contraseña?' para\n"
        "# restablecerla de forma segura.\n"
        "# Consérvalo en un lugar seguro.\n"
        "# ================================================================\n\n"
        f"{key}\n"
    )
    with open(RECOVERY_KEY_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    return key
