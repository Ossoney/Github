"""
common.py - Utilidades comunes para la suite PDFCBZtoEPUB
Contiene perfiles de dispositivos, generadores de EPUB, división de páginas dobles,
extracción de cómics (CBZ y CBR), selector gráfico de carpetas y utilidades de log/consola.
"""

import io
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import zipfile
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from xml.sax.saxutils import escape as xml_escape

from PIL import Image

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

# =========================================================
# PERFILES DE DISPOSITIVOS
# =========================================================
DEVICE_PROFILES = {
    'default': {
        'name': 'Estándar / Genérico (1600x2400)',
        'max_width': 1600,
        'max_height': 2400,
        'quality': 82,
    },
    'kindle_oasis': {
        'name': 'Kindle Oasis / Paperwhite (1264x1680)',
        'max_width': 1264,
        'max_height': 1680,
        'quality': 80,
    },
    'kindle_basic': {
        'name': 'Kindle Básico (1072x1448)',
        'max_width': 1072,
        'max_height': 1448,
        'quality': 78,
    },
    'kobo_forma': {
        'name': 'Kobo Forma / Sage / Elipsa (1440x1920)',
        'max_width': 1440,
        'max_height': 1920,
        'quality': 82,
    },
    'kobo_clara': {
        'name': 'Kobo Clara / Nia (1072x1448)',
        'max_width': 1072,
        'max_height': 1448,
        'quality': 78,
    },
    'tablet_hd': {
        'name': 'Tablet HD / iPad (2048x2732)',
        'max_width': 2048,
        'max_height': 2732,
        'quality': 85,
    },
}

# =========================================================
# UTILIDADES DE CONSOLA Y CARPETAS
# =========================================================
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner(text: str):
    print("=" * 64)
    print(f" {text}")
    print("=" * 64)

def sanitize_filename(name: str) -> str:
    name = re.sub(r'[\\/*?:"<>|]', "", name).strip()
    return name[:200]

def select_folder_dialog(initial_dir: Optional[str] = None) -> Optional[str]:
    """Abre un diálogo nativo de Windows/SO para elegir carpeta con Tkinter."""
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        selected = filedialog.askdirectory(
            initialdir=initial_dir or os.getcwd(),
            title="Selecciona la carpeta de cómics / libros"
        )
        root.destroy()
        if selected:
            return os.path.normpath(selected)
    except Exception:
        pass
    return None

def input_path_with_fallback(prompt: str, allow_dialog: bool = True) -> str:
    """
    Solicita ruta por consola. Si se escribe 'g' o se deja vacío con allow_dialog,
    intenta abrir el selector gráfico.
    """
    entrada = input(prompt).strip().strip('"\'')
    if entrada.lower() in ('g', 'gui', 'd', 'dialog') and allow_dialog:
        gui_folder = select_folder_dialog()
        if gui_folder:
            print(f" -> Carpeta seleccionada: {gui_folder}")
            return gui_folder
    return entrada

# =========================================================
# SOPORTE DE ARCHIVOS CBZ Y CBR
# =========================================================
SEVEN_ZIP_PATH = None
for candidate in [
    Path(os.environ.get("ProgramFiles", "C:\\Program Files")) / "7-Zip" / "7z.exe",
    Path(os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)")) / "7-Zip" / "7z.exe",
    Path("C:/Program Files/7-Zip/7z.exe"),
    Path("C:/Program Files (x86)/7-Zip/7z.exe"),
]:
    if candidate.exists():
        SEVEN_ZIP_PATH = str(candidate)
        break

