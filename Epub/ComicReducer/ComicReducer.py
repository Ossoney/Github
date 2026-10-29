"""
ComicReducer - Utilidad para optimizar cómics CBR, CBZ y PDF a formato WebP CBZ.
"""

import os
import sys
import zipfile
import shutil
import locale
import logging
import argparse
import subprocess
import tempfile
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
from PIL import Image, ImageChops
import numpy as np

# Soporte opcional para PDF con PyMuPDF (fitz)
try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None

# Barra de progreso opcional
try:
    from tqdm import tqdm
except ImportError:
    tqdm = None

# ---------------------------------------------------------------------------
# DETECCIÓN DE IDIOMA
# ---------------------------------------------------------------------------

def _detect_lang():
    """Devuelve 'es' si el sistema está en español, 'en' en caso contrario."""
    try:
        lang = locale.getdefaultlocale()[0] or ''
        return 'es' if lang.lower().startswith('es') else 'en'
    except Exception:
        return 'en'

LANG = _detect_lang()

# Perfiles predefinidos de optimización
PROFILES = {
    '1': {'name_es': 'Habitual / Equilibrado (1600px altura, Calidad 80)',
          'name_en': 'Standard / Balanced (1600px height, Quality 80)',
          'height': 1600, 'quality': 80},
    '2': {'name_es': 'Tablet / iPad HD (2048px altura, Calidad 85)',
          'name_en': 'Tablet / iPad HD (2048px height, Quality 85)',
          'height': 2048, 'quality': 85},
    '3': {'name_es': 'Móvil / E-Reader (1280px altura, Calidad 75)',
          'name_en': 'Mobile / E-Reader (1280px height, Quality 75)',
          'height': 1280, 'quality': 75},
    '4': {'name_es': 'Ultra Ahorro / Ligero (1080px altura, Calidad 65)',
          'name_en': 'Ultra Savings / Lightweight (1080px height, Quality 65)',
          'height': 1080, 'quality': 65},
    '5': {'name_es': 'Sin Reescalar (Mantiene resolución original, Calidad 80)',
          'name_en': 'No Rescaling (Keep original resolution, Quality 80)',
          'height': 0, 'quality': 80},
}

