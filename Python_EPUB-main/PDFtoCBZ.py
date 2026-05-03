import io
import logging
import os
import shutil
import sys
import tempfile
import time
from pathlib import Path
import zipfile
import locale
from typing import Tuple, List

import fitz  # PyMuPDF
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np

# FIX LOCALE
try:
    locale.setlocale(locale.LC_ALL, '')
    IDIOMA = locale.getlocale()[0]
    ES_ESPANOL = IDIOMA and ('es' in IDIOMA.lower() or 'spanish' in IDIOMA.lower())
except:
    ES_ESPANOL = True  # Fallback

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler('pdf_cbz_perfecto.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# CONFIGURACIÓN OPTIMIZADA
KCC_OASIS = {
    'resolucion': (1264, 1680),
    'contraste': 1.10,
    'nitidez': 1.10
}

# ⭐ 3 MODOS AUTOMÁTICOS
KCC_MODOS = {
    'normal': {'dpi': 1.4, 'calidad': 75},
    'alta': {'dpi': 1.6, 'calidad': 80},
    'pdf_like': {'extraer_original': True}
}

# MENSAJES
if ES_ESPANOL:
    PROMO_INICIO = """PDFtoCBZ es un programa freeware que optimiza tus comics en PDF,
ahorrando espacio de almacenamiento al convertirlos en CBZ y haciendo más rápida la carga de los comics. En resumen: Transforma-reduce-reescala imágenes. 
No te preocupes, los archivos originales se mantienen."""

    PROMO_END = """---------------------------------------------------------------
Si el programa te ha sido útil invítame a un café en paypal.me/ossoney.
Envíame 1$ - 2$ - 3$ o lo que te apetezca.
---------------------------------------------------------------"""
    
    CONTINUE_PROMPT = "\n¿Deseas continuar con la optimización (S/N)?: "
    
    MSJS = {
        'intro': "Escaneando carpetas con PDFs...\n",
        'carpetas_titulo': "📚 CARPETAS CON PDFs (RAÍZ - nivel 1)",
        'selecciona': "👉 Carpetas (ej: '1,3' 'todas'): ",
        'procesando': "✅ Carpetas seleccionadas: {}",
        'subcarpetas': "📂 ¿Incluir SUBCARPETAS de estas carpetas? (s/N): ",
        'no_encontrados': "❌ NO SE ENCONTRARON PDFs",
        'completado': "🎉 COMPLETADO: {}/{} CBZ creados",
        'reduccion': "📊 Reducción media de peso: {:.1f}%",
        'log': "📋 Log: pdf_cbz_perfecto.log"
    }
else:
    PROMO_INICIO = "PDFtoCBZ Optimizer v2.4"
    PROMO_END = "Done."
    CONTINUE_PROMPT = "Continue? (Y/N): "
    MSJS = {
        'intro': "Scanning...\n",
        'carpetas_titulo': "📚 FOLDERS",
        'selecciona': "👉 Select: ",
        'procesando': "✅ Selected: {}",
        'subcarpetas': "📂 Subfolders detected. Include? (y/N): ",
        'no_encontrados': "❌ No PDFs",
        'completado': "🎉 DONE: {}/{}",
        'reduccion': "📊 Avg Size Reduction: {:.1f}%",
        'log': "📋 Log: pdf_cbz_perfecto.log"
    }


def detectar_problema_calidad(img: Image.Image, pdf_nombre: str) -> str:
    """Detecta problema Y devuelve MODO a usar."""
    try:
        if img.mode != 'RGB':
            img = img.convert('RGB')
        img_array = np.array(img)
        gris = np.mean(img_array, axis=2)
        varianza = np.var(gris)
        media = np.mean(gris)
        
        if varianza < 800 or media < 35 or media > 225 or img.width < 700:
            logger.warning(f"⚠️  {pdf_nombre}: Calidad crítica -> PDF-LIKE")
            return 'pdf_like'
        if varianza < 1500 or img.width < 900:
            logger.warning(f"⚠️  {pdf_nombre}: Calidad media -> ALTA")
            return 'alta'
        return 'normal'
    except:
        return 'normal'


def modo_pdf_like(doc: fitz.Document, temp_dir: Path, npags: int) -> None:
    """Extracción directa de imágenes (Lossless)."""
    logger.info("   📸 MODO PDF-LIKE: Extrayendo imágenes originales")
    
    contador = 1
    for i in range(npags):
        try:
            page = doc.load_page(i)
            images = page.get_images(full=True)
            
            if images:
                xref = images[0][0]
                img_data = doc.extract_image(xref)
                img_bytes = img_data["image"]
                ext = img_data["ext"].lower()
                nombre = temp_dir / f"{contador:04d}.{ext}"
                with open(nombre, "wb") as f:
                    f.write(img_bytes)
                if ext not in ['jpg', 'jpeg']:
                    img_pil = Image.open(nombre).convert('RGB')
                    nombre_jpg = nombre.with_suffix('.jpg')
                    img_pil.save(nombre_jpg, "JPEG", quality=95)
                    try: os.remove(nombre)
                    except: pass
            else:
                pix = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0))
                img = Image.open(io.BytesIO(pix.tobytes("ppm")))
                nombre = temp_dir / f"{contador:04d}.jpg"
                img.save(nombre, "JPEG", quality=95)
            contador += 1
        except Exception:
            pass


