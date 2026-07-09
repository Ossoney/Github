"""
------------------------------------------------------------------------------
GUÍA DE INSTALACIÓN DE DEPENDENCIAS
------------------------------------------------------------------------------
Para que el programa funcione, abre tu terminal y ejecuta:

[WINDOWS]
pip install Pillow

[LINUX / MACOS]
pip3 install Pillow
------------------------------------------------------------------------------
"""

import concurrent.futures
import io
import locale
import logging
import os
import re
import shutil
import sys
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
import tempfile
import time
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

# =========================================================
# DEPENDENCIAS EXTERNAS
# =========================================================
try:
    from PIL import Image
    Image.MAX_IMAGE_PIXELS = 200_000_000
except ImportError:
    print("Error: Install Pillow → pip install Pillow")
    sys.exit(1)

# =========================================================
# LOGGER
# =========================================================
DOCUMENTS_DIR = Path.home() / "Documents" / "Epubbiblio"
DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)
LOG_PATH = DOCUMENTS_DIR / 'cbztoepub.log'

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
            "CBZtoEPUB es un programa freeware que convierte tus archivos de cómic (CBZ)\n"
            "en formato EPUB Fixed-Layout, optimizando las imágenes para lectura fluida.\n"
            "No te preocupes, los archivos originales se mantienen."
        ),
        'PROMO_END': (
            "---------------------------------------------------------------\n"
            "Si el programa te ha sido útil invítame a un café en paypal.me/ossoney.\n"
            "Envíame 1$ - 2$ - 3$ o lo que te apetezca.\n"
            "---------------------------------------------------------------"
        ),
        'CONTINUE_PROMPT': "\n¿Deseas continuar (S/N)?: ",
        'GOODBYE':         "\nOperación cancelada. ¡Gracias por usar CBZtoEPUB!",
        'INTERRUPT':       "\n\n(x) Salida forzada por el usuario.",

        'BANNER_CONFIG': "CBZ TO EPUB - CONFIGURACIÓN",
        'BANNER_MENU':   "CBZ TO EPUB - MENÚ PRINCIPAL",

        'FOLDER_INTRO':  "Selecciona la carpeta donde guardas tus CBZs.",
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
        'NO_FILES':        "\nNo se encontraron archivos CBZ en esta carpeta.",
        'FOUND_FILES':     "\n[INFO] Se encontraron {} archivos CBZs. Arrancando motores...",
        'SUCCESS_ALL':     "\n → [COMPLETADO] Conversión terminada.",
        'SIM_FILE':        "[SIMULACIÓN] Convertiría: {} → {}",
        'SIM_MOVE':        "[SIMULACIÓN] Trasladaría original a: ORIGINAL/{}",
        'PROCESSING':      "\n → Procesando: {}",
        'SAVED_OK':        " → [OK] Guardado: {} ({:.1f} MB)",
        'MOVED_OK':        " → [OK] Original trasladado a: ORIGINAL/{}",
        'MOVE_ERROR':      " → [AVISO] No se pudo trasladar el original: {}",
        'PROC_ERROR':      " → [ERROR] Falló: {} → {}",
        'SKIP_EXISTS':     " → [SKIP] Ya existe: {}",
        'SKIP_EMPTY':      " → [SKIP] Archivo vacío o sin contenido válido: {}",
        'CBZ_CONVERT':     "   🖼️  Convirtiendo CBZ (cómic) a EPUB Fixed-Layout",
        'PAGES_FOUND':     "   📄 {} páginas procesadas",
        'OPT_BW_DETECTED': "   🔲 Imagen B/N detectada → escala de grises (ahorro extra)",
        'OPT_SAVINGS':     "   📦 Optimización: {:.1f} MB → {:.1f} MB ({:.1f}% ahorro)",
        'JPEG_PASSTHRU':   "   ⚡ {} imágenes JPEG copiadas sin recodificación (cero pérdida)",
        'COMIC_INFO':      "   📋 Metadatos ComicInfo.xml encontrados: {}",
        'PROGRESS':        "   [{}/{}]",
        'FILE_SIZE_CMP':   "   📊 Original: {:.1f} MB → EPUB: {:.1f} MB",

        'SUMMARY_TITLE':       "RESUMEN DE CONVERSIÓN",
        'SUMMARY_PROCESSED':   "Archivos procesados:",
        'SUMMARY_CBZ':         "CBZs → EPUB:",
        'SUMMARY_SKIPPED':     "Saltados / Errores:",
        'SUMMARY_COL_TYPE':    "TIPO",
        'SUMMARY_COL_COUNT':   "ARCH.",
        'SUMMARY_COL_ORIG':    "ORIGINAL",
        'SUMMARY_COL_EPUB':    "EPUB",
        'SUMMARY_COL_SAVED':   "AHORRO",
        'SUMMARY_ROW_CBZ':     "CBZ",
        'SUMMARY_ROW_TOTAL':   "TOTAL",
        'SUMMARY_ROW_SKIP':    "Saltados/Errores",
        'SUMMARY_ROW_MOVED':   "Orig. trasladados",

        'ON':  'SÍ',
        'OFF': 'NO',
    },
    'en': {
        'PROMO_START': (
            "CBZtoEPUB is freeware that converts your CBZ files\n"
            "into Fixed-Layout EPUB format, optimizing images for a fluid reading experience.\n"
            "Don't worry, your original files are kept safe."
        ),
        'PROMO_END': (
            "---------------------------------------------------------------\n"
            "If the program was useful, invite me for a coffee at paypal.me/ossoney.\n"
            "Send $1 - $2 - $3 or whatever you feel like.\n"
            "---------------------------------------------------------------"
        ),
        'CONTINUE_PROMPT': "\nDo you want to continue (Y/N)?: ",
        'GOODBYE':         "\nOperation cancelled. Thank you for using CBZtoEPUB!",
        'INTERRUPT':       "\n\n(x) Forced exit by user.",

        'BANNER_CONFIG': "CBZ TO EPUB - SETUP",
        'BANNER_MENU':   "CBZ TO EPUB - MAIN MENU",

        'FOLDER_INTRO':  "Select the folder where your CBZs are stored.",
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
        'NO_FILES':        "\nNo CBZ files found in this folder.",
        'FOUND_FILES':     "\n[INFO] Found {} CBZ files. Starting engines...",
        'SUCCESS_ALL':     "\n → [COMPLETE] Conversion finished.",
        'SIM_FILE':        "[SIMULATION] Would convert: {} → {}",
        'SIM_MOVE':        "[SIMULATION] Would move original to: ORIGINAL/{}",
        'PROCESSING':      "\n → Processing: {}",
        'SAVED_OK':        " → [OK] Saved: {} ({:.1f} MB)",
        'MOVED_OK':        " → [OK] Original moved to: ORIGINAL/{}",
        'MOVE_ERROR':      " → [WARNING] Could not move original: {}",
        'PROC_ERROR':      " → [ERROR] Failed: {} → {}",
        'SKIP_EXISTS':     " → [SKIP] Already exists: {}",
        'SKIP_EMPTY':      " → [SKIP] Empty file or no valid content: {}",
        'CBZ_CONVERT':     "   🖼️  Converting CBZ (comic) to Fixed-Layout EPUB",
        'PAGES_FOUND':     "   📄 {} pages processed",
        'OPT_BW_DETECTED': "   🔲 B/W image detected → grayscale (extra savings)",
        'OPT_SAVINGS':     "   📦 Optimization: {:.1f} MB → {:.1f} MB ({:.1f}% savings)",
        'JPEG_PASSTHRU':   "   ⚡ {} JPEG images copied without re-encoding (zero loss)",
        'COMIC_INFO':      "   📋 ComicInfo.xml metadata found: {}",
        'PROGRESS':        "   [{}/{}]",
        'FILE_SIZE_CMP':   "   📊 Original: {:.1f} MB → EPUB: {:.1f} MB",

        'SUMMARY_TITLE':       "CONVERSION SUMMARY",
        'SUMMARY_PROCESSED':   "Files processed:",
        'SUMMARY_CBZ':         "CBZs → EPUB:",
        'SUMMARY_SKIPPED':     "Skipped / Errors:",
        'SUMMARY_COL_TYPE':    "TYPE",
        'SUMMARY_COL_COUNT':   "FILES",
        'SUMMARY_COL_ORIG':    "ORIGINAL",
        'SUMMARY_COL_EPUB':    "EPUB",
        'SUMMARY_COL_SAVED':   "SAVINGS",
        'SUMMARY_ROW_CBZ':     "CBZ",
        'SUMMARY_ROW_TOTAL':   "TOTAL",
        'SUMMARY_ROW_SKIP':    "Skipped/Errors",
        'SUMMARY_ROW_MOVED':   "Originals moved",

        'ON':  'YES',
        'OFF': 'NO',
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

def generate_opf_fxl(title: str, uid: str, pages: List[dict],
                      width: int, height: int,
                      author: str = '', language: str = 'es') -> str:
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

def generate_nav_fxl(pages: List[dict]) -> str:
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
    with zipfile.ZipFile(epub_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
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
# CONFIGURACIÓN DE OPTIMIZACIÓN
# =========================================================

OPT_COMIC = {
    'max_width': 1600,
    'max_height': 2400,
    'quality': 82,
}

def _is_grayscale_image(img: Image.Image) -> bool:
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
        try:
            small = img.resize((50, 50), Image.Resampling.BILINEAR)
            diffs = [abs(r - g) + abs(g - b) for r, g, b in small.getdata()]
            return (sum(diffs) / len(diffs)) < 10.0
        except Exception:
            return False

def optimize_image_for_epub(img: Image.Image, original_data: bytes = None, is_bw: bool = None) -> bytes:
    conf = OPT_COMIC
    max_w = conf['max_width']
    max_h = conf.get('max_height', max_w * 2)
    quality = conf['quality']

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

    if is_bw is None:
        is_bw = _is_grayscale_image(img)
        
    active_max_w = 1100 if is_bw else max_w
    active_max_h = active_max_w * 1.5

    if img.width > active_max_w or img.height > active_max_h:
        ratio = min(active_max_w / img.width, active_max_h / img.height)
        new_size = (int(img.width * ratio), int(img.height * ratio))
        img = img.resize(new_size, Image.Resampling.LANCZOS)

    if is_bw:
        img = img.convert('L')
        quality = min(quality, 30)

    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=quality, optimize=True)
    optimized_data = buf.getvalue()

    if original_data and len(optimized_data) >= len(original_data):
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

            if img_fallback.width > active_max_w:
                ratio = active_max_w / img_fallback.width
                new_size = (active_max_w, int(img_fallback.height * ratio))
                img_fallback = img_fallback.resize(new_size, Image.Resampling.LANCZOS)

            buf2 = io.BytesIO()
            img_fallback.save(buf2, "JPEG", quality=quality, optimize=True)
            return buf2.getvalue()
        except Exception:
            return optimized_data

    return optimized_data

def minify_xhtml(content: str) -> str:
    content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
    content = re.sub(r'\s{2,}', ' ', content)
    return content.strip()

# =========================================================
# CONVERSOR CBZ
# =========================================================

def _process_cbz_image(args):
    idx, raw_path, out_path = args
    try:
        with open(raw_path, 'rb') as f:
            img_bytes = f.read()
        img = Image.open(io.BytesIO(img_bytes))
        is_bw = _is_grayscale_image(img)

        can_passthrough = (
            img.format == 'JPEG'
            and img.width <= OPT_COMIC['max_width']
            and img.height <= OPT_COMIC.get('max_height', 2400)
            and not is_bw
        )
        if can_passthrough:
            bytes_per_pixel = len(img_bytes) / max(1, img.width * img.height)
            if bytes_per_pixel < 0.4:
                Path(out_path).write_bytes(img_bytes)
                return idx, len(img_bytes), len(img_bytes), False, True

        optimized = optimize_image_for_epub(img, original_data=img_bytes, is_bw=is_bw)
        Path(out_path).write_bytes(optimized)
        try:
            Path(raw_path).unlink()
        except Exception:
            pass
        return idx, len(img_bytes), len(optimized), is_bw, False
    except Exception:
        Path(out_path).write_bytes(img_bytes)
        try:
            Path(raw_path).unlink()
        except Exception:
            pass
        return idx, len(img_bytes), len(img_bytes), False, False

def convert_cbz_to_epub(cbz_path: Path, epub_path: Path, T: dict) -> bool:
    IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff'}

    try:
        with zipfile.ZipFile(cbz_path, 'r') as zf:
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
                vp_width, vp_height = 1200, 1800
            if vp_width > 1600:
                ratio = 1600 / vp_width
                vp_width = 1600
                vp_height = int(vp_height * ratio)

            with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
                base = Path(tmp)
                (base / 'META-INF').mkdir()
                (base / 'OEBPS' / 'images').mkdir(parents=True)

                (base / 'mimetype').write_text(MIMETYPE, encoding='utf-8')
                (base / 'META-INF' / 'container.xml').write_text(CONTAINER_XML, encoding='utf-8')
                (base / 'OEBPS' / 'estilos.css').write_text(CSS_FXL, encoding='utf-8')

                worker_tasks = []
                for idx, img_name in enumerate(image_names, 1):
                    print(T['PROGRESS'].format(idx, len(image_names)), end='\r')
                    raw_path = str(base / 'OEBPS' / 'images' / f"raw_{idx:04d}{Path(img_name).suffix}")
                    out_path = str(base / 'OEBPS' / 'images' / f"{idx:04d}.jpg")
                    with open(raw_path, 'wb') as f:
                        f.write(zf.read(img_name))
                    worker_tasks.append((idx, raw_path, out_path))

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

                pages_meta = []
                for idx in range(1, len(image_names) + 1):
                    img_filename = f"{idx:04d}.jpg"
                    page_href = f"page_{idx:04d}.xhtml"
                    page_xhtml = generate_fxl_page_xhtml(img_filename, vp_width, vp_height)
                    (base / 'OEBPS' / page_href).write_text(page_xhtml, encoding='utf-8')

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
                uid = f"cbztoepub-{cbz_path.stem}-{int(time.time())}"

                opf = generate_opf_fxl(title, uid, pages_meta, vp_width, vp_height, author=cbz_author)
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

class CBZtoEPUBApp:
    def __init__(self, T: dict):
        self.T = T
        self.folder_path = None
        self.dry_run = False
        self.include_subfolders = False
        self.reset_metrics()

    def reset_metrics(self):
        self.metrics = {
            'total': 0,
            'cbz': 0,
            'skipped': 0,
            'errors': 0,
            'moved': 0,
            'total_size': 0,
            'total_original_size': 0,
            'size_cbz': [0, 0],
        }

    def scan_files(self) -> List[Path]:
        path = Path(self.folder_path)
        if self.include_subfolders:
            return sorted(path.rglob('*.cbz'))
        else:
            return sorted(path.glob('*.cbz'))

    def process_single_file(self, file_path: Path):
        T = self.T
        epub_path = file_path.with_suffix('.epub')

        if epub_path.exists():
            print(T['SKIP_EXISTS'].format(epub_path.name))
            self.metrics['skipped'] += 1
            return

        if self.dry_run:
            orig_size = file_path.stat().st_size
            est_size = orig_size * 0.80

            print(f"[SIMULACIÓN] {file_path.name}")
            print(f"    ↳ Acción: CBZ → EPUB")
            print(f"    ↳ Ahorro Estimado: {orig_size/(1024*1024):.1f}MB → ~{est_size/(1024*1024):.1f}MB")
            
            try:
                rel = file_path.relative_to(self.folder_path)
            except:
                rel = Path(file_path.name)
            print(f"    ↳ Traslado: ORIGINAL/{rel}")
            
            self.metrics['total_original_size'] += orig_size
            self.metrics['total_size'] += est_size
            self.metrics['cbz'] += 1
            self.metrics['size_cbz'][0] += orig_size
            self.metrics['size_cbz'][1] += est_size
            return

        print(T['PROCESSING'].format(file_path.name))
        inicio = time.time()
        
        success = convert_cbz_to_epub(file_path, epub_path, T)

        if success and epub_path.exists():
            self.metrics['cbz'] += 1
            epub_size = epub_path.stat().st_size
            original_size = file_path.stat().st_size
            size_mb = epub_size / (1024 * 1024)
            orig_mb = original_size / (1024 * 1024)
            self.metrics['total_size'] += epub_size
            self.metrics['total_original_size'] += original_size

            self.metrics['size_cbz'][0] += original_size
            self.metrics['size_cbz'][1] += epub_size

            elapsed = time.time() - inicio
            print(T['SAVED_OK'].format(epub_path.name, size_mb))
            print(T['FILE_SIZE_CMP'].format(orig_mb, size_mb))
            print(f"   ⏱️  {elapsed:.1f}s")

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

    def run_conversion(self):
        T = self.T
        path = Path(self.folder_path)

        if not path.is_dir():
            print(T['INVALID_PATH'])
            return

        cbzs = self.scan_files()

        if not cbzs:
            print(T['NO_FILES'])
            return

        print(T['FOUND_FILES'].format(len(cbzs)))

        self.reset_metrics()
        self.metrics['total'] = len(cbzs)

        for f in cbzs:
            self.process_single_file(f)

        self.print_summary()
        print(T['SUCCESS_ALL'])

    def print_summary(self):
        T = self.T
        m = self.metrics

        def _fmt_row(label, count, orig_b, epub_b):
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

        print(f"  {T['SUMMARY_COL_TYPE']:<14} {T['SUMMARY_COL_COUNT']:>4}   "
              f"{T['SUMMARY_COL_ORIG']:>10}  {T['SUMMARY_COL_EPUB']:>10}  "
              f"{T['SUMMARY_COL_SAVED']:>18}")
        print("  " + "-" * 64)

        if m['cbz'] > 0:
            print(_fmt_row(T['SUMMARY_ROW_CBZ'], m['cbz'],
                           m['size_cbz'][0], m['size_cbz'][1]))

        skip_total = m['skipped'] + m['errors']
        if skip_total > 0:
            print(f"  {T['SUMMARY_ROW_SKIP']:<14} {skip_total:>4}")

        print("  " + "-" * 64)
        print(_fmt_row(T['SUMMARY_ROW_TOTAL'], m['cbz'],
                       m['total_original_size'], m['total_size']))
        if m['moved'] > 0:
            print(f"  {T['SUMMARY_ROW_MOVED']:<14} {m['moved']:>4}   -> ORIGINAL/")
        print("=" * 68)

    def select_folder(self):
        T = self.T
        clear_screen()
        print_banner(T['BANNER_CONFIG'])
        print(T['FOLDER_INTRO'])
        self.folder_path = input_path(T['FOLDER_PROMPT'])
        if not self.folder_path:
            self.folder_path = os.getcwd()

    def show_menu(self):
        T = self.T
        while True:
            clear_screen()
            print_banner(T['BANNER_MENU'])
            print(T['ACTIVE_FOLDER'].format(self.folder_path))

            sim_label = T['SIM_LABEL'] if self.dry_run else ""
            print(T['ACTIONS_HEADER'].format(sim_label))
            
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
    app = CBZtoEPUBApp(T)
    app.start()
