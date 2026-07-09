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
import sys
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
import tempfile
import time
import unicodedata
import zipfile
import statistics
from pathlib import Path
from typing import Dict, List, Tuple, Optional
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

DOCUMENTS_DIR = Path.home() / "Documents" / "Epubbiblio"
DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)
LOG_PATH = DOCUMENTS_DIR / 'pdftoepub.log'

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
        'ACTIVE_FOLDER': "Carpeta activa: {}",
        'SIM_LABEL': " [SIMULACIÓN]",
        'ACTIONS_HEADER': "\nACCIONES DISPONIBLES{}:",
        'MENU_1': "Iniciar Conversión a EPUB",
        'MENU_2_ON': "Desactivar Modo Simulación (Dry-Run)",
        'MENU_2_OFF': "Activar Modo Simulación (Dry-Run)",
        'MENU_3': "Cambiar Carpeta",
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
        'SUMMARY_TITLE': "RESUMEN DE CONVERSIÓN",
    },
    'en': {
        'PROMO_START': "PDFtoEPUB converts your PDF files (text, scanned or OCR) into navigable EPUBs.",
        'PROMO_END': "If the program was useful, buy me a coffee at paypal.me/ossoney.",
        'CONTINUE_PROMPT': "\nDo you want to continue (Y/N)?: ",
        'GOODBYE': "\nOperation cancelled. Thank you for using PDFtoEPUB!",
        'BANNER_MENU': "PDF TO EPUB - MAIN MENU",
        'ACTIVE_FOLDER': "Active folder: {}",
        'SIM_LABEL': " [SIMULATION]",
        'ACTIONS_HEADER': "\nAVAILABLE ACTIONS{}:",
        'MENU_1': "Start Conversion to EPUB",
        'MENU_2_ON': "Disable Simulation Mode (Dry-Run)",
        'MENU_2_OFF': "Enable Simulation Mode (Dry-Run)",
        'MENU_3': "Change Folder",
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
        'SUMMARY_TITLE': "CONVERSION SUMMARY",
    }
}

def clear_screen(): os.system('cls' if os.name == 'nt' else 'clear')

MIMETYPE = "application/epub+zip"
CONTAINER_XML = '<?xml version="1.0" encoding="UTF-8"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles></container>'

CSS_REFLOWABLE = """
@page { margin: 1cm; }
html { background-color: #1e1e1e; }
body { margin: 0; padding: 5% 8%; font-family: "Segoe UI", sans-serif; font-size: 1.15em; line-height: 1.6; color: #e0e0e0; background-color: #1e1e1e; text-align: justify; }
h1, h2, h3 { color: #ffffff; text-align: center; margin-top: 1.5em; border-bottom: 1px solid #333; padding-bottom: 0.3em; }
p { text-indent: 1.5em; margin: 0.5em 0; }
strong { font-weight: bold; } em { font-style: italic; }
.img-container { text-align: center; margin: 2em 0; }
.img-container img { max-width: 100%; height: auto; border-radius: 8px; }
"""

CSS_FXL = """
html, body { margin: 0; padding: 0; width: 100%; height: 100%; background-color: #000000; }
.fxl-page { display: flex; justify-content: center; align-items: center; width: 100%; height: 100%; }
img { max-width: 100%; max-height: 100%; object-fit: contain; }
"""

def generate_opf_reflowable(title, author, uid, manifest_items, spine_items, language='es'):
    return f'<?xml version="1.0" encoding="UTF-8"?><package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="uid"><metadata xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:identifier id="uid">{xml_escape(uid)}</dc:identifier><dc:title>{xml_escape(title)}</dc:title><dc:creator>{xml_escape(author)}</dc:creator><dc:language>{xml_escape(language)}</dc:language></metadata><manifest>{"".join(manifest_items)}</manifest><spine>{"".join(spine_items)}</spine></package>'

def generate_opf_fxl(title, uid, pages, width, height, author='', language='es'):
    manifest = ['<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>', '<item id="css" href="estilos.css" media-type="text/css"/>']
    spine = []
    for p in pages:
        manifest.append(f'<item id="{p["page_id"]}" href="{p["page_href"]}" media-type="application/xhtml+xml"/>')
        mtype = "image/png" if p["img_href"].lower().endswith('.png') else "image/jpeg"
        manifest.append(f'<item id="{p["img_id"]}" href="{p["img_href"]}" media-type="{mtype}"/>')
        spine.append(f'<itemref idref="{p["page_id"]}"/>')
    author_tag = f"<dc:creator>{xml_escape(author)}</dc:creator>" if author else ""
    return f'<?xml version="1.0" encoding="UTF-8"?><package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="uid"><metadata xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:identifier id="uid">{xml_escape(uid)}</dc:identifier><dc:title>{xml_escape(title)}</dc:title>{author_tag}<dc:language>{xml_escape(language)}</dc:language><meta property="rendition:layout">pre-paginated</meta><meta name="viewport" content="width={width}, height={height}"/></metadata><manifest>{"".join(manifest)}</manifest><spine>{"".join(spine)}</spine></package>'