_STRINGS = {
    'es': {
        'promo_inicio': (
            "ComicReducer es un programa freeware que optimiza tus cómics CBR, CBZ y PDF,\n"
            "ahorrando espacio de almacenamiento al convertirlos a formato WebP y\n"
            "redimensionando inteligentemente las páginas sin perder calidad visual.\n"
            "En resumen: Transforma-reduce-reescala imágenes."
        ),
        'promo_end': (
            "---------------------------------------------------------------\n"
            "Si el programa te ha sido útil invítame a un café en paypal.me/ossoney.\n"
            "Envíame 1$ - 2$ - 3$ o lo que te apetezca.\n"
            "---------------------------------------------------------------"
        ),
        'log_7zip_found':       "7-Zip encontrado: {path}",
        'log_7zip_not_found':   ("7-Zip NO encontrado. Los archivos .cbr (RAR) no podrán procesarse. "
                                 "Instala 7-Zip desde https://www.7-zip.org"),
        'log_pymupdf_not_found': "PyMuPDF (fitz) no está instalado. Los archivos .pdf no podrán procesarse (pip install pymupdf).",
        'log_no_folders':       "NO SE ENCONTRARON CARPETAS en el directorio raíz.",
        'log_scanning':         "Escaneando carpetas en busca de cómics...",
        'log_total_comics':     "Total cómics a procesar: {n}",
        'log_no_comics':        "NO SE ENCONTRARON CÓMICS",
        'log_file_exists':      "{name} ya existe, saltando...",
        'log_processing':       "Procesando: {name}",
        'log_no_images':        "No se encontraron imágenes en el archivo.",
        'log_ok_done':          "OK FINALIZADO: {orig:.1f}MB -> {new:.1f}MB (-{pct:.1f}%)",
        'log_error':            "ERROR al procesar {name}: {err}",
        'log_deleted_orig':     "Original eliminado: {name}",
        'log_start':            "INICIO CONVERSIÓN...",
        'log_done':             "COMPLETADO",
        'log_invalid_input':    "No se reconoce como índice, rango ni ruta válida: {val}",
        'log_folders_selected': "Carpetas seleccionadas: {names}",
        'log_invalid_comic':    "El archivo {path} no es un cómic o PDF válido.",
        'title_folders':        "📚 CARPETAS DISPONIBLES (RAÍZ - nivel 1)",
        'folder_current':       "Directorio Actual (.)",
        'comics_label':         "Cómics/PDFs",
        'prompt_folders':       "👉 Carpetas (ej: '1,3', 'todas' o escribe la ruta): ",
        'prompt_subfolders':    "📂 ¿Incluir SUBCARPETAS de estas carpetas? (s/N): ",
        'prompt_profiles':      "⚙️  PERFILES DE OPTIMIZACIÓN DISPONIBLES:",
        'prompt_select_profile': "Elige un perfil [1-5] (ENTER = 1 Habitual): ",
        'prompt_autocrop':      "✂️  ¿Deseas activar auto-recorte de bordes blancos/negros? (s/N): ",
        'prompt_remove_blank':  "📄 ¿Deseas eliminar páginas en blanco o negro vacías? (s/N): ",
        'prompt_delete_orig':   "🗑️  ¿Deseas ELIMINAR el archivo original tras optimizarlo con éxito? (s/N): ",
        'prompt_continue':      "\n¿Deseas continuar con la optimización (S/N)?: ",
        'answer_yes':           ('s', 'y'),
        'keyword_all':          ['todas', 'all', '*'],
        'result_title':         "📊 RESULTADO",
        'result_processed':     "✅ Archivos procesados:               {n}",
        'result_skipped':       "⏭️  Archivos omitidos (ya existían):  {n}",
        'result_failed':        "❌ Archivos fallidos:                 {n}",
        'result_deleted':       "🗑️  Originales eliminados:            {n}",
        'result_original':      "⚖️  Peso Total Original:   {mb:.2f} MB",
        'result_final':         "📦 Peso Total Final:      {mb:.2f} MB",
        'result_saved':         "🚀 ESPACIO LIBERADO:      {mb:.2f} MB ({pct:.1f}%)",
        'prompt_exit':          "Presiona ENTER para salir...",
        'tqdm_desc':            "Optimizando",
        'error_7zip':           "7-Zip no pudo extraer el archivo: {detail}",
        'error_no_tool':        "No se puede extraer el archivo. Instala 7-Zip desde https://www.7-zip.org",
        'error_pdf_support':    "Para procesar archivos PDF, instala PyMuPDF ejecutando: pip install pymupdf",
    },
    'en': {
        'promo_inicio': (
            "ComicReducer is a freeware tool that optimizes your CBR, CBZ and PDF comics,\n"
            "saving storage space by converting them to WebP format and\n"
            "intelligently resizing pages without visible quality loss.\n"
            "In short: Transform-reduce-rescale images."
        ),
        'promo_end': (
            "---------------------------------------------------------------\n"
            "If this tool was useful, buy me a coffee at paypal.me/ossoney.\n"
            "Send $1 - $2 - $3 or whatever you like.\n"
            "---------------------------------------------------------------"
        ),
        'log_7zip_found':       "7-Zip found: {path}",
        'log_7zip_not_found':   ("7-Zip NOT found. .cbr (RAR) files cannot be processed. "
                                 "Install 7-Zip from https://www.7-zip.org"),
        'log_pymupdf_not_found': "PyMuPDF (fitz) is not installed. .pdf files cannot be processed (pip install pymupdf).",
        'log_no_folders':       "NO FOLDERS FOUND in the root directory.",
        'log_scanning':         "Scanning folders for comics...",
        'log_total_comics':     "Total comics to process: {n}",
        'log_no_comics':        "NO COMICS FOUND",
        'log_file_exists':      "{name} already exists, skipping...",
        'log_processing':       "Processing: {name}",
        'log_no_images':        "No images found in the file.",
        'log_ok_done':          "OK DONE: {orig:.1f}MB -> {new:.1f}MB (-{pct:.1f}%)",
        'log_error':            "ERROR processing {name}: {err}",
        'log_deleted_orig':     "Original deleted: {name}",
        'log_start':            "STARTING CONVERSION...",
        'log_done':             "COMPLETED",
        'log_invalid_input':    "Not recognized as index, range or valid path: {val}",
        'log_folders_selected': "Selected folders: {names}",
        'log_invalid_comic':    "File {path} is not a valid comic or PDF.",
        'title_folders':        "📚 AVAILABLE FOLDERS (ROOT - level 1)",
        'folder_current':       "Current Directory (.)",
        'comics_label':         "Comics/PDFs",
        'prompt_folders':       "👉 Folders (e.g. '1,3', 'all' or type a path): ",
        'prompt_subfolders':    "📂 Include SUBFOLDERS of these folders? (y/N): ",
        'prompt_profiles':      "⚙️  AVAILABLE OPTIMIZATION PROFILES:",
        'prompt_select_profile': "Choose a profile [1-5] (ENTER = 1 Standard): ",
        'prompt_autocrop':      "✂️  Enable auto-crop of solid black/white borders? (y/N): ",
        'prompt_remove_blank':  "📄 Remove blank/black empty pages? (y/N): ",
        'prompt_delete_orig':   "🗑️  DELETE original files after successful optimization? (y/N): ",
        'prompt_continue':      "\nDo you want to continue with optimization (Y/N)?: ",
        'answer_yes':           ('y', 's'),
        'keyword_all':          ['all', 'todas', '*'],
        'result_title':         "📊 RESULTS",
        'result_processed':     "✅ Files processed:                  {n}",
        'result_skipped':       "⏭️  Files skipped (already existed): {n}",
        'result_failed':        "❌ Files failed:                     {n}",
        'result_deleted':       "🗑️  Originals deleted:               {n}",
        'result_original':      "⚖️  Total Original Size:  {mb:.2f} MB",
        'result_final':         "📦 Total Final Size:      {mb:.2f} MB",
        'result_saved':         "🚀 SPACE SAVED:           {mb:.2f} MB ({pct:.1f}%)",
        'prompt_exit':          "Press ENTER to exit...",
        'tqdm_desc':            "Optimizing",
        'error_7zip':           "7-Zip could not extract the file: {detail}",
        'error_no_tool':        "Cannot extract file. Install 7-Zip from https://www.7-zip.org",
        'error_pdf_support':    "To process PDF files, install PyMuPDF by running: pip install pymupdf",
    },
}

