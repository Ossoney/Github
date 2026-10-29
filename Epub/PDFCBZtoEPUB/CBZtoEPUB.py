"""
CBZtoEPUB.py - Conversión optimizada de CBZ / CBR a EPUB Fixed-Layout.
Incluye:
 - Soporte para archivos .cbz y .cbr
 - Perfiles de dispositivo configurables (Kindle Oasis, Paperwhite, Kobo, Tablet, etc.)
 - División de doble página automática (Double-page split)
 - Soporte para dirección de lectura Manga (RTL) u Occidental (LTR)
 - Registro explícito de Portada (cover image) en el EPUB
 - Selector de carpeta gráfico (Tkinter) y fallback de consola
 - Modo simulación (Dry-Run) y modo desatendido (CLI)
"""

import argparse
import concurrent.futures
import io
import locale
import logging
import os
import re
import shutil
import sys
import tempfile
import time
import zipfile
from collections import Counter
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from xml.etree import ElementTree

if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

try:
    from PIL import Image
    Image.MAX_IMAGE_PIXELS = 200_000_000
except ImportError:
    print("Error: Install Pillow → pip install Pillow")
    sys.exit(1)

from common import (
    DEVICE_PROFILES,
    clear_screen,
    print_banner,
    select_folder_dialog,
    input_path_with_fallback,
    extract_archive_images,
    split_double_page_if_needed,
    is_blank_or_black_page,
    generate_opf_fxl,
    generate_nav_fxl,
    generate_fxl_page_xhtml,
    pack_epub,
    MIMETYPE,
    CONTAINER_XML,
    CSS_FXL,
)

