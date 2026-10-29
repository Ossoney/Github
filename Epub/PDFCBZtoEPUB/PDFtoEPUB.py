"""
PDFtoEPUB.py - Conversión inteligente de PDF a EPUB (Reflowable o Fixed-Layout).
Incluye:
 - Menú amigable completo TUI
 - Perfiles de dispositivo configurables
 - División de doble página (Double-page split) con lectura LTR / RTL
 - Registro explícito de Portada (cover-image)
 - Selector de carpetas gráfico (Tkinter) y de consola
 - Modo simulación (Dry-Run) y modo desatendido (CLI)
 - Detección de texto + OCR con Tesseract
 - Traslado seguro a ORIGINAL/
"""

import argparse
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
from typing import Dict, List, Optional, Tuple
from xml.sax.saxutils import escape as xml_escape

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
    import pytesseract
    # Auto-detección de ruta de tesseract en Windows si no está en PATH
    if os.name == 'nt':
        default_tess_paths = [
            r'C:\Program Files\Tesseract-OCR\tesseract.exe',
            r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
            os.path.expandvars(r'%LOCALAPPDATA%\Programs\Tesseract-OCR\tesseract.exe'),
        ]
        for p in default_tess_paths:
            if os.path.exists(p):
                pytesseract.pytesseract.tesseract_cmd = p
                break
    HAS_TESSERACT = True
except ImportError:
    HAS_TESSERACT = False

LANG_MAP_TESSERACT = {
    'es': 'spa', 'spa': 'spa', 'ca': 'cat', 'gl': 'glg',
    'en': 'eng', 'eng': 'eng',
    'fr': 'fra', 'fra': 'fra',
    'de': 'deu', 'deu': 'deu',
    'it': 'ita', 'por': 'por', 'pt': 'por',
}

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