def t(key, **kwargs):
    """Devuelve el string localizado. Acepta kwargs para formatear con .format()."""
    s = _STRINGS.get(LANG, _STRINGS['en']).get(key, key)
    return s.format(**kwargs) if kwargs else s

# ---------------------------------------------------------------------------
# LOGGING (Siempre en el directorio donde reside ComicReducer.py)
# ---------------------------------------------------------------------------

logger = logging.getLogger("ComicReducer")
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

LOG_FILE = Path(__file__).resolve().parent / 'ComicReducer.log'
fh = logging.FileHandler(LOG_FILE, encoding='utf-8')
fh.setFormatter(formatter)
logger.addHandler(fh)

ch = logging.StreamHandler(sys.stdout)
ch.setFormatter(formatter)
logger.addHandler(ch)

# ---------------------------------------------------------------------------
# DETECCIÓN DE 7-ZIP
# ---------------------------------------------------------------------------

_SEVEN_ZIP_PATHS = [
    r"C:\Program Files\7-Zip\7z.exe",
    r"C:\Program Files (x86)\7-Zip\7z.exe",
]

def _find_7zip():
    """Devuelve la ruta a 7z.exe si está disponible, o None."""
    for path in _SEVEN_ZIP_PATHS:
        if Path(path).is_file():
            return path
    try:
        result = subprocess.run(["7z", "i"], capture_output=True, timeout=5)
        if result.returncode == 0:
            return "7z"
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return None

SEVEN_ZIP_EXE = _find_7zip()

# ---------------------------------------------------------------------------
# PROCESAMIENTO DE IMÁGENES Y AUTOCROP
# ---------------------------------------------------------------------------

def get_file_size_mb(file_path):
    try:
        return os.path.getsize(file_path) / (1024 * 1024)
    except OSError:
        return 0.0

def autocrop_borders(img, tol=15):
    """
    Detecta y recorta bordes homogéneos blancos o negros alrededor de la página.
    tol: tolerancia de diferencia de color.
    """
    try:
        # Convertir a escala de grises para recorte de bordes
        gray = img.convert('L')
        # Comparar con fondo negro puro
        bg_black = Image.new('L', img.size, 0)
        diff_black = ImageChops.difference(gray, bg_black)
        bbox_black = diff_black.point(lambda p: 255 if p > tol else 0).getbbox()

        # Comparar con fondo blanco puro
        bg_white = Image.new('L', img.size, 255)
        diff_white = ImageChops.difference(gray, bg_white)
        bbox_white = diff_white.point(lambda p: 255 if p > tol else 0).getbbox()

        # Decidir cuál recorta de forma válida sin destruir la imagen
        bbox = bbox_black or bbox_white
        if bbox:
            # Si el área resultante es al menos un 40% de la original para seguridad
            w_orig, h_orig = img.size
            w_box = bbox[2] - bbox[0]
            h_box = bbox[3] - bbox[1]
            if (w_box * h_box) >= (w_orig * h_orig * 0.40):
                return img.crop(bbox)
    except Exception:
        pass
    return img

def is_blank_or_black_page(img, tol_std=3.5):
    """
    Determina si una imagen es una página en blanco o en negro sin contenido sustancial.
    Utiliza submuestreo ::8 para máxima velocidad en la comprobación.
    tol_std: desviación estándar máxima para considerar la página uniforme/vacía.
    """
    try:
        # Muestreo rápido en escala de grises
        gray_sample = np.array(img.convert('L'))[::8, ::8]
        std_val = float(np.std(gray_sample))
        mean_val = float(np.mean(gray_sample))

        # 1. Página prácticamente uniforme (std muy bajo)
        if std_val < tol_std:
            # Si es negra pura o casi negra (media < 25)
            if mean_val < 25.0:
                return True
            # Si es blanca pura o casi blanca (media > 230)
            if mean_val > 230.0:
                return True
    except Exception:
        pass
    return False