# =========================================================
# LOGGER UNIFICADO
# =========================================================
BASE_DIR = Path(__file__).resolve().parent
LOG_PATH = BASE_DIR / 'PDFCBZtoEPUB.log'

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
            "CBZtoEPUB es un programa freeware que convierte tus cómics (CBZ / CBR)\n"
            "en formato EPUB Fixed-Layout optimizado para lectura fluida.\n"
            "Los archivos originales se conservan intactos en la carpeta ORIGINAL/."
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

        'BANNER_CONFIG': "CBZ / CBR TO EPUB - CONFIGURACIÓN",
        'BANNER_MENU':   "CBZ / CBR TO EPUB - MENÚ PRINCIPAL",

        'FOLDER_INTRO':  "Selecciona la carpeta de cómics (o escribe 'g' para abrir ventana de diálogo):",
        'FOLDER_PROMPT': "Ruta ('g' para diálogo, Enter para carpeta actual): ",

        'ACTIVE_FOLDER':  "Carpeta activa: {}",
        'SIM_LABEL':      " [SIMULACIÓN]",
        'ACTIONS_HEADER': "\nACCIONES DISPONIBLES{}:",
        'MENU_1':         "Iniciar Conversión a EPUB",
        'MENU_2_ON':      "Desactivar Modo Simulación (Dry-Run)",
        'MENU_2_OFF':     "Activar Modo Simulación (Dry-Run)",
        'MENU_3':         "Cambiar Carpeta",
        'MENU_4':         "Incluir Subcarpetas: {}",
        'MENU_5':         "Perfil Dispositivo: {}",
        'MENU_6':         "Dividir Páginas Dobles: {}",
        'MENU_7':         "Dirección Lectura: {}",
        'MENU_8':         "Eliminar Páginas Vacías (B/N): {}",
        'MENU_0':         "Salir",
        'SELECT_OPTION':  "\nSelecciona una opción: ",
        'PRESS_ENTER':    "\nPresiona ENTER para volver al menú...",
        'UNKNOWN_CMD':    "Comando no reconocido. Presiona ENTER para continuar...",
        'EXIT_MSG':       "\n¡Desconectando sistemas! Hasta luego.",

        'INVALID_PATH':    "\nError: La ruta seleccionada no es válida.",
        'NO_FILES':        "\nNo se encontraron archivos de cómic (.cbz / .cbr) en esta carpeta.",
        'FOUND_FILES':     "\n[INFO] Se encontraron {} archivos de cómic. Arrancando motores...",
        'SUCCESS_ALL':     "\n → [COMPLETADO] Conversión terminada.",
        'PROCESSING':      "\n → Procesando: {}",
        'SAVED_OK':        " → [OK] Guardado: {} ({:.1f} MB)",
        'MOVED_OK':        " → [OK] Original trasladado a: ORIGINAL/{}",
        'MOVE_ERROR':      " → [AVISO] No se pudo trasladar el original: {}",
        'PROC_ERROR':      " → [ERROR] Falló: {} → {}",
        'SKIP_EXISTS':     " → [SKIP] Ya existe: {}",
        'SKIP_EMPTY':      " → [SKIP] Archivo vacío o sin imágenes válidas: {}",
        'CBZ_CONVERT':     "   🖼️ Convirtiendo Cómic a EPUB Fixed-Layout",
        'PAGES_FOUND':     "   📄 {} páginas generadas",
        'OPT_BW_DETECTED': "   🔲 Imagen B/N detectada → escala de grises (ahorro extra)",
        'BLANK_PAGES_REMOVED': "   🗑️ {} páginas en blanco/negro vacías eliminadas",
        'OPT_SAVINGS':     "   📦 Optimización: {:.1f} MB → {:.1f} MB ({:.1f}% ahorro)",
        'JPEG_PASSTHRU':   "   ⚡ {} imágenes JPEG pasadas sin recodificar (cero pérdida)",
        'COMIC_INFO':      "   📋 Metadatos ComicInfo.xml encontrados: {}",
        'PROGRESS':        "   [{}/{}]",
        'FILE_SIZE_CMP':   "   📊 Original: {:.1f} MB → EPUB: {:.1f} MB",

        'SUMMARY_TITLE':       "RESUMEN DE CONVERSIÓN",
        'SUMMARY_PROCESSED':   "Archivos procesados:",
        'SUMMARY_CBZ':         "Cómics → EPUB:",
        'SUMMARY_SKIPPED':     "Saltados / Errores:",
        'SUMMARY_COL_TYPE':    "TIPO",
        'SUMMARY_COL_COUNT':   "ARCH.",
        'SUMMARY_COL_ORIG':    "ORIGINAL",
        'SUMMARY_COL_EPUB':    "EPUB",
        'SUMMARY_COL_SAVED':   "AHORRO",
        'SUMMARY_ROW_CBZ':     "CÓMICS",
        'SUMMARY_ROW_TOTAL':   "TOTAL",
        'SUMMARY_ROW_SKIP':    "Saltados/Errores",
        'SUMMARY_ROW_MOVED':   "Orig. trasladados",

        'ON':  'SÍ',
        'OFF': 'NO',
        'LTR': 'Occidental (Izq. a Der.)',
        'RTL': 'Manga (Der. a Izq.)',
    },
    'en': {
        'PROMO_START': (
            "CBZtoEPUB is freeware that converts your comics (CBZ / CBR)\n"
            "into Fixed-Layout EPUB format optimized for fluid reading.\n"
            "Original files are kept safe inside the ORIGINAL/ directory."
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

        'BANNER_CONFIG': "CBZ / CBR TO EPUB - CONFIGURATION",
        'BANNER_MENU':   "CBZ / CBR TO EPUB - MAIN MENU",

        'FOLDER_INTRO':  "Select comic folder (or type 'g' for graphical file picker):",
        'FOLDER_PROMPT': "Folder path ('g' for GUI dialog, Enter for current): ",

        'ACTIVE_FOLDER':  "Active folder: {}",
        'SIM_LABEL':      " [SIMULATION]",
        'ACTIONS_HEADER': "\nAVAILABLE ACTIONS{}:",
        'MENU_1':         "Start Conversion to EPUB",
        'MENU_2_ON':      "Disable Simulation Mode (Dry-Run)",
        'MENU_2_OFF':     "Enable Simulation Mode (Dry-Run)",
        'MENU_3':         "Change Folder",
        'MENU_4':         "Include Subfolders: {}",
        'MENU_5':         "Device Profile: {}",
        'MENU_6':         "Split Double Pages: {}",
        'MENU_7':         "Reading Direction: {}",
        'MENU_8':         "Remove Empty Pages (B/W): {}",
        'MENU_0':         "Exit",
        'SELECT_OPTION':  "\nSelect an option: ",
        'PRESS_ENTER':    "\nPress ENTER to return to menu...",
        'UNKNOWN_CMD':    "Unrecognized command. Press ENTER to continue...",
        'EXIT_MSG':       "\nShutting down systems! Goodbye.",

        'INVALID_PATH':    "\nError: The selected path is not valid.",
        'NO_FILES':        "\nNo comic files (.cbz / .cbr) found in this folder.",
        'FOUND_FILES':     "\n[INFO] Found {} comic files. Starting engines...",
        'SUCCESS_ALL':     "\n → [COMPLETE] Conversion finished.",
        'PROCESSING':      "\n → Processing: {}",
        'SAVED_OK':        " → [OK] Saved: {} ({:.1f} MB)",
        'MOVED_OK':        " → [OK] Original moved to: ORIGINAL/{}",
        'MOVE_ERROR':      " → [WARNING] Could not move original: {}",
        'PROC_ERROR':      " → [ERROR] Failed: {} → {}",
        'SKIP_EXISTS':     " → [SKIP] Already exists: {}",
        'SKIP_EMPTY':      " → [SKIP] Empty file or no valid images: {}",
        'CBZ_CONVERT':     "   🖼️ Converting Comic to Fixed-Layout EPUB",
        'PAGES_FOUND':     "   📄 {} pages generated",
        'OPT_BW_DETECTED': "   🔲 B/W image detected → grayscale (extra savings)",
        'BLANK_PAGES_REMOVED': "   🗑️ {} blank/black empty pages removed",
        'OPT_SAVINGS':     "   📦 Optimization: {:.1f} MB → {:.1f} MB ({:.1f}% savings)",
        'JPEG_PASSTHRU':   "   ⚡ {} JPEG images copied without re-encoding (zero loss)",
        'COMIC_INFO':      "   📋 ComicInfo.xml metadata found: {}",
        'PROGRESS':        "   [{}/{}]",
        'FILE_SIZE_CMP':   "   📊 Original: {:.1f} MB → EPUB: {:.1f} MB",

        'SUMMARY_TITLE':       "CONVERSION SUMMARY",
        'SUMMARY_PROCESSED':   "Files processed:",
        'SUMMARY_CBZ':         "Comics → EPUB:",
        'SUMMARY_SKIPPED':     "Skipped / Errors:",
        'SUMMARY_COL_TYPE':    "TYPE",
        'SUMMARY_COL_COUNT':   "FILES",
        'SUMMARY_COL_ORIG':    "ORIGINAL",
        'SUMMARY_COL_EPUB':    "EPUB",
        'SUMMARY_COL_SAVED':   "SAVINGS",
        'SUMMARY_ROW_CBZ':     "COMICS",
        'SUMMARY_ROW_TOTAL':   "TOTAL",
        'SUMMARY_ROW_SKIP':    "Skipped/Errors",
        'SUMMARY_ROW_MOVED':   "Originals moved",

        'ON':  'YES',
        'OFF': 'NO',
        'LTR': 'Western (Left-to-Right)',
        'RTL': 'Manga (Right-to-Left)',
    },
}