from common import (
    DEVICE_PROFILES,
    clear_screen,
    print_banner,
    select_folder_dialog,
    input_path_with_fallback,
    split_double_page_if_needed,
    is_blank_or_black_page,
    deskew_image_if_needed,
    autocrop_margins,
    preprocess_image_for_ocr,
    clean_ocr_text_stream,
    generate_opf_fxl,
    generate_nav_fxl,
    generate_fxl_page_xhtml,
    generate_opf_reflowable,
    generate_nav_reflowable,
    generate_chapter_xhtml,
    pack_epub,
    MIMETYPE,
    CONTAINER_XML,
    CSS_FXL,
    CSS_REFLOWABLE,
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
        'PROMO_START': "PDFtoEPUB convierte tus archivos PDF (texto, escaneados u OCR) a EPUB navegable.",
        'PROMO_END': "Si el programa te ha sido útil invítame a un café en paypal.me/ossoney.",
        'CONTINUE_PROMPT': "\n¿Deseas continuar (S/N)?: ",
        'GOODBYE': "\nOperación cancelada. ¡Gracias por usar PDFtoEPUB!",
        'BANNER_MENU': "PDF TO EPUB - MENÚ PRINCIPAL",
        'BANNER_CONFIG': "PDF TO EPUB - CONFIGURACIÓN",
        'ACTIVE_FOLDER': "Carpeta activa: {}",
        'SIM_LABEL': " [SIMULACIÓN]",
        'ACTIONS_HEADER': "\nACCIONES DISPONIBLES{}:",
        'MENU_1': "Iniciar Conversión a EPUB",
        'MENU_2_ON': "Desactivar Modo Simulación (Dry-Run)",
        'MENU_2_OFF': "Activar Modo Simulación (Dry-Run)",
        'MENU_3': "Cambiar Carpeta",
        'MENU_4': "Incluir Subcarpetas: {}",
        'MENU_5': "Perfil Dispositivo (Imágenes): {}",
        'MENU_6': "Dividir Páginas Dobles: {}",
        'MENU_7': "Dirección Lectura: {}",
        'MENU_8': "Eliminar Páginas Vacías (B/N): {}",
        'MENU_0': "Salir",
        'SELECT_OPTION': "\nSelecciona una opción: ",
        'INVALID_PATH': "\nError: La ruta seleccionada no es válida.",
        'NO_FILES': "\nNo se encontraron archivos PDF en esta carpeta.",
        'FOUND_FILES': "\n[INFO] Se encontraron {} archivos PDFs. Arrancando motores...",
        'PROCESSING': "\n → Procesando: {}",
        'SKIP_EXISTS': " → [SKIP] Ya existe: {}",
        'SKIP_PROTECTED': " → [SKIP] PDF protegido: {}",
        'DETECTED_TEXT': "   📖 Detectado como PDF de TEXTO ({} caracteres/página)",
        'DETECTED_IMAGE': "   🖼️ Detectado como PDF de IMAGEN ({} caracteres/página)",
        'CHAPTER_FOUND': "   📑 {} capítulos detectados",
        'PAGES_FOUND': "   📄 {} páginas procesadas",
        'BLANK_PAGES_REMOVED': "   🗑️ {} páginas vacías eliminadas (en blanco/negro)",
        'TOC_NATIVE': "   📚 TOC nativo del PDF encontrado ({} entradas)",
        'TOC_HEURISTIC': "   🔍 Sin TOC nativo. Usando detección heurística",
        'PARALLEL_START': "🚀 Iniciando turbo-procesamiento paralelo ({} núcleos)...",
        'OCR_START': "   🔍 OCR: procesando {} páginas con Tesseract...",
        'OCR_VIABLE': "   🔍 OCR viable → convirtiendo a EPUB de texto",
        'OCR_LOW_QUALITY': "   🖼️ OCR: calidad insuficiente → usando modo imagen",
        'OCR_NOT_AVAIL': "   ℹ️ Instala pytesseract+Tesseract para activar OCR",
        'OCR_DONE': "   ✅ OCR completado: {} capítulos detectados",
        'SAVED_OK': " → [OK] Guardado: {} ({:.1f} MB)",
        'MOVED_OK': " → [OK] Original trasladado a: ORIGINAL/{}",
        'PROC_ERROR': " → [ERROR] Falló: {} → {}",
        'SUCCESS_ALL': "\n → [COMPLETADO] Conversión terminada.",
        'FOLDER_INTRO': "Selecciona la carpeta donde guardas tus PDFs ('g' para diálogo gráfico):",
        'FOLDER_PROMPT': "Ruta ('g' para diálogo, Enter para usar la actual): ",
        'PRESS_ENTER': "\nPresiona ENTER para volver al menú...",
        'UNKNOWN_CMD': "Comando no reconocido. Presiona ENTER para continuar...",
        'EXIT_MSG': "\n¡Desconectando sistemas! Hasta luego.",
        'ON': 'SÍ',
        'OFF': 'NO',
        'LTR': 'Occidental (Izq. a Der.)',
        'RTL': 'Manga (Der. a Izq.)',
    },
    'en': {
        'PROMO_START': "PDFtoEPUB converts your PDF files (text, scanned or OCR) into navigable EPUBs.",
        'PROMO_END': "If the program was useful, buy me a coffee at paypal.me/ossoney.",
        'CONTINUE_PROMPT': "\nDo you want to continue (Y/N)?: ",
        'GOODBYE': "\nOperation cancelled. Thank you for using PDFtoEPUB!",
        'BANNER_MENU': "PDF TO EPUB - MAIN MENU",
        'BANNER_CONFIG': "PDF TO EPUB - CONFIGURATION",
        'ACTIVE_FOLDER': "Active folder: {}",
        'SIM_LABEL': " [SIMULATION]",
        'ACTIONS_HEADER': "\nAVAILABLE ACTIONS{}:",
        'MENU_1': "Start Conversion to EPUB",
        'MENU_2_ON': "Disable Simulation Mode (Dry-Run)",
        'MENU_2_OFF': "Enable Simulation Mode (Dry-Run)",
        'MENU_3': "Change Folder",
        'MENU_4': "Include Subfolders: {}",
        'MENU_5': "Device Profile (Images): {}",
        'MENU_6': "Split Double Pages: {}",
        'MENU_7': "Reading Direction: {}",
        'MENU_8': "Remove Blank Pages (B/W): {}",
        'MENU_0': "Exit",
        'SELECT_OPTION': "\nSelect an option: ",
        'INVALID_PATH': "\nError: The selected path is not valid.",
        'NO_FILES': "\nNo PDF files found in this folder.",
        'FOUND_FILES': "\n[INFO] Found {} PDF files. Starting engines...",
        'PROCESSING': "\n → Processing: {}",
        'SKIP_EXISTS': " → [SKIP] Already exists: {}",
        'SKIP_PROTECTED': " → [SKIP] Protected PDF: {}",
        'DETECTED_TEXT': "   📖 Detected as TEXT PDF ({} chars/page)",
        'DETECTED_IMAGE': "   🖼️ Detected as IMAGE PDF ({} chars/page)",
        'CHAPTER_FOUND': "   📑 {} chapters detected",
        'PAGES_FOUND': "   📄 {} pages processed",
        'BLANK_PAGES_REMOVED': "   🗑️ {} blank/black empty pages removed",
        'TOC_NATIVE': "   📚 Native PDF TOC found ({} entries)",
        'TOC_HEURISTIC': "   🔍 No native TOC. Using heuristic detection",
        'PARALLEL_START': "🚀 Starting parallel processing ({} cores)...",
        'OCR_START': "   🔍 OCR: processing {} pages with Tesseract...",
        'OCR_VIABLE': "   🔍 OCR viable → converting to text EPUB",
        'OCR_LOW_QUALITY': "   🖼️ OCR: insufficient quality → using image mode",
        'OCR_NOT_AVAIL': "   ℹ️ Install pytesseract+Tesseract for OCR",
        'OCR_DONE': "   ✅ OCR done: {} chapters detected",
        'SAVED_OK': " → [OK] Saved: {} ({:.1f} MB)",
        'MOVED_OK': " → [OK] Original moved to: ORIGINAL/{}",
        'PROC_ERROR': " → [ERROR] Failed: {} → {}",
        'SUCCESS_ALL': "\n → [COMPLETE] Conversion finished.",
        'FOLDER_INTRO': "Select the folder where your PDFs are stored ('g' for GUI dialog):",
        'FOLDER_PROMPT': "Folder path ('g' for GUI dialog, Enter for current): ",
        'PRESS_ENTER': "\nPress ENTER to return to menu...",
        'UNKNOWN_CMD': "Unrecognized command. Press ENTER to continue...",
        'EXIT_MSG': "\nShutting down systems! Goodbye.",
        'ON': 'YES',
        'OFF': 'NO',
        'LTR': 'Western (Left-to-Right)',
        'RTL': 'Manga (Right-to-Left)',
    }
}