def process_single_image(image_path, target_height=1600, quality=80, autocrop=False, remove_blank=False, is_protected=False):
    """
    Optimiza una página individual:
    - Comprobación y eliminación opcional de páginas en blanco/negro vacías.
    - Auto-recorte opcional de bordes negros/blancos.
    - Detección de doble página (aplica target basado en aspect ratio para no sobre-encogerlas).
    - Redimensionado Lanczos si excede dimensiones objetivo.
    - Detección de escala de grises / B&W (convierte a 'L').
    - Guardado en WebP (calidad configurable, method=4).
    """
    original_size = os.path.getsize(image_path)

    try:
        with Image.open(image_path) as img:
            if img.mode in ('RGBA', 'P', 'CMYK'):
                img = img.convert('RGB')

            # 0. Detección de página en blanco o negro vacía (si no está protegida ej: portada)
            if remove_blank and not is_protected:
                if is_blank_or_black_page(img):
                    try:
                        os.remove(image_path)
                    except OSError:
                        pass
                    return {'status': 'blank_removed', 'path': image_path, 'original_size': original_size, 'new_size': 0, 'saved': original_size}

            # 1. Auto-recorte de bordes si está activado
            if autocrop:
                img = autocrop_borders(img)

            original_width, original_height = img.size

            # 2. Manejo de reescalado y páginas dobles (Double-page spread)
            if target_height > 0:
                is_double_page = original_width > original_height
                if is_double_page:
                    # En páginas dobles (apaisadas), el ancho equivalente de dos páginas es aprox ~2 * target_height
                    # Usamos una altura objetivo o ancho objetivo proporcional
                    target_double_width = int(target_height * 1.4)
                    if original_height > target_height or original_width > target_double_width:
                        # Calcular factor de escala para no sobrepasar ni el ancho doble ni la altura
                        ratio = min(target_height / original_height, target_double_width / original_width)
                        new_width = max(1, int(original_width * ratio))
                        new_height = max(1, int(original_height * ratio))
                        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                else:
                    if original_height > target_height:
                        ratio = target_height / original_height
                        new_width = max(1, int(original_width * ratio))
                        img = img.resize((new_width, target_height), Image.Resampling.LANCZOS)

            # 3. Auto-detectar Blanco y Negro con submuestreo de alta velocidad
            try:
                # Usar submuestreo por pasos (striding) ::8 para analizar ~1/64 de píxeles
                # Esto reduce el tiempo de CPU en ~85% manteniendo la misma fiabilidad
                sample_array = np.array(img)[::8, ::8, :]
                if len(sample_array.shape) >= 3 and sample_array.shape[2] >= 3:
                    diff = (np.mean(np.abs(sample_array[:, :, 0].astype(np.int16) - sample_array[:, :, 1].astype(np.int16))) +
                            np.mean(np.abs(sample_array[:, :, 1].astype(np.int16) - sample_array[:, :, 2].astype(np.int16))))
                    if diff < 5.0:
                        img = img.convert('L')
            except Exception:
                pass

            webp_path = image_path.with_suffix('.webp')
            # method=4 ofrece prácticamente el mismo ratio de compresión que method=6 con el doble de velocidad
            img.save(webp_path, 'WEBP', quality=quality, method=4)

    except Exception as e:
        return {'status': 'error', 'path': image_path, 'msg': str(e)}

    webp_size = os.path.getsize(webp_path)

    if webp_size < original_size:
        if webp_path != image_path:
            try:
                os.remove(image_path)
            except OSError:
                pass
        return {'status': 'compressed', 'original_size': original_size,
                'new_size': webp_size, 'saved': original_size - webp_size}
    else:
        # Si WebP resulta más pesado, mantenemos el archivo original
        if webp_path != image_path:
            try:
                os.remove(webp_path)
            except OSError:
                pass
        return {'status': 'skipped', 'original_size': original_size,
                'new_size': original_size, 'saved': 0}

# ---------------------------------------------------------------------------
# EXTRACCIÓN Y EMPAQUETADO (CBZ, CBR, PDF, PRESERVACIÓN DE METADATOS)
# ---------------------------------------------------------------------------

def extract_pdf(input_file, temp_folder):
    """Extrae las páginas de un archivo PDF como imágenes de alta resolución."""
    if fitz is None:
        raise ValueError(t('error_pdf_support'))

    doc = fitz.open(input_file)
    zoom = 2.0  # Render a alta definición (144 dpi aprox)
    mat = fitz.Matrix(zoom, zoom)

    pad_digits = max(4, len(str(len(doc))))
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        filename = f"page_{page_num + 1:0{pad_digits}d}.png"
        out_path = Path(temp_folder) / filename
        pix.save(str(out_path))
    doc.close()

def extract_comic(input_file, temp_folder):
    """
    Extrae cómic a una carpeta temporal preservando metadatos.
    Soporta CBZ (ZIP), CBR (RAR vía 7-Zip) y PDF.
    """
    suffix = input_file.suffix.lower()

    if suffix == '.pdf':
        extract_pdf(input_file, temp_folder)
        return

    # Intentar primero como ZIP (muchos CBR son simplemente ZIP renombrados)
    try:
        with zipfile.ZipFile(input_file, 'r') as comic:
            comic.extractall(temp_folder)
            return
    except zipfile.BadZipFile:
        pass

    # Intentar con 7-Zip (para CBR / RAR / 7Z)
    if SEVEN_ZIP_EXE:
        result = subprocess.run(
            [SEVEN_ZIP_EXE, 'x', str(input_file), f'-o{temp_folder}', '-y'],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            return
        else:
            raise ValueError(t('error_7zip', detail=result.stderr.strip()))

    raise ValueError(t('error_no_tool'))

def pack_comic(output_file, temp_folder):
    """
    Empaqueta el directorio temporal en un nuevo archivo .cbz.
    - Utiliza ZIP_STORED: WebP ya está óptimamente comprimido.
    - Preserva todos los metadatos (ComicInfo.xml, metadatos JSON/TXT, etc.).
    """
    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_STORED) as new_comic:
        for root, _, files in os.walk(temp_folder):
            for file in files:
                file_path = Path(root) / file
                # Omitir archivos temporales de sistema como .DS_Store o de macOS
                if file.startswith('._') or file == '.DS_Store':
                    continue
                arcname = file_path.relative_to(temp_folder)
                new_comic.write(file_path, arcname)

