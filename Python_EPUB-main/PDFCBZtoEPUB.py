"""
------------------------------------------------------------------------------
GUÍA DE INSTALACIÓN DE DEPENDENCIAS
------------------------------------------------------------------------------
Para que el programa funcione, abre tu terminal y ejecuta:

[WINDOWS]
pip install PyMuPDF Pillow

[LINUX / MACOS]
pip3 install PyMuPDF Pillow
------------------------------------------------------------------------------
"""

import concurrent.futures
import io
import locale
import logging
import os
import re
import shutil
import statistics
import sys
import tempfile
import time
import unicodedata
import zipfile
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from xml.etree import ElementTree
from xml.sax.saxutils import escape as xml_escape

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

try:
    import pytesseract
    HAS_TESSERACT = True
except ImportError:
    HAS_TESSERACT = False

# Mapa de códigos de idioma PDF → Tesseract
LANG_MAP_TESSERACT = {
    'es': 'spa', 'spa': 'spa', 'ca': 'cat', 'gl': 'glg',
    'en': 'eng', 'eng': 'eng',
    'fr': 'fra', 'fra': 'fra',
    'de': 'deu', 'deu': 'deu',
    'it': 'ita', 'por': 'por', 'pt': 'por',
}

# =========================================================
# DEPENDENCIAS EXTERNAS
# =========================================================
try:
    import fitz  # PyMuPDF
except ImportError:
    print("Error: Install PyMuPDF → pip install PyMuPDF")
    sys.exit(1)

try:
    from PIL import Image
    Image.MAX_IMAGE_PIXELS = 200_000_000
except ImportError:
    print("Error: Install Pillow → pip install Pillow")
    sys.exit(1)

# =========================================================
# LOGGER (Externalized to avoid Git bloat)
# =========================================================
DOCUMENTS_DIR = Path.home() / "Documents" / "Epubbiblio"
DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)
LOG_PATH = DOCUMENTS_DIR / 'pdfcbztoepub.log'

logging.basicConfig(
    filename=str(LOG_PATH),
    level=logging.INFO,
    format='%(asctime)s | %(message)s',
    encoding='utf-8'
)

import builtins
original_print = builtins.print

def log_print(*args, **kwargs):
    text = " ".join(str(arg) for arg in args)
    if text and not text.startswith('='):
        clean_text = text.replace('\r', '').replace('\n', ' ').strip()
        if clean_text:
            if '[ERROR]' in clean_text or 'Error' in clean_text or '❌' in clean_text:
                logging.error(clean_text)
            else:
                logging.info(clean_text)
    original_print(*args, **kwargs)

builtins.print = log_print

# =========================================================
# LOCALIZACIÓN
# =========================================================

def get_ui_language():
    """Devuelve 'es' si el sistema está en español, 'en' en el resto de casos."""
    try:
        default_locale = locale.getlocale()[0]
        if default_locale and default_locale.lower().startswith('es'):
            return 'es'
    except Exception:
        pass
    return 'en'


TEXTS = {
    'es': {
        'PROMO_START': (
            "PDF&CBZtoEPUB es un programa freeware que convierte tus archivos PDF y CBZ\n"
            "en formato EPUB, unificando tu biblioteca en un solo formato.\n"
            "Los PDFs de texto se convierten en EPUBs con capítulos navegables.\n"
            "Los PDFs de imagen y los CBZ (cómics) se convierten en EPUBs de maquetación fija.\n"
            "No te preocupes, los archivos originales se mantienen."
        ),
        'PROMO_END': (
            "---------------------------------------------------------------\n"
            "Si el programa te ha sido útil invítame a un café en paypal.me/ossoney.\n"
            "Envíame 1$ - 2$ - 3$ o lo que te apetezca.\n"
            "---------------------------------------------------------------"
        ),
        'CONTINUE_PROMPT': "\n¿Deseas continuar (S/N)?: ",
        'GOODBYE':         "\nOperación cancelada. ¡Gracias por usar PDF&CBZtoEPUB!",
        'INTERRUPT':       "\n\n(x) Salida forzada por el usuario.",

        'BANNER_CONFIG': "PDF & CBZ TO EPUB - CONFIGURACIÓN",
        'BANNER_MENU':   "PDF & CBZ TO EPUB - MENÚ PRINCIPAL",

        'FOLDER_INTRO':  "Selecciona la carpeta donde guardas tus PDFs y CBZs.",
        'FOLDER_PROMPT': "Ruta de la carpeta (Enter para usar la actual): ",

        'ACTIVE_FOLDER':  "Carpeta activa: {}",
        'SIM_LABEL':      " [SIMULACIÓN]",
        'ACTIONS_HEADER': "\nACCIONES DISPONIBLES{}:",
        'MENU_1':         "Iniciar Conversión a EPUB",
        'MENU_2_ON':      "Desactivar Modo Simulación (Dry-Run)",
        'MENU_2_OFF':     "Activar Modo Simulación (Dry-Run)",
        'MENU_3':         "Cambiar Carpeta",
        'MENU_4':         "Incluir Subcarpetas: {}",
        'MENU_0':         "Salir",
        'SELECT_OPTION':  "\nSelecciona una opción: ",
        'PRESS_ENTER':    "\nPresiona ENTER para volver al menú...",
        'UNKNOWN_CMD':    "Comando no reconocido. Presiona ENTER para continuar...",
        'EXIT_MSG':       "\n¡Desconectando sistemas! Hasta luego.",

        'INVALID_PATH':    "\nError: La ruta seleccionada no es válida.",
        'NO_FILES':        "\nNo se encontraron archivos PDF ni CBZ en esta carpeta.",
        'FOUND_FILES':     "\n[INFO] Se encontraron {} archivos ({} PDFs, {} CBZs). Arrancando motores...",
        'SUCCESS_ALL':     "\n → [COMPLETADO] Conversión terminada.",
        'SIM_FILE':        "[SIMULACIÓN] Convertiría: {} → {}",
        'SIM_MOVE':        "[SIMULACIÓN] Trasladaría original a: ORIGINAL/{}",
        'PROCESSING':      "\n → Procesando: {}",
        'SAVED_OK':        " → [OK] Guardado: {} ({:.1f} MB)",
        'MOVED_OK':        " → [OK] Original trasladado a: ORIGINAL/{}",
        'MOVE_ERROR':      " → [AVISO] No se pudo trasladar el original: {}",
        'PROC_ERROR':      " → [ERROR] Falló: {} → {}",
        'SKIP_EXISTS':     " → [SKIP] Ya existe: {}",
        'SKIP_PROTECTED':  " → [SKIP] PDF protegido: {}",
        'SKIP_EMPTY':      " → [SKIP] Archivo vacío o sin contenido: {}",
        'DETECTED_TEXT':   "   📖 Detectado como PDF de TEXTO ({} caracteres/página de media)",
        'DETECTED_IMAGE':  "   🖼️  Detectado como PDF de IMAGEN ({} caracteres/página de media)",
        'CBZ_CONVERT':     "   🖼️  Convirtiendo CBZ (cómic) a EPUB Fixed-Layout",
        'CHAPTER_FOUND':   "   📑 {} capítulos detectados",
        'PAGES_FOUND':     "   📄 {} páginas procesadas",
        'OPT_BW_DETECTED': "   🔲 Imagen B/N detectada → escala de grises (ahorro extra)",
        'OPT_SAVINGS':     "   📦 Optimización: {:.1f} MB → {:.1f} MB ({:.1f}% ahorro)",
        'TOC_NATIVE':      "   📚 TOC nativo del PDF encontrado ({} entradas)",
        'TOC_HEURISTIC':   "   🔍 Sin TOC nativo. Usando detección heurística de capítulos",
        'RICH_TEXT':        "   ✨ Formato preservado (negrita, cursiva, encabezados)",
        'JPEG_PASSTHRU':   "   ⚡ {} imágenes JPEG copiadas sin recodificación (cero pérdida)",
        'COMIC_INFO':      "   📋 Metadatos ComicInfo.xml encontrados: {}",
        'PROGRESS':        "   [{}/{}]",
        'FILE_SIZE_CMP':   "   📊 Original: {:.1f} MB → EPUB: {:.1f} MB",
        'EXTRACTION':      "   📸 Extrayendo imágenes originales (Modo Lossless)",

        'SUMMARY_TITLE':       "RESUMEN DE CONVERSIÓN",
        'SUMMARY_PROCESSED':   "Archivos procesados:",
        'SUMMARY_PDF_TEXT':    "PDFs de texto → EPUB:",
        'SUMMARY_PDF_IMAGE':   "PDFs de imagen → EPUB:",
        'SUMMARY_CBZ':         "CBZs → EPUB:",
        'SUMMARY_SKIPPED':     "Saltados / Errores:",
        'SUMMARY_COL_TYPE':    "TIPO",
        'SUMMARY_COL_COUNT':   "ARCH.",
        'SUMMARY_COL_ORIG':    "ORIGINAL",
        'SUMMARY_COL_EPUB':    "EPUB",
        'SUMMARY_COL_SAVED':   "AHORRO",
        'SUMMARY_ROW_TEXT':    "PDF Texto",
        'SUMMARY_ROW_IMAGE':   "PDF Imagen",
        'SUMMARY_ROW_CBZ':     "CBZ",
        'SUMMARY_ROW_TOTAL':   "TOTAL",
        'SUMMARY_ROW_SKIP':    "Saltados/Errores",
        'SUMMARY_ROW_MOVED':   "Orig. trasladados",

        'ON':  'SÍ',
        'OFF': 'NO',

        'GOLDEN_TOC_FOUND': "   💎 {} historias detectadas en el índice de la revista",
        'PARALLEL_START':   "🚀 Iniciando turbo-procesamiento paralelo ({} núcleos)...",
        'ASSEMBLING_EPUB':  "📦 Ensamblando EPUB...",
        'SIZE_IMAGES':      "   ⚖️ Tamaño final imágenes: {:.2f} MB",
        'OCR_START':        "   🔍 OCR: procesando {} páginas con Tesseract...",
        'OCR_VIABLE':       "   🔍 OCR viable → convirtiendo a EPUB de texto",
        'OCR_LOW_QUALITY':  "   🖼️  OCR: calidad insuficiente → usando modo imagen",
        'OCR_NOT_AVAIL':    "   ℹ️  Instala pytesseract+Tesseract para activar OCR",
        'OCR_DONE':         "   ✅ OCR completado: {} capítulos detectados",
    },
    'en': {
        'PROMO_START': (
            "PDF&CBZtoEPUB is freeware that converts your PDF and CBZ files\n"
            "into EPUB format, unifying your library into a single format.\n"
            "Text PDFs are converted into EPUBs with navigable chapters.\n"
            "Image PDFs and CBZs (comics) are converted into fixed-layout EPUBs.\n"
            "Don't worry, your original files are kept safe."
        ),
        'PROMO_END': (
            "---------------------------------------------------------------\n"
            "If the program was useful, invite me for a coffee at paypal.me/ossoney.\n"
            "Send $1 - $2 - $3 or whatever you feel like.\n"
            "---------------------------------------------------------------"
        ),
        'CONTINUE_PROMPT': "\nDo you want to continue (Y/N)?: ",
        'GOODBYE':         "\nOperation cancelled. Thank you for using PDF&CBZtoEPUB!",
        'INTERRUPT':       "\n\n(x) Forced exit by user.",

        'BANNER_CONFIG': "PDF & CBZ TO EPUB - SETUP",
        'BANNER_MENU':   "PDF & CBZ TO EPUB - MAIN MENU",

        'FOLDER_INTRO':  "Select the folder where your PDFs and CBZs are stored.",
        'FOLDER_PROMPT': "Folder path (press Enter to use current): ",

        'ACTIVE_FOLDER':  "Active folder: {}",
        'SIM_LABEL':      " [SIMULATION]",
        'ACTIONS_HEADER': "\nAVAILABLE ACTIONS{}:",
        'MENU_1':         "Start Conversion to EPUB",
        'MENU_2_ON':      "Disable Simulation Mode (Dry-Run)",
        'MENU_2_OFF':     "Enable Simulation Mode (Dry-Run)",
        'MENU_3':         "Change Folder",
        'MENU_4':         "Include Subfolders: {}",
        'MENU_0':         "Exit",
        'SELECT_OPTION':  "\nSelect an option: ",
        'PRESS_ENTER':    "\nPress ENTER to return to the menu...",
        'UNKNOWN_CMD':    "Unknown command. Press ENTER to continue...",
        'EXIT_MSG':       "\nShutting down! Goodbye.",

        'INVALID_PATH':    "\nError: The selected path is not valid.",
        'NO_FILES':        "\nNo PDF or CBZ files found in this folder.",
        'FOUND_FILES':     "\n[INFO] Found {} files ({} PDFs, {} CBZs). Starting engines...",
        'SUCCESS_ALL':     "\n → [COMPLETE] Conversion finished.",
        'SIM_FILE':        "[SIMULATION] Would convert: {} → {}",
        'SIM_MOVE':        "[SIMULATION] Would move original to: ORIGINAL/{}",
        'PROCESSING':      "\n → Processing: {}",
        'SAVED_OK':        " → [OK] Saved: {} ({:.1f} MB)",
        'MOVED_OK':        " → [OK] Original moved to: ORIGINAL/{}",
        'MOVE_ERROR':      " → [WARNING] Could not move original: {}",
        'PROC_ERROR':      " → [ERROR] Failed: {} → {}",
        'SKIP_EXISTS':     " → [SKIP] Already exists: {}",
        'SKIP_PROTECTED':  " → [SKIP] Protected PDF: {}",
        'SKIP_EMPTY':      " → [SKIP] Empty file or no content: {}",
        'DETECTED_TEXT':   "   📖 Detected as TEXT PDF ({} chars/page average)",
        'DETECTED_IMAGE':  "   🖼️  Detected as IMAGE PDF ({} chars/page average)",
        'CBZ_CONVERT':     "   🖼️  Converting CBZ (comic) to Fixed-Layout EPUB",
        'CHAPTER_FOUND':   "   📑 {} chapters detected",
        'PAGES_FOUND':     "   📄 {} pages processed",
        'OPT_BW_DETECTED': "   🔲 B/W image detected → grayscale (extra savings)",
        'OPT_SAVINGS':     "   📦 Optimization: {:.1f} MB → {:.1f} MB ({:.1f}% savings)",
        'TOC_NATIVE':      "   📚 Native PDF TOC found ({} entries)",
        'TOC_HEURISTIC':   "   🔍 No native TOC. Using heuristic chapter detection",
        'RICH_TEXT':        "   ✨ Formatting preserved (bold, italic, headings)",
        'JPEG_PASSTHRU':   "   ⚡ {} JPEG images copied without re-encoding (zero loss)",
        'COMIC_INFO':      "   📋 ComicInfo.xml metadata found: {}",
        'PROGRESS':        "   [{}/{}]",
        'FILE_SIZE_CMP':   "   📊 Original: {:.1f} MB → EPUB: {:.1f} MB",
        'EXTRACTION':      "   📸 Extracting original images (Lossless Mode)",

        'SUMMARY_TITLE':       "CONVERSION SUMMARY",
        'SUMMARY_PROCESSED':   "Files processed:",
        'SUMMARY_PDF_TEXT':    "Text PDFs → EPUB:",
        'SUMMARY_PDF_IMAGE':   "Image PDFs → EPUB:",
        'SUMMARY_CBZ':         "CBZs → EPUB:",
        'SUMMARY_SKIPPED':     "Skipped / Errors:",
        'SUMMARY_COL_TYPE':    "TYPE",
        'SUMMARY_COL_COUNT':   "FILES",
        'SUMMARY_COL_ORIG':    "ORIGINAL",
        'SUMMARY_COL_EPUB':    "EPUB",
        'SUMMARY_COL_SAVED':   "SAVINGS",
        'SUMMARY_ROW_TEXT':    "PDF Text",
        'SUMMARY_ROW_IMAGE':   "PDF Image",
        'SUMMARY_ROW_CBZ':     "CBZ",
        'SUMMARY_ROW_TOTAL':   "TOTAL",
        'SUMMARY_ROW_SKIP':    "Skipped/Errors",
        'SUMMARY_ROW_MOVED':   "Originals moved",

        'ON':  'YES',
        'OFF': 'NO',

        'GOLDEN_TOC_FOUND': "   💎 {} stories detected in the magazine index",
        'PARALLEL_START':   "🚀 Starting turbo parallel processing ({} cores)...",
        'ASSEMBLING_EPUB':  "📦 Assembling EPUB...",
        'SIZE_IMAGES':      "   ⚖️ Final image size: {:.2f} MB",
        'OCR_START':        "   🔍 OCR: processing {} pages with Tesseract...",
        'OCR_VIABLE':       "   🔍 OCR viable → converting to text EPUB",
        'OCR_LOW_QUALITY':  "   🖼️  OCR: insufficient quality → using image mode",
        'OCR_NOT_AVAIL':    "   ℹ️  Install pytesseract+Tesseract to enable OCR",
        'OCR_DONE':         "   ✅ OCR done: {} chapters detected",
    },
}