def generate_nav_reflowable(title, chapters):
    lis = "".join([f'<li><a href="chapter_{i+1:03d}.xhtml">{xml_escape(ch["title"])}</a></li>' for i, ch in enumerate(chapters)])
    return f'<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE html><html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops"><head><title>Navigation</title></head><body><nav epub:type="toc" id="toc"><h1>{xml_escape(title)}</h1><ol>{lis}</ol></nav></body></html>'

def generate_nav_fxl(pages):
    lis = "".join([f'<li><a href="{p["page_href"]}">{xml_escape(p["label"])}</a></li>' for p in pages])
    return f'<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE html><html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops"><head><title>Navigation</title></head><body><nav epub:type="toc" id="toc"><h1>Contents</h1><ol>{lis}</ol></nav></body></html>'

def generate_chapter_xhtml(title, content_html):
    body = "".join(content_html)
    return f'<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE html><html xmlns="http://www.w3.org/1999/xhtml"><head><title>{xml_escape(title)}</title><link rel="stylesheet" type="text/css" href="estilos.css"/></head><body><h1>{xml_escape(title)}</h1>{body}</body></html>'

def generate_fxl_page_xhtml(img_filename, width, height):
    return f'<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE html><html xmlns="http://www.w3.org/1999/xhtml"><head><title>Page</title><meta name="viewport" content="width={width}, height={height}"/><link rel="stylesheet" type="text/css" href="estilos.css"/></head><body style="margin:0;padding:0;"><div class="fxl-page"><img src="images/{img_filename}" alt="page" style="width:100%;height:100%;"/></div></body></html>'