# ---------------------------------------------------------------------------
# OPTIMIZACIÓN DE CÓMIC COMPLETO
# ---------------------------------------------------------------------------

def optimize_comic(input_file, target_height=1600, quality=80, autocrop=False, delete_original=False, remove_blank=False):
    input_file = Path(input_file)
    output_file = input_file.with_name(f"{input_file.stem}_optimized.cbz")

    if output_file.exists():
        logger.warning(t('log_file_exists', name=output_file.name))
        return {'status': 'skipped', 'original_mb': get_file_size_mb(input_file),
                'new_mb': get_file_size_mb(output_file), 'deleted': False}

    temp_folder = Path(tempfile.mkdtemp(prefix=f"comicreducer_{input_file.stem}_"))
    logger.info(t('log_processing', name=input_file.name))

    try:
        extract_comic(input_file, temp_folder)

        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.webp', '.tif', '.tiff'}
        images_to_process = []
        for root, _, files in os.walk(temp_folder):
            for file in files:
                file_path = Path(root) / file
                if file_path.suffix.lower() in image_extensions and not file_path.name.startswith('._'):
                    images_to_process.append(file_path)

        if not images_to_process:
            logger.error(t('log_no_images'))
            return {'status': 'error', 'original_mb': get_file_size_mb(input_file), 'new_mb': 0, 'deleted': False}

        # Ordenar imágenes alfabéticamente para proteger de forma fidedigna primera y última página
        images_to_process.sort(key=lambda p: str(p).lower())
        total_imgs = len(images_to_process)

        with ProcessPoolExecutor() as executor:
            futures = {}
            for idx, img in enumerate(images_to_process):
                # La primera (portada) y última página (contraportada) siempre se protegen contra borrado
                is_protected = (idx == 0) or (idx == total_imgs - 1)
                f = executor.submit(process_single_image, img, target_height, quality, autocrop, remove_blank, is_protected)
                futures[f] = img

            progress_bar = None
            if tqdm:
                progress_bar = tqdm(total=len(images_to_process), desc=t('tqdm_desc'), leave=False)

            blank_count = 0
            for future in as_completed(futures):
                res_img = future.result()
                if res_img and res_img.get('status') == 'blank_removed':
                    blank_count += 1
                if progress_bar:
                    progress_bar.update(1)

            if progress_bar:
                progress_bar.close()

            if blank_count > 0:
                logger.info(f"Páginas vacías eliminadas: {blank_count}")

        # Empaquetar a .cbz (conservando metadatos ComicInfo.xml intactos)
        pack_comic(output_file, temp_folder)

        original_mb = get_file_size_mb(input_file)
        new_mb = get_file_size_mb(output_file)
        savings_percent = ((original_mb - new_mb) / original_mb) * 100 if original_mb > 0 else 0

        logger.info(t('log_ok_done', orig=original_mb, new=new_mb, pct=savings_percent))

        was_deleted = False
        if delete_original and output_file.exists() and output_file.stat().st_size > 0:
            try:
                input_file.unlink()
                was_deleted = True
                logger.info(t('log_deleted_orig', name=input_file.name))
            except Exception as de:
                logger.warning(f"No se pudo eliminar el original {input_file.name}: {de}")

        return {'status': 'success', 'original_mb': original_mb, 'new_mb': new_mb, 'deleted': was_deleted}

    except Exception as e:
        logger.error(t('log_error', name=input_file.name, err=e))
        if output_file.exists():
            try:
                output_file.unlink()
            except OSError:
                pass
        return {'status': 'error', 'original_mb': get_file_size_mb(input_file), 'new_mb': 0, 'deleted': False}
    finally:
        if temp_folder.exists():
            shutil.rmtree(temp_folder, ignore_errors=True)

# ---------------------------------------------------------------------------
# MENÚS Y LÓGICA DE DIRECTORIO
# ---------------------------------------------------------------------------

SUPPORTED_EXTENSIONS = ('.cbz', '.cbr', '.pdf')

def escanear_carpetas_raiz():
    p = Path('.')
    carpetas = [p]
    try:
        for item in p.iterdir():
            if (item.is_dir() and not item.name.startswith('.')
                    and 'temp_' not in item.name and '__pycache__' not in item.name):
                carpetas.append(item)
    except Exception:
        pass
    return carpetas