# =========================================================
# DETECCIÓN DE CONTENIDO Y ESTRUCTURA
# =========================================================
def detect_pdf_type(doc: fitz.Document):
    total_chars, has_full_page_images = 0, 0
    pages_to_check = min(len(doc), 10)
    for i in range(pages_to_check):
        page = doc.load_page(i)
        total_chars += len(page.get_text("text").strip())
        img_info = page.get_image_info()
        if img_info and any(img['width'] > 500 and img['height'] > 700 for img in img_info):
            has_full_page_images += 1
    avg_chars = total_chars / max(1, pages_to_check)
    if avg_chars > 300 and has_full_page_images < (pages_to_check * 0.7):
        return 'text', int(avg_chars)
    return 'image', int(avg_chars)

def _pdf_lang_to_tesseract(pdf_lang: str) -> str:
    if not pdf_lang: return 'spa'
    code = pdf_lang.strip().lower()[:3]
    return LANG_MAP_TESSERACT.get(code, LANG_MAP_TESSERACT.get(code[:2], 'spa'))

def _get_body_font_size(doc: fitz.Document) -> float:
    font_sizes = []
    for page_num in range(min(5, len(doc))):
        page = doc.load_page(page_num)
        blocks = page.get_text("dict", flags=fitz.TEXT_DEHYPHENATE).get("blocks", [])
        for b in blocks:
            if b.get("type") == 0:
                for line in b.get("lines", []):
                    for span in line.get("spans", []):
                        if len(span.get("text", "").strip()) > 3:
                            font_sizes.append(round(span.get("size", 12), 1))
    return statistics.mode(font_sizes) if font_sizes else 11.0