# =========================================================
# UTILIDADES DE INTERFAZ
# =========================================================

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner(text):
    print("=" * 64)
    print(f" {text}")
    print("=" * 64)

def input_path(prompt):
    ruta = input(prompt).strip()
    return ruta.strip('"\'')

def sanitize_filename(name: str) -> str:
    """Elimina caracteres prohibidos y acorta nombres."""
    name = re.sub(r'[\\/*?:"<>|]', "", name).strip()
    return name[:200]

# =========================================================
# GENERADORES DE ESTRUCTURA EPUB
# =========================================================

MIMETYPE = "application/epub+zip"

CONTAINER_XML = """<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>"""


def generate_opf_reflowable(title: str, author: str, uid: str,
                             manifest_items: List[str], spine_items: List[str],
                             language: str = 'es') -> str:
    """Genera content.opf para un EPUB reflowable (texto)."""
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="uid">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="uid">{xml_escape(uid)}</dc:identifier>
    <dc:title>{xml_escape(title)}</dc:title>
    <dc:creator>{xml_escape(author)}</dc:creator>
    <dc:language>{xml_escape(language)}</dc:language>
    <meta property="dcterms:modified">2026-01-01T00:00:00Z</meta>
  </metadata>
  <manifest>
{chr(10).join(manifest_items)}
  </manifest>
  <spine>
{chr(10).join(spine_items)}
  </spine>
</package>"""


def generate_opf_fxl(title: str, uid: str, pages: List[dict],
                      width: int, height: int,
                      author: str = '', language: str = 'es') -> str:
    """Genera content.opf para un EPUB Fixed-Layout (imágenes)."""
    manifest_lines = []
    spine_lines = []

    manifest_lines.append(
        '    <item id="nav" href="nav.xhtml" '
        'media-type="application/xhtml+xml" properties="nav"/>'
    )
    manifest_lines.append(
        '    <item id="css" href="estilos.css" media-type="text/css"/>'
    )

    for p in pages:
        manifest_lines.append(
            f'    <item id="{p["page_id"]}" href="{p["page_href"]}" '
            f'media-type="application/xhtml+xml"/>'
        )
        # Detectar media-type real según extensión de la imagen
        img_href = p["img_href"]
        if img_href.lower().endswith('.png'):
            img_media_type = "image/png"
        elif img_href.lower().endswith('.webp'):
            img_media_type = "image/webp"
        else:
            img_media_type = "image/jpeg"
        manifest_lines.append(
            f'    <item id="{p["img_id"]}" href="{img_href}" '
            f'media-type="{img_media_type}"/>'
        )
        spine_lines.append(f'    <itemref idref="{p["page_id"]}"/>')

    author_tag = f"\n    <dc:creator>{xml_escape(author)}</dc:creator>" if author else ""
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="uid">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="uid">{xml_escape(uid)}</dc:identifier>
    <dc:title>{xml_escape(title)}</dc:title>{author_tag}
    <dc:language>{xml_escape(language)}</dc:language>
    <meta property="dcterms:modified">2026-01-01T00:00:00Z</meta>
    <meta property="rendition:layout">pre-paginated</meta>
    <meta property="rendition:spread">auto</meta>
    <meta name="viewport" content="width={width}, height={height}"/>
  </metadata>
  <manifest>
{chr(10).join(manifest_lines)}
  </manifest>
  <spine>
{chr(10).join(spine_lines)}
  </spine>
</package>"""


def generate_nav_reflowable(title: str, chapters: List[dict]) -> str:
    """Genera nav.xhtml para EPUB reflowable."""
    li_lines = []
    for i, ch in enumerate(chapters, 1):
        href = f"chapter_{i:03d}.xhtml"
        li_lines.append(
            f'        <li><a href="{href}">{xml_escape(ch["title"])}</a></li>'
        )
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head><title>Navigation</title></head>
<body>
  <nav epub:type="toc" id="toc">
    <h1>{xml_escape(title)}</h1>
    <ol>
{chr(10).join(li_lines)}
    </ol>
  </nav>
</body>
</html>"""


def generate_nav_fxl(pages: List[dict]) -> str:
    """Genera nav.xhtml para EPUB Fixed-Layout."""
    li_lines = []
    for p in pages:
        li_lines.append(
            f'        <li><a href="{p["page_href"]}">{xml_escape(p["label"])}</a></li>'
        )
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head><title>Navigation</title></head>
<body>
  <nav epub:type="toc" id="toc">
    <h1>Contents</h1>
    <ol>
{chr(10).join(li_lines)}
    </ol>
  </nav>
</body>
</html>"""


def generate_fxl_page_xhtml(img_filename: str, width: int, height: int) -> str:
    """Genera el XHTML de una página FXL que muestra una imagen."""
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <title>Page</title>
  <meta name="viewport" content="width={width}, height={height}"/>
  <link rel="stylesheet" type="text/css" href="estilos.css"/>
</head>
<body style="margin:0;padding:0;">
  <div class="fxl-page">
    <img src="images/{img_filename}" alt="page" style="width:100%;height:100%;"/>
  </div>
</body>
</html>"""


def generate_cover_xhtml(cover_filename: str = 'cover.jpg') -> str:
    """Genera la página de portada para EPUB reflowable."""
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <title>Cover</title>
  <link rel="stylesheet" type="text/css" href="estilos.css"/>
</head>
<body>
  <div class="cover-page">
    <img src="images/{cover_filename}" alt="Cover"/>
  </div>
</body>
</html>"""


def generate_chapter_xhtml(title: str, content_html: List[str]) -> str:
    """Genera el XHTML de un capítulo reflowable.
    Acepta contenido HTML pre-formateado (con <p>, <strong>, <em>, <h2>, etc.)."""
    body_lines = []
    for element in content_html:
        if element and element.strip():
            body_lines.append(f"  {element}")

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <title>{xml_escape(title)}</title>
  <link rel="stylesheet" type="text/css" href="estilos.css"/>