def mostrar_y_seleccionar_carpetas(carpetas):
    if not carpetas:
        logger.error(t('log_no_folders'))
        return [], False

    print(f"\n{t('title_folders')}")
    print("-" * 50)
    for idx, c in enumerate(carpetas, 1):
        nombre = c.name if c.name else t('folder_current')
        n = sum(len(list(c.glob(f"*{ext}"))) for ext in SUPPORTED_EXTENSIONS)
        print(f"  [{idx}] {nombre:<30} ({t('comics_label')}: {n})")
    print("-" * 50)

    sel_raw = input(t('prompt_folders')).strip()
    seleccionadas = []

    if sel_raw.lower() in t('keyword_all'):
        seleccionadas = carpetas
    else:
        partes = sel_raw.split(',')
        for p in partes:
            p = p.strip()
            if not p:
                continue

            if '-' in p:
                subpartes = p.split('-')
                if len(subpartes) == 2 and subpartes[0].isdigit() and subpartes[1].isdigit():
                    inicio, fin = int(subpartes[0]), int(subpartes[1])
                    for i in range(inicio, fin + 1):
                        if 1 <= i <= len(carpetas):
                            if carpetas[i - 1] not in seleccionadas:
                                seleccionadas.append(carpetas[i - 1])
                    continue

            if p.isdigit():
                idx = int(p)
                if 1 <= idx <= len(carpetas):
                    if carpetas[idx - 1] not in seleccionadas:
                        seleccionadas.append(carpetas[idx - 1])
                    continue

            path_obj = Path(p)
            if path_obj.is_dir():
                if path_obj not in seleccionadas:
                    seleccionadas.append(path_obj)
            else:
                logger.warning(t('log_invalid_input', val=p))

    if not seleccionadas:
        return [], False

    nombres = ", ".join([c.name if c.name else str(c) for c in seleccionadas[:3]])
    logger.info(t('log_folders_selected', names=nombres + ('...' if len(seleccionadas) > 3 else '')))

    hay_subs = False
    try:
        for c in seleccionadas:
            if any(sub.is_dir() for sub in c.iterdir()):
                hay_subs = True
                break
    except Exception:
        pass

    incluir_subs = False
    if hay_subs:
        resp = input(t('prompt_subfolders')).strip().lower()
        incluir_subs = resp.startswith(t('answer_yes'))

    return seleccionadas, incluir_subs

def seleccionar_perfil_y_opciones():
    """Muestra menú de perfiles predefinidos y opciones on/off (borrado y autocrop)."""
    print(f"\n{t('prompt_profiles')}")
    print("-" * 65)
    for k, v in PROFILES.items():
        nom = v['name_es'] if LANG == 'es' else v['name_en']
        print(f"  [{k}] {nom}")
    print("-" * 65)

    elec = input(t('prompt_select_profile')).strip()
    perfil = PROFILES.get(elec, PROFILES['1'])
    target_height = perfil['height']
    quality = perfil['quality']

    # Opción Auto-recorte on/off
    resp_crop = input(t('prompt_autocrop')).strip().lower()
    autocrop = resp_crop.startswith(t('answer_yes'))

    # Opción Eliminar páginas en blanco o negro on/off
    resp_blank = input(t('prompt_remove_blank')).strip().lower()
    remove_blank = resp_blank.startswith(t('answer_yes'))

    # Opción Borrado de original on/off
    resp_del = input(t('prompt_delete_orig')).strip().lower()
    delete_original = resp_del.startswith(t('answer_yes'))

    return target_height, quality, autocrop, delete_original, remove_blank

def obtener_todos_comics(carpetas, subs):
    comics = []
    logger.info(t('log_scanning'))
    for c in carpetas:
        for ext in SUPPORTED_EXTENSIONS:
            if subs:
                found = list(c.rglob(f"*{ext}"))
            else:
                found = list(c.glob(f"*{ext}"))
            comics.extend(found)

    comics = [c for c in comics if not c.stem.endswith('_optimized')]
    comics = sorted(set(c.resolve() for c in comics))

    if not comics:
        logger.warning(t('log_no_comics'))
    else:
        logger.info(t('log_total_comics', n=len(comics)))
    return comics

# ---------------------------------------------------------------------------
# INTERFAZ GRÁFICA (GUI OPCIONAL)
# ---------------------------------------------------------------------------