def detect_chapters_from_pdf(doc: fitz.Document, T: dict, pdf_path_str: str) -> List[Dict]:
    toc = doc.get_toc()
    if toc:
        print(T['TOC_NATIVE'].format(len(toc)))
        chapters = []
        for i, item in enumerate(toc):
            lvl, title, start_page = item
            end_page = toc[i+1][2] - 1 if i + 1 < len(toc) else len(doc)
            content = []
            for p_num in range(start_page - 1, min(end_page, len(doc))):
                text = doc.load_page(p_num).get_text("text").strip()
                if text:
                    for para in text.split('\n\n'):
                        if para.strip(): content.append(f"<p>{xml_escape(para.strip())}</p>")
            chapters.append({'title': title.strip(), 'content_html': content})
        return chapters

    print(T['TOC_HEURISTIC'])
    body_size = _get_body_font_size(doc)
    threshold = body_size * 1.25
    chapters, current_html, current_title = [], [], None

    for p_num in range(len(doc)):
        page = doc.load_page(p_num)
        blocks = page.get_text("dict", flags=fitz.TEXT_DEHYPHENATE).get("blocks", [])
        for b in blocks:
            if b.get("type") == 0:
                for line in b.get("lines", []):
                    line_text = "".join([s.get("text", "") for s in line.get("spans", [])]).strip()
                    if not line_text: continue
                    is_title = any(s.get("size", 0) >= threshold for s in line.get("spans", []))
                    if is_title and len(line_text) < 80:
                        if current_html:
                            chapters.append({'title': current_title or f"Capítulo {len(chapters)+1}", 'content_html': current_html})
                        current_html, current_title = [], line_text
                    else:
                        spans_html = []
                        for s in line.get("spans", []):
                            txt = xml_escape(s.get("text", ""))
                            flags = s.get("flags", 0)
                            if flags & 2: txt = f"<em>{txt}</em>"
                            if flags & 16: txt = f"<strong>{txt}</strong>"
                            spans_html.append(txt)
                        current_html.append(f"<p>{''.join(spans_html)}</p>")

    if current_html:
        chapters.append({'title': current_title or f"Capítulo {len(chapters)+1}", 'content_html': current_html})
    if not chapters:
        chapters.append({'title': "Inicio", 'content_html': ["<p>Documento sin estructura de texto clara.</p>"]})
    return chapters

def _test_ocr_quality(pdf_path: str, lang: str) -> bool:
    try:
        doc = fitz.open(pdf_path)
        pix = doc.load_page(0).get_pixmap(matrix=fitz.Matrix(2, 2))
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        doc.close()
        processed_img = preprocess_image_for_ocr(img)
        text = pytesseract.image_to_string(processed_img, lang=lang).strip()
        return len(text) >= 120
    except Exception:
        return False

def _ocr_page_worker(args):
    pdf_path, page_num, lang = args
    try:
        doc = fitz.open(pdf_path)
        pix = doc.load_page(page_num).get_pixmap(matrix=fitz.Matrix(2, 2))
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        doc.close()
        # Preprocesar imagen escaneada: deskew + binarización adaptativa
        processed_img = preprocess_image_for_ocr(img)
        raw_text = pytesseract.image_to_string(processed_img, lang=lang).strip()
        # Limpieza NLP: quitar cabeceras/pies, de-hyphenation, párrafos continuos
        cleaned_text = clean_ocr_text_stream(raw_text)
        return page_num, cleaned_text
    except Exception:
        return page_num, ""

def _split_ocr_text_into_chapters(pages_text):
    chapters, current_html, current_title = [], [], None
    for _, text in pages_text:
        if not text:
            continue
        for para in text.split('\n\n'):
            clean = para.strip()
            if len(clean) > 3:
                # Título de capítulo en mayúsculas o con encabezado claro
                if (clean == clean.upper() and len(clean) < 60) or re.match(r'^(cap[ií]tulo\s+\w+|capítulo\s+\d+|libro\s+\w+)', clean, re.IGNORECASE):
                    if current_html:
                        chapters.append({'title': current_title or f"Capítulo {len(chapters)+1}", 'content_html': current_html})
                    current_html, current_title = [], clean
                else:
                    current_html.append(f'<p>{xml_escape(clean)}</p>')
    if current_html:
        chapters.append({'title': current_title or f"Capítulo {len(chapters)+1}", 'content_html': current_html})
    if not chapters:
        chapters.append({'title': "Inicio", 'content_html': ["<p>Documento sin estructura clara.</p>"]})
    return chapters