def optimizar_kcc_oasis(imagen: Image.Image) -> Image.Image:
    """Optimización con detección de B/N."""
    if imagen.mode != 'RGB': imagen = imagen.convert('RGB')
    ancho_orig, alto_orig = imagen.size
    ancho_oasis, alto_oasis = KCC_OASIS['resolucion']
    
    if ancho_orig > ancho_oasis or alto_orig > alto_oasis:
        ratio = min(ancho_oasis/ancho_orig, alto_oasis/alto_orig)
        nuevo_tam = (int(ancho_orig * ratio), int(alto_orig * ratio))
        img = imagen.resize(nuevo_tam, Image.Resampling.LANCZOS)
    else:
        img = imagen.copy()
    
    img = ImageEnhance.Contrast(img).enhance(KCC_OASIS['contraste'])
    img = ImageEnhance.Sharpness(img).enhance(1.05)
    
    img_array = np.array(img)
    diff = np.mean(np.abs(img_array[:,:,0] - img_array[:,:,1])) + \
           np.mean(np.abs(img_array[:,:,1] - img_array[:,:,2]))
    if diff < 5.0:
        img = img.convert('L')
    return img


def crear_zip_desde_temp(temp_dir: Path, cbz_path: Path):
    """Función auxiliar para zippear."""
    imgs = sorted(list(temp_dir.glob("*.*")))
    if not imgs: return False
    with zipfile.ZipFile(cbz_path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for img in imgs:
            zf.write(img, img.name)
    return True


def convertir_pdf_kcc(pdf_path: Path) -> Tuple[Path, float]:
    inicio = time.time()
    cbz_path = pdf_path.with_suffix(".cbz")
    
    if cbz_path.exists():
        logger.warning(f"⚠️  {cbz_path.name} ya existe")
        return None, 0
    
    temp_dir = Path(tempfile.mkdtemp(prefix="cbz_"))
    logger.info(f"🔄 {pdf_path.name}")
    
    doc = None
    try:
        doc = fitz.open(pdf_path)
        npags = len(doc)
        tam_original = pdf_path.stat().st_size
        logger.info(f"📄 {npags} págs | {tam_original/(1024*1024):.1f}MB")
        
        # 1. Detectar modo
        modo = 'normal'
        if npags > 0:
            try:
                pagina_test = doc.load_page(0)
                pix_test = pagina_test.get_pixmap(matrix=fitz.Matrix(1.5, 1.5))
                img_test = Image.open(io.BytesIO(pix_test.tobytes("ppm")))
                modo = detectar_problema_calidad(img_test, pdf_path.name)
            except: pass
        
        logger.info(f"   🎯 Modo seleccionado: {modo.upper()}")
        
        # 2. Procesar (Primer Intento)
        if modo == 'pdf_like':
            modo_pdf_like(doc, temp_dir, npags)
        else:
            conf = KCC_MODOS[modo]
            dpi_usar = conf['dpi']
            calidad_usar = conf['calidad']
            contador = 1
            for i in range(npags):
                try:
                    pagina = doc.load_page(i)
                    pix = pagina.get_pixmap(matrix=fitz.Matrix(dpi_usar, dpi_usar))
                    img = Image.open(io.BytesIO(pix.tobytes("ppm")))
                    img_opt = optimizar_kcc_oasis(img)
                    nombre = temp_dir / f"{contador:04d}.jpg"
                    img_opt.save(nombre, "JPEG", quality=calidad_usar, optimize=True)
                    contador += 1
                except: pass

        # 3. Crear ZIP inicial
        if not crear_zip_desde_temp(temp_dir, cbz_path):
            doc.close(); doc = None
            return None, 0
            
        # ⭐ 4. VERIFICACIÓN DE TAMAÑO (FAIL-SAFE)
        tam_final = cbz_path.stat().st_size
        
        if tam_final > tam_original and modo != 'pdf_like':
            diff_mb = (tam_final - tam_original) / (1024*1024)
            logger.warning(f"⚠️  RESULTADO MÁS GRANDE (+{diff_mb:.1f}MB). Activando protocolo PDF-Like...")
            
            cbz_path.unlink() 
            shutil.rmtree(temp_dir)
            temp_dir = Path(tempfile.mkdtemp(prefix="cbz_retry_"))
            
            modo_pdf_like(doc, temp_dir, npags)
            crear_zip_desde_temp(temp_dir, cbz_path)
            
            tam_final = cbz_path.stat().st_size
            modo = "PDF-LIKE (RETRY)"

        doc.close(); doc = None
        
        tam_orig_mb = tam_original / (1024*1024)
        tam_final_mb = tam_final / (1024*1024)
        
        # --- CÁLCULO CORREGIDO (DIFERENCIA REAL) ---
        # (Final - Original) / Original
        # Negativo = Reducción (Bueno) | Positivo = Crecimiento (Malo)
        variacion_pct = 0
        if tam_original > 0:
            variacion_pct = ((tam_final - tam_original) / tam_original) * 100
            
        tiempo = time.time() - inicio
        
        # El formato "+.1f" forzará el signo: -20.5% (si bajó) o +5.0% (si subió)
        logger.info(f"✅ {tam_orig_mb:.1f} -> {tam_final_mb:.1f}MB ({variacion_pct:+.1f}%) [{modo.upper()}] [{tiempo:.1f}s]")
        return cbz_path, variacion_pct
        
    except Exception as e:
        logger.error(f"❌ ERROR: {e}")
        if cbz_path.exists(): 
            try: os.remove(cbz_path)
            except: pass
        return None, 0
    finally:
        if doc is not None: 
            try: doc.close()
            except: pass
        shutil.rmtree(temp_dir, ignore_errors=True)


# --- FUNCIONES DE INTERFAZ ---

def escanear_carpetas_raiz() -> List[Path]:
    p = Path('.')
    carpetas = []
    try:
        for item in p.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                carpetas.append(item)
    except: pass
    return sorted(carpetas)

def mostrar_y_seleccionar_carpetas(carpetas: List[Path]) -> Tuple[List[Path], bool]:
    if not carpetas:
        print(f"\n{MSJS['no_encontrados']} (root).")
        return [], False

    print(f"\n{MSJS['carpetas_titulo']}")
    print("-" * 50)
    for idx, c in enumerate(carpetas, 1):
        n = len(list(c.glob('*.pdf')))
        print(f"  [{idx}] {c.name:<30} (PDFs: {n})")
    print("-" * 50)
    
    sel = input(MSJS['selecciona']).strip().lower()
    seleccionadas = []
    
    if sel in ['todas', 'all', '*']:
        seleccionadas = carpetas
    else:
        partes = sel.replace('-', ',').split(',')
        validos = []
        if '-' in sel and len(partes) == 2:
            try: validos = list(range(int(partes[0]), int(partes[1]) + 1))
            except: pass
        if not validos:
            for p in partes:
                try: validos.append(int(p))
                except: pass
        for i in validos:
            if 1 <= i <= len(carpetas):
                seleccionadas.append(carpetas[i-1])

    if not seleccionadas: return [], False

    nombres = ", ".join([c.name for c in seleccionadas[:2]])
    print(MSJS['procesando'].format(nombres + "..."))
    
    hay_subs = False
    try:
        for c in seleccionadas:
            if any(sub.is_dir() for sub in c.iterdir()):
                hay_subs = True; break
    except: pass

    incluir_subs = False
    if hay_subs:
        resp = input(MSJS['subcarpetas']).strip().lower()
        incluir_subs = resp.startswith(('s', 'y'))
    
    return seleccionadas, incluir_subs

def obtener_todos_pdfs(carpetas: List[Path], subs: bool) -> List[Path]:
    pdfs = []
    print(MSJS['intro'], end='')
    for c in carpetas:
        found = list(c.rglob("*.pdf")) if subs else list(c.glob("*.pdf"))
        pdfs.extend(found)
    pdfs = sorted(list(set(pdfs)))
    if not pdfs: print(f"\n{MSJS['no_encontrados']}")
    else: print(f"📄 Total PDFs: {len(pdfs)}")
    return pdfs

def main():
    logger.info("🚀 START")
    print("\n" + "="*75)
    print(PROMO_INICIO)
    print("="*75)
    
    r = input(CONTINUE_PROMPT).strip().upper()
    if not r.startswith(('S', 'Y')): return
    
    raiz = escanear_carpetas_raiz()
    sel, subs = mostrar_y_seleccionar_carpetas(raiz)
    if not sel: return
    
    todos = obtener_todos_pdfs(sel, subs)
    if not todos: return

    total_ahorro = 0
    exitos = 0
    
    print("\n⚡ START CONVERSION...")
    for pdf in todos:
        # Ahora devuelve la variacion (ej: -20.5 para reduccion)
        cbz, variacion = convertir_pdf_kcc(pdf)
        if cbz:
            exitos += 1
            # Para el ahorro total, invertimos el signo
            # Si variacion fue -20% (reducción), el ahorro es +20%
            total_ahorro += (variacion * -1)
    
    print("\n" + "="*60)
    logger.info(MSJS['completado'].format(exitos, len(todos)))
    if exitos:
        logger.info(MSJS['reduccion'].format(total_ahorro/exitos))
    print(PROMO_END)
    print(MSJS['log'])
    input("Presiona ENTER para salir...")

if __name__ == "__main__":
    main()