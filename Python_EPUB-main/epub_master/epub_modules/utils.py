import os
import sys
import locale
import datetime
from pathlib import Path

# =========================================================
# CONFIGURACIÓN GLOBAL
# =========================================================

LOG_FILENAME = "epubmaster.log"

# =========================================================
# GESTIÓN DE IDIOMA
# =========================================================

def get_system_language():
    """Detecta el idioma del sistema. Devuelve 'es' si es español, 'en' si no."""
    try:
        lang_code = locale.getlocale()[0]
        if lang_code and lang_code.lower().startswith('es'):
            return 'es'
    except:
        pass
    # Fallback a variable de entorno si locale falla
    lang_env = os.environ.get('LANG', 'en_US')
    if lang_env and lang_env.lower().startswith('es'):
        return 'es'
        
    return 'en'

# =========================================================
# LOGGING UNIFICADO
# =========================================================

class Logger:
    def __init__(self, folder_path=None):
        # Usamos el directorio padre de epub_modules como base
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.log_file_path = os.path.join(self.base_dir, LOG_FILENAME)
        self.file_handle = None
        # Iniciamos el log inmediatamente
        try:
            self.file_handle = open(self.log_file_path, 'a', encoding='utf-8')
            self.log("--- SESIÓN INICIADA ---")
        except Exception as e:
            print(f"[ERROR] No se pudo crear archivo de log: {e}")

    def set_folder(self, folder_path):
        """Registra el cambio de la carpeta de trabajo y lo notifica en el log."""
        self.log(f"Carpeta de trabajo establecida en: {folder_path}")

    def log(self, message, print_to_console=False):
        """Escribe en el log y opcionalmente en consola."""
        timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        formatted_message = f"{timestamp} {message}"
        
        if self.file_handle:
            try:
                self.file_handle.write(formatted_message + "\n")
                self.file_handle.flush()
            except:
                pass
        
        if print_to_console:
            print(message)

    def close(self):
        if self.file_handle:
            self.log("--- SESIÓN FINALIZADA ---")
            self.file_handle.close()
            self.file_handle = None

# Instancia global para ser usada por todos los módulos
logger = Logger()

# =========================================================
# UI HELPERS
# =========================================================

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner(title, char='='):
    width = 60
    print(f"\n{char * width}")
    print(f"{title.center(width)}")
    print(f"{char * width}\n")

def ask_yes_no(question, lang='es'):
    """Pregunta S/N o Y/N según idioma."""
    opts = "S/N" if lang == 'es' else "Y/N"
    affirmative = ['S', 'Y']
    
    while True:
        response = input(f"{question} ({opts}): ").strip().upper()
        if not response:
            continue
        if response in affirmative:
            return True
        if response in ['N']:
            return False
            
def input_path(prompt, default_current=True):
    """Solicita una ruta, valida que exista."""
    while True:
        path_str = input(prompt).strip()
        if not path_str and default_current:
            return os.getcwd()
            
        if os.path.isdir(path_str):
            return path_str
        else:
            print(f"Error: '{path_str}' no es un directorio válido.")

# =========================================================
# TEXTOS COMUNES
# =========================================================

COMMON_TEXTS = {
    'es': {
        'continue_prompt': "¿Desea continuar?",
        'operation_cancelled': "Operación cancelada.",
        'process_finished': "Proceso finalizado.",
        'press_enter': "Presione ENTER para continuar...",
        'invalid_option': "Opción no válida."
    },
    'en': {
        'continue_prompt': "Do you wish to continue?",
        'operation_cancelled': "Operation cancelled.",
        'process_finished': "Process finished.",
        'press_enter': "Press ENTER to continue...",
        'invalid_option': "Invalid option."
    }
}