def convert_pdf_text_to_epub(pdf_path: Path, epub_path: Path, T: dict) -> bool:
    try:
        doc = fitz.open(pdf_path)
        meta = doc.metadata or {}
        title = meta.get('title') or pdf_path.stem
        author = meta.get('author') or 'Unknown'
        lang = meta.get('language') or 'es'
        chapters = detect_chapters_from_pdf(doc, T, str(pdf_path))
        print(T['CHAPTER_FOUND'].format(len(chapters)))

        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            (base / 'META-INF').mkdir()
            (base / 'OEBPS' / 'images').mkdir(parents=True)
            (base / 'mimetype').write_text(MIMETYPE)
            (base / 'META-INF' / 'container.xml').write_text(CONTAINER_XML)
            (base / 'OEBPS' / 'estilos.css').write_text(CSS_REFLOWABLE)

            manifest, spine = [], []
            for i, ch in enumerate(chapters):
                href = f"chapter_{i+1:03d}.xhtml"
                (base / 'OEBPS' / href).write_text(generate_chapter_xhtml(ch['title'], ch['content_html']))
                manifest.append(f'<item id="ch_{i}" href="{href}" media-type="application/xhtml+xml"/>')
                spine.append(f'<itemref idref="ch_{i}"/>')

            manifest.append('<item id="css" href="estilos.css" media-type="text/css"/>')
            manifest.append('<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>')

            (base / 'OEBPS' / 'content.opf').write_text(generate_opf_reflowable(title, author, f"id-{time.time()}", manifest, spine, lang))
            (base / 'OEBPS' / 'nav.xhtml').write_text(generate_nav_reflowable(title, chapters))
            pack_epub(base, epub_path)
        doc.close()
        return True
    except Exception as e:
        print(T['PROC_ERROR'].format(pdf_path.name, e))
        return False

def _process_page_worker(args):
    pdf_path, page_num, profile_key, split_double, reading_dir, remove_blank, is_protected = args
    try:
        doc = fitz.open(pdf_path)
        pix = doc.load_page(page_num).get_pixmap(matrix=fitz.Matrix(2, 2))
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        doc.close()

        # Si se solicita eliminar páginas vacías y no es la portada
        if remove_blank and not is_protected and is_blank_or_black_page(img):
            return page_num, [], True  # page_num, byte_list, is_blank

        # Enderezado (deskew) y autocrop de márgenes para escaneos (no portada)
        if not is_protected:
            img = deskew_image_if_needed(img)
            img = autocrop_margins(img)

        sub_images = [img]
        if split_double:
            sub_images = split_double_page_if_needed(img, reading_direction=reading_dir)

        conf = DEVICE_PROFILES.get(profile_key, DEVICE_PROFILES['default'])
        max_w = conf['max_width']
        max_h = conf['max_height']

        byte_list = []
        for s_img in sub_images:
            # Comprobar sub-imagen individual si se dividió página doble
            if remove_blank and not is_protected and len(sub_images) > 1 and is_blank_or_black_page(s_img):
                continue

            if not is_protected and len(sub_images) > 1:
                s_img = autocrop_margins(s_img)

            if s_img.width > max_w or s_img.height > max_h:
                r = min(max_w / s_img.width, max_h / s_img.height)
                s_img = s_img.resize((int(s_img.width * r), int(s_img.height * r)), Image.Resampling.LANCZOS)

            if HAS_NUMPY:
                diff = np.mean(np.abs(np.array(s_img)[:,:,0].astype(int) - np.array(s_img)[:,:,1].astype(int)))
                if diff < 5: s_img = s_img.convert('L')

            buf = io.BytesIO()
            s_img.save(buf, "JPEG", quality=conf.get('quality', 75), optimize=True)
            byte_list.append(buf.getvalue())

        return page_num, byte_list, False
    except Exception:
        return page_num, [], False