def extract_archive_images(archive_path: Path, output_dir: Path) -> List[Path]:
    """
    Extrae imágenes tanto de CBZ (ZIP) como de CBR (RAR vía 7-zip o rarfile).
    Retorna la lista de rutas de imágenes extraídas en orden natural.
    """
    IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff'}
    output_dir.mkdir(parents=True, exist_ok=True)
    suffix = archive_path.suffix.lower()

    if suffix in ('.cbz', '.zip'):
        with zipfile.ZipFile(archive_path, 'r') as zf:
            for name in zf.namelist():
                if Path(name).suffix.lower() in IMAGE_EXTS and not Path(name).name.startswith('.') and '__MACOSX' not in name:
                    zf.extract(name, output_dir)

    elif suffix in ('.cbr', '.rar'):
        extracted = False
        # Intento 1: 7-Zip si está disponible
        if SEVEN_ZIP_PATH:
            try:
                cmd = [SEVEN_ZIP_PATH, "x", "-y", f"-o{str(output_dir)}", str(archive_path)]
                subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
                extracted = True
            except Exception:
                extracted = False

        # Intento 2: rarfile si 7z falló
        if not extracted:
            try:
                import rarfile
                with rarfile.RarFile(archive_path, 'r') as rf:
                    for name in rf.namelist():
                        if Path(name).suffix.lower() in IMAGE_EXTS and not Path(name).name.startswith('.') and '__MACOSX' not in name:
                            rf.extract(name, output_dir)
                extracted = True
            except Exception as e:
                raise RuntimeError(f"No se pudo extraer CBR ({archive_path.name}). Asegúrate de tener 7-Zip o WinRAR instalado.")

    # Buscar todas las imágenes extraídas y ordenarlas naturalmente
    found_images = []
    for root, _, files in os.walk(output_dir):
        for f in files:
            p = Path(root) / f
            if p.suffix.lower() in IMAGE_EXTS and not p.name.startswith('.'):
                found_images.append(p)

    def _natural_sort_key(p: Path):
        return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', p.name)]

    found_images.sort(key=_natural_sort_key)
    return found_images

# =========================================================
# DETECCIÓN DE PÁGINAS EN BLANCO / EN NEGRO / VACÍAS
# =========================================================
def is_blank_or_black_page(img: Image.Image, tol_std: float = 3.5) -> bool:
    """
    Determina si una imagen es una página en blanco o en negro sin contenido sustancial.
    Utiliza submuestreo ::8 para máxima velocidad en la comprobación.
    tol_std: desviación estándar máxima para considerar la página uniforme/vacía.
    """
    try:
        gray_img = img.convert('L')
        if HAS_NUMPY:
            gray_sample = np.array(gray_img)[::8, ::8]
            std_val = float(np.std(gray_sample))
            mean_val = float(np.mean(gray_sample))
        else:
            small = gray_img.resize((50, 50), Image.Resampling.BILINEAR)
            pixels = list(small.getdata())
            mean_val = sum(pixels) / len(pixels)
            variance = sum((p - mean_val) ** 2 for p in pixels) / len(pixels)
            std_val = variance ** 0.5

        # Si la desviación estándar es muy baja (página prácticamente uniforme)
        if std_val < tol_std:
            # Página en negro puro o casi negro (media < 25)
            if mean_val < 25.0:
                return True
            # Página en blanco puro o casi blanco (media > 230)
            if mean_val > 230.0:
                return True
    except Exception:
        pass
    return False

# =========================================================
# OPTIMIZACIONES PARA HOJAS ESCANEADAS (DESKEW, AUTOCROP, LIMPIEZA)
# =========================================================
def estimate_skew_angle(img: Image.Image) -> float:
    """
    Estima el ángulo de inclinación (skew) de una página de texto escaneada
    utilizando el perfil de proyección horizontal sobre una versión reducida.
    Rango de búsqueda: -4.0 a +4.0 grados.
    """
    try:
        w, h = img.size
        target_h = 400
        target_w = max(100, int(w * (target_h / max(1, h))))
        small = img.convert('L').resize((target_w, target_h), Image.Resampling.BILINEAR)

        if HAS_NUMPY:
            arr_small = np.array(small)
            bin_small = (arr_small < 200).astype(np.int32)
            if np.sum(bin_small) < 50:
                return 0.0

            angles = np.linspace(-4.0, 4.0, 17)
            best_score = -1.0
            best_angle = 0.0

            for a in angles:
                rot = small.rotate(a, resample=Image.Resampling.BILINEAR, fillcolor=255)
                rot_arr = (np.array(rot) < 200).astype(np.int32)
                score = float(np.sum(np.sum(rot_arr, axis=1) ** 2))
                if score > best_score:
                    best_score = score
                    best_angle = a

            return float(best_angle)
    except Exception:
        pass
    return 0.0

def deskew_image_if_needed(img: Image.Image) -> Image.Image:
    """Endereza una imagen escaneada si detecta una inclinación >= 0.5 grados."""
    try:
        angle = estimate_skew_angle(img)
        if abs(angle) >= 0.5:
            return img.rotate(angle, resample=Image.Resampling.BICUBIC, fillcolor=(255, 255, 255) if img.mode == 'RGB' else 255)
    except Exception:
        pass
    return img