def pack_epub(source_dir: Path, epub_path: Path):
    with zipfile.ZipFile(epub_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        mimetype_path = source_dir / 'mimetype'
        if mimetype_path.exists(): zf.write(mimetype_path, 'mimetype', compress_type=zipfile.ZIP_STORED)
        for root, dirs, files in os.walk(source_dir):
            for fname in sorted(files):
                if fname == 'mimetype' and Path(root) == source_dir: continue
                full = Path(root) / fname
                zf.write(full, full.relative_to(source_dir).as_posix())

def detect_pdf_type(doc: fitz.Document):
    total_chars, has_full_page_images = 0, 0
    pages_to_check = min(len(doc), 10)
    for i in range(pages_to_check):
        page = doc.load_page(i)
        total_chars += len(page.get_text("text").strip())
        img_info = page.get_image_info()
        page_area = page.rect.width * page.rect.height
        for info in img_info:
            bbox = info['bbox']
            if (bbox[2] - bbox[0]) * (bbox[3] - bbox[1]) > page_area * 0.7:
                has_full_page_images += 1
                break
    avg = total_chars // max(pages_to_check, 1)
    return ('image', avg) if has_full_page_images > (pages_to_check / 2) else ('text', avg)

def _detect_body_font_size(doc: fitz.Document):
    all_sizes = []
    for i in range(min(len(doc), 5)):
        for block in doc.load_page(i).get_text("dict").get("blocks", []):
            if block.get("type") == 0:
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        if len(span.get("text", "").strip()) > 10: all_sizes.append(span.get("size", 12.0))
    return statistics.median(all_sizes) if all_sizes else 12.0

def clean_text_for_epub(text: str):
    return "".join(ch for ch in unicodedata.normalize('NFKC', text) if unicodedata.category(ch)[0] != 'C' or ch in "\n\r\t")

def _extract_rich_text_from_page(page, body_size, image_map=None):
    blocks = page.get_text("dict", flags=fitz.TEXT_PRESERVE_WHITESPACE).get("blocks", [])
    elements = []
    for block in blocks:
        if block.get("type") == 1 and image_map and block.get("xref") in image_map:
            elements.append(f'<div class="img-container"><img src="images/{image_map[block.get("xref")]}" alt="Image"/></div>')
            continue
        if block.get("type") != 0: continue
        current_p_lines = []
        for line in block.get("lines", []):
            line_html = ""
            for span in line.get("spans", []):
                text = clean_text_for_epub(span.get("text", ""))
                if not text.strip(): line_html += " "; continue
                flags = span.get("flags", 0)
                escaped = xml_escape(text)
                is_bold = bool(flags & (1 << 4))
                is_italic = bool(flags & (1 << 1))
                if is_bold and is_italic: escaped = f"<strong><em>{escaped}</em></strong>"
                elif is_bold: escaped = f"<strong>{escaped}</strong>"
                elif is_italic: escaped = f"<em>{escaped}</em>"
                line_html += escaped
            if line_html.strip(): current_p_lines.append(line_html.strip())
        if current_p_lines:
            full = " ".join(current_p_lines).strip()
            if len(full) > 3 and not re.match(r'^[-—=._\s]{3,}$', full):
                elements.append(f"<p>{full}</p>")
    return elements

def _extract_page_text_worker(args):
    pdf_path, page_num, body_size = args
    try:
        doc = fitz.open(pdf_path)
        page = doc.load_page(page_num)
        elements = _extract_rich_text_from_page(page, body_size)
        doc.close()
        return page_num, elements
    except Exception: return page_num, []

def detect_chapters_from_pdf(doc, T, pdf_path):
    body_size = _detect_body_font_size(doc)
    toc = doc.get_toc()
    
    if toc:
        main = [(t, p) for l, t, p in toc if l <= 2]
        if len(main) >= 3:
            print(T['TOC_NATIVE'].format(len(main)))
            chapters = []
            for i, (title, start_page) in enumerate(main):
                end_page = main[i + 1][1] if i + 1 < len(main) else len(doc) + 1
                content_html = []
                for pg in range(start_page - 1, min(end_page - 1, len(doc))):
                    content_html.extend(_extract_rich_text_from_page(doc.load_page(pg), body_size))
                if content_html: chapters.append({'title': title.strip(), 'content_html': content_html})
            if chapters: return chapters

    print(T['TOC_HEURISTIC'])
    args = [(pdf_path, i, body_size) for i in range(len(doc))]
    with concurrent.futures.ThreadPoolExecutor(max_workers=max(2, min(os.cpu_count() or 4, 8))) as executor:
        results = sorted(executor.map(_extract_page_text_worker, args), key=lambda x: x[0])
    
    chapters, current_html, current_title = [], [], None
    chapter_patterns = [re.compile(r'^(CH\d+|cap[ií]tulo|chapter|parte)\b', re.IGNORECASE)]
    
    for _, elements in results:
        for el in elements:
            stripped = re.sub(r'<[^>]+>', '', el).strip()
            is_header = any(p.match(stripped) for p in chapter_patterns) or (stripped == stripped.upper() and len(stripped) > 3 and len(stripped) < 50)
            if is_header and current_html:
                chapters.append({'title': current_title or f"Sección {len(chapters)+1}", 'content_html': current_html})
                current_html, current_title = [], stripped
            elif is_header:
                current_title = stripped
            current_html.append(el)
    if current_html: chapters.append({'title': current_title or f"Sección {len(chapters)+1}", 'content_html': current_html})
    return chapters if chapters else [{'title': 'Contenido', 'content_html': [el for _, els in results for el in els]}]

def _test_ocr_quality(pdf_path, lang):
    try:
        doc = fitz.open(pdf_path)
        pix = doc.load_page(0).get_pixmap(matrix=fitz.Matrix(2, 2))
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        doc.close()
        return len(pytesseract.image_to_string(img, lang=lang).strip()) >= 150
    except: return False

def _ocr_page_worker(args):
    pdf_path, page_num, lang = args
    try:
        doc = fitz.open(pdf_path)
        pix = doc.load_page(page_num).get_pixmap(matrix=fitz.Matrix(2, 2))
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        doc.close()
        return page_num, pytesseract.image_to_string(img, lang=lang).strip()
    except: return page_num, ""

def _split_ocr_text_into_chapters(pages_text):
    chapters, current_html, current_title = [], [], None
    for _, text in pages_text:
        for para in re.split(r'\n{2,}|\x0c', text):
            clean = ' '.join(para.split())
            if len(clean) > 3:
                if clean == clean.upper() and len(clean) < 60:
                    if current_html: chapters.append({'title': current_title or f"Capítulo {len(chapters)+1}", 'content_html': current_html})
                    current_html, current_title = [], clean
                else:
                    current_html.append(f'<p>{xml_escape(clean)}</p>')
    if current_html: chapters.append({'title': current_title or f"Capítulo {len(chapters)+1}", 'content_html': current_html})
    return chapters

def convert_pdf_text_to_epub(pdf_path: Path, epub_path: Path, T: dict):
    try:
        doc = fitz.open(pdf_path)
        meta = doc.metadata or {}
        title, author, lang = meta.get('title') or pdf_path.stem, meta.get('author') or 'Unknown', meta.get('language') or 'es'
        chapters = detect_chapters_from_pdf(doc, T, str(pdf_path))
        print(T['CHAPTER_FOUND'].format(len(chapters)))
        
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            (base / 'META-INF').mkdir(); (base / 'OEBPS' / 'images').mkdir(parents=True)
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
    pdf_path, page_num = args
    try:
        doc = fitz.open(pdf_path)
        pix = doc.load_page(page_num).get_pixmap(matrix=fitz.Matrix(2, 2))
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        
        if HAS_NUMPY:
            diff = np.mean(np.abs(np.array(img)[:,:,0].astype(int) - np.array(img)[:,:,1].astype(int)))
            if diff < 5: img = img.convert('L')
            
        buf = io.BytesIO()
        img.save(buf, "JPEG", quality=75, optimize=True)
        doc.close()
        return page_num, buf.getvalue()
    except Exception: return page_num, b""

def convert_pdf_image_to_epub(pdf_path: Path, epub_path: Path, T: dict):
    try:
        doc = fitz.open(pdf_path)
        npages, vp_width, vp_height = len(doc), 1200, 1800
        doc.close()
        
        print(T['PARALLEL_START'].format(os.cpu_count()))
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            (base / 'META-INF').mkdir(); (base / 'OEBPS' / 'images').mkdir(parents=True)
            (base / 'mimetype').write_text(MIMETYPE)
            (base / 'META-INF' / 'container.xml').write_text(CONTAINER_XML)
            (base / 'OEBPS' / 'estilos.css').write_text(CSS_FXL)
            
            args = [(str(pdf_path), i) for i in range(npages)]
            with concurrent.futures.ProcessPoolExecutor() as executor:
                results = sorted(executor.map(_process_page_worker, args), key=lambda x: x[0])
            
            pages_meta = []
            for i, (idx, img_bytes) in enumerate(results):
                img_name = f"page_{idx:04d}.jpg"
                (base / 'OEBPS' / 'images' / img_name).write_bytes(img_bytes)
                page_href = f"page_{idx:04d}.xhtml"
                (base / 'OEBPS' / page_href).write_text(generate_fxl_page_xhtml(img_name, vp_width, vp_height))
                pages_meta.append({'page_id': f"p_{idx}", 'page_href': page_href, 'img_id': f"img_{idx}", 'img_href': f"images/{img_name}", 'label': f"Page {idx+1}"})
            
            (base / 'OEBPS' / 'content.opf').write_text(generate_opf_fxl(pdf_path.stem, f"id-{time.time()}", pages_meta, vp_width, vp_height))
            (base / 'OEBPS' / 'nav.xhtml').write_text(generate_nav_fxl(pages_meta))
            pack_epub(base, epub_path)
            print(T['PAGES_FOUND'].format(npages))
        return True
    except Exception as e:
        print(T['PROC_ERROR'].format(pdf_path.name, e))
        return False

class PDFtoEPUBApp:
    def __init__(self, T: dict):
        self.T = T
        self.folder_path = os.getcwd()
        self.dry_run = False

    def run_conversion(self):
        T = self.T
        pdfs = sorted(Path(self.folder_path).glob('*.pdf'))
        if not pdfs:
            print(T['NO_FILES'])
            return
        
        print(T['FOUND_FILES'].format(len(pdfs)))
        
        for file_path in pdfs:
            epub_path = file_path.with_suffix('.epub')
            if epub_path.exists():
                print(T['SKIP_EXISTS'].format(epub_path.name))
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
                        (base / 'META-INF').mkdir(); (base / 'OEBPS').mkdir()
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
                    success = convert_pdf_image_to_epub(file_path, epub_path, T)

            if success and epub_path.exists():
                print(T['SAVED_OK'].format(epub_path.name, epub_path.stat().st_size/(1024*1024)))
                print(f"   ⏱️  {time.time()-inicio:.1f}s")
                dest = file_path.parent / 'ORIGINAL' / file_path.name
                dest.parent.mkdir(exist_ok=True)
                shutil.move(str(file_path), str(dest))
                print(T['MOVED_OK'].format(file_path.name))

        print(T['SUCCESS_ALL'])

    def start(self):
        T = self.T
        clear_screen()
        print(T['PROMO_START'])
        if input(T['CONTINUE_PROMPT']).strip().upper() not in ('S', 'Y'):
            print(T['GOODBYE'])
            return
        
        while True:
            clear_screen()
            print("="*64)
            print(T['BANNER_MENU'])
            print("="*64)
            print(f" 1. {T['MENU_1']}")
            print(f" 0. {T['MENU_0']}")
            opt = input(T['SELECT_OPTION']).strip()
            if opt == '1':
                self.run_conversion()
                input("\nPresiona ENTER...")
            elif opt == '0':
                break

if __name__ == "__main__":
    app = PDFtoEPUBApp(TEXTS[get_ui_language()])
    app.start()
