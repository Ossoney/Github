import os
import sys
import zipfile
import shutil
import locale
import logging
import subprocess
import tempfile
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
from PIL import Image
import numpy as np

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

_STRINGS = {
    'es': {
        'promo_inicio': (
            "ComicReducer es un programa freeware que optimiza tus comics CBR y CBZ,\n"
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
        'log_no_folders':       "NO SE ENCONTRARON CARPETAS en el directorio raíz.",
        'log_scanning':         "Escaneando carpetas en busca de cómics...",
        'log_total_comics':     "Total cómics a procesar: {n}",
        'log_no_comics':        "NO SE ENCONTRARON CÓMICS",
        'log_file_exists':      "{name} ya existe, saltando...",
        'log_processing':       "Procesando: {name}",
        'log_no_images':        "No se encontraron imágenes en el archivo.",
        'log_ok_done':          "OK FINALIZADO: {orig:.1f}MB -> {new:.1f}MB (-{pct:.1f}%)",
        'log_error':            "ERROR al procesar {name}: {err}",
        'log_start':            "INICIO CONVERSIÓN...",
        'log_done':             "COMPLETADO",
        'log_invalid_input':    "No se reconoce como índice, rango ni ruta válida: {val}",
        'log_folders_selected': "Carpetas seleccionadas: {names}",
        'log_invalid_comic':    "El archivo {path} no es un cómic válido.",
        'title_folders':        "📚 CARPETAS DISPONIBLES (RAÍZ - nivel 1)",
        'folder_current':       "Directorio Actual (.)",
        'comics_label':         "Cómics",
        'prompt_folders':       "👉 Carpetas (ej: '1,3', 'todas' o escribe la ruta): ",
        'prompt_subfolders':    "📂 ¿Incluir SUBCARPETAS de estas carpetas? (s/N): ",
        'prompt_continue':      "\n¿Deseas continuar con la optimización (S/N)?: ",
        'answer_yes':           ('s', 'y'),
        'keyword_all':          ['todas', 'all', '*'],
        'result_title':         "📊 RESULTADO",
        'result_processed':     "✅ Archivos procesados:               {n}",
        'result_skipped':       "⏭️  Archivos omitidos (ya existían):  {n}",
        'result_failed':        "❌ Archivos fallidos:                 {n}",
        'result_original':      "⚖️  Peso Total Original:   {mb:.2f} MB",
        'result_final':         "📦 Peso Total Final:      {mb:.2f} MB",
        'result_saved':         "🚀 ESPACIO LIBERADO:      {mb:.2f} MB ({pct:.1f}%)",
        'prompt_exit':          "Presiona ENTER para salir...",
        'tqdm_desc':            "Optimizando",
        'error_7zip':           "7-Zip no pudo extraer el archivo: {detail}",
        'error_no_tool':        "No se puede extraer el archivo. Instala 7-Zip desde https://www.7-zip.org",
    },
    'en': {
        'promo_inicio': (
            "ComicReducer is a freeware tool that optimizes your CBR and CBZ comics,\n"
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
        'log_no_folders':       "NO FOLDERS FOUND in the root directory.",
        'log_scanning':         "Scanning folders for comics...",
        'log_total_comics':     "Total comics to process: {n}",
        'log_no_comics':        "NO COMICS FOUND",
        'log_file_exists':      "{name} already exists, skipping...",
        'log_processing':       "Processing: {name}",
        'log_no_images':        "No images found in the file.",
        'log_ok_done':          "OK DONE: {orig:.1f}MB -> {new:.1f}MB (-{pct:.1f}%)",
        'log_error':            "ERROR processing {name}: {err}",
        'log_start':            "STARTING CONVERSION...",
        'log_done':             "COMPLETED",
        'log_invalid_input':    "Not recognized as index, range or valid path: {val}",
        'log_folders_selected': "Selected folders: {names}",
        'log_invalid_comic':    "File {path} is not a valid comic.",
        'title_folders':        "📚 AVAILABLE FOLDERS (ROOT - level 1)",
        'folder_current':       "Current Directory (.)",
        'comics_label':         "Comics",
        'prompt_folders':       "👉 Folders (e.g. '1,3', 'all' or type a path): ",
        'prompt_subfolders':    "📂 Include SUBFOLDERS of these folders? (y/N): ",
        'prompt_continue':      "\nDo you want to continue with optimization (Y/N)?: ",
        'answer_yes':           ('y', 's'),
        'keyword_all':          ['all', 'todas', '*'],
        'result_title':         "📊 RESULTS",
        'result_processed':     "✅ Files processed:                  {n}",
        'result_skipped':       "⏭️  Files skipped (already existed): {n}",
        'result_failed':        "❌ Files failed:                     {n}",
        'result_original':      "⚖️  Total Original Size:  {mb:.2f} MB",
        'result_final':         "📦 Total Final Size:      {mb:.2f} MB",
        'result_saved':         "🚀 SPACE SAVED:           {mb:.2f} MB ({pct:.1f}%)",
        'prompt_exit':          "Press ENTER to exit...",
        'tqdm_desc':            "Optimizing",
        'error_7zip':           "7-Zip could not extract the file: {detail}",
        'error_no_tool':        "Cannot extract file. Install 7-Zip from https://www.7-zip.org",
    },
}

def t(key, **kwargs):
    """Devuelve el string localizado. Acepta kwargs para formatear con .format()."""
    s = _STRINGS.get(LANG, _STRINGS['en']).get(key, key)
    return s.format(**kwargs) if kwargs else s

# ---------------------------------------------------------------------------
# LOGGING
# ---------------------------------------------------------------------------

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

fh = logging.FileHandler('ComicReducer.log', encoding='utf-8')
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
# El log de detección se emite solo desde main() para evitar
# que los procesos hijo de ProcessPoolExecutor lo repitan.

try:
    from tqdm import tqdm
except ImportError:
    tqdm = None

# ---------------------------------------------------------------------------
# FUNCIONES DE PROCESADO
# ---------------------------------------------------------------------------

def get_file_size_mb(file_path):
    return os.path.getsize(file_path) / (1024 * 1024)

def process_single_image(image_path, target_height, quality):
    original_size = os.path.getsize(image_path)

    try:
        with Image.open(image_path) as img:
            if img.mode in ('RGBA', 'P', 'CMYK'):
                img = img.convert('RGB')

            original_width, original_height = img.size

            if original_height > target_height:
                ratio = target_height / original_height
                new_width = int(original_width * ratio)
                img = img.resize((new_width, target_height), Image.Resampling.LANCZOS)

            # Auto-detectar Blanco y Negro
            try:
                img_array = np.array(img)
                if len(img_array.shape) >= 3 and img_array.shape[2] >= 3:
                    diff = (np.mean(np.abs(img_array[:,:,0].astype(int) - img_array[:,:,1].astype(int))) +
                            np.mean(np.abs(img_array[:,:,1].astype(int) - img_array[:,:,2].astype(int))))
                    if diff < 5.0:
                        img = img.convert('L')
            except Exception:
                pass

            webp_path = image_path.with_suffix('.webp')
            img.save(webp_path, 'WEBP', quality=quality, method=6)

    except Exception as e:
        return {'status': 'error', 'path': image_path, 'msg': str(e)}

    webp_size = os.path.getsize(webp_path)

    if webp_size < original_size:
        if webp_path != image_path:
            try: os.remove(image_path)
            except: pass
        return {'status': 'compressed', 'original_size': original_size,
                'new_size': webp_size, 'saved': original_size - webp_size}
    else:
        if webp_path != image_path:
            try: os.remove(webp_path)
            except: pass
        return {'status': 'skipped', 'original_size': original_size,
                'new_size': original_size, 'saved': 0}

def extract_comic(input_file, temp_folder):
    # Intentar primero como ZIP (muchos CBR son ZIP renombrados)
    try:
        with zipfile.ZipFile(input_file, 'r') as comic:
            comic.extractall(temp_folder)
            return
    except zipfile.BadZipFile:
        pass

    # Intentar con 7-Zip (soporta RAR, CBR, 7z, etc.)
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
    # ZIP_STORED: WebP ya está comprimido, recomprimir malgasta CPU sin ganar espacio
    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_STORED) as new_comic:
        for root, _, files in os.walk(temp_folder):
            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(temp_folder)
                new_comic.write(file_path, arcname)

def optimize_comic(input_file, target_height=1600, quality=80):
    input_file = Path(input_file)
    output_file = input_file.with_name(f"{input_file.stem}_optimized.cbz")

    if output_file.exists():
        logger.warning(t('log_file_exists', name=output_file.name))
        return {'status': 'skipped', 'original_mb': get_file_size_mb(input_file),
                'new_mb': get_file_size_mb(output_file)}

    temp_folder = Path(tempfile.mkdtemp(prefix=f"comicreducer_{input_file.stem}_"))

    logger.info(t('log_processing', name=input_file.name))
    try:
        extract_comic(input_file, temp_folder)

        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.webp'}
        images_to_process = []
        for root, _, files in os.walk(temp_folder):
            for file in files:
                file_path = Path(root) / file
                if file_path.suffix.lower() in image_extensions and not file_path.name.startswith('._'):
                    images_to_process.append(file_path)

        if not images_to_process:
            logger.error(t('log_no_images'))
            return {'status': 'error', 'original_mb': get_file_size_mb(input_file), 'new_mb': 0}

        with ProcessPoolExecutor() as executor:
            futures = {executor.submit(process_single_image, img, target_height, quality): img
                       for img in images_to_process}

            if tqdm:
                progress_bar = tqdm(total=len(images_to_process), desc=t('tqdm_desc'), leave=False)

            for future in as_completed(futures):
                future.result()
                if tqdm:
                    progress_bar.update(1)

            if tqdm:
                progress_bar.close()

        pack_comic(output_file, temp_folder)

        original_mb = get_file_size_mb(input_file)
        new_mb = get_file_size_mb(output_file)
        savings_percent = ((original_mb - new_mb) / original_mb) * 100 if original_mb > 0 else 0

        logger.info(t('log_ok_done', orig=original_mb, new=new_mb, pct=savings_percent))
        return {'status': 'success', 'original_mb': original_mb, 'new_mb': new_mb}

    except Exception as e:
        logger.error(t('log_error', name=input_file.name, err=e))
        if output_file.exists():
            try: os.remove(output_file)
            except: pass
        return {'status': 'error', 'original_mb': get_file_size_mb(input_file), 'new_mb': 0}
    finally:
        if temp_folder.exists():
            shutil.rmtree(temp_folder)

# ---------------------------------------------------------------------------
# MENÚS Y LÓGICA DE DIRECTORIO
# ---------------------------------------------------------------------------

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
        n = len(list(c.glob('*.cbz'))) + len(list(c.glob('*.cbr')))
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

            # ¿Es un rango de índices? (ej: 1-5)
            if '-' in p:
                subpartes = p.split('-')
                if len(subpartes) == 2 and subpartes[0].isdigit() and subpartes[1].isdigit():
                    inicio, fin = int(subpartes[0]), int(subpartes[1])
                    for i in range(inicio, fin + 1):
                        if 1 <= i <= len(carpetas):
                            if carpetas[i-1] not in seleccionadas:
                                seleccionadas.append(carpetas[i-1])
                    continue

            # ¿Es un índice simple?
            if p.isdigit():
                idx = int(p)
                if 1 <= idx <= len(carpetas):
                    if carpetas[idx-1] not in seleccionadas:
                        seleccionadas.append(carpetas[idx-1])
                    continue

            # ¿Es una ruta de directorio?
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

def obtener_todos_comics(carpetas, subs):
    comics = []
    logger.info(t('log_scanning'))
    for c in carpetas:
        if subs:
            found = list(c.rglob("*.cbz")) + list(c.rglob("*.cbr"))
        else:
            found = list(c.glob("*.cbz")) + list(c.glob("*.cbr"))
        comics.extend(found)

    comics = [c for c in comics if not c.stem.endswith('_optimized')]
    # Resolver rutas absolutas para evitar duplicados por casing distinto en Windows
    comics = sorted(set(c.resolve() for c in comics))

    if not comics:
        logger.warning(t('log_no_comics'))
    else:
        logger.info(t('log_total_comics', n=len(comics)))
    return comics

# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main():
    # Si se pasa un argumento, procesar directamente ese archivo
    if len(sys.argv) > 1:
        archivo = Path(sys.argv[1])
        if archivo.is_file() and archivo.suffix.lower() in ['.cbz', '.cbr']:
            optimize_comic(archivo)
        else:
            logger.error(t('log_invalid_comic', path=archivo))
        return

    print("\n" + "="*75)
    print(t('promo_inicio'))
    print("="*75)

    r = input(t('prompt_continue')).strip().upper()
    if not r.startswith(tuple(c.upper() for c in t('answer_yes'))):
        return

    # Informar detección de 7-Zip una sola vez al arrancar
    if SEVEN_ZIP_EXE:
        logger.info(t('log_7zip_found', path=SEVEN_ZIP_EXE))
    else:
        logger.warning(t('log_7zip_not_found'))

    raiz = escanear_carpetas_raiz()
    sel, subs = mostrar_y_seleccionar_carpetas(raiz)
    if not sel:
        return

    todos = obtener_todos_comics(sel, subs)
    if not todos:
        return

    target_height = 1600
    quality = 80

    logger.info(t('log_start'))

    resultados = []
    for comic in todos:
        res = optimize_comic(comic, target_height, quality)
        resultados.append(res)

    exitos  = [r for r in resultados if r['status'] == 'success']
    omitidos = [r for r in resultados if r['status'] == 'skipped']
    fallidos = [r for r in resultados if r['status'] == 'error']

    total_original = sum(r['original_mb'] for r in exitos)
    total_final    = sum(r['new_mb']      for r in exitos)
    ahorro = total_original - total_final
    pct    = (ahorro / total_original * 100) if total_original > 0 else 0

    print("\n" + "="*75)
    print(t('result_title'))
    print("="*75)
    print(t('result_processed', n=len(exitos)))
    print(t('result_skipped',   n=len(omitidos)))
    print(t('result_failed',    n=len(fallidos)))
    print("-" * 40)
    print(t('result_original',  mb=total_original))
    print(t('result_final',     mb=total_final))
    print(t('result_saved',     mb=ahorro, pct=pct))
    print("="*75)

    logger.info(t('log_done'))
    print(t('promo_end'))
    input(t('prompt_exit'))

if __name__ == "__main__":
    main()