# =========================================================
# PIPELINE DE OPTIMIZACIÓN DE IMÁGENES
# =========================================================
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

def optimize_image_for_epub(img: Image.Image, profile_key: str = 'default',
                            original_data: bytes = None, is_bw: bool = None) -> bytes:
    conf = DEVICE_PROFILES.get(profile_key, DEVICE_PROFILES['default'])
    max_w = conf['max_width']
    max_h = conf['max_height']
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

    # Autocropping márgenes blancos
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

    active_max_w = min(1100, max_w) if is_bw else max_w
    active_max_h = active_max_w * 1.5

    if img.width > active_max_w or img.height > active_max_h:
        ratio = min(active_max_w / img.width, active_max_h / img.height)
        new_size = (int(img.width * ratio), int(img.height * ratio))
        img = img.resize(new_size, Image.Resampling.LANCZOS)

    if is_bw:
        img = img.convert('L')
        quality = min(quality, 40)

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

    return optimized_data

def _process_single_page_worker(args):
    idx, raw_path, out_path, profile_key, split_double, reading_dir, remove_blank, is_protected = args
    try:
        with open(raw_path, 'rb') as f:
            raw_bytes = f.read()

        img = Image.open(io.BytesIO(raw_bytes))

        # Detección y descarte de página vacía en blanco o en negro (protegiendo portada)
        if remove_blank and not is_protected:
            if is_blank_or_black_page(img):
                try: Path(raw_path).unlink()
                except Exception: pass
                return idx, len(raw_bytes), 0, False, False, 0, True

        is_bw = _is_grayscale_image(img)
        conf = DEVICE_PROFILES.get(profile_key, DEVICE_PROFILES['default'])

        # Passthrough si no se requiere dividir y ya es óptima
        can_passthrough = (
            not split_double
            and img.format == 'JPEG'
            and img.width <= conf['max_width']
            and img.height <= conf['max_height']
            and not is_bw
            and (len(raw_bytes) / max(1, img.width * img.height) < 0.4)
        )
        if can_passthrough:
            Path(out_path).write_bytes(raw_bytes)
            try: Path(raw_path).unlink()
            except Exception: pass
            return idx, len(raw_bytes), len(raw_bytes), False, True, 1, False

        sub_images = [img]
        if split_double:
            sub_images = split_double_page_if_needed(img, reading_direction=reading_dir)

        out_base = Path(out_path)
        total_opt_size = 0
        pages_produced = len(sub_images)

        if pages_produced == 1:
            opt = optimize_image_for_epub(sub_images[0], profile_key=profile_key, original_data=raw_bytes, is_bw=is_bw)
            out_base.write_bytes(opt)
            total_opt_size = len(opt)
        else:
            # Se divide en dos o más imágenes (ej. 0001_1.jpg, 0001_2.jpg)
            for part_idx, sub_img in enumerate(sub_images, 1):
                part_out = out_base.parent / f"{out_base.stem}_{part_idx}.jpg"
                opt = optimize_image_for_epub(sub_img, profile_key=profile_key, is_bw=is_bw)
                part_out.write_bytes(opt)
                total_opt_size += len(opt)

        try: Path(raw_path).unlink()
        except Exception: pass

        return idx, len(raw_bytes), total_opt_size, is_bw, False, pages_produced, False
    except Exception:
        try:
            with open(raw_path, 'rb') as f:
                b = f.read()
            Path(out_path).write_bytes(b)
            try: Path(raw_path).unlink()
            except Exception: pass
            return idx, len(b), len(b), False, False, 1, False
        except Exception:
            return idx, 0, 0, False, False, 0, False