def convert_pdf_image_to_epub(pdf_path: Path, epub_path: Path, T: dict,
                              profile_key: str = 'default',
                              split_double: bool = False,
                              reading_direction: str = 'ltr',
                              remove_blank: bool = True) -> bool:
    try:
        doc = fitz.open(pdf_path)
        npages = len(doc)
        doc.close()

        conf = DEVICE_PROFILES.get(profile_key, DEVICE_PROFILES['default'])
        vp_width, vp_height = conf['max_width'], conf['max_height']

        print(T['PARALLEL_START'].format(os.cpu_count()))
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            (base / 'META-INF').mkdir()
            (base / 'OEBPS' / 'images').mkdir(parents=True)
            (base / 'mimetype').write_text(MIMETYPE)
            (base / 'META-INF' / 'container.xml').write_text(CONTAINER_XML)
            (base / 'OEBPS' / 'estilos.css').write_text(CSS_FXL)

            args = [
                (str(pdf_path), i, profile_key, split_double, reading_direction, remove_blank, (i == 0))
                for i in range(npages)
            ]
            workers = max(2, min(os.cpu_count() or 4, 8))
            with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
                results = sorted(executor.map(_process_page_worker, args), key=lambda x: x[0])

            pages_meta = []
            curr_idx = 1
            blank_count = 0
            for page_num, byte_list, was_blank in results:
                if was_blank:
                    blank_count += 1
                for b in byte_list:
                    img_name = f"page_{curr_idx:04d}.jpg"
                    (base / 'OEBPS' / 'images' / img_name).write_bytes(b)
                    page_href = f"page_{curr_idx:04d}.xhtml"
                    (base / 'OEBPS' / page_href).write_text(generate_fxl_page_xhtml(img_name, vp_width, vp_height))
                    pages_meta.append({
                        'page_id': f"p_{curr_idx}",
                        'page_href': page_href,
                        'img_id': f"img_{curr_idx:04d}",
                        'img_href': f"images/{img_name}",
                        'label': f"Page {curr_idx}"
                    })
                    curr_idx += 1

            if blank_count > 0:
                print(T['BLANK_PAGES_REMOVED'].format(blank_count))

            opf = generate_opf_fxl(
                pdf_path.stem, f"id-{time.time()}", pages_meta, vp_width, vp_height,
                reading_direction=reading_direction
            )
            (base / 'OEBPS' / 'content.opf').write_text(opf)
            (base / 'OEBPS' / 'nav.xhtml').write_text(generate_nav_fxl(pages_meta))
            pack_epub(base, epub_path)
            print(T['PAGES_FOUND'].format(len(pages_meta)))
        return True
    except Exception as e:
        print(T['PROC_ERROR'].format(pdf_path.name, e))
        return False