def autocrop_margins(img: Image.Image, padding: int = 15, white_threshold: int = 240) -> Image.Image:
    """
    Recorta automáticamente márgenes blancos excesivos en páginas escaneadas
    para aprovechar la pantalla completa del lector digital.
    """
    try:
        w, h = img.size
        gray = img.convert('L')
        if HAS_NUMPY:
            arr = np.array(gray)
            content_coords = np.where(arr < white_threshold)
            if content_coords[0].size < 100:
                return img
            ymin, ymax = int(content_coords[0].min()), int(content_coords[0].max())
            xmin, xmax = int(content_coords[1].min()), int(content_coords[1].max())
        else:
            from PIL import ImageOps
            bbox = ImageOps.invert(gray).getbbox()
            if not bbox:
                return img
            xmin, ymin, xmax, ymax = bbox

        box = (
            max(0, xmin - padding),
            max(0, ymin - padding),
            min(w, xmax + 1 + padding),
            min(h, ymax + 1 + padding)
        )
        crop_w = box[2] - box[0]
        crop_h = box[3] - box[1]

        # Solo recortar si se elimina al menos un 5% de margen y no es un recorte destructivo (>40% mantenido)
        if crop_w >= w * 0.4 and crop_h >= h * 0.4:
            if crop_w < w * 0.95 or crop_h < h * 0.95:
                return img.crop(box)
    except Exception:
        pass
    return img

def preprocess_image_for_ocr(img: Image.Image) -> Image.Image:
    """
    Preprocesa una imagen escaneada para maximizar la precisión de Tesseract OCR:
    1. Conversión a escala de grises
    2. Enderezado de inclinación (Deskew)
    3. Binarización adaptativa ligera que aísla la tinta y elimina sombras/fondo amarillo
    """
    try:
        gray = img.convert('L')
        # Enderezar primero
        angle = estimate_skew_angle(gray)
        if abs(angle) >= 0.5:
            gray = gray.rotate(angle, resample=Image.Resampling.BICUBIC, fillcolor=255)

        if HAS_NUMPY:
            arr = np.array(gray)
            med = float(np.median(arr))
            thresh = max(110, min(195, int(med * 0.85)))
            enhanced = gray.point(lambda p: 255 if p > thresh else 0)
            return enhanced
    except Exception:
        pass
    return img.convert('L')

def clean_ocr_text_stream(raw_text: str) -> str:
    """
    Post-procesamiento y limpieza de texto OCR:
    1. Filtra cabeceras y números de página aislados (ej. '124' o 'Pág. 124')
    2. Une palabras partidas por guión de final de línea (de-hyphenation)
    3. Reconstruye párrafos continuos fluidos evitando saltos de línea a mitad de oración
    """
    if not raw_text:
        return ''

    lines = [l.strip() for l in raw_text.splitlines() if l.strip()]
    if not lines:
        return ''

    # Filtrar encabezado típico (número aislado o cabecera de página)
    if lines and (lines[0].isdigit() or re.match(r'^(p[aá]g\.?\s*\d+|\d+\s*[-/|]\s*\d+|[ivxlcdm]+)$', lines[0], re.IGNORECASE)):
        lines = lines[1:]

    # Filtrar pie de página típico
    if lines and (lines[-1].isdigit() or re.match(r'^(p[aá]g\.?\s*\d+|\d+\s*[-/|]\s*\d+|[ivxlcdm]+)$', lines[-1], re.IGNORECASE)):
        lines = lines[:-1]

    text = '\n'.join(lines)
    # De-hyphenation: unir palabras cortadas con guión al final de la línea
    text = re.sub(r'(\b\w+)[-\u2010\u2013\u2014]\s*\n\s*(\w+\b)', r'\1\2', text)

    # Reconstrucción de párrafos
    paragraphs = []
    current_para = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            if current_para:
                paragraphs.append(' '.join(current_para))
                current_para = []
            continue

        if current_para:
            prev = current_para[-1]
            if prev.endswith(('.', '!', '?', ':')) and (line[0].isupper() or line.startswith(('-', '—', '«', '"'))):
                paragraphs.append(' '.join(current_para))
                current_para = [line]
            else:
                current_para.append(line)
        else:
            current_para.append(line)

    if current_para:
        paragraphs.append(' '.join(current_para))

    return '\n\n'.join(paragraphs)