</head>
<body>
  <h1>{xml_escape(title)}</h1>
{chr(10).join(body_lines)}
</body>
</html>"""


CSS_REFLOWABLE = """
@page { margin: 1cm; }
html {
  background-color: #1e1e1e; /* Color oscuro premium para el navegador */
}
body {
  margin: 0;
  padding: 5% 8%;
  font-family: "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  font-size: 1.15em; /* Tamaño de letra más grande y evidente */
  line-height: 1.6;
  color: #e0e0e0; /* Texto claro de alto contraste */
  background-color: #1e1e1e;
  text-align: justify;
}
h1, h2, h3 {
  color: #ffffff;
  text-align: center;
  margin-top: 1.5em;
  border-bottom: 1px solid #333;
  padding-bottom: 0.3em;
}
p {
  text-indent: 1.5em;
  margin: 0.5em 0;
}
strong {
  font-weight: bold;
}
em {
  font-style: italic;
}
.img-container {
  text-align: center;
  margin: 2em 0;
}
.img-container img {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.5);
}
"""

CSS_FXL = """
html, body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  background-color: #000000; /* Negro puro para máximo contraste en imágenes */
}
.fxl-page {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
}
img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}
"""


# =========================================================
# EMPAQUETADOR EPUB
# =========================================================

def pack_epub(source_dir: Path, epub_path: Path):
    """Empaqueta un directorio como EPUB respetando el estándar
    (mimetype primero, sin compresión). Usa compresión nivel 9 para XHTML/CSS."""
    with zipfile.ZipFile(epub_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        # mimetype DEBE ir primero y sin compresión
        mimetype_path = source_dir / 'mimetype'
        if mimetype_path.exists():
            zf.write(mimetype_path, 'mimetype', compress_type=zipfile.ZIP_STORED)

        for root, dirs, files in os.walk(source_dir):
            for fname in sorted(files):
                if fname == 'mimetype' and Path(root) == source_dir:
                    continue
                full = Path(root) / fname
                arcname = full.relative_to(source_dir).as_posix()
                zf.write(full, arcname)


# =========================================================
# CONVERSORES
# =========================================================

def detect_pdf_type(doc: fitz.Document) -> Tuple[str, int]:
    """Detecta si un PDF es de texto o de imagen.
    Si detecta imágenes que cubren gran parte de la página incluso
    con texto presente (OCR), lo clasifica como imagen para preservar calidad."""
    total_chars = 0
    pages_to_check = min(len(doc), 10)
    has_full_page_images = 0

    for i in range(pages_to_check):
        page = doc.load_page(i)
        text = page.get_text("text").strip()
        total_chars += len(text)
        
        # Comprobar si hay imágenes grandes (posible OCR)
        img_info = page.get_image_info()
        page_area = page.rect.width * page.rect.height
        for info in img_info:
            bbox = info['bbox']
            inv_area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])
            if inv_area > page_area * 0.7:
                has_full_page_images += 1
                break

    avg_chars = total_chars // max(pages_to_check, 1)
    
    if has_full_page_images > (pages_to_check / 2):
        return 'image', avg_chars
        
    if avg_chars > 200:
        return 'text', avg_chars
    else:
        return 'image', avg_chars


def extract_cover_from_pdf(doc: fitz.Document) -> Optional[bytes]:
    """Intenta extraer la portada del PDF (primera página como imagen)."""
    try:
        page = doc.load_page(0)
        pix = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0))
        img = Image.open(io.BytesIO(pix.tobytes("ppm")))
        if img.mode != 'RGB':
            img = img.convert('RGB')
        buf = io.BytesIO()
        img.save(buf, "JPEG", quality=85, optimize=True)
        return buf.getvalue()
    except Exception:
        return None


def _detect_body_font_size(doc: fitz.Document) -> float:
    """Determina el tamaño de fuente del cuerpo de texto (mediana).
    Muestrea hasta 5 páginas para ser rápido."""
    all_sizes = []
    pages_to_check = min(len(doc), 5)
    for i in range(pages_to_check):
        page = doc.load_page(i)
        blocks = page.get_text("dict", flags=fitz.TEXT_PRESERVE_WHITESPACE).get("blocks", [])
        for block in blocks:
            if block.get("type") != 0:
                continue
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = span.get("text", "").strip()
                    if len(text) > 10:  # Solo texto sustancial
                        all_sizes.append(span.get("size", 12.0))
    if all_sizes:
        return statistics.median(all_sizes)
    return 12.0


def clean_text_for_epub(text: str) -> str:
    """Normaliza unicode y elimina caracteres no imprimibles o problemáticos."""
    if not text: return ""
    # Normalizar (ligaduras, acentos combinados, etc)
    text = unicodedata.normalize('NFKC', text)
    # Eliminar caracteres de la categoría Other (Cc, Cf, Cs, Co, Cn) excepto saltos y tabs
    cleaned = "".join(
        ch for ch in text 
        if unicodedata.category(ch)[0] != 'C' or ch in "\n\r\t"
    )
    return cleaned


def _extract_rich_text_from_page(page, body_size: float, image_map: dict = None) -> Tuple[List[str], float]:
    """Extrae texto enriquecido. 
    Novedad: Une líneas en párrafos coherentes y añade imágenes embebidas."""
    blocks = page.get_text("dict", flags=fitz.TEXT_PRESERVE_WHITESPACE).get("blocks", [])
    elements = []
    page_max_size = body_size

    for block in blocks:
        if block.get("type") == 1 and image_map: # Bloque de imagen
            xref = block.get("xref")
            if xref in image_map:
                elements.append(f'<div class="img-container"><img src="images/{image_map[xref]}" alt="Image"/></div>')
            continue

        if block.get("type") != 0:
            continue

        current_p_lines = []
        p_max_font = 0

        def emit_paragraph():
            if not current_p_lines: return
            full_text = " ".join(current_p_lines).strip()
            if not full_text: return
            
            noise_patterns = [
                r'^\d+$', r'^https?://\S+$', r'^www\.\S+$', r'^[-—=._\s]{3,}$'
            ]
            if any(re.match(p, full_text, re.IGNORECASE) for p in noise_patterns): return
            if len(full_text.replace(' ', '').replace('\xa0', '')) < 3: return
            
            if p_max_font > body_size * 1.5:
                elements.append(f"<h2>{full_text}</h2>")
            elif p_max_font > body_size * 1.25:
                elements.append(f"<h3>{full_text}</h3>")
            else:
                elements.append(f"<p>{full_text}</p>")

        prev_line_short = False
        block_bbox = block.get("bbox", [0,0,0,0])
        block_width = block_bbox[2] - block_bbox[0]

        for line in block.get("lines", []):
            line_html = ""
            line_raw = ""
            line_bbox = line.get("bbox", [0,0,0,0])
            line_width = line_bbox[2] - line_bbox[0]
            
            for span in line.get("spans", []):
                text = span.get("text", "")
                if not text.strip(): 
                    line_html += " "
                    line_raw += " "
                    continue
                
                line_raw += text
                text = clean_text_for_epub(text)
                flags = span.get("flags", 0)
                size = span.get("size", body_size)
                
                p_max_font = max(p_max_font, size)
                page_max_size = max(page_max_size, size)
                
                is_bold = bool(flags & (1 << 4))
                is_italic = bool(flags & (1 << 1))
                
                escaped = xml_escape(text)
                if is_bold and is_italic: escaped = f"<strong><em>{escaped}</em></strong>"
                elif is_bold: escaped = f"<strong>{escaped}</strong>"
                elif is_italic: escaped = f"<em>{escaped}</em>"
                line_html += escaped
            
            line_raw_stripped = line_raw.strip()
            # Un nuevo párrafo empieza si:
            # 1. Hay sangría (espacios al inicio)
            # 2. Es un encabezado (CH001, Capítulo, etc.)
            # 3. La línea anterior era corta (< 85% del ancho del bloque)
            # 4. Es todo mayúsculas (típico de títulos)
            is_indented = line_raw.startswith("  ") or line_raw.startswith("\t")
            is_header = bool(re.match(r'^\s*(CH\d+|cap[ií]tulo|chapter|parte)\b', line_raw, re.IGNORECASE)) or bool(re.match(r'^\s*part\s+(?:[0-9IVX]+|one|two|three)\b', line_raw, re.IGNORECASE))
            is_all_caps = (line_raw_stripped == line_raw_stripped.upper() and len(line_raw_stripped) > 3 and not line_raw_stripped.isdigit())
            
            # No romper si es una línea corta pero tiene una fuente grande (probablemente un título multilínea)
            should_split = is_indented or is_header or is_all_caps or (prev_line_short and p_max_font <= body_size * 1.2)

            if current_p_lines and should_split:
                emit_paragraph()
                current_p_lines = []
                p_max_font = 0

            if line_html.strip():
                current_p_lines.append(line_html.strip())
                prev_line_short = (line_width < block_width * 0.85)
            else:
                prev_line_short = False

        emit_paragraph()

    return elements, page_max_size


def detect_chapters_from_pdf(doc: fitz.Document, T: dict,
                              image_map: dict = None,
                              pdf_path: str = None) -> List[dict]:
    """Extrae texto del PDF y lo divide en capítulos.
    Estrategia:
    1. Intentar usar el TOC nativo del PDF (doc.get_toc()) → capítulos perfectos.
    2. Fallback: detección heurística. Si pdf_path está disponible, usa
       ThreadPoolExecutor para extraer texto en paralelo (más rápido en PDFs largos).
    En ambos casos, usa extracción de texto enriquecido (negrita, cursiva, enc.)."""

    body_size = _detect_body_font_size(doc)
    toc = doc.get_toc()  # [(nivel, título, página), ...]

    # ─── ESTRATEGIA 1: TOC NATIVO ────────────────────────────
    if toc:
        # Filtrar solo nivel 1 (capítulos principales)
        main_entries = [(title, page_num) for level, title, page_num in toc if level <= 2]
        if main_entries and len(main_entries) >= 3:
            print(T['TOC_NATIVE'].format(len(main_entries)))
            print(T['RICH_TEXT'])

            chapters = []
            for i, (title, start_page) in enumerate(main_entries):
                # Rango de páginas: desde esta entrada hasta la siguiente
                if i + 1 < len(main_entries):
                    end_page = main_entries[i + 1][1]
                else:
                    end_page = len(doc) + 1  # Hasta el final

                content_html = []
                for pg in range(start_page - 1, min(end_page - 1, len(doc))):
                    if 0 <= pg < len(doc):
                        page = doc.load_page(pg)
                        page_elements, _ = _extract_rich_text_from_page(page, body_size, image_map=image_map)
                        content_html.extend(page_elements)

                if content_html:
                    chapters.append({'title': title.strip(), 'content_html': content_html})

            if chapters:
                return chapters

    # ─── ESTRATEGIA 2: DETECCIÓN HEURÍSTICA MEJORADA ──────────
    print(T['TOC_HEURISTIC'])

    # Intentar extraer "Lista de Oro" de capítulos (Específico para revistas)
    golden_toc = []
    for i in range(min(len(doc), 15)):
        p_text = doc[i].get_text()
        p_lines = [l.strip() for l in p_text.split('\n') if l.strip()]
        
        is_in_contents = False
        for j, line in enumerate(p_lines):
            # Detectar inicio de bloque de contenidos
            if any(kw in line.upper() for kw in ['CONTENTS', 'INDEX', 'NOVELETTES', 'SHORT STORIES', 'DEPARTMENTS']):
                is_in_contents = True
                continue
            
            # Si estamos en zona de contenidos, buscar historias
            if is_in_contents:
                if line.startswith('* * * *'): # Fin de zona TOC
                    is_in_contents = False
                    break
                
                # Caso A: Título by Autor (ej: YELLOW CARD MAN by Paolo Bacigalupi)
                if ' by ' in line:
                    parts = re.split(r'\s+by\s+', line, flags=re.IGNORECASE)
                    if len(parts) >= 2:
                        t, a = parts[0], parts[1]
                        # Limpiar departamentos (ej: "EDITORIAL: TITLE")
                        if ':' in t:
                            sub_parts = t.split(':')
                            t = sub_parts[-1]
                        
                        t_clean = t.strip().strip('*').strip()
                        if 3 < len(t_clean) < 80 and 3 < len(a.strip()) < 60:
                            golden_toc.append({'title': t_clean, 'author': a.strip()})
                
                # Caso B: Marcador CHxxx
                elif 'CH' in line and re.search(r'CH\d+', line):
                    m = re.search(r'CH\d+\s*\*?([^*]+)\*?(?:\s+by\s+(.+))?', line)
                    if m:
                        t, a = m.groups()
                        t = t.strip().strip('*')
                        if t and len(t) > 2:
                            golden_toc.append({'title': t, 'author': a.strip() if a else ""})
                    elif j+1 < len(p_lines):
                        next_l = p_lines[j+1]
                        m = re.search(r'\*?([^*]+)\*?(?:\s+by\s+(.+))?', next_l)
                        if m:
                            t, a = m.groups()
                            t = t.strip().strip('*')
                            if t and len(t) > 2:
                                golden_toc.append({'title': t, 'author': a.strip() if a else ""})
            
            # Caso C: *Título* by Autor directo (fuera de bloque CONTENTS)
            elif re.search(r'^\*([^*]+)\*\s+by\s+(.+)$', line):
                m = re.search(r'^\*([^*]+)\*\s+by\s+(.+)$', line)
                t, a = m.groups()
                golden_toc.append({'title': t.strip(), 'author': a.strip()})

        if len(golden_toc) > 3:
            print(T['GOLDEN_TOC_FOUND'].format(len(golden_toc)))
            break

    # Imprimir si encontramos algo pero menos de 4 entradas (y no hemos impreso ya)
    # Buscamos en el código si ya se imprimió, pero por seguridad:
    if len(golden_toc) > 0 and len(golden_toc) <= 3:
         print(T['GOLDEN_TOC_FOUND'].format(len(golden_toc)))

    chapter_patterns = [
        re.compile(r'^\s*CH\d+', re.IGNORECASE),
        re.compile(r'^\s*cap[ií]tulo\s+\w+', re.IGNORECASE),
        re.compile(r'^\s*chapter\s+\w+', re.IGNORECASE),
        re.compile(r'^\s*parte\s+\w+', re.IGNORECASE),
        re.compile(r'^\s*part\s+(?:[0-9IVX]+|one|two|three)\b', re.IGNORECASE),
        re.compile(r'^\s*(?:prólogo|epilogo|epílogo|prologue|epilogue)\b', re.IGNORECASE),
        re.compile(r'^\s*(?:introducción|introduction)\b', re.IGNORECASE),
        re.compile(r'^\s*(?:novella|novelette|short story|editorial|reflections|on books|on the net|thought experiments|letters|verse|upcoming chats|sf conventional calendar)\b', re.IGNORECASE),
    ]

    # Extraer texto enriquecido de todas las páginas (paralelo si tenemos la ruta)
    all_pages_html = []
    if pdf_path:
        import os as _os
        n_threads = max(2, min(_os.cpu_count() or 4, 8))
        thread_args = [(pdf_path, i, body_size) for i in range(len(doc))]
        with concurrent.futures.ThreadPoolExecutor(max_workers=n_threads) as executor:
            thread_results = sorted(
                executor.map(_extract_page_text_worker, thread_args),
                key=lambda x: x[0]
            )
        for _, page_text, page_elements, max_font in thread_results:
            page_elements = [
                el for el in page_elements
                if not re.match(r'^<p>\s*[-—=._\s]{3,}\s*</p>$', el)
            ]
            all_pages_html.append((page_text, page_elements, max_font))
    else:
        # Fallback secuencial cuando no tenemos la ruta del PDF
        for i in range(len(doc)):
            page = doc.load_page(i)
            page_elements, max_font = _extract_rich_text_from_page(page, body_size, image_map=image_map)
            page_elements = [
                el for el in page_elements
                if not re.match(r'^<p>\s*[-—=._\s]{3,}\s*</p>$', el)
            ]
            page_text = page.get_text("text").strip()
            all_pages_html.append((page_text, page_elements, max_font))

    chapters = []
    current_title = None
    current_html = []

    def flush_chapter():
        nonlocal current_title, current_html
        if current_html:
            filtered = [h for h in current_html if h.strip()]
            if filtered:
                # Si tenemos autor guardado de la Golden List, lo añadimos al título
                title_to_save = current_title or f"Sección {len(chapters) + 1}"
                chapters.append({
                    'title': title_to_save,
                    'content_html': filtered
                })
        current_title = None
        current_html = []

    chars_since_last_break = 0

    # --- LOOP PRINCIPAL DE PÁGINAS ---
    page_num = -1
    for page_text, page_elements, max_font in all_pages_html:
        page_num += 1
        if not page_elements:
            continue

        # UNIÓN INTELIGENTE DE PÁRRAFOS ENTRE PÁGINAS
        if current_html and page_elements:
            last_el = current_html[-1]
            first_el = page_elements[0]
            if last_el.startswith("<p>") and first_el.startswith("<p>"):
                last_content = last_el[3:-4].strip()
                first_content = first_el[3:-4].strip()
                if last_content and (last_content[-1] not in ".!?:;\"”" or last_content.endswith("-")):
                    if last_content.endswith("-"):
                        last_content = last_content[:-1]
                    current_html[-1] = f"<p>{last_content} {first_content}</p>"
                    page_elements.pop(0)

        for el in page_elements:
            stripped = re.sub(r'<[^>]+>', '', el).strip()
            if not stripped:
                current_html.append(el)
                continue

            chars_since_last_break += len(stripped)
            is_chapter_header = False
            is_golden_match = False
            found_author = ""

            # 1. COMPROBAR GOLDEN LIST (Prioridad Máxima)
            stripped_clean = stripped.replace('*', '').strip()
            is_large_font = any(tag in el for tag in ['<h2>', '<h3>', '<h4>'])
            
            for entry in golden_toc:
                t = entry['title']
                if t.upper() in stripped_clean.upper() and len(stripped_clean) < len(t) + 60:
                    # Solo romper si no es una página inicial (TOC) o si tiene fuente grande/CH
                    if is_large_font or 'CH' in stripped_clean or page_num > 5:
                        is_chapter_header = True
                        is_golden_match = True
                        found_author = entry['author']
                        stripped = f"{t} ({found_author})" if found_author else t
                        break

            # 2. COMPROBAR PATRONES EXPLÍCITOS
            if not is_chapter_header:
                for pattern in chapter_patterns:
                    if pattern.match(stripped):
                        is_chapter_header = True
                        break

            # 3. COMPROBAR SMART HEURISTIC (Backup para libros normales)
            if not is_chapter_header:
                if el.startswith("<h2>") or el.startswith("<h3>"):
                    is_all_caps = (stripped == stripped.upper() and not stripped.isdigit())
                    # Los H2 y H3 suelen ser capítulos en estas revistas
                    if 3 < len(stripped) < 75:
                        is_chapter_header = True

            # --- LÓGICA DE DETECCIÓN Y RUPTURA ---
            # Decidir si flushear o actualizar título
            is_generic = current_title and re.match(r'^(CH\d+|CAP[IÍ]TULO|CHAPTER|PARTE?)\b', current_title, re.IGNORECASE)
            
            if is_chapter_header:
                if is_golden_match:
                    stripped = stripped.replace('*', '').strip()
                
                # Caso A: Actualizar título genérico (CH001 -> Título Real)
                if is_generic and is_golden_match and chars_since_last_break < 600:
                    current_title = stripped.strip()
                    chars_since_last_break = 0
                
                # Caso B: Nuevo capítulo (ruptura normal)
                else:
                    # Reducir el límite si es un encabezado claro (H2, H3) o match de lista de oro
                    # Las revistas tienen secciones cortas al inicio
                    min_break = 150 if (el.startswith("<h") or is_golden_match) else 1000
                    if not current_title or chars_since_last_break > min_break:
                        flush_chapter()
                        current_title = stripped.strip()
                        chars_since_last_break = 0
                
                # Caso C: Backup de actualización genérica
                if is_generic and chars_since_last_break < 500:
                    current_title = stripped.strip()
            
            # Caso D: Intento de upgrade incluso si no se detectó como header
            elif is_generic and chars_since_last_break < 600:
                s_clean = " ".join(stripped.replace('*', '').split()).upper()
                for entry in golden_toc:
                    t_norm = " ".join(entry['title'].upper().split())
                    if t_norm and t_norm in s_clean and len(s_clean) < 150:
                        current_title = f"{entry['title']} ({entry['author']})" if entry['author'] else entry['title']
                        chars_since_last_break = 0
                        break

            current_html.append(el)

    flush_chapter()

    if not chapters:
        all_html = []
        for _, elements, _ in all_pages_html:  # Fix: desempaqueta los 3 elementos de la tupla
            all_html.extend(elements)
        if all_html:
            chapters = [{'title': 'Contenido', 'content_html': all_html}]

    return chapters


# =========================================================
# CONFIGURACIÓN DE OPTIMIZACIÓN (estilo EPUBMaster/EPUBOptimizer)
# =========================================================

# Perfil para imágenes de contenido visual (cómics, manga, escaneados)
OPT_COMIC = {
    'max_width': 1600,
    'max_height': 2400,
    'quality': 82,        # Alta calidad: pérdida imperceptible en cómics
}

# Perfil B/N para revistas y libros escaneados en blanco y negro.
# El límite bajo es intencional: JBIG2 usa ~15KB/pág; a 900px+q30 nosotros logramos ~40-60KB/pág.
OPT_SCAN_BW = {
    'max_width': 950,
    'quality': 45,        # Calidad óptima para texto nítido sin ruido
    'format': 'JPEG',
    'bitonal': False
}

# Perfil color para PDFs de imagen a color (fotos, revistas en color)
OPT_SCAN_COLOR = {
    'max_width': 1200,
    'max_height': 1800,
    'quality': 72,
}

# Perfil para imágenes decorativas/portadas de libros de texto
OPT_TEXT = {
    'max_width': 1000,
    'quality': 75,         # Como EPUBOptimizer: buen balance tamaño/calidad
}


def _is_grayscale_image(img: Image.Image) -> bool:
    """Detecta si una imagen RGB es realmente en blanco y negro.
    Usa la misma heurística que PDFtoCBZ: diferencia media entre canales < 5."""
    if img.mode == 'L':
        return True
    if img.mode != 'RGB':
        return False

    if HAS_NUMPY:
        try:
            img_array = np.array(img)
            diff = (np.mean(np.abs(img_array[:, :, 0].astype(float) - img_array[:, :, 1].astype(float))) +
                    np.mean(np.abs(img_array[:, :, 1].astype(float) - img_array[:, :, 2].astype(float))))
            return diff < 5.0
        except Exception:
            return False
    else:
        # Fallback sin numpy: redimensionar a 50x50 para muestrear rápido sin cargar todo en RAM
        try:
            small = img.resize((50, 50), Image.Resampling.BILINEAR)
            diffs = [abs(r - g) + abs(g - b) for r, g, b in small.getdata()]
            return (sum(diffs) / len(diffs)) < 10.0
        except Exception:
            return False


def _calc_render_matrix(page_width: float, page_height: float,
                         target_width: int = 1600) -> float:
    """Calcula el zoom mínimo de renderizado para alcanzar la resolución objetivo.
    Evita renderizar a 2.0x cuando la página nativa ya es grande (ahorra RAM y CPU).
    Nunca baja de 1.0x para evitar pérdida."""
    if page_width <= 0:
        return 2.0
    zoom = target_width / page_width
    # Clamp: mínimo 1.0 (calidad nativa), máximo 3.0 (calidad extrema)
    return max(1.0, min(zoom, 3.0))


def optimize_image_for_epub(img: Image.Image, profile: str = 'comic',
                            original_data: bytes = None,
                            is_bw: bool = None) -> bytes:
    """Optimiza una imagen para inclusión en EPUB.

    Aplica el pipeline de optimización inspirado en EPUBMaster:
    1. Aplanar canal Alpha sobre fondo blanco
    2. Reescalar al máximo del perfil (sin upscaling)
    3. Detección automática de B/N → convertir a escala de grises
    4. Compresión JPEG con calidad optimizada
    5. Comparación inteligente: solo si el resultado es más pequeño

    Args:
        img: Imagen PIL a optimizar.
        profile: 'comic' (FXL, alta calidad) o 'text' (reflowable, más compresión).
        original_data: Bytes originales de la imagen para comparación de tamaño.
        is_bw: Pre-computed B/W flag (None = auto-detect).

    Returns:
        bytes: Datos JPEG optimizados.
    """
    conf = OPT_COMIC if profile == 'comic' else OPT_TEXT
    max_w = conf['max_width']
    max_h = conf.get('max_height', max_w * 2)  # Proporción 1:2 por defecto
    quality = conf['quality']

    # 1. Aplanar canal Alpha sobre fondo blanco (evita fondo negro en PNGs)
    if img.mode in ('RGBA', 'LA', 'P'):
        background = Image.new('RGB', img.size, (255, 255, 255))
        if img.mode == 'P':
            img = img.convert('RGBA')
        if img.mode in ('RGBA', 'LA'):
            background.paste(img, mask=img.split()[-1])
            img = background
        else:
            img = img.convert('RGB')
    elif img.mode != 'RGB':
        img = img.convert('RGB')

    # 1.5 Auto-Cropping (Recorte Inteligente de márgenes)
    try:
        from PIL import ImageChops
        bg = Image.new(img.mode, img.size, img.getpixel((0,0)))
        diff = ImageChops.difference(img, bg)
        diff = ImageChops.add(diff, diff, 2.0, -100)
        bbox = diff.getbbox()
        if bbox:
            img = img.crop(bbox)
    except Exception:
        pass

    # 2. Reescalar si excede los máximos (nunca hacer upscale)
    # ⚡ AJUSTE CRÍTICO: Si es B/N (escaneo), bajamos el tope a 1100px.
    # 1600px es demasiado para libros de texto o revistas de 1000 páginas.
    if is_bw is None:
        is_bw = _is_grayscale_image(img)
        
    active_max_w = 1100 if (is_bw and profile == 'comic') else max_w
    active_max_h = active_max_w * 1.5

    if img.width > active_max_w or img.height > active_max_h:
        ratio = min(active_max_w / img.width, active_max_h / img.height)
        new_size = (int(img.width * ratio), int(img.height * ratio))
        img = img.resize(new_size, Image.Resampling.LANCZOS)

    # 3. Detección de B/N: escala de grises y compresión agresiva
    if is_bw:
        img = img.convert('L')
        # Para B/N de texto, calidad 25-30 es suficiente.
        # JBIG2 usa ~15KB/pág. Nosotros intentamos bajar de 60KB/pág.
        quality = min(quality, 30)

    # 4. Compresión JPEG optimizada
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=quality, optimize=True)
    optimized_data = buf.getvalue()

    # 5. Comparación inteligente
    if original_data and len(optimized_data) >= len(original_data):
        # Si el original es pequeño (< 150KB) y formato válido, usarlo sin más.
        try:
            head = original_data[:10]
            is_valid_format = (b'JFIF' in head or b'Exif' in head or b'PNG' in head)
            if is_valid_format and len(original_data) < 150_000:
                return original_data
        except Exception:
            pass

        try:
            img_fallback = Image.open(io.BytesIO(original_data))
            img_fallback = img_fallback.convert('L') if is_bw else img_fallback.convert('RGB')

            # Reescalado de seguridad en fallback
            if img_fallback.width > active_max_w:
                ratio = active_max_w / img_fallback.width
                new_size = (active_max_w, int(img_fallback.height * ratio))
                img_fallback = img_fallback.resize(new_size, Image.Resampling.LANCZOS)

            buf2 = io.BytesIO()
            img_fallback.save(buf2, "JPEG", quality=quality, optimize=True)
            return buf2.getvalue()
        except Exception:
            # Si el fallback falla, devolver lo que tenemos (optimizado aunque sea mayor)
            return optimized_data

    return optimized_data


def minify_xhtml(content: str) -> str:
    """Minifica XHTML generado: elimina comentarios HTML y espacios redundantes.
    (Misma técnica que EPUBMaster/EPUBOptimizer)."""
    content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
    content = re.sub(r'\s{2,}', ' ', content)
    return content.strip()


# =========================================================
# MOTOR OCR (Tesseract — opcional)
# =========================================================

def _pdf_lang_to_tesseract(pdf_lang: str) -> str:
    """Convierte el código de idioma del PDF al formato que espera Tesseract."""
    code = (pdf_lang or '').lower()[:3].strip()
    return LANG_MAP_TESSERACT.get(code, LANG_MAP_TESSERACT.get(code[:2], 'spa+eng'))


def _test_ocr_quality(pdf_path: str, lang: str = 'spa+eng', min_chars: int = 150) -> bool:
    """OCR rápido de la primera página (150 DPI) para comprobar si el texto es recuperable."""
    try:
        import fitz as _fitz
        import pytesseract as _tess
        from PIL import Image as _Image
        doc = _fitz.open(pdf_path)
        page = doc.load_page(0)
        zoom = 150 / 72.0
        pix = page.get_pixmap(matrix=_fitz.Matrix(zoom, zoom), colorspace=_fitz.csRGB)
        img = _Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        doc.close()
        text = _tess.image_to_string(img, lang=lang, config='--oem 3 --psm 6')
        return len(text.strip()) >= min_chars
    except Exception:
        return False


def _ocr_page_worker(args: tuple) -> tuple:
    """Worker de proceso para OCR de una página (process-safe).
    Cada proceso abre su propio fitz.Document para evitar conflictos."""
    pdf_path, page_num, lang, dpi = args
    try:
        import fitz as _fitz
        import pytesseract as _tess
        from PIL import Image as _Image
        doc = _fitz.open(pdf_path)
        page = doc.load_page(page_num)
        zoom = dpi / 72.0
        pix = page.get_pixmap(matrix=_fitz.Matrix(zoom, zoom), colorspace=_fitz.csRGB)
        img = _Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        doc.close()
        text = _tess.image_to_string(img, lang=lang, config='--oem 3 --psm 6')
        return page_num, text.strip()
    except Exception:
        return page_num, ""


def _split_ocr_text_into_chapters(pages_text: list) -> list:
    """Divide el texto OCR (lista de (page_num, text)) en capítulos usando
    patrones explícitos + heurística ALL-CAPS para títulos."""
    chapter_patterns = [
        re.compile(r'^\s*cap[ií]tulo\s+\w+', re.IGNORECASE),
        re.compile(r'^\s*chapter\s+\w+', re.IGNORECASE),
        re.compile(r'^\s*parte\s+\w+', re.IGNORECASE),
        re.compile(r'^\s*part\s+\w+', re.IGNORECASE),
        re.compile(r'^\s*(?:prólogo|epílogo|prologue|epilogue)\s*$', re.IGNORECASE),
        re.compile(r'^\s*(?:introducción|introduction)\s*$', re.IGNORECASE),
    ]
    chapters, current_title, current_html = [], None, []

    def _flush():
        nonlocal current_title, current_html
        if current_html:
            chapters.append({
                'title': current_title or f'Sección {len(chapters) + 1}',
                'content_html': current_html[:]
            })
        current_title, current_html = None, []

    for _, page_text in pages_text:
        if not page_text:
            continue
        for para in re.split(r'\n{2,}|\x0c', page_text):
            clean = ' '.join(para.split())
            if not clean or len(clean) < 3:
                continue
            # Filtrar ruido OCR: solo dígitos/símbolos sueltos
            if re.match(r'^[\d\s\.\-_\|]{1,6}$', clean):
                continue

            is_header = any(p.match(clean) for p in chapter_patterns)
            if not is_header:
                # ALL-CAPS corto = probable título
                words = clean.split()
                if (clean == clean.upper() and 3 < len(clean) < 60
                        and not clean.isdigit() and len(words) <= 8):
                    is_header = True

            if is_header:
                content_len = sum(len(h) for h in current_html)
                if content_len > 300:
                    _flush()
                current_title = clean
            else:
                current_html.append(f'<p>{xml_escape(clean)}</p>')

    _flush()

    if not chapters:
        all_html = []
        for _, text in pages_text:
            for para in re.split(r'\n{2,}|\x0c', text):
                p = ' '.join(para.split())
                if p and len(p) > 5:
                    all_html.append(f'<p>{xml_escape(p)}</p>')
        if all_html:
            chapters = [{'title': 'Contenido', 'content_html': all_html}]
    return chapters


def convert_pdf_ocr_to_epub(pdf_path: Path, epub_path: Path, T: dict,
                             lang: str = 'spa+eng') -> bool:
    """Convierte un PDF de imágenes a EPUB reflowable usando OCR (Tesseract).
    Usa ProcessPoolExecutor para paralelizar el OCR en todos los núcleos disponibles.
    Requiere: pip install pytesseract  +  Tesseract instalado en el sistema."""
    import multiprocessing as _mp
    doc = None
    try:
        doc = fitz.open(pdf_path)
        npages = len(doc)
        metadata = doc.metadata or {}
        title    = metadata.get('title', '')    or pdf_path.stem
        author   = metadata.get('author', '')   or ''
        language = metadata.get('language', 'es') or 'es'
        cover_data = extract_cover_from_pdf(doc)
        doc.close()
        doc = None

        print(T['OCR_START'].format(npages))

        n_workers = max(2, min(_mp.cpu_count(), 6))
        ocr_args = [(str(pdf_path), i, lang, 300) for i in range(npages)]
        with concurrent.futures.ProcessPoolExecutor(max_workers=n_workers) as executor:
            raw = list(executor.map(_ocr_page_worker, ocr_args))

        pages_text = sorted(raw, key=lambda x: x[0])
        chapters = _split_ocr_text_into_chapters(pages_text)
        print(T['OCR_DONE'].format(len(chapters)))
        print(T['CHAPTER_FOUND'].format(len(chapters)))

        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
            base = Path(tmp)
            (base / 'META-INF').mkdir()
            (base / 'OEBPS' / 'images').mkdir(parents=True)
            (base / 'mimetype').write_text(MIMETYPE, encoding='utf-8')
            (base / 'META-INF' / 'container.xml').write_text(CONTAINER_XML, encoding='utf-8')
            (base / 'OEBPS' / 'estilos.css').write_text(CSS_REFLOWABLE, encoding='utf-8')

            has_cover = False
            if cover_data:
                (base / 'OEBPS' / 'images' / 'cover.jpg').write_bytes(cover_data)
                (base / 'OEBPS' / 'cover.xhtml').write_text(
                    generate_cover_xhtml('cover.jpg'), encoding='utf-8')
                has_cover = True

            manifest_items, spine_items = [], []
            if has_cover:
                manifest_items.append(
                    '    <item id="cover-image" href="images/cover.jpg"'
                    ' media-type="image/jpeg" properties="cover-image"/>')
                manifest_items.append(
                    '    <item id="cover" href="cover.xhtml"'
                    ' media-type="application/xhtml+xml"/>')
                spine_items.append('    <itemref idref="cover"/>')

            for idx, ch in enumerate(chapters, 1):
                ch_id   = f'chapter_{idx:03d}'
                ch_href = f'chapter_{idx:03d}.xhtml'
                xhtml   = generate_chapter_xhtml(ch['title'], ch['content_html'])
                (base / 'OEBPS' / ch_href).write_text(minify_xhtml(xhtml), encoding='utf-8')
                manifest_items.append(
                    f'    <item id="{ch_id}" href="{ch_href}"'
                    ' media-type="application/xhtml+xml"/>')
                spine_items.append(f'    <itemref idref="{ch_id}"/>')

            manifest_items.append(
                '<item id="css" href="estilos.css" media-type="text/css"/>')
            manifest_items.append(
                '<item id="nav" href="nav.xhtml"'
                ' media-type="application/xhtml+xml" properties="nav"/>')

            uid = f'pdfcbztoepub-{pdf_path.stem}-{int(time.time())}'
            opf = generate_opf_reflowable(title, author, uid,
                                          manifest_items, spine_items,
                                          language=language)
            (base / 'OEBPS' / 'content.opf').write_text(opf, encoding='utf-8')
            nav = generate_nav_reflowable(title, chapters)
            (base / 'OEBPS' / 'nav.xhtml').write_text(nav, encoding='utf-8')
            pack_epub(base, epub_path)

        return True

    except Exception as e:
        if doc:
            try: doc.close()
            except Exception: pass
        print(T['PROC_ERROR'].format(pdf_path.name, e))
        if epub_path.exists():
            try: epub_path.unlink()
            except Exception: pass
        return False


def _extract_page_text_worker(args: tuple) -> tuple:
    """Worker de hilo para extrae texto de una página de forma paralela.
    Cada hilo abre su propio fitz.Document para ser thread-safe."""
    pdf_path, page_num, body_size = args
    try:
        import fitz as _fitz
        doc = _fitz.open(pdf_path)
        page = doc.load_page(page_num)
        elements, max_font = _extract_rich_text_from_page(page, body_size)
        page_text = page.get_text("text").strip()
        doc.close()
        return page_num, page_text, elements, max_font
    except Exception:
        return page_num, "", [], body_size


# ─── CONVERSOR: PDF DE TEXTO → EPUB REFLOWABLE ──────────────────────

def convert_pdf_text_to_epub(pdf_path: Path, epub_path: Path, T: dict) -> bool:
    """Convierte un PDF de texto en un EPUB reflowable con capítulos."""
    doc = None
    try:
        doc = fitz.open(pdf_path)

        # Extraer metadatos
        metadata = doc.metadata or {}
        title = metadata.get('title', '') or pdf_path.stem
        author = metadata.get('author', '') or 'Unknown'
        language = metadata.get('language', 'es') or 'es'
        
        # --- NUEVO: Extracción de imágenes para PDFs de texto ---
        image_map = {}
        images_data = {}
        try:
            img_count = 0
            for i in range(len(doc)):
                page_imgs = doc[i].get_images()
                for img in page_imgs:
                    xref = img[0]
                    if xref not in image_map:
                        try:
                            base = doc.extract_image(xref)
                            if base['width'] > 30 and base['height'] > 30:
                                img_count += 1
                                ext = base['ext']
                                img_name = f"img_{img_count:03d}.{ext}"
                                image_map[xref] = img_name
                                images_data[img_name] = base['image']
                        except Exception:
                            continue
        except Exception as e:
            print(f"   ⚠️  Error escaneando imágenes: {e}")

        # Detectar capítulos (prioriza TOC nativo, fallback a heurísticas)
        # pdf_path se pasa para habilitar la extracción paralela de texto
        chapters = detect_chapters_from_pdf(doc, T, image_map=image_map, pdf_path=str(pdf_path))
        print(T['CHAPTER_FOUND'].format(len(chapters)))

        # Extraer portada (optimizada como imagen de texto/portada)
        cover_data = extract_cover_from_pdf(doc)

        # Construir en directorio temporal
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
            base = Path(tmp)

            # Estructura de directorios
            (base / 'META-INF').mkdir()
            (base / 'OEBPS' / 'images').mkdir(parents=True)

            # mimetype
            (base / 'mimetype').write_text(MIMETYPE, encoding='utf-8')

            # container.xml
            (base / 'META-INF' / 'container.xml').write_text(
                CONTAINER_XML, encoding='utf-8')

            # CSS
            (base / 'OEBPS' / 'estilos.css').write_text(
                CSS_REFLOWABLE, encoding='utf-8')

            # Portada
            has_cover = False
            if cover_data:
                (base / 'OEBPS' / 'images' / 'cover.jpg').write_bytes(cover_data)
                (base / 'OEBPS' / 'cover.xhtml').write_text(
                    generate_cover_xhtml(), encoding='utf-8')
                has_cover = True

            # Guardar las imágenes extraídas al disco
            for img_name, img_bytes in images_data.items():
                (base / 'OEBPS' / 'images' / img_name).write_bytes(img_bytes)

            # Capítulos
            nav_entries = []
            manifest_items = []
            spine_items = []

            if has_cover:
                manifest_items.append('    <item id="cover-image" href="images/cover.jpg" media-type="image/jpeg" properties="cover-image"/>')
                manifest_items.append('    <item id="cover" href="cover.xhtml" media-type="application/xhtml+xml"/>')
                spine_items.append('    <itemref idref="cover"/>')

            for idx, ch in enumerate(chapters, 1):
                ch_id = f"chapter_{idx:03d}"
                ch_href = f"chapter_{idx:03d}.xhtml"
                xhtml = generate_chapter_xhtml(ch['title'], ch['content_html'])
                (base / 'OEBPS' / ch_href).write_text(minify_xhtml(xhtml), encoding='utf-8')
                manifest_items.append(f'    <item id="{ch_id}" href="{ch_href}" media-type="application/xhtml+xml"/>')
                spine_items.append(f'    <itemref idref="{ch_id}"/>')
                nav_entries.append({'href': ch_href, 'title': ch['title']})

            # Añadir imágenes al manifest si existen (extracción de imágenes internas)
            for img_name in images_data.keys():
                mtype = "image/jpeg" if img_name.lower().endswith(('.jpg', '.jpeg')) else "image/png"
                manifest_items.append(f'    <item id="{img_name.replace(".", "_")}" href="images/{img_name}" media-type="{mtype}"/>')

            manifest_items.append('<item id="css" href="estilos.css" media-type="text/css"/>')
            manifest_items.append('<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>')

            # OPF
            uid = f"pdfcbztoepub-{pdf_path.stem}-{int(time.time())}"
            opf = generate_opf_reflowable(title, author, uid, manifest_items, spine_items, language=language)
            (base / 'OEBPS' / 'content.opf').write_text(opf, encoding='utf-8')

            # NAV
            nav = generate_nav_reflowable(title, chapters)
            (base / 'OEBPS' / 'nav.xhtml').write_text(nav, encoding='utf-8')

            # Empaquetar
            pack_epub(base, epub_path)

        doc.close()
        return True

    except Exception as e:
        if doc:
            try:
                doc.close()
            except Exception:
                pass
        print(T['PROC_ERROR'].format(pdf_path.name, e))
        if epub_path.exists():
            try:
                epub_path.unlink()
            except Exception:
                pass
        return False


def _process_image_worker(args):
    """Worker universal para CBZ: optimiza una imagen PIL bytes.
    Para PDFs, ya no se usa este worker: el render directo a JPEG se hace en convert_pdf_image_to_epub."""
    idx, img_bytes, out_path = args
    try:
        img = Image.open(io.BytesIO(img_bytes))
        is_bw = _is_grayscale_image(img)

        # JPEG passthrough para CBZ: si ya es JPEG pequeño y no B/N, copiar sin recodificar
        if img.format == 'JPEG' and not is_bw:
            bpp = len(img_bytes) / max(1, img.width * img.height)
            if img.width <= OPT_COMIC['max_width'] and bpp < 0.4:
                Path(out_path).write_bytes(img_bytes)
                return idx, len(img_bytes), len(img_bytes), False, True

        optimized = optimize_image_for_epub(img, profile='comic', original_data=img_bytes, is_bw=is_bw)
        Path(out_path).write_bytes(optimized)
        return idx, len(img_bytes), len(optimized), is_bw, False

    except Exception:
        Path(out_path).write_bytes(img_bytes)
        return idx, len(img_bytes), len(img_bytes), False, False


def _render_page_to_image(page, target_width: int, quality: int, grayscale: bool, bitonal: bool = False) -> Tuple[bytes, str]:
    """Renderiza página a JPEG o PNG (bitonal) optimizado."""
    rect = page.rect
    zoom = 1.0
    if rect.width > target_width:
        zoom = target_width / rect.width
    
    matrix = fitz.Matrix(zoom, zoom)
    
    if bitonal:
        # Renderizar directo a gris para binarizar
        pix = page.get_pixmap(matrix=matrix, colorspace=fitz.csGRAY)
        img = Image.frombytes("L", [pix.width, pix.height], pix.samples)
        # Binarización: texto negro puro sobre fondo blanco
        img = img.point(lambda p: 255 if p > 150 else 0).convert('1')
        buf = io.BytesIO()
        img.save(buf, "PNG", optimize=True)
        return buf.getvalue(), ".png"
    else:
        cs = fitz.csGRAY if grayscale else fitz.csRGB
        pix = page.get_pixmap(matrix=matrix, colorspace=cs)
        mode = "L" if grayscale else "RGB"
        img = Image.frombytes(mode, [pix.width, pix.height], pix.samples)
        buf = io.BytesIO()
        img.save(buf, "JPEG", quality=quality, optimize=True)
        return buf.getvalue(), ".jpg"


def _process_page_worker(pdf_path: str, page_num: int, opt_bw: dict, opt_color: dict) -> dict:
    """Función trabajadora para procesar una página en un proceso separado."""
    import fitz # Importar dentro del worker para evitar problemas de pickling
    from PIL import Image
    import io
    
    doc = fitz.open(pdf_path)
    page = doc.load_page(page_num)
    
    # Detección de color dinámica optimizada
    pix_tiny = page.get_pixmap(matrix=fitz.Matrix(0.1, 0.1), colorspace=fitz.csRGB)
    img_tiny = Image.frombytes("RGB", [pix_tiny.width, pix_tiny.height], pix_tiny.samples)
    
    # Lógica de detección rápida
    is_page_bw = True
    samples = img_tiny.getdata()
    for r, g, b in samples:
        if abs(r - g) > 20 or abs(r - b) > 20: # Tolerancia de color
            is_page_bw = False
            break
            
    profile = opt_bw if is_page_bw else opt_color
    target_w = profile['max_width']
    quality = profile['quality']
    is_bitonal = profile.get('bitonal', False)
    
    # Renderizado (reutiliza la función global _render_page_to_image)
    render_bytes, ext = _render_page_to_image(page, target_w, quality, is_page_bw, bitonal=is_bitonal)
    
    # Información de de-duplicación
    img_list = page.get_images()
    xref = None
    extract_bytes = None
    if img_list:
        biggest_img = max(img_list, key=lambda x: x[2])
        xref = biggest_img[0]
        if not is_bitonal:
            try:
                # Intentamos extraer nativo para ver si es más pequeño
                ext_base = doc.extract_image(xref)
                if ext_base['ext'] in ('jpeg', 'jpg') and ext_base['width'] > 400:
                    extract_bytes = ext_base['image']
            except Exception:
                pass

    doc.close()
    return {
        'index': page_num,
        'render_bytes': render_bytes,
        'extract_bytes': extract_bytes,
        'ext': ext,
        'xref': xref,
        'is_bw': is_page_bw
    }


def convert_pdf_image_to_epub(pdf_path: Path, epub_path: Path, T: dict) -> bool:
    """Convierte un PDF de imágenes en un EPUB Fixed-Layout con Turbo Multiprocessing."""
    doc = None
    try:
        doc = fitz.open(pdf_path)
        npages = len(doc)
        
        # Viewport: calibración
        default_w = 950
        first_page = doc.load_page(0)
        zoom = default_w / max(first_page.rect.width, 1)
        zoom = max(0.5, min(zoom, 3.0))
        vp_width = int(first_page.rect.width * zoom)
        vp_height = int(first_page.rect.height * zoom)
        doc.close()

        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
            base = Path(tmp)
            (base / 'META-INF').mkdir()
            (base / 'OEBPS' / 'images').mkdir(parents=True)
            (base / 'mimetype').write_text(MIMETYPE, encoding='utf-8')
            (base / 'META-INF/container.xml').write_text(CONTAINER_XML, encoding='utf-8')
            (base / 'OEBPS/estilos.css').write_text(CSS_FXL, encoding='utf-8')

            total_out = 0
            pages_meta = []
            xref_to_image = {} 

            import multiprocessing
            print(T['PARALLEL_START'].format(multiprocessing.cpu_count()))
            
            results = []
            with concurrent.futures.ProcessPoolExecutor() as executor:
                futures = [executor.submit(_process_page_worker, str(pdf_path), i, OPT_SCAN_BW, OPT_SCAN_COLOR) for i in range(npages)]
                for future in concurrent.futures.as_completed(futures):
                    res = future.result()
                    results.append(res)
                    print(f"  → Procesando: {len(results)}/{npages}", end='\r')
            
            results.sort(key=lambda x: x['index'])

            print("\n" + T['ASSEMBLING_EPUB'])
            for res in results:
                i = res['index']
                xref = res['xref']
                img_filename = None

                if xref and xref in xref_to_image:
                    img_filename = xref_to_image[xref]
                else:
                    r_bytes = res['render_bytes']
                    e_bytes = res['extract_bytes']
                    final_bytes = e_bytes if (e_bytes and len(e_bytes) < len(r_bytes)) else r_bytes
                    ext = res['ext']
                    img_filename = f"img_{xref:05d}{ext}" if xref else f"pg_{i+1:04d}{ext}"
                    (base / 'OEBPS' / 'images' / img_filename).write_bytes(final_bytes)
                    if xref: xref_to_image[xref] = img_filename
                    total_out += len(final_bytes)

                page_href = f"page_{i+1:04d}.xhtml"
                page_xhtml = generate_fxl_page_xhtml(img_filename, vp_width, vp_height)
                (base / 'OEBPS' / page_href).write_text(page_xhtml, encoding='utf-8')
                pages_meta.append({
                    'page_id': f"page_{i+1:04d}",
                    'page_href': page_href,
                    'img_id': f"img_{i+1:04d}",
                    'img_href': f"images/{img_filename}",
                    'label': f"Page {i+1}",
                })

            print(T['PAGES_FOUND'].format(npages))
            out_mb = total_out / (1024 * 1024)
            print(T['SIZE_IMAGES'].format(out_mb))

            # Extraer metadatos y generar OPF con autor e idioma
            with fitz.open(pdf_path) as doc_meta:
                metadata = doc_meta.metadata or {}
            title = metadata.get('title', '') or pdf_path.stem
            author = metadata.get('author', '') or ''
            language = metadata.get('language', 'es') or 'es'
            uid = f"pdfcbztoepub-{pdf_path.stem}-{int(time.time())}"
            opf = generate_opf_fxl(title, uid, pages_meta, vp_width, vp_height,
                                    author=author, language=language)
            (base / 'OEBPS' / 'content.opf').write_text(opf, encoding='utf-8')
            nav = generate_nav_fxl(pages_meta)
            (base / 'OEBPS' / 'nav.xhtml').write_text(nav, encoding='utf-8')
            pack_epub(base, epub_path)
            return True
    except Exception as e:
        print(T['PROC_ERROR'].format(pdf_path.name, e))
        if epub_path.exists():
            try:
                epub_path.unlink()
            except Exception:
                pass
        return False

def _process_cbz_image(args):
    """Worker para optimizar una imagen de CBZ (process-safe).
    Aplica Lazy Loading y Auto-Cropping."""
    idx, raw_path, out_path = args
    try:
        with open(raw_path, 'rb') as f:
            img_bytes = f.read()
        img = Image.open(io.BytesIO(img_bytes))
        is_bw = _is_grayscale_image(img)

        # ⚡ JPEG PASSTHROUGH: evitar pérdida generacional
        # Si el JPEG original ya tiene dimensiones OK y buena compresión,
        # copiarlo directamente sin recodificar
        can_passthrough = (
            img.format == 'JPEG'
            and img.width <= OPT_COMIC['max_width']
            and img.height <= OPT_COMIC.get('max_height', 2400)
            and not is_bw  # B/N se beneficia de conversión a grayscale
        )
        if can_passthrough:
            # Verificar que ya está bien comprimido (< 0.4 bytes/pixel)
            bytes_per_pixel = len(img_bytes) / max(1, img.width * img.height)
            if bytes_per_pixel < 0.4:
                Path(out_path).write_bytes(img_bytes)
                return idx, len(img_bytes), len(img_bytes), False, True  # passthrough=True

        optimized = optimize_image_for_epub(
            img, profile='comic', original_data=img_bytes, is_bw=is_bw)
        Path(out_path).write_bytes(optimized)
        try:
            Path(raw_path).unlink()
        except Exception:
            pass
        return idx, len(img_bytes), len(optimized), is_bw, False
    except Exception:
        # Fallback: escribir original
        Path(out_path).write_bytes(img_bytes)
        try:
            Path(raw_path).unlink()
        except Exception:
            pass
        return idx, len(img_bytes), len(img_bytes), False, False


def convert_cbz_to_epub(cbz_path: Path, epub_path: Path, T: dict) -> bool:
    """Convierte un CBZ (ZIP de imágenes) en un EPUB Fixed-Layout.
    Usa multihilo (8 workers) para optimizar imágenes en paralelo."""
    IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff'}

    try:
        with zipfile.ZipFile(cbz_path, 'r') as zf:
            # Filtrar y ordenar imágenes
            image_names = sorted([
                n for n in zf.namelist()
                if Path(n).suffix.lower() in IMAGE_EXTS
                   and not Path(n).name.startswith('.')
                   and '__MACOSX' not in n
            ])

            if not image_names:
                print(T['SKIP_EMPTY'].format(cbz_path.name))
                return False

            print(T['CBZ_CONVERT'])

            # Intentar leer metadatos de ComicInfo.xml
            cbz_title = cbz_path.stem
            cbz_author = ''
            if 'ComicInfo.xml' in zf.namelist():
                try:
                    ci_data = zf.read('ComicInfo.xml')
                    ci_root = ElementTree.fromstring(ci_data)
                    ci_title = ci_root.findtext('Title', '').strip()
                    ci_series = ci_root.findtext('Series', '').strip()
                    ci_writer = ci_root.findtext('Writer', '').strip()
                    ci_number = ci_root.findtext('Number', '').strip()
                    if ci_title:
                        cbz_title = ci_title
                    elif ci_series and ci_number:
                        cbz_title = f"{ci_series} #{ci_number}"
                    elif ci_series:
                        cbz_title = ci_series
                    if ci_writer:
                        cbz_author = ci_writer
                    info_str = cbz_title
                    if cbz_author:
                        info_str += f" ({cbz_author})"
                    print(T['COMIC_INFO'].format(info_str))
                except Exception:
                    pass

            # Calcular viewport usando la moda del tamaño de las primeras imágenes
            # (evita que una doble-página aislada distorsione el viewport)
            from collections import Counter
            size_samples = []
            for sample_name in image_names[:min(8, len(image_names))]:
                try:
                    sample_data = zf.read(sample_name)
                    sample_img = Image.open(io.BytesIO(sample_data))
                    size_samples.append(sample_img.size)
                except Exception:
                    continue
            if size_samples:
                vp_width, vp_height = Counter(size_samples).most_common(1)[0][0]
            else:
                vp_width, vp_height = 1200, 1800  # fallback seguro
            if vp_width > 1600:
                ratio = 1600 / vp_width
                vp_width = 1600
                vp_height = int(vp_height * ratio)

            with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
                base = Path(tmp)
                (base / 'META-INF').mkdir()
                (base / 'OEBPS' / 'images').mkdir(parents=True)

                (base / 'mimetype').write_text(MIMETYPE, encoding='utf-8')
                (base / 'META-INF' / 'container.xml').write_text(
                    CONTAINER_XML, encoding='utf-8')
                (base / 'OEBPS' / 'estilos.css').write_text(CSS_FXL, encoding='utf-8')

                # Fase 1: Lazy Loading (guardar raw en disco temporalmente para no saturar RAM)
                worker_tasks = []
                for idx, img_name in enumerate(image_names, 1):
                    print(T['PROGRESS'].format(idx, len(image_names)), end='\r')
                    raw_path = str(base / 'OEBPS' / 'images' / f"raw_{idx:04d}{Path(img_name).suffix}")
                    out_path = str(base / 'OEBPS' / 'images' / f"{idx:04d}.jpg")
                    with open(raw_path, 'wb') as f:
                        f.write(zf.read(img_name))
                    worker_tasks.append((idx, raw_path, out_path))

                # Fase 2: Optimizar en paralelo con Multiprocesamiento real
                total_raw = 0
                total_opt = 0
                bw_count = 0
                passthrough_count = 0
                import os
                workers = max(2, min(os.cpu_count() or 4, 8))
                with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
                    results = list(executor.map(_process_cbz_image, worker_tasks))

                for idx, raw_size, opt_size, is_bw, passthrough in results:
                    total_raw += raw_size
                    total_opt += opt_size
                    if is_bw:
                        bw_count += 1
                    if passthrough:
                        passthrough_count += 1

                # Fase 3: Generar XHTML de cada página
                pages_meta = []
                for idx in range(1, len(image_names) + 1):
                    img_filename = f"{idx:04d}.jpg"
                    page_href = f"page_{idx:04d}.xhtml"
                    page_xhtml = generate_fxl_page_xhtml(
                        img_filename, vp_width, vp_height)
                    (base / 'OEBPS' / page_href).write_text(
                        page_xhtml, encoding='utf-8')

                    pages_meta.append({
                        'page_id': f"page_{idx:04d}",
                        'page_href': page_href,
                        'img_id': f"img_{idx:04d}",
                        'img_href': f"images/{img_filename}",
                        'label': f"Page {idx}",
                    })

                print(T['PAGES_FOUND'].format(len(image_names)))
                if passthrough_count > 0:
                    print(T['JPEG_PASSTHRU'].format(passthrough_count))
                if bw_count > len(image_names) * 0.5:
                    print(T['OPT_BW_DETECTED'])
                if total_raw > 0:
                    raw_mb = total_raw / (1024 * 1024)
                    opt_mb = total_opt / (1024 * 1024)
                    savings_pct = (1 - total_opt / total_raw) * 100
                    print(T['OPT_SAVINGS'].format(raw_mb, opt_mb, savings_pct))

                title = cbz_title
                uid = f"pdfcbztoepub-{cbz_path.stem}-{int(time.time())}"

                opf = generate_opf_fxl(title, uid, pages_meta, vp_width, vp_height,
                                       author=cbz_author)
                (base / 'OEBPS' / 'content.opf').write_text(opf, encoding='utf-8')

                nav = generate_nav_fxl(pages_meta)
                (base / 'OEBPS' / 'nav.xhtml').write_text(nav, encoding='utf-8')

                pack_epub(base, epub_path)

        return True

    except zipfile.BadZipFile:
        print(T['PROC_ERROR'].format(cbz_path.name, "Archivo CBZ corrupto"))
        return False
    except Exception as e:
        print(T['PROC_ERROR'].format(cbz_path.name, e))
        if epub_path.exists():
            try:
                epub_path.unlink()
            except Exception:
                pass
        return False


# =========================================================
# APLICACIÓN PRINCIPAL
# =========================================================

class PDFCBZtoEPUBApp:
    def __init__(self, T: dict):
        self.T = T
        self.folder_path = None
        self.dry_run = False
        self.include_subfolders = False

        # Métricas
        self.reset_metrics()

    def reset_metrics(self):
        self.metrics = {
            'total': 0,
            'pdf_text': 0,
            'pdf_image': 0,
            'cbz': 0,
            'skipped': 0,
            'errors': 0,
            'moved': 0,
            'total_size': 0,
            'total_original_size': 0,
            # Desglose por tipo: (original_bytes, epub_bytes)
            'size_pdf_text': [0, 0],
            'size_pdf_image': [0, 0],
            'size_cbz': [0, 0],
        }

    # ─── ESCANEO DE ARCHIVOS ─────────────────────────────────────────

    def scan_files(self) -> Tuple[List[Path], List[Path]]:
        """Escanea y devuelve (pdfs, cbzs)."""
        path = Path(self.folder_path)
        if self.include_subfolders:
            pdfs = sorted(path.rglob('*.pdf'))
            cbzs = sorted(path.rglob('*.cbz'))
        else:
            pdfs = sorted(path.glob('*.pdf'))
            cbzs = sorted(path.glob('*.cbz'))
        return pdfs, cbzs

    # ─── CONVERSIÓN DE 1 ARCHIVO ─────────────────────────────────────

    def process_single_file(self, file_path: Path):
        """Procesa un único archivo (PDF o CBZ)."""
        T = self.T
        ext = file_path.suffix.lower()
        epub_path = file_path.with_suffix('.epub')

        # Verificar si ya existe
        if epub_path.exists():
            print(T['SKIP_EXISTS'].format(epub_path.name))
            self.metrics['skipped'] += 1
            return

        # Modo simulación evolucionado: categoriza y estima
        if self.dry_run:
            pdf_type = "N/A"
            orig_size = file_path.stat().st_size
            est_size = orig_size
            category = "CBZ" if ext == '.cbz' else "PDF"
            
            if ext == '.pdf':
                try:
                    doc = fitz.open(file_path)
                    pdf_type, _ = detect_pdf_type(doc)
                    doc.close()
                    category = f"PDF {pdf_type.upper()}"
                    # Estimación heurística de ahorro
                    est_size = orig_size * (0.25 if pdf_type == 'text' else 0.85)
                except:
                    category = "PDF (PROTEGIDO)"
            else:
                # Estimación para CBZ
                est_size = orig_size * 0.80

            print(f"[SIMULACIÓN] {file_path.name}")
            print(f"    ↳ Acción: {category} → EPUB")
            print(f"    ↳ Ahorro Estimado: {orig_size/(1024*1024):.1f}MB → ~{est_size/(1024*1024):.1f}MB")
            
            try:
                rel = file_path.relative_to(self.folder_path)
            except:
                rel = Path(file_path.name)
            print(f"    ↳ Traslado: ORIGINAL/{rel}")
            
            # Actualizar métricas para el resumen final (proyectado)
            self.metrics['total_original_size'] += orig_size
            self.metrics['total_size'] += est_size
            if ext == '.cbz':
                self.metrics['cbz'] += 1
                self.metrics['size_cbz'][0] += orig_size
                self.metrics['size_cbz'][1] += est_size
            elif ext == '.pdf':
                if pdf_type == 'text':
                    self.metrics['pdf_text'] += 1
                    self.metrics['size_pdf_text'][0] += orig_size
                    self.metrics['size_pdf_text'][1] += est_size
                else:
                    self.metrics['pdf_image'] += 1
                    self.metrics['size_pdf_image'][0] += orig_size
                    self.metrics['size_pdf_image'][1] += est_size
            return

        print(T['PROCESSING'].format(file_path.name))
        inicio = time.time()
        success = False
        pdf_type = None

        if ext == '.cbz':
            success = convert_cbz_to_epub(file_path, epub_path, T)
            if success:
                self.metrics['cbz'] += 1

        elif ext == '.pdf':
            # Detectar tipo de PDF
            try:
                doc = fitz.open(file_path)
            except Exception:
                print(T['SKIP_PROTECTED'].format(file_path.name))
                self.metrics['skipped'] += 1
                return

            if len(doc) == 0:
                print(T['SKIP_EMPTY'].format(file_path.name))
                doc.close()
                self.metrics['skipped'] += 1
                return

            pdf_type, avg_chars = detect_pdf_type(doc)
            pdf_meta_lang = (doc.metadata or {}).get('language', '')
            doc.close()

            if pdf_type == 'text':
                print(T['DETECTED_TEXT'].format(avg_chars))
                success = convert_pdf_text_to_epub(file_path, epub_path, T)
                if success:
                    self.metrics['pdf_text'] += 1
            else:
                print(T['DETECTED_IMAGE'].format(avg_chars))
                ocr_used = False
                if HAS_TESSERACT:
                    tess_lang = _pdf_lang_to_tesseract(pdf_meta_lang)
                    if _test_ocr_quality(str(file_path), lang=tess_lang):
                        print(T['OCR_VIABLE'])
                        success = convert_pdf_ocr_to_epub(
                            file_path, epub_path, T, lang=tess_lang)
                        if success:
                            self.metrics['pdf_text'] += 1  # OCR -> EPUB texto
                            ocr_used = True
                else:
                    print(T['OCR_NOT_AVAIL'])

                if not ocr_used:
                    if HAS_TESSERACT:
                        print(T['OCR_LOW_QUALITY'])
                    success = convert_pdf_image_to_epub(file_path, epub_path, T)
                    if success:
                        self.metrics['pdf_image'] += 1

        if success and epub_path.exists():
            epub_size = epub_path.stat().st_size
            original_size = file_path.stat().st_size
            size_mb = epub_size / (1024 * 1024)
            orig_mb = original_size / (1024 * 1024)
            self.metrics['total_size'] += epub_size
            self.metrics['total_original_size'] += original_size

            # Acumular por tipo
            if ext == '.cbz':
                self.metrics['size_cbz'][0] += original_size
                self.metrics['size_cbz'][1] += epub_size
            elif ext == '.pdf' and pdf_type == 'text':
                self.metrics['size_pdf_text'][0] += original_size
                self.metrics['size_pdf_text'][1] += epub_size
            elif ext == '.pdf':
                self.metrics['size_pdf_image'][0] += original_size
                self.metrics['size_pdf_image'][1] += epub_size

            elapsed = time.time() - inicio
            print(T['SAVED_OK'].format(epub_path.name, size_mb))
            print(T['FILE_SIZE_CMP'].format(orig_mb, size_mb))
            print(f"   ⏱️  {elapsed:.1f}s")

            # Trasladar original a ORIGINAL/
            try:
                base_path = Path(self.folder_path)
                try:
                    rel = file_path.relative_to(base_path)
                except ValueError:
                    rel = Path(file_path.name)
                dest = base_path / 'ORIGINAL' / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(file_path), str(dest))
                print(T['MOVED_OK'].format(rel))
                self.metrics['moved'] += 1
            except Exception as e:
                print(T['MOVE_ERROR'].format(e))

        elif not success:
            self.metrics['errors'] += 1

    # ─── EJECUCIÓN EN LOTE ───────────────────────────────────────────

    def run_conversion(self):
        T = self.T
        path = Path(self.folder_path)

        if not path.is_dir():
            print(T['INVALID_PATH'])
            return

        pdfs, cbzs = self.scan_files()

        if not pdfs and not cbzs:
            print(T['NO_FILES'])
            return

        total = len(pdfs) + len(cbzs)
        print(T['FOUND_FILES'].format(total, len(pdfs), len(cbzs)))

        self.reset_metrics()
        self.metrics['total'] = total

        # Procesar CBZs primero (más rápidos)
        for f in cbzs:
            self.process_single_file(f)

        # Luego PDFs
        for f in pdfs:
            self.process_single_file(f)

        # Resumen
        self.print_summary()
        print(T['SUCCESS_ALL'])

    # ─── RESUMEN ─────────────────────────────────────────────────────

    def print_summary(self):
        T = self.T
        m = self.metrics

        def _fmt_row(label, count, orig_b, epub_b):
            """Formatea una fila del resumen con tamaños y ahorro."""
            orig_mb = orig_b / (1024 * 1024)
            epub_mb = epub_b / (1024 * 1024)
            if orig_b > 0:
                saved_mb = orig_mb - epub_mb
                saved_pct = saved_mb / orig_mb * 100
                return (f"  {label:<14} {count:>4}   "
                        f"{orig_mb:>8.1f} MB  {epub_mb:>8.1f} MB  "
                        f"{saved_mb:>+8.1f} MB ({saved_pct:>5.1f}%)")
            else:
                return f"  {label:<14} {count:>4}         -           -           -"

        print("\n" + "=" * 68)
        title = T['SUMMARY_TITLE']
        if self.dry_run:
            title += " [PROYECTADO]"
        print(f"  {title}")
        print("=" * 68)

        # Cabecera
        print(f"  {T['SUMMARY_COL_TYPE']:<14} {T['SUMMARY_COL_COUNT']:>4}   "
              f"{T['SUMMARY_COL_ORIG']:>10}  {T['SUMMARY_COL_EPUB']:>10}  "
              f"{T['SUMMARY_COL_SAVED']:>18}")
        print("  " + "-" * 64)

        # Filas por tipo
        if m['pdf_text'] > 0:
            print(_fmt_row(T['SUMMARY_ROW_TEXT'], m['pdf_text'],
                           m['size_pdf_text'][0], m['size_pdf_text'][1]))
        if m['pdf_image'] > 0:
            print(_fmt_row(T['SUMMARY_ROW_IMAGE'], m['pdf_image'],
                           m['size_pdf_image'][0], m['size_pdf_image'][1]))
        if m['cbz'] > 0:
            print(_fmt_row(T['SUMMARY_ROW_CBZ'], m['cbz'],
                           m['size_cbz'][0], m['size_cbz'][1]))

        # Fila de saltados
        skip_total = m['skipped'] + m['errors']
        if skip_total > 0:
            print(f"  {T['SUMMARY_ROW_SKIP']:<14} {skip_total:>4}")

        # Total
        converted = m['pdf_text'] + m['pdf_image'] + m['cbz']
        print("  " + "-" * 64)
        print(_fmt_row(T['SUMMARY_ROW_TOTAL'], converted,
                       m['total_original_size'], m['total_size']))
        if m['moved'] > 0:
            print(f"  {T['SUMMARY_ROW_MOVED']:<14} {m['moved']:>4}   -> ORIGINAL/")
        print("=" * 68)

    # ─── UI: SELECCIÓN DE CARPETA ────────────────────────────────────

    def select_folder(self):
        T = self.T
        clear_screen()
        print_banner(T['BANNER_CONFIG'])
        print(T['FOLDER_INTRO'])
        self.folder_path = input_path(T['FOLDER_PROMPT'])
        if not self.folder_path:
            self.folder_path = os.getcwd()

    # ─── UI: MENÚ INTERACTIVO ────────────────────────────────────────

    def show_menu(self):
        T = self.T
        while True:
            clear_screen()
            print_banner(T['BANNER_MENU'])
            print(T['ACTIVE_FOLDER'].format(self.folder_path))

            sim_label = T['SIM_LABEL'] if self.dry_run else ""
            print(T['ACTIONS_HEADER'].format(sim_label))
            
            # --- INTERFAZ DE PULSADORES ---
            print(" ╔══════════════════════════════════════════════════════════╗")
            print(f" ║  [ 1 ]  {T['MENU_1'].strip():<48} ║")
            print(f" ║  [ 2 ]  {(T['MENU_2_ON'] if self.dry_run else T['MENU_2_OFF']).strip():<48} ║")
            print(f" ║  [ 3 ]  {T['MENU_3'].strip():<48} ║")
            subs_state = T['ON'] if self.include_subfolders else T['OFF']
            print(f" ║  [ 4 ]  {T['MENU_4'].format(subs_state).strip():<48} ║")
            print(" ╟──────────────────────────────────────────────────────────╢")
            print(f" ║  [ 0 ]  {T['MENU_0'].strip():<48} ║")
            print(" ╚══════════════════════════════════════════════════════════╝")

            choice = input(T['SELECT_OPTION']).strip()

            if choice == '1':
                self.run_conversion()
                input(T['PRESS_ENTER'])
            elif choice == '2':
                self.dry_run = not self.dry_run
            elif choice == '3':
                self.select_folder()
            elif choice == '4':
                self.include_subfolders = not self.include_subfolders
            elif choice == '0':
                print(T['EXIT_MSG'])
                sys.exit(0)
            else:
                input(T['UNKNOWN_CMD'])

    # ─── PUNTO DE ENTRADA ────────────────────────────────────────────

    def start(self):
        T = self.T
        try:
            clear_screen()
            print(T['PROMO_START'])
            print(f"\n{T['PROMO_END']}")

            user_choice = input(T['CONTINUE_PROMPT']).strip().upper()
            if user_choice not in ('S', 'Y'):
                print(T['GOODBYE'])
                sys.exit(0)

            self.select_folder()
            self.show_menu()
        except KeyboardInterrupt:
            print(T['INTERRUPT'])
            sys.exit(0)


# =========================================================

if __name__ == "__main__":
    lang = get_ui_language()
    T = TEXTS[lang]
    app = PDFCBZtoEPUBApp(T)
    app.start()