# =========================================================
# APLICACIÓN INTERACTIVA
# =========================================================
class PDFtoEPUBApp:
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

    def scan_files(self) -> List[Path]:
        path = Path(self.folder_path)
        if self.include_subfolders:
            return sorted(path.rglob('*.pdf'))
        return sorted(path.glob('*.pdf'))

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

    def run_conversion(self):
        T = self.T
        path = Path(self.folder_path)
        if not path.is_dir():
            print(T['INVALID_PATH'])
            return

        pdfs = self.scan_files()
        if not pdfs:
            print(T['NO_FILES'])
            return

        print(T['FOUND_FILES'].format(len(pdfs)))

        for file_path in pdfs:
            epub_path = file_path.with_suffix('.epub')
            if epub_path.exists():
                print(T['SKIP_EXISTS'].format(epub_path.name))
                continue

            if self.dry_run:
                orig_size = file_path.stat().st_size
                print(f"[SIMULACIÓN] {file_path.name}")
                print(f"    ↳ Acción: PDF → EPUB")
                print(f"    ↳ Perfil: {DEVICE_PROFILES.get(self.profile, {}).get('name')}")
                print(f"    ↳ Dobles: {T['ON'] if self.split_double else T['OFF']} | Dirección: {self.reading_direction.upper()}")
                print(f"    ↳ Tamaño actual: {orig_size/(1024*1024):.1f}MB")
                try: rel = file_path.relative_to(self.folder_path)
                except Exception: rel = Path(file_path.name)
                print(f"    ↳ Traslado: ORIGINAL/{rel}")
                continue

            print(T['PROCESSING'].format(file_path.name))
            inicio = time.time()

            doc = fitz.open(file_path)
            pdf_type, avg_chars = detect_pdf_type(doc)
            lang = _pdf_lang_to_tesseract((doc.metadata or {}).get('language', 'es')) if HAS_TESSERACT else 'spa'
            doc.close()

            success = False
            if pdf_type == 'text':
                print(T['DETECTED_TEXT'].format(avg_chars))
                success = convert_pdf_text_to_epub(file_path, epub_path, T)
            else:
                print(T['DETECTED_IMAGE'].format(avg_chars))
                if HAS_TESSERACT and _test_ocr_quality(str(file_path), lang):
                    print(T['OCR_VIABLE'])
                    print(T['OCR_START'].format(len(fitz.open(file_path))))

                    args = [(str(file_path), i, lang) for i in range(len(fitz.open(file_path)))]
                    with concurrent.futures.ProcessPoolExecutor() as executor:
                        ocr_res = sorted(executor.map(_ocr_page_worker, args), key=lambda x: x[0])

                    chapters = _split_ocr_text_into_chapters(ocr_res)
                    print(T['OCR_DONE'].format(len(chapters)))

                    with tempfile.TemporaryDirectory() as tmp:
                        base = Path(tmp)
                        (base / 'META-INF').mkdir()
                        (base / 'OEBPS').mkdir()
                        (base / 'mimetype').write_text(MIMETYPE)
                        (base / 'META-INF' / 'container.xml').write_text(CONTAINER_XML)
                        (base / 'OEBPS' / 'estilos.css').write_text(CSS_REFLOWABLE)

                        manifest, spine = [], []
                        for i, ch in enumerate(chapters):
                            href = f"chapter_{i+1:03d}.xhtml"
                            (base / 'OEBPS' / href).write_text(generate_chapter_xhtml(ch['title'], ch['content_html']))
                            manifest.append(f'<item id="ch_{i}" href="{href}" media-type="application/xhtml+xml"/>')
                            spine.append(f'<itemref idref="ch_{i}"/>')

                        manifest.append('<item id="css" href="estilos.css" media-type="text/css"/>')
                        manifest.append('<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>')

                        (base / 'OEBPS' / 'content.opf').write_text(generate_opf_reflowable(file_path.stem, "Unknown", f"id-{time.time()}", manifest, spine, "es"))
                        (base / 'OEBPS' / 'nav.xhtml').write_text(generate_nav_reflowable(file_path.stem, chapters))
                        pack_epub(base, epub_path)
                    success = True
                else:
                    if HAS_TESSERACT: print(T['OCR_LOW_QUALITY'])
                    else: print(T['OCR_NOT_AVAIL'])
                    success = convert_pdf_image_to_epub(
                        file_path, epub_path, T,
                        profile_key=self.profile,
                        split_double=self.split_double,
                        reading_direction=self.reading_direction,
                        remove_blank=self.remove_blank
                    )

            if success and epub_path.exists():
                print(T['SAVED_OK'].format(epub_path.name, epub_path.stat().st_size/(1024*1024)))
                print(f"   ⏱️  {time.time()-inicio:.1f}s")
                try:
                    base_path = Path(self.folder_path)
                    try: rel = file_path.relative_to(base_path)
                    except ValueError: rel = Path(file_path.name)
                    dest = base_path / 'ORIGINAL' / rel
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(file_path), str(dest))
                    print(T['MOVED_OK'].format(rel))
                except Exception as e:
                    print(f"   ⚠️ Error al mover: {e}")

        print(T['SUCCESS_ALL'])

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
            if input(T['CONTINUE_PROMPT']).strip().upper() not in ('S', 'Y'):
                print(T['GOODBYE'])
                return
            self.select_folder()
            self.show_menu()
        except KeyboardInterrupt:
            print("\n\n(x) Salida forzada.")
            sys.exit(0)

def main():
    parser = argparse.ArgumentParser(description="PDF to EPUB Converter")
    parser.add_argument("-i", "--input", help="Ruta de la carpeta a procesar")
    parser.add_argument("-p", "--profile", choices=list(DEVICE_PROFILES.keys()), default="default", help="Perfil de dispositivo")
    parser.add_argument("--subfolders", action="store_true", help="Incluir subcarpetas")
    parser.add_argument("--split-double", action="store_true", help="Dividir páginas dobles en dos")
    parser.add_argument("--direction", choices=["ltr", "rtl"], default="ltr", help="Dirección de lectura: ltr o rtl")
    parser.add_argument("--remove-blank", action="store_true", default=True, help="Eliminar páginas en blanco o en negro (activado por defecto)")
    parser.add_argument("--no-remove-blank", dest="remove_blank", action="store_false", help="No eliminar páginas en blanco o en negro")
    parser.add_argument("--dry-run", action="store_true", help="Modo simulación")

    args = parser.parse_args()
    T = TEXTS[get_ui_language()]

    if args.input:
        app = PDFtoEPUBApp(
            T, folder=args.input, profile=args.profile, dry_run=args.dry_run,
            subfolders=args.subfolders, split_double=args.split_double, reading_dir=args.direction,
            remove_blank=args.remove_blank
        )
        app.run_conversion()
    else:
        app = PDFtoEPUBApp(T)
        app.start()

if __name__ == "__main__":
    main()