# =========================================================
# CONVERSIÓN DE CÓMIC A EPUB
# =========================================================
def convert_comic_to_epub(comic_path: Path, epub_path: Path, T: dict,
                          profile_key: str = 'default',
                          split_double: bool = False,
                          reading_direction: str = 'ltr',
                          remove_blank: bool = True) -> bool:
    try:
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
            tmp_dir = Path(tmp)
            raw_extract_dir = tmp_dir / "raw"
            epub_base = tmp_dir / "epub"
            (epub_base / 'META-INF').mkdir(parents=True)
            (epub_base / 'OEBPS' / 'images').mkdir(parents=True)

            (epub_base / 'mimetype').write_text(MIMETYPE, encoding='utf-8')
            (epub_base / 'META-INF' / 'container.xml').write_text(CONTAINER_XML, encoding='utf-8')
            (epub_base / 'OEBPS' / 'estilos.css').write_text(CSS_FXL, encoding='utf-8')

            print(T['CBZ_CONVERT'])
            image_files = extract_archive_images(comic_path, raw_extract_dir)
            if not image_files:
                print(T['SKIP_EMPTY'].format(comic_path.name))
                return False

            # Leer metadatos ComicInfo.xml si existe
            comic_title = comic_path.stem
            comic_author = ''
            ci_path = raw_extract_dir / "ComicInfo.xml"
            if not ci_path.exists():
                for p in raw_extract_dir.rglob("ComicInfo.xml"):
                    ci_path = p
                    break

            if ci_path.exists():
                try:
                    ci_root = ElementTree.fromstring(ci_path.read_bytes())
                    t = ci_root.findtext('Title', '').strip()
                    s = ci_root.findtext('Series', '').strip()
                    n = ci_root.findtext('Number', '').strip()
                    w = ci_root.findtext('Writer', '').strip()
                    if t: comic_title = t
                    elif s and n: comic_title = f"{s} #{n}"
                    elif s: comic_title = s
                    if w: comic_author = w
                    info_str = comic_title + (f" ({comic_author})" if comic_author else "")
                    print(T['COMIC_INFO'].format(info_str))
                except Exception:
                    pass

            # Cálculo de resolución viewport con muestra de imágenes
            size_samples = []
            for sample in image_files[:min(8, len(image_files))]:
                try:
                    with Image.open(sample) as img:
                        size_samples.append(img.size)
                except Exception:
                    continue
            if size_samples:
                vp_width, vp_height = Counter(size_samples).most_common(1)[0][0]
            else:
                vp_width, vp_height = 1200, 1800

            max_profile_w = DEVICE_PROFILES.get(profile_key, DEVICE_PROFILES['default'])['max_width']
            if vp_width > max_profile_w:
                ratio = max_profile_w / vp_width
                vp_width = max_profile_w
                vp_height = int(vp_height * ratio)

            # Preparar tareas para multiprocessing
            worker_tasks = []
            for idx, img_p in enumerate(image_files, 1):
                out_path = epub_base / 'OEBPS' / 'images' / f"{idx:04d}.jpg"
                is_protected = (idx == 1)  # Proteger portada
                worker_tasks.append((idx, str(img_p), str(out_path), profile_key, split_double, reading_direction, remove_blank, is_protected))

            total_raw = 0
            total_opt = 0
            bw_count = 0
            passthrough_count = 0
            blank_removed_count = 0
            workers = max(2, min(os.cpu_count() or 4, 8))

            with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
                results = list(executor.map(_process_single_page_worker, worker_tasks))

            for idx, raw_size, opt_size, is_bw, passthrough, pages_count, is_blank in results:
                total_raw += raw_size
                total_opt += opt_size
                if is_blank:
                    blank_removed_count += 1
                if is_bw: bw_count += 1
                if passthrough: passthrough_count += 1

            # Recolectar las páginas generadas en OEBPS/images en orden
            generated_images = sorted(list((epub_base / 'OEBPS' / 'images').glob("*.jpg")))
            pages_meta = []
            for p_idx, img_p in enumerate(generated_images, 1):
                page_href = f"page_{p_idx:04d}.xhtml"
                page_xhtml = generate_fxl_page_xhtml(img_p.name, vp_width, vp_height)
                (epub_base / 'OEBPS' / page_href).write_text(page_xhtml, encoding='utf-8')
                pages_meta.append({
                    'page_id': f"page_{p_idx:04d}",
                    'page_href': page_href,
                    'img_id': f"img_{p_idx:04d}",
                    'img_href': f"images/{img_p.name}",
                    'label': f"Page {p_idx}",
                })

            print(T['PAGES_FOUND'].format(len(pages_meta)))
            if blank_removed_count > 0:
                print(T['BLANK_PAGES_REMOVED'].format(blank_removed_count))
            if passthrough_count > 0:
                print(T['JPEG_PASSTHRU'].format(passthrough_count))
            if bw_count > len(image_files) * 0.5:
                print(T['OPT_BW_DETECTED'])
            if total_raw > 0:
                raw_mb = total_raw / (1024 * 1024)
                opt_mb = total_opt / (1024 * 1024)
                savings_pct = (1 - total_opt / total_raw) * 100
                print(T['OPT_SAVINGS'].format(raw_mb, opt_mb, savings_pct))

            uid = f"cbztoepub-{comic_path.stem}-{int(time.time())}"
            opf = generate_opf_fxl(
                comic_title, uid, pages_meta, vp_width, vp_height,
                author=comic_author, reading_direction=reading_direction
            )
            (epub_base / 'OEBPS' / 'content.opf').write_text(opf, encoding='utf-8')

            nav = generate_nav_fxl(pages_meta)
            (epub_base / 'OEBPS' / 'nav.xhtml').write_text(nav, encoding='utf-8')

            pack_epub(epub_base, epub_path)
            return True

    except Exception as e:
        print(T['PROC_ERROR'].format(comic_path.name, e))
        if epub_path.exists():
            try: epub_path.unlink()
            except Exception: pass
        return False