def launch_gui():
    """Lanza una interfaz gráfica de usuario sencilla con tkinter."""
    try:
        import tkinter as tk
        from tkinter import ttk, filedialog, messagebox
    except ImportError:
        print("tkinter no está disponible en este entorno.")
        return

    root = tk.Tk()
    root.title("ComicReducer")
    root.geometry("640x520")
    root.minsize(580, 480)

    # Estilos
    style = ttk.Style()
    try:
        style.theme_use('clam')
    except Exception:
        pass

    pad_opts = {'padx': 10, 'pady': 5}

    # Frame Selección
    frame_files = ttk.LabelFrame(root, text=" 📂 Selección de Archivo o Carpeta ", padding=10)
    frame_files.pack(fill='x', **pad_opts)

    path_var = tk.StringVar()
    entry_path = ttk.Entry(frame_files, textvariable=path_var, width=50)
    entry_path.pack(side='left', fill='x', expand=True, padx=(0, 5))

    def choose_file():
        f = filedialog.askopenfilename(
            filetypes=[("Cómics y PDFs", "*.cbz *.cbr *.pdf"), ("Todos los archivos", "*.*")]
        )
        if f:
            path_var.set(f)

    def choose_folder():
        d = filedialog.askdirectory()
        if d:
            path_var.set(d)

    btn_file = ttk.Button(frame_files, text="Archivo...", command=choose_file)
    btn_file.pack(side='left', padx=2)
    btn_folder = ttk.Button(frame_files, text="Carpeta...", command=choose_folder)
    btn_folder.pack(side='left', padx=2)

    # Frame Opciones
    frame_opts = ttk.LabelFrame(root, text=" ⚙️ Configuración y Perfil ", padding=10)
    frame_opts.pack(fill='x', **pad_opts)

    ttk.Label(frame_opts, text="Perfil de Optimización:").grid(row=0, column=0, sticky='w', pady=4)
    profile_var = tk.StringVar(value="1")
    combo_profiles = ttk.Combobox(frame_opts, textvariable=profile_var, state="readonly", width=42)
    combo_profiles['values'] = [
        f"{k} - " + (v['name_es'] if LANG == 'es' else v['name_en'])
        for k, v in PROFILES.items()
    ]
    combo_profiles.current(0)
    combo_profiles.grid(row=0, column=1, sticky='w', padx=5, pady=4)

    subs_var = tk.BooleanVar(value=False)
    chk_subs = ttk.Checkbutton(frame_opts, text="Incluir subcarpetas recursivamente", variable=subs_var)
    chk_subs.grid(row=1, column=0, columnspan=2, sticky='w', pady=2)

    crop_var = tk.BooleanVar(value=False)
    chk_crop = ttk.Checkbutton(frame_opts, text="Auto-recortar márgenes blancos / negros", variable=crop_var)
    chk_crop.grid(row=2, column=0, columnspan=2, sticky='w', pady=2)

    blank_var = tk.BooleanVar(value=False)
    chk_blank = ttk.Checkbutton(frame_opts, text="Eliminar páginas en blanco o negro vacías (protege portadas)", variable=blank_var)
    chk_blank.grid(row=3, column=0, columnspan=2, sticky='w', pady=2)

    del_var = tk.BooleanVar(value=False)
    chk_del = ttk.Checkbutton(frame_opts, text="⚠️ Eliminar archivos originales optimizados con éxito", variable=del_var)
    chk_del.grid(row=4, column=0, columnspan=2, sticky='w', pady=2)

    # Progreso y Estado
    frame_status = ttk.LabelFrame(root, text=" 📊 Progreso ", padding=10)
    frame_status.pack(fill='both', expand=True, **pad_opts)

    lbl_status = ttk.Label(frame_status, text="Listo para comenzar.", foreground="#333")
    lbl_status.pack(anchor='w', pady=(0, 5))

    pbar = ttk.Progressbar(frame_status, mode='determinate')
    pbar.pack(fill='x', pady=5)

    txt_log = tk.Text(frame_status, height=7, state='disabled', wrap='word', font=("Consolas", 9))
    txt_log.pack(fill='both', expand=True, pady=5)

    def log_gui(msg):
        txt_log.config(state='normal')
        txt_log.insert('end', msg + "\n")
        txt_log.see('end')
        txt_log.config(state='disabled')
        root.update_idletasks()

    def run_process():
        target_path_str = path_var.get().strip()
        if not target_path_str:
            messagebox.showwarning("Atención", "Por favor selecciona un archivo o carpeta primero.")
            return

        target_path = Path(target_path_str)
        if not target_path.exists():
            messagebox.showerror("Error", f"La ruta no existe: {target_path}")
            return

        sel_profile_idx = profile_var.get().split(' ')[0]
        cfg = PROFILES.get(sel_profile_idx, PROFILES['1'])
        th = cfg['height']
        q = cfg['quality']
        ac = crop_var.get()
        de = del_var.get()
        rb = blank_var.get()

        btn_run.config(state='disabled')

        comics_list = []
        if target_path.is_file():
            if target_path.suffix.lower() in SUPPORTED_EXTENSIONS:
                comics_list = [target_path]
            else:
                messagebox.showerror("Error", "El archivo seleccionado no es un cómic (CBZ, CBR) ni PDF.")
                btn_run.config(state='normal')
                return
        else:
            comics_list = obtener_todos_comics([target_path], subs_var.get())

        if not comics_list:
            messagebox.showinfo("Información", "No se encontraron cómics para procesar.")
            btn_run.config(state='normal')
            return

        pbar['maximum'] = len(comics_list)
        pbar['value'] = 0

        tot_orig, tot_fin = 0.0, 0.0
        success_count = 0

        for i, c in enumerate(comics_list, 1):
            lbl_status.config(text=f"Procesando ({i}/{len(comics_list)}): {c.name}")
            log_gui(f"[{i}/{len(comics_list)}] {c.name}...")
            res = optimize_comic(c, target_height=th, quality=q, autocrop=ac, delete_original=de, remove_blank=rb)
            if res['status'] == 'success':
                success_count += 1
                tot_orig += res['original_mb']
                tot_fin += res['new_mb']
                log_gui(f"  -> OK: {res['original_mb']:.1f}MB -> {res['new_mb']:.1f}MB")
            elif res['status'] == 'skipped':
                log_gui(f"  -> Omitido (ya existía).")
            else:
                log_gui(f"  -> Error al procesar.")
            pbar['value'] = i
            root.update()

        saved = tot_orig - tot_fin
        pct = (saved / tot_orig * 100) if tot_orig > 0 else 0
        lbl_status.config(text="¡Completado con éxito!")
        log_gui(f"\nFinalizado: {success_count} procesados. Ahorro total: {saved:.1f} MB ({pct:.1f}%)")
        messagebox.showinfo(
            "Completado",
            f"Proceso finalizado.\nArchivos procesados: {success_count}\nAhorro: {saved:.2f} MB ({pct:.1f}%)"
        )
        btn_run.config(state='normal')

    btn_run = ttk.Button(root, text="🚀 Iniciar Optimización", command=run_process)
    btn_run.pack(fill='x', padx=10, pady=(0, 10))

    root.mainloop()

