import os
import sys
import zipfile
import shutil
import time
import logging
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
from PIL import Image
import numpy as np

# Logging configuration
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# File handler
fh = logging.FileHandler('ComicReducer.log', encoding='utf-8')
fh.setFormatter(formatter)
logger.addHandler(fh)

# Console handler
ch = logging.StreamHandler(sys.stdout)
ch.setFormatter(formatter)
logger.addHandler(ch)


try:
    import rarfile
except ImportError:
    logger.warning("'rarfile' module not found. CBR extraction will not work. Install with: pip install rarfile")

try:
    from tqdm import tqdm
except ImportError:
    tqdm = None

PROMO_INICIO = """ComicReducer es un programa freeware que optimiza tus comics CBR y CBZ,
ahorrando espacio de almacenamiento al convertirlos a formato WebP y
redimensionando inteligentemente las páginas sin perder calidad visual.
En resumen: Transforma-reduce-reescala imágenes."""

PROMO_END = """---------------------------------------------------------------
Si el programa te ha sido útil invítame a un café en paypal.me/ossoney.
Envíame 1$ - 2$ - 3$ o lo que te apetezca.
---------------------------------------------------------------"""

def get_file_size_mb(file_path):
    return os.path.getsize(file_path) / (1024 * 1024)

def process_single_image(image_path, target_height, quality):
    original_size = os.path.getsize(image_path)
    
    try:
        with Image.open(image_path) as img:
            if img.mode in ('RGBA', 'P', 'CMYK'):
                img = img.convert('RGB')
                
            original_width, original_height = img.size
            new_width, new_height = original_width, original_height
            
            if original_height > target_height:
                ratio = target_height / original_height
                new_width = int(original_width * ratio)
                new_height = target_height
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Auto-detectar Blanco y Negro
            try:
                img_array = np.array(img)
                if len(img_array.shape) >= 3 and img_array.shape[2] >= 3:
                    diff = np.mean(np.abs(img_array[:,:,0].astype(int) - img_array[:,:,1].astype(int))) + \
                           np.mean(np.abs(img_array[:,:,1].astype(int) - img_array[:,:,2].astype(int)))
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
        return {
            'status': 'compressed',
            'original_size': original_size,
            'new_size': webp_size,
            'saved': original_size - webp_size
        }
    else:
        if webp_path != image_path:
            try: os.remove(webp_path)
            except: pass
        return {
            'status': 'skipped',
            'original_size': original_size,
            'new_size': original_size,
            'saved': 0
        }

def extract_comic(input_file, temp_folder):
    try:
        # Intentar primero como ZIP (muchos programas guardan zip con extensión cbr)
        with zipfile.ZipFile(input_file, 'r') as comic:
            comic.extractall(temp_folder)
            return
    except zipfile.BadZipFile:
        pass
        
    try:
        # Si falló como ZIP, intentar como RAR
        if 'rarfile' not in sys.modules:
            raise ImportError("Módulo 'rarfile' no instalado.")
        with rarfile.RarFile(input_file, 'r') as comic:
            comic.extractall(temp_folder)
    except rarfile.NotRarFile:
        raise ValueError(f"El archivo no es un ZIP ni un RAR válido.")

def pack_comic(output_file, temp_folder):
    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as new_comic:
        for root, _, files in os.walk(temp_folder):
            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(temp_folder)
                new_comic.write(file_path, arcname)

def optimize_comic(input_file, target_height=1600, quality=80):
    input_file = Path(input_file)
    output_file = input_file.with_name(f"{input_file.stem}_optimized.cbz")
    
    if output_file.exists():
        logger.warning(f"{output_file.name} ya existe, saltando...")
        return {'status': 'skipped', 'original_mb': get_file_size_mb(input_file), 'new_mb': get_file_size_mb(output_file)}
        
    temp_folder = Path(f"temp_{input_file.stem}")
    
    if temp_folder.exists():
        shutil.rmtree(temp_folder)
    temp_folder.mkdir(exist_ok=True)

    logger.info(f"Procesando: {input_file.name}")
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
            logger.error("No se encontraron imágenes en el archivo.")
            return {'status': 'error', 'original_mb': get_file_size_mb(input_file), 'new_mb': 0}

        with ProcessPoolExecutor() as executor:
            futures = {executor.submit(process_single_image, img, target_height, quality): img for img in images_to_process}
            
            if tqdm:
                progress_bar = tqdm(total=len(images_to_process), desc="Optimizando", leave=False)
            
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
        
        logger.info(f"OK FINALIZADO: {original_mb:.1f}MB -> {new_mb:.1f}MB (-{savings_percent:.1f}%)")
        return {'status': 'success', 'original_mb': original_mb, 'new_mb': new_mb}

    except Exception as e:
        logger.error(f"ERROR al procesar {input_file.name}: {e}")
        if output_file.exists():
            try: os.remove(output_file)
            except: pass
        return {'status': 'error', 'original_mb': get_file_size_mb(input_file), 'new_mb': 0}
    finally:
        if temp_folder.exists():
            shutil.rmtree(temp_folder)

# --- MENÚS Y LÓGICA DE DIRECTORIO ---