# =========================================================
# APLICACIÓN INTERACTIVA
# =========================================================
class CBZtoEPUBApp:
    def __init__(self, T: dict, folder: Optional[str] = None,
                 profile: str = 'default', dry_run: bool = False,
                 subfolders: bool = False, split_double: bool = False,
                 reading_dir: str = 'ltr', remove_blank: bool = True):
        self.T = T
        self.folder_path = folder or os.getcwd()
        self.profile = profile
        self.dry_run = dry_run
        self.include_subfolders = subfolders
        self.split_double = split_double
        self.reading_direction = reading_dir
        self.remove_blank = remove_blank
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
        }

    def scan_files(self) -> List[Path]:
        path = Path(self.folder_path)
        files = []
        exts = ('*.cbz', '*.cbr')
        for ext in exts:
            if self.include_subfolders:
                files.extend(path.rglob(ext))
            else:
                files.extend(path.glob(ext))
        return sorted(list(set(files)))

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
            print(f"    ↳ Acción: {file_path.suffix.upper()} → EPUB Fixed-Layout")
            print(f"    ↳ Perfil: {DEVICE_PROFILES.get(self.profile, {}).get('name')}")
            print(f"    ↳ División dobles: {T['ON'] if self.split_double else T['OFF']} | Dirección: {self.reading_direction.upper()}")
            print(f"    ↳ Ahorro Estimado: {orig_size/(1024*1024):.1f}MB → ~{est_size/(1024*1024):.1f}MB")
            try:
                rel = file_path.relative_to(self.folder_path)
            except Exception:
                rel = Path(file_path.name)
            print(f"    ↳ Traslado: ORIGINAL/{rel}")
            self.metrics['total_original_size'] += orig_size
            self.metrics['total_size'] += est_size
            self.metrics['cbz'] += 1
            return

        print(T['PROCESSING'].format(file_path.name))
        inicio = time.time()

        success = convert_comic_to_epub(
            file_path, epub_path, T,
            profile_key=self.profile,
            split_double=self.split_double,
            reading_direction=self.reading_direction,
            remove_blank=self.remove_blank
        )

        if success and epub_path.exists():
            self.metrics['cbz'] += 1
            epub_size = epub_path.stat().st_size
            orig_size = file_path.stat().st_size
            size_mb = epub_size / (1024 * 1024)
            orig_mb = orig_size / (1024 * 1024)
            self.metrics['total_size'] += epub_size
            self.metrics['total_original_size'] += orig_size

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

        comics = self.scan_files()
        if not comics:
            print(T['NO_FILES'])
            return

        print(T['FOUND_FILES'].format(len(comics)))
        self.reset_metrics()
        self.metrics['total'] = len(comics)

        for f in comics:
            self.process_single_file(f)

        self.print_summary()
        print(T['SUCCESS_ALL'])

    def print_summary(self):
        T = self.T
        m = self.metrics
        orig_mb = m['total_original_size'] / (1024 * 1024)
        epub_mb = m['total_size'] / (1024 * 1024)
        saved_mb = orig_mb - epub_mb
        saved_pct = (saved_mb / orig_mb * 100) if orig_mb > 0 else 0

        print("\n" + "=" * 68)
        title = T['SUMMARY_TITLE']
        if self.dry_run: title += " [PROYECTADO]"
        print(f"  {title}")
        print("=" * 68)
        print(f"  {T['SUMMARY_COL_TYPE']:<14} {T['SUMMARY_COL_COUNT']:>4}   "
              f"{T['SUMMARY_COL_ORIG']:>10}  {T['SUMMARY_COL_EPUB']:>10}  "
              f"{T['SUMMARY_COL_SAVED']:>18}")
        print("  " + "-" * 64)
        print(f"  {T['SUMMARY_ROW_CBZ']:<14} {m['cbz']:>4}   "
              f"{orig_mb:>8.1f} MB  {epub_mb:>8.1f} MB  {saved_mb:>+8.1f} MB ({saved_pct:>5.1f}%)")
        if m['skipped'] + m['errors'] > 0:
            print(f"  {T['SUMMARY_ROW_SKIP']:<14} {m['skipped'] + m['errors']:>4}")
        if m['moved'] > 0:
            print(f"  {T['SUMMARY_ROW_MOVED']:<14} {m['moved']:>4}   -> ORIGINAL/")
        print("=" * 68)

    def select_folder(self):
        T = self.T
        clear_screen()
        print_banner(T['BANNER_CONFIG'])
        print(T['FOLDER_INTRO'])
        nueva = input_path_with_fallback(T['FOLDER_PROMPT'], allow_dialog=True)
        if nueva:
            self.folder_path = nueva

    def toggle_profile(self):
        keys = list(DEVICE_PROFILES.keys())
        idx = keys.index(self.profile) if self.profile in keys else 0
        self.profile = keys[(idx + 1) % len(keys)]

    def toggle_direction(self):
        self.reading_direction = 'rtl' if self.reading_direction == 'ltr' else 'ltr'

    def show_menu(self):
        T = self.T
        while True:
            clear_screen()
            print_banner(T['BANNER_MENU'])
            print(T['ACTIVE_FOLDER'].format(self.folder_path))

            sim_label = T['SIM_LABEL'] if self.dry_run else ""
            print(T['ACTIONS_HEADER'].format(sim_label))

            p_name = DEVICE_PROFILES.get(self.profile, {}).get('name', self.profile)
            subs_state = T['ON'] if self.include_subfolders else T['OFF']
            split_state = T['ON'] if self.split_double else T['OFF']
            dir_state = T['RTL'] if self.reading_direction == 'rtl' else T['LTR']
            blank_state = T['ON'] if self.remove_blank else T['OFF']

            print(" ╔══════════════════════════════════════════════════════════╗")
            print(f" ║  [ 1 ]  {T['MENU_1'].strip():<48} ║")
            print(f" ║  [ 2 ]  {(T['MENU_2_ON'] if self.dry_run else T['MENU_2_OFF']).strip():<48} ║")
            print(f" ║  [ 3 ]  {T['MENU_3'].strip():<48} ║")
            print(f" ║  [ 4 ]  {T['MENU_4'].format(subs_state).strip():<48} ║")
            print(f" ║  [ 5 ]  {T['MENU_5'].format(p_name)[:48]:<48} ║")
            print(f" ║  [ 6 ]  {T['MENU_6'].format(split_state).strip():<48} ║")
            print(f" ║  [ 7 ]  {T['MENU_7'].format(dir_state)[:48]:<48} ║")
            print(f" ║  [ 8 ]  {T['MENU_8'].format(blank_state).strip():<48} ║")
            print(" ╟──────────────────────────────────────────────────────────╢")
            print(f" ║  [ 0 ]  {T['MENU_0'].strip():<48} ║")
            print(" ╚══════════════════════════════════════════════════════════╝")

            opt = input(T['SELECT_OPTION']).strip()
            if opt == '1':
                self.run_conversion()
                input(T['PRESS_ENTER'])
            elif opt == '2':
                self.dry_run = not self.dry_run
            elif opt == '3':
                self.select_folder()
            elif opt == '4':
                self.include_subfolders = not self.include_subfolders
            elif opt == '5':
                self.toggle_profile()
            elif opt == '6':
                self.split_double = not self.split_double
            elif opt == '7':
                self.toggle_direction()
            elif opt == '8':
                self.remove_blank = not self.remove_blank
            elif opt == '0':
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