# ---------------------------------------------------------------------------
# MAIN CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="ComicReducer - Comic & PDF Optimizer")
    parser.add_argument('path', nargs='?', help="Archivo o carpeta a procesar directamente")
    parser.add_argument('--gui', action='store_true', help="Lanza la interfaz gráfica (GUI)")
    parser.add_argument('--profile', choices=list(PROFILES.keys()), default=None,
                        help="Perfil de optimización [1-5]")
    parser.add_argument('--height', type=int, default=None,
                        help="Altura máxima en píxeles (0 = mantener original)")
    parser.add_argument('--quality', type=int, default=None,
                        help="Calidad WebP (1-100)")
    parser.add_argument('--autocrop', action='store_true',
                        help="Activa el auto-recorte de bordes blancos/negros")
    parser.add_argument('--remove-blank', action='store_true',
                        help="Elimina páginas en blanco o negro vacías")
    parser.add_argument('--delete-original', action='store_true',
                        help="Elimina el archivo original tras optimizarlo")
    parser.add_argument('--subfolders', action='store_true',
                        help="Incluye subcarpetas recursivamente si se procesa un directorio")

    args = parser.parse_args()

    # Si se pide GUI explícitamente
    if args.gui:
        launch_gui()
        return

    # Si se pasa archivo o carpeta directamente por argumento CLI
    if args.path:
        input_path = Path(args.path)
        if not input_path.exists():
            logger.error(t('log_invalid_comic', path=input_path))
            return

        # Determinar perfil y valores
        if args.profile:
            cfg = PROFILES[args.profile]
            th = cfg['height']
            q = cfg['quality']
        else:
            th = 1600 if args.height is None else args.height
            q = 80 if args.quality is None else args.quality

        ac = args.autocrop
        del_orig = args.delete_original
        rb = args.remove_blank

        if input_path.is_file():
            if input_path.suffix.lower() in SUPPORTED_EXTENSIONS:
                optimize_comic(input_path, target_height=th, quality=q, autocrop=ac, delete_original=del_orig, remove_blank=rb)
            else:
                logger.error(t('log_invalid_comic', path=input_path))
        elif input_path.is_dir():
            comics = obtener_todos_comics([input_path], args.subfolders)
            for c in comics:
                optimize_comic(c, target_height=th, quality=q, autocrop=ac, delete_original=del_orig, remove_blank=rb)
        return

    # Modo interactivo por consola
    print("\n" + "=" * 75)
    print(t('promo_inicio'))
    print("=" * 75)

    # Información sobre herramientas disponibles
    if SEVEN_ZIP_EXE:
        logger.info(t('log_7zip_found', path=SEVEN_ZIP_EXE))
    else:
        logger.warning(t('log_7zip_not_found'))

    if fitz is None:
        logger.warning(t('log_pymupdf_not_found'))

    raiz = escanear_carpetas_raiz()
    sel, subs = mostrar_y_seleccionar_carpetas(raiz)
    if not sel:
        return

    todos = obtener_todos_comics(sel, subs)
    if not todos:
        return

    target_height, quality, autocrop, delete_original, remove_blank = seleccionar_perfil_y_opciones()

    logger.info(t('log_start'))

    resultados = []
    for comic in todos:
        res = optimize_comic(
            comic,
            target_height=target_height,
            quality=quality,
            autocrop=autocrop,
            delete_original=delete_original,
            remove_blank=remove_blank
        )
        resultados.append(res)

    exitos = [r for r in resultados if r['status'] == 'success']
    omitidos = [r for r in resultados if r['status'] == 'skipped']
    fallidos = [r for r in resultados if r['status'] == 'error']
    eliminados = [r for r in resultados if r.get('deleted', False)]

    total_original = sum(r['original_mb'] for r in exitos)
    total_final = sum(r['new_mb'] for r in exitos)
    ahorro = total_original - total_final
    pct = (ahorro / total_original * 100) if total_original > 0 else 0

    print("\n" + "=" * 75)
    print(t('result_title'))
    print("=" * 75)
    print(t('result_processed', n=len(exitos)))
    print(t('result_skipped', n=len(omitidos)))
    print(t('result_failed', n=len(fallidos)))
    if delete_original:
        print(t('result_deleted', n=len(eliminados)))
    print("-" * 40)
    print(t('result_original', mb=total_original))
    print(t('result_final', mb=total_final))
    print(t('result_saved', mb=ahorro, pct=pct))
    print("=" * 75)

    logger.info(t('log_done'))
    print(t('promo_end'))
    input(t('prompt_exit'))

if __name__ == "__main__":
    main()
