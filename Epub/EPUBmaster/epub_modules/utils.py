import os
import sys
import re
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
        """Necesario para que os.system() y similares no fallen."""
        return self._original.fileno()

    def isatty(self):
        return self._original.isatty()


class Logger:
    def __init__(self):
        # Directorio raíz del programa (donde reside EPUBMaster.py)
        self.doc_dir = str(Path(__file__).resolve().parent.parent)
        self.log_file_path = os.path.join(self.doc_dir, LOG_FILENAME)
        self.file_handle = None
        self._original_stdout = sys.stdout  # guardamos el stdout real

        try:
            self.file_handle = open(self.log_file_path, 'a', encoding='utf-8')
            # Redirigimos stdout para que todo print() vaya también al log
            sys.stdout = _TeeStream(self._original_stdout, self.file_handle)
            # Primera entrada con separador de sesión
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.file_handle.write(f"\n{'='*60}\n")
            self.file_handle.write(f"  SESIÓN INICIADA: {timestamp}\n")
            self.file_handle.write(f"{'='*60}\n")
            self.file_handle.flush()
        except Exception as e:
            # Si no podemos abrir el log, al menos no rompemos la app
            sys.stderr.write(f"[LOG ERROR] No se pudo crear archivo de log: {e}\n")

    def set_folder(self, folder_path):
        """Registra el cambio de carpeta de trabajo en el log."""
        print(f"[LOG] Carpeta de trabajo: {folder_path}")

    def log(self, message):
        """Log a message directly."""
        print(message)

    def close(self):
        """Restaura stdout original y cierra el fichero de log."""
        if self.file_handle and not self.file_handle.closed:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try:
                self.file_handle.write(f"{'='*60}\n")
                self.file_handle.write(f"  SESIÓN FINALIZADA: {timestamp}\n")
                self.file_handle.write(f"{'='*60}\n")
                self.file_handle.flush()
            except Exception:
                pass
            # Restauramos stdout antes de cerrar el fichero
            sys.stdout = self._original_stdout
            self.file_handle.close()
            self.file_handle = None


# Instancia global — al instanciarse ya redirige sys.stdout
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

# =========================================================
# EXTRACCIÓN RÁPIDA DE METADATOS EPUB (ZIP + XML)
# =========================================================

def get_epub_metadata_fast(epub_path):
    """
    Extrae título y autor directamente leyendo el archivo OPF del ZIP.
    Es de 15 a 50 veces más rápido que ebooklib.read_epub() y no se rompe
    si el libro contiene imágenes o recursos faltantes referenciados en el manifest.
    Retorna: (title, author) o (None, None)
    """
    import zipfile
    import xml.etree.ElementTree as ET

    try:
        with zipfile.ZipFile(str(epub_path), 'r') as z:
            # 1. Encontrar la ruta del archivo OPF mediante META-INF/container.xml
            opf_rel = None
            try:
                container_data = z.read('META-INF/container.xml')
                root = ET.fromstring(container_data)
                for elem in root.iter():
                    if elem.tag.endswith('rootfile'):
                        opf_rel = elem.attrib.get('full-path')
                        if opf_rel:
                            break
            except Exception:
                pass

            # Si container.xml no existe o no tiene rootfile, buscar primer .opf
            if not opf_rel:
                for name in z.namelist():
                    if name.lower().endswith('.opf'):
                        opf_rel = name
                        break

            if not opf_rel or opf_rel not in z.namelist():
                return None, None

            # 2. Parsear el archivo OPF
            opf_data = z.read(opf_rel)
            opf_root = ET.fromstring(opf_data)

            title = ""
            creator = ""

            for elem in opf_root.iter():
                tag_lower = elem.tag.lower()
                if tag_lower.endswith('title') and not title:
                    title = (elem.text or "").strip()
                elif tag_lower.endswith('creator') and not creator:
                    creator = (elem.text or "").strip()
                if title and creator:
                    break

            return (title if title else None), (creator if creator else None)
    except Exception:
        return None, None


def update_epub_author_metadata(epub_path, new_author="VV.AA."):
    """
    Actualiza el metadato de autor (dc:creator) dentro del OPF del archivo EPUB.
    Preserva mimetype al inicio sin comprimir y realiza reemplazo atómico.
    Retorna True si tuvo éxito, False en caso contrario.
    """
    import zipfile
    import xml.etree.ElementTree as ET
    from pathlib import Path

    path = Path(epub_path)
    tmp_path = path.with_suffix(".tmp_meta")

    try:
        with zipfile.ZipFile(str(path), 'r') as zin:
            # 1. Localizar OPF
            opf_rel = None
            try:
                container_data = zin.read('META-INF/container.xml')
                root = ET.fromstring(container_data)
                for elem in root.iter():
                    if elem.tag.endswith('rootfile'):
                        opf_rel = elem.attrib.get('full-path')
                        if opf_rel:
                            break
            except Exception:
                pass

            if not opf_rel:
                for name in zin.namelist():
                    if name.lower().endswith('.opf'):
                        opf_rel = name
                        break

            if not opf_rel or opf_rel not in zin.namelist():
                return False

            opf_content = zin.read(opf_rel).decode('utf-8', errors='replace')

            # Reemplazar texto de <...creator...>...</...creator...>
            # Preservando atributos de etiqueta (ej: opf:role="aut")
            creator_pattern = re.compile(
                r'(<[^:>]*:?creator\b[^>]*>)(.*?)(</[^:>]*:?creator>)',
                re.IGNORECASE | re.DOTALL
            )

            if creator_pattern.search(opf_content):
                updated_opf = creator_pattern.sub(rf'\g<1>{new_author}\g<3>', opf_content)
                # También actualizar atributo opf:file-as si existe
                updated_opf = re.sub(
                    r'(file-as\s*=\s*["\'])([^"\']*)(["\'])',
                    rf'\g<1>{new_author}\g<3>',
                    updated_opf,
                    flags=re.IGNORECASE
                )
            else:
                # Si no existe tag creator, añadirlo dentro de <metadata>
                metadata_match = re.search(r'(<[^:>]*:?metadata\b[^>]*>)', opf_content, re.IGNORECASE)
                if metadata_match:
                    insert_tag = f"\n    <dc:creator>{new_author}</dc:creator>"
                    pos = metadata_match.end()
                    updated_opf = opf_content[:pos] + insert_tag + opf_content[pos:]
                else:
                    return False

            updated_opf_bytes = updated_opf.encode('utf-8')

            # 2. Escribir nuevo zip temporal
            with zipfile.ZipFile(str(tmp_path), 'w', zipfile.ZIP_DEFLATED) as zout:
                if 'mimetype' in zin.namelist():
                    zout.writestr('mimetype', zin.read('mimetype'), compress_type=zipfile.ZIP_STORED)

                for item in zin.infolist():
                    if item.filename == 'mimetype':
                        continue
                    if item.filename == opf_rel:
                        zout.writestr(item, updated_opf_bytes)
                    else:
                        zout.writestr(item, zin.read(item.filename))

        # Reemplazo atómico
        tmp_path.replace(path)
        return True
    except Exception as e:
        logger.log(f"[METADATA ERROR] {path.name}: {e}")
        if tmp_path.exists():
            try:
                tmp_path.unlink()
            except Exception:
                pass
        return False