def main():
    parser = argparse.ArgumentParser(description="CBZ / CBR to EPUB Fixed-Layout Converter")
    parser.add_argument("-i", "--input", help="Ruta de la carpeta a procesar")
    parser.add_argument("-p", "--profile", choices=list(DEVICE_PROFILES.keys()), default="default", help="Perfil de dispositivo")
    parser.add_argument("--subfolders", action="store_true", help="Incluir subcarpetas")
    parser.add_argument("--split-double", action="store_true", help="Dividir páginas dobles en dos")
    parser.add_argument("--direction", choices=["ltr", "rtl"], default="ltr", help="Dirección de lectura: ltr (occidental) o rtl (manga)")
    parser.add_argument("--remove-blank", action="store_true", default=True, help="Eliminar páginas en blanco o en negro (activado por defecto)")
    parser.add_argument("--no-remove-blank", dest="remove_blank", action="store_false", help="No eliminar páginas en blanco o en negro")
    parser.add_argument("--dry-run", action="store_true", help="Modo simulación (sin escribir archivos)")

    args = parser.parse_args()
    T = TEXTS[get_ui_language()]

    if args.input:
        # Modo CLI desatendido
        app = CBZtoEPUBApp(
            T, folder=args.input, profile=args.profile, dry_run=args.dry_run,
            subfolders=args.subfolders, split_double=args.split_double, reading_dir=args.direction,
            remove_blank=args.remove_blank
        )
        app.run_conversion()
    else:
        app = CBZtoEPUBApp(T)
        app.start()

if __name__ == "__main__":
    main()