# =========================================================
# DIVISIÓN DE PÁGINAS DOBLES (DOUBLE-PAGE SPLIT)
# =========================================================
def split_double_page_if_needed(img: Image.Image, reading_direction: str = 'ltr') -> List[Image.Image]:
    """
    Si una imagen es más ancha que alta con ratio >= 1.25, es una página doble.
    Se divide en dos mitades (izquierda y derecha).
    - ltr (occidental): página 1 = izquierda, página 2 = derecha
    - rtl (manga): página 1 = derecha, página 2 = izquierda
    """
    w, h = img.size
    if w / max(1, h) >= 1.25:
        mid = w // 2
        left_box = (0, 0, mid, h)
        right_box = (mid, 0, w, h)
        left_img = img.crop(left_box)
        right_img = img.crop(right_box)

        if reading_direction.lower() == 'rtl':
            return [right_img, left_img]
        else:
            return [left_img, right_img]
    return [img]

# =========================================================
# GENERADORES EPUB (OPF, NAV, XHTML, CSS)
# =========================================================
MIMETYPE = "application/epub+zip"

CONTAINER_XML = """<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>"""

CSS_FXL = """
html, body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  background-color: #000000;
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

def generate_opf_fxl(title: str, uid: str, pages: List[dict],
                      width: int, height: int,
                      author: str = '', language: str = 'es',
                      reading_direction: str = 'ltr') -> str:
    """Genera content.opf para Fixed-Layout con soporte para cover y dirección de lectura (ltr/rtl)."""
    manifest_lines = [
        '    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>',
        '    <item id="css" href="estilos.css" media-type="text/css"/>'
    ]
    spine_lines = []

    for idx, p in enumerate(pages):
        manifest_lines.append(
            f'    <item id="{p["page_id"]}" href="{p["page_href"]}" media-type="application/xhtml+xml"/>'
        )
        img_href = p["img_href"]
        if img_href.lower().endswith('.png'):
            img_mtype = "image/png"
        elif img_href.lower().endswith('.webp'):
            img_mtype = "image/webp"
        else:
            img_mtype = "image/jpeg"

        cover_prop = ' properties="cover-image"' if idx == 0 else ''
        manifest_lines.append(
            f'    <item id="{p["img_id"]}" href="{img_href}" media-type="{img_mtype}"{cover_prop}/>'
        )
        spine_lines.append(f'    <itemref idref="{p["page_id"]}"/>')

    author_tag = f"\n    <dc:creator>{xml_escape(author)}</dc:creator>" if author else ""
    page_progression = 'page-progression-direction="rtl"' if reading_direction.lower() == 'rtl' else 'page-progression-direction="ltr"'

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
    <meta name="cover" content="img_0001"/>
  </metadata>
  <manifest>
{chr(10).join(manifest_lines)}
  </manifest>
  <spine {page_progression}>
{chr(10).join(spine_lines)}
  </spine>
</package>"""

def generate_nav_fxl(pages: List[dict]) -> str:
    li_lines = [f'        <li><a href="{p["page_href"]}">{xml_escape(p["label"])}</a></li>' for p in pages]
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

def generate_opf_reflowable(title: str, author: str, uid: str, manifest_items: List[str], spine_items: List[str], language: str = 'es') -> str:
    author_tag = f"<dc:creator>{xml_escape(author)}</dc:creator>" if author else ""
    return f'<?xml version="1.0" encoding="UTF-8"?><package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="uid"><metadata xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:identifier id="uid">{xml_escape(uid)}</dc:identifier><dc:title>{xml_escape(title)}</dc:title>{author_tag}<dc:language>{xml_escape(language)}</dc:language></metadata><manifest>{"".join(manifest_items)}</manifest><spine>{"".join(spine_items)}</spine></package>'

def generate_nav_reflowable(title: str, chapters: List[dict]) -> str:
    lis = "".join([f'<li><a href="chapter_{i+1:03d}.xhtml">{xml_escape(ch["title"])}</a></li>' for i, ch in enumerate(chapters)])
    return f'<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE html><html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops"><head><title>Navigation</title></head><body><nav epub:type="toc" id="toc"><h1>{xml_escape(title)}</h1><ol>{lis}</ol></nav></body></html>'

def generate_chapter_xhtml(title: str, content_html: List[str]) -> str:
    body = "".join(content_html)
    return f'<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE html><html xmlns="http://www.w3.org/1999/xhtml"><head><title>{xml_escape(title)}</title><link rel="stylesheet" type="text/css" href="estilos.css"/></head><body><h1>{xml_escape(title)}</h1>{body}</body></html>'

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