def escanear_carpetas_raiz():
    p = Path('.')
    carpetas = []
    # Añadir directorio actual (.)
    carpetas.append(p)
    try:
        for item in p.iterdir():
            if item.is_dir() and not item.name.startswith('.') and 'temp_' not in item.name and '__pycache__' not in item.name:
                carpetas.append(item)
    except: pass
    return carpetas

def mostrar_y_seleccionar_carpetas(carpetas):
    if not carpetas:
        logger.error("NO SE ENCONTRARON CARPETAS en el directorio raíz.")
        return [], False

    print("\n📚 CARPETAS DISPONIBLES (RAÍZ - nivel 1)")
    print("-" * 50)
    for idx, c in enumerate(carpetas, 1):
        nombre = c.name if c.name else "Directorio Actual (.)"
        n = len(list(c.glob('*.cbz'))) + len(list(c.glob('*.cbr')))
        print(f"  [{idx}] {nombre:<30} (Cómics: {n})")
    print("-" * 50)
    
    sel = input("👉 Carpetas (ej: '1,3' 'todas'): ").strip().lower()
    seleccionadas = []
    
    if sel in ['todas', 'all', '*']:
        seleccionadas = carpetas
    else:
        partes = sel.replace('-', ',').split(',')
        validos = []
        for p in partes:
            try: validos.append(int(p))
            except: pass
        for i in validos:
            if 1 <= i <= len(carpetas):
                seleccionadas.append(carpetas[i-1])

    if not seleccionadas: return [], False

    nombres = ", ".join([c.name if c.name else "." for c in seleccionadas[:2]])
    logger.info(f"Carpetas seleccionadas: {nombres}...")
    
    hay_subs = False
    try:
        for c in seleccionadas:
            if any(sub.is_dir() for sub in c.iterdir()):
                hay_subs = True; break
    except: pass

    incluir_subs = False
    if hay_subs:
        resp = input("📂 ¿Incluir SUBCARPETAS de estas carpetas? (s/N): ").strip().lower()
        incluir_subs = resp.startswith(('s', 'y'))
    
    return seleccionadas, incluir_subs

def obtener_todos_comics(carpetas, subs):
    comics = []
    logger.info("Escaneando carpetas en busca de cómics...")
    for c in carpetas:
        if subs:
            found = list(c.rglob("*.cbz")) + list(c.rglob("*.cbr"))
        else:
            found = list(c.glob("*.cbz")) + list(c.glob("*.cbr"))
        comics.extend(found)
        
    comics = [c for c in comics if not c.stem.endswith('_optimized')]
    comics = sorted(list(set(comics)))
    
    if not comics: 
        logger.warning("NO SE ENCONTRARON CÓMICS")
    else: 
        logger.info(f"Total Cómics a procesar: {len(comics)}")
    return comics

def main():
    # Si se pasa un argumento, procesar directamente ese archivo
    if len(sys.argv) > 1:
        archivo = Path(sys.argv[1])
        if archivo.is_file() and archivo.suffix.lower() in ['.cbz', '.cbr']:
            optimize_comic(archivo)
        else:
            logger.error(f"El archivo {archivo} no es un cómic válido.")
        return

    print("\n" + "="*75)
    print(PROMO_INICIO)
    print("="*75)
    
    r = input("\n¿Deseas continuar con la optimización (S/N)?: ").strip().upper()
    if not r.startswith(('S', 'Y')): return
    
    raiz = escanear_carpetas_raiz()
    sel, subs = mostrar_y_seleccionar_carpetas(raiz)
    if not sel: return
    
    todos = obtener_todos_comics(sel, subs)
    if not todos: return

    target_height = 1600
    quality = 80
    
    logger.info("START CONVERSION...")
    
    resultados = []
    for comic in todos:
        res = optimize_comic(comic, target_height, quality)
        resultados.append(res)
    
    # RESULTADO TOTALIZADOR
    exitos = [r for r in resultados if r['status'] == 'success']
    omitidos = [r for r in resultados if r['status'] == 'skipped']
    fallidos = [r for r in resultados if r['status'] == 'error']
    
    total_original = sum(r['original_mb'] for r in exitos)
    total_final = sum(r['new_mb'] for r in exitos)
    ahorro = total_original - total_final
    pct = (ahorro / total_original * 100) if total_original > 0 else 0

    print("\n" + "="*75)
    print("📊 RESULTADO TOTALIZADOR")
    print("="*75)
    print(f"✅ Procesados con éxito:  {len(exitos)}")
    print(f"⏭️  Omitidos (ya existían): {len(omitidos)}")
    print(f"❌ Fallidos:              {len(fallidos)}")
    print("-" * 40)
    print(f"⚖️  Peso Total Original:   {total_original:.2f} MB")
    print(f"📦 Peso Total Final:      {total_final:.2f} MB")
    print(f"🚀 ESPACIO LIBERADO:      {ahorro:.2f} MB ({pct:.1f}%)")
    print("="*75)
    
    logger.info("COMPLETADO")
    print(PROMO_END)
    input("Presiona ENTER para salir...")

if __name__ == "__main__":
    main()
