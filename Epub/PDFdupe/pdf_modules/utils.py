import os
import sys
import locale
import datetime
from pathlib import Path

# =========================================================
# CONFIGURACIÓN GLOBAL
# =========================================================

LOG_FILENAME = "pdfdupe.log"

# =========================================================
# GESTIÓN DE IDIOMA
# =========================================================

def get_system_language():
    """Detecta el idioma del sistema. Devuelve 'es' si es español, 'en' si no."""
    try:
        lang_code = locale.getlocale()[0]
        if lang_code and lang_code.lower().startswith('es'):
            return 'es'
    except Exception:
        pass
    lang_env = os.environ.get('LANG', 'en_US')
    if lang_env and lang_env.lower().startswith('es'):
        return 'es'
    return 'en'

# =========================================================
# LOGGING UNIFICADO
# =========================================================

class _TeeStream:
    """Duplica la salida: escribe en la consola original Y en el fichero de log."""
    def __init__(self, original_stream, file_handle):
        self._original = original_stream
        self._file = file_handle

    def write(self, data):
        self._original.write(data)
        if self._file and not self._file.closed:
            try:
                self._file.write(data)
            except Exception:
                pass

    def flush(self):
        self._original.flush()
        if self._file and not self._file.closed:
            try:
                self._file.flush()
            except Exception:
                pass

    def fileno(self):
        return self._original.fileno()

    def isatty(self):
        return self._original.isatty()


class Logger:
    def __init__(self):
        # Directorio interno del proyecto
        base_dir = Path(__file__).resolve().parent.parent
        self.doc_dir = os.path.join(base_dir, "data")
        if not os.path.exists(self.doc_dir):
            os.makedirs(self.doc_dir, exist_ok=True)
            
        self.log_file_path = os.path.join(self.doc_dir, LOG_FILENAME)
        self.file_handle = None
        self._original_stdout = sys.stdout

        try:
            self.file_handle = open(self.log_file_path, 'a', encoding='utf-8')
            sys.stdout = _TeeStream(self._original_stdout, self.file_handle)
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.file_handle.write(f"\n{'='*60}\n")
            self.file_handle.write(f"  SESIÓN INICIADA: {timestamp}\n")
            self.file_handle.write(f"{'='*60}\n")
            self.file_handle.flush()
        except Exception as e:
            sys.stderr.write(f"[LOG ERROR] No se pudo crear archivo de log: {e}\n")

    def set_folder(self, folder_path):
        print(f"[LOG] Carpeta de trabajo: {folder_path}")

    def log(self, message):
        print(message)

    def close(self):
        if self.file_handle and not self.file_handle.closed:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try:
                self.file_handle.write(f"{'='*60}\n")
                self.file_handle.write(f"  SESIÓN FINALIZADA: {timestamp}\n")
                self.file_handle.write(f"{'='*60}\n")
                self.file_handle.flush()
            except Exception:
                pass
            sys.stdout = self._original_stdout
            self.file_handle.close()
            self.file_handle = None


logger = Logger()

# =========================================================
# UI HELPERS
# =========================================================

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner(title, char='='):
    width = 65
    print(f"\n{char * width}")
    print(f"{title.center(width)}")
    print(f"{char * width}\n")

def ask_yes_no(question, lang='es'):
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
    while True:
        path_str = input(prompt).strip()
        if (path_str.startswith('"') and path_str.endswith('"')) or (path_str.startswith("'") and path_str.endswith("'")):
            path_str = path_str[1:-1].strip()
        if not path_str and default_current:
            return os.getcwd()
        if os.path.isdir(path_str):
            return os.path.abspath(path_str)
        else:
            print(f"Error: '{path_str}' no es un directorio válido.")

def format_size(bytes_val):
    """Devuelve formato legible KB/MB/GB."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_val < 1024.0:
            return f"{bytes_val:3.1f} {unit}"
        bytes_val /= 1024.0
    return f"{bytes_val:.1f} TB"

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
