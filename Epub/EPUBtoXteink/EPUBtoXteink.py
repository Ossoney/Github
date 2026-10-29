import sys
import os
import zipfile
import logging
import locale
import builtins
import concurrent.futures
from pathlib import Path
import tempfile
import json
import argparse

# =========================================================
# RUTAS BASE
# =========================================================
SCRIPT_DIR = Path(__file__).resolve().parent
LOG_PATH = SCRIPT_DIR / 'EPUBtoXteink.log'
CONFIG_PATH = SCRIPT_DIR / 'config.json'

# =========================================================
# CONFIGURACIÓN PERSISTENTE (config.json)
# =========================================================
def load_config():
    """Carga la configuración guardada del usuario si existe."""
    if CONFIG_PATH.is_file():
        try:
            with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def save_config(config_dict):
    """Guarda la configuración del usuario en config.json."""
    try:
        current = load_config()
        current.update(config_dict)
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            json.dump(current, f, indent=4, ensure_ascii=False)
    except Exception as e:
        logging.warning("No se pudo guardar config.json: %s", e)

# =========================================================
# LOGGER: guardado en la carpeta del programa
# =========================================================
logging.basicConfig(
    filename=str(LOG_PATH),
    level=logging.INFO,
    format='%(asctime)s | %(message)s',
    encoding='utf-8'
)
# Redirige TODOS los warnings de Python al log (no a la consola)
logging.captureWarnings(True)

original_print = builtins.print

def log_print(*args, **kwargs):
    text = " ".join(str(arg) for arg in args)
    if text and not text.startswith('='):
        clean_text = text.replace('\r', '').replace('\n', '').strip()
        if clean_text:
            if '[ERROR]' in clean_text or 'Error' in clean_text:
                logging.error(clean_text)
            else:
                logging.info(clean_text)
    original_print(*args, **kwargs)

builtins.print = log_print

# =========================================================
# DEPENDENCIAS EXTERNAS
# =========================================================
try:
    from bs4 import BeautifulSoup
except ImportError:
    print("Error: Install BeautifulSoup4 → pip install beautifulsoup4")
    sys.exit(1)

try:
    from PIL import Image
    # Protección contra Decompression Bombs (200 millones de píxeles)
    Image.MAX_IMAGE_PIXELS = 200_000_000
except ImportError:
    print("Error: Install Pillow → pip install Pillow")
    sys.exit(1)

# Detección del parser más veloz (lxml). El aviso se imprime después
# de cargar el idioma, dentro de start().
try:
    import lxml  # noqa: F401
    HTML_PARSER = 'lxml'
    _LXML_AVAILABLE = True
except ImportError:
    HTML_PARSER = 'html.parser'
    _LXML_AVAILABLE = False

# =========================================================
# PERFILES DE DISPOSITIVO
# =========================================================
# Ambos dispositivos usan el mismo procesador ESP32 y tienen 128 MB de RAM,
# por lo que el umbral de splitting de capítulos es idéntico (300 KB).
# La diferencia relevante para la optimización de imágenes es la resolución
# de pantalla nativa de cada modelo.
#
# Xteink X3: pantalla 3.7" — resolución ~480 × 640 px (≈250 PPI)
# Xteink X4 / X4 Pro: pantalla 4.3" — resolución ~480 × 800 px (≈220 PPI)
#
# Las imágenes que superen estas dimensiones se redimensionarán para ajustarse
# al límite del dispositivo, ahorrando memoria y tiempo de renderizado.

DEVICE_PROFILES = {
    'X3': {
        'max_width':  480,
        'max_height': 640,
    },
    'X4': {
        'max_width':  480,
        'max_height': 800,
    },
    'X4p': {
        'max_width':  480,
        'max_height': 800,
    },
}

# Paleta de 4 grises nativos del panel E-Ink (#000000, #555555, #AAAAAA, #FFFFFF).
# Para el modo 'P' de Pillow, la paleta debe contener exactamente 256 colores * 3 canales = 768 valores.
# Los primeros 4 colores (12 valores) definen los 4 tonos; los 756 restantes se rellenan con ceros.
EINK_4GRAY_PALETTE = [0, 0, 0,  85, 85, 85,  170, 170, 170,  255, 255, 255] + [0] * (768 - 12)

def create_4gray_palette_image():
    """Crea una imagen modo 'P' con la paleta exacta de 4 grises para Pillow."""
    pal_img = Image.new('P', (1, 1))
    pal_img.putpalette(EINK_4GRAY_PALETTE)
    return pal_img

# =========================================================
# LOCALIZACIÓN
# =========================================================

def get_ui_language():
    """Devuelve 'es' si el sistema está en español, 'en' en el resto de casos."""
    try:
        lang = locale.getlocale()[0]
        if not lang:
            lang = os.environ.get('LANG', '')
        
        if lang:
            lang = lang.lower()
            if lang.startswith('es') or 'spanish' in lang:
                return 'es'
    except Exception:
        pass
    return 'en'

TEXTS = {
    'es': {
        # Detección de motor HTML
        'LXML_ON':  "[INFO] Motor lxml detectado. ¡Modo de Alto Rendimiento Activado!",
        'LXML_OFF': "[INFO] Usando html.parser (Para más velocidad, instala 'lxml')",

        # Pantalla de inicio
        'PROMO_START': (
            "EPUBtoXteink es un programa freeware que adapta tus archivos EPUB\n"
            "para lectores de tinta electrónica con hardware limitado (como el Xteink X3/X4).\n"
            "En resumen: convierte imágenes a escala de grises con dithering Floyd-Steinberg,\n"
            "elimina fuentes y CSS pesado, y divide capítulos gigantes para evitar cuelgues de RAM.\n"
            "No te preocupes, los archivos originales se mantienen."
        ),
        'PROMO_END': (
            "---------------------------------------------------------------\n"
            "Si el programa te ha sido útil invítame a un café en paypal.me/ossoney.\n"
            "Envíame 1$ - 2$ - 3$ o lo que te apetezca.\n"
            "---------------------------------------------------------------"
        ),
        'CONTINUE_PROMPT': "\n¿Deseas continuar (S/N)?: ",
        'GOODBYE':         "\nOperación cancelada. ¡Gracias por usar EPUBtoXteink!",
        'INTERRUPT':       "\n\n(x) Salida forzada por el usuario.",

        # Banners
        'BANNER_CONFIG': "EPUB TO XTEINK - CONFIGURACIÓN",
        'BANNER_MENU':   "EPUB TO XTEINK - MENÚ PRINCIPAL",

        # Selección de dispositivo
        'DEVICE_INTRO':  (
            "Selecciona el modelo de tu lector Xteink.\n"
            "  [1] Xteink X3      (3.7\" — 480×640 px — ≈250 PPI)\n"
            "  [2] Xteink X4      (4.3\" — 480×800 px — ≈220 PPI)\n"
            "  [3] Xteink X4 Pro  (4.3\" — 480×800 px — ≈220 PPI)"
        ),
        'DEVICE_PROMPT': "Modelo (1, 2 o 3, Enter para mantener '{}'): ",
        'DEVICE_INVALID':"Opción inválida. Selecciona 1 (X3), 2 (X4) o 3 (X4 Pro): ",
        'DEVICE_SET':    "[INFO] Perfil activo: Xteink {} — máx. {}×{} px",

        # Selección de carpeta
        'FOLDER_INTRO':  "Selecciona la carpeta o archivo de trabajo.",
        'FOLDER_PROMPT': "Ruta de carpeta o archivo .epub (Enter para '{}'): ",

        # Menú
        'ACTIVE_FOLDER':  "Carpeta activa: {}",
        'ACTIVE_DEVICE':  "Dispositivo:    Xteink {} ({}×{} px)",
        'SIM_LABEL':      " [ESTADO DE SIMULACIÓN]",
        'ACTIONS_HEADER': "\nACCIONES DISPONIBLES{}:",
        'MENU_1':         " [1] Iniciar Optimización Híper-acelerada de EPUBs (Multihilo + Splitting de RAM)",
        'MENU_2_ON':      " [2] Desactivar Modo Simulación (Dry-Run)",
        'MENU_2_OFF':     " [2] Activar Modo Simulación (Dry-Run)",
        'MENU_3':         " [3] Cambiar Carpeta de Trabajo",
        'MENU_4':         " [4] Cambiar Modelo de Dispositivo",
        'MENU_5':         " [5] Optimizar Imágenes para Fondos de Pantalla (X3/X4/X4p)",
        'MENU_0':         " [0] Salir",
        'SELECT_OPTION':  "\nSelecciona una opción: ",
        'PRESS_ENTER':    "\nPresiona ENTER para volver al menú...",
        'UNKNOWN_CMD':    "Comando no reconocido. Presiona ENTER para continuar...",
        'EXIT_MSG':       "\n¡Desconectando sistemas! Hasta luego.",

        # Optimizador de fondos de pantalla
        'IMG_FOLDER_INTRO':  "Selecciona la carpeta con las imágenes a optimizar.",
        'IMG_FOLDER_PROMPT': "Ruta de la carpeta (Enter para usar la actual): ",
        'NO_IMAGES':         "\nNo se encontraron imágenes en esta carpeta.",
        'FOUND_IMAGES':      "\n[INFO] Se encontraron {} imágenes. Procesando...",
        'IMG_SAVED_OK':      " -> [OK] Guardado: {}",
        'IMG_SKIPPED':       " -> [OMITIDA] Imagen demasiado pequeña: {}",
        'IMG_ERROR':         " -> [ERROR] Falló {}: {}",
        'IMG_SUCCESS':       "\n -> [ÉXITO] Imágenes optimizadas correctamente.",

        # Procesamiento
        'INVALID_PATH':  "\nError: La ruta seleccionada no es válida.",
        'NO_EPUBS':      "\nNo se encontraron archivos EPUB originales en esta carpeta.",
        'FOUND_EPUBS':   "\n[INFO] Se encontraron {} libros. Arrancando motores...",
        'SUCCESS_ALL':   "\n -> [ÉXITO TOTAL] Optimización terminada.",
        'SIM_EPUB':      "[{}/{}] [SIMULACIÓN] Optimizaría usando Multihilo y Splitting: {}",
        'PROCESSING':    "\n[{}/{}] Procesando: {}",
        'SAVED_OK':      " -> [OK] Guardado: {}",
        'PROC_ERROR':    " -> [ERROR] Falló el procesamiento de {}: {}",
        'SPLIT_MSG':     "   [SPLIT] Capítulo dividido: {} → {}",
    },
    'en': {
        # HTML engine detection
        'LXML_ON':  "[INFO] lxml engine detected. High-Performance Mode Activated!",
        'LXML_OFF': "[INFO] Using html.parser (For more speed, install 'lxml')",

        # Startup screen
        'PROMO_START': (
            "EPUBtoXteink is freeware that adapts your EPUB files\n"
            "for e-ink readers with limited hardware (such as the Xteink X3/X4).\n"
            "In short: converts images to grayscale with Floyd-Steinberg dithering,\n"
            "removes heavy fonts and CSS, and splits large chapters to prevent RAM crashes.\n"
            "Don't worry, your original files are kept safe."
        ),
        'PROMO_END': (
            "---------------------------------------------------------------\n"
            "If the program was useful, invite me for a coffee at paypal.me/ossoney.\n"
            "Send $1 - $2 - $3 or whatever you feel like.\n"
            "---------------------------------------------------------------"
        ),
        'CONTINUE_PROMPT': "\nDo you want to continue (Y/N)?: ",
        'GOODBYE':         "\nOperation cancelled. Thank you for using EPUBtoXteink!",
        'INTERRUPT':       "\n\n(x) Forced exit by user.",

        # Banners
        'BANNER_CONFIG': "EPUB TO XTEINK - SETUP",
        'BANNER_MENU':   "EPUB TO XTEINK - MAIN MENU",

        # Device selection
        'DEVICE_INTRO':  (
            "Select your Xteink reader model.\n"
            "  [1] Xteink X3      (3.7\" — 480×640 px — ≈250 PPI)\n"
            "  [2] Xteink X4      (4.3\" — 480×800 px — ≈220 PPI)\n"
            "  [3] Xteink X4 Pro  (4.3\" — 480×800 px — ≈220 PPI)"
        ),
        'DEVICE_PROMPT': "Model (1, 2 or 3, Enter to keep '{}'): ",
        'DEVICE_INVALID':"Invalid option. Select 1 (X3), 2 (X4) or 3 (X4 Pro): ",
        'DEVICE_SET':    "[INFO] Active profile: Xteink {} — max {}×{} px",

        # Folder selection
        'FOLDER_INTRO':  "Select working folder or EPUB file.",
        'FOLDER_PROMPT': "Folder path or .epub file (Enter for '{}'): ",

        # Menu
        'ACTIVE_FOLDER':  "Active folder: {}",
        'ACTIVE_DEVICE':  "Device:        Xteink {} ({}×{} px)",
        'SIM_LABEL':      " [SIMULATION MODE]",
        'ACTIONS_HEADER': "\nAVAILABLE ACTIONS{}:",
        'MENU_1':         " [1] Start Hyper-Accelerated EPUB Optimization (Multithreading + RAM Splitting)",
        'MENU_2_ON':      " [2] Disable Simulation Mode (Dry-Run)",
        'MENU_2_OFF':     " [2] Enable Simulation Mode (Dry-Run)",
        'MENU_3':         " [3] Change Working Folder",
        'MENU_4':         " [4] Change Device Model",
        'MENU_5':         " [5] Optimize Images for Wallpapers (X3/X4/X4p)",
        'MENU_0':         " [0] Exit",
        'SELECT_OPTION':  "\nSelect an option: ",
        'PRESS_ENTER':    "\nPress ENTER to return to the menu...",
        'UNKNOWN_CMD':    "Unknown command. Press ENTER to continue...",
        'EXIT_MSG':       "\nShutting down! Goodbye.",

        # Wallpaper optimizer
        'IMG_FOLDER_INTRO':  "Select the folder containing the images to optimize.",
        'IMG_FOLDER_PROMPT': "Folder path (press Enter to use current): ",
        'NO_IMAGES':         "\nNo images found in this folder.",
        'FOUND_IMAGES':      "\n[INFO] Found {} images. Processing...",
        'IMG_SAVED_OK':      " -> [OK] Saved: {}",
        'IMG_SKIPPED':       " -> [SKIPPED] Image too small (decorative): {}",
        'IMG_ERROR':         " -> [ERROR] Failed {}: {}",
        'IMG_SUCCESS':       "\n -> [DONE] Images optimized successfully.",

        # Processing
        'INVALID_PATH':  "\nError: The selected path is not valid.",
        'NO_EPUBS':      "\nNo original EPUB files found in this folder.",
        'FOUND_EPUBS':   "\n[INFO] Found {} books. Starting engines...",
        'SUCCESS_ALL':   "\n -> [COMPLETE] Optimization finished.",
        'SIM_EPUB':      "[{}/{}] [SIMULATION] Would optimize using Multithreading and Splitting: {}",
        'PROCESSING':    "\n[{}/{}] Processing: {}",
        'SAVED_OK':      " -> [OK] Saved: {}",
        'PROC_ERROR':    " -> [ERROR] Failed to process {}: {}",
        'SPLIT_MSG':     "   [SPLIT] Chapter split: {} → {}",
    },
}

# =========================================================
# HERRAMIENTAS DE ESTÉTICA
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

# =========================================================
# LÓGICA PRINCIPAL - OPTIMIZADOR
# =========================================================

class XteinkOptimizerApp:
    def __init__(self, T: dict):
        self.T = T
        saved_config = load_config()

        # Ruta por defecto desde config o directorio actual
        saved_folder = saved_config.get('folder_path')
        if saved_folder and (Path(saved_folder).is_dir() or Path(saved_folder).is_file()):
            self.folder_path = saved_folder
        else:
            self.folder_path = os.getcwd()

        self.dry_run = False

        # Perfil de dispositivo desde config o por defecto 'X4p'
        saved_device = saved_config.get('device_name', 'X4p')
        if saved_device in DEVICE_PROFILES:
            self.device_name = saved_device
        else:
            self.device_name = 'X4p'

        self.max_width   = DEVICE_PROFILES[self.device_name]['max_width']
        self.max_height  = DEVICE_PROFILES[self.device_name]['max_height']

        # Tamaño crítico a partir del cual el lector crashea (~300 KB).
        # Idéntico en X3, X4 y X4p ya que montan 128 MB de RAM con ESP32.
        self.max_html_size = 300 * 1024
        self.cover_dimensions = {}

    # ----------------------------------------------------------
    # UI: selección de dispositivo
    # ----------------------------------------------------------
    def select_device(self):
        """Muestra el selector de modelo (X3 / X4 / X4 Pro) y actualiza el perfil activo."""
        T = self.T
        print()
        print(T['DEVICE_INTRO'])
        while True:
            choice = input(T['DEVICE_PROMPT'].format(self.device_name)).strip()
            if not choice:
                break
            elif choice == '1':
                self.device_name = 'X3'
                break
            elif choice == '2':
                self.device_name = 'X4'
                break
            elif choice == '3':
                self.device_name = 'X4p'
                break
            else:
                print(T['DEVICE_INVALID'], end='')

        profile = DEVICE_PROFILES[self.device_name]
        self.max_width  = profile['max_width']
        self.max_height = profile['max_height']
        save_config({'device_name': self.device_name})
        print(T['DEVICE_SET'].format(self.device_name, self.max_width, self.max_height))

    # ----------------------------------------------------------
    # IMAGEN: Grises + Alpha flatten + Resize + Floyd-Steinberg
    # ----------------------------------------------------------
    def _optimize_image(self, file_path, is_cover=False):
        """
        Pipeline completo de imagen para e-readers:
          1. Elimina miniaturas decorativas (<= 15 px).
          2. Reduce resolución al máximo del dispositivo seleccionado.
          3. Aplana canal Alpha sobre fondo blanco (evita fondo negro).
          4. Convierte a escala de grises de 8 bits.
          5. Dithering Floyd-Steinberg cuantizado a los 4 grises nativos del panel.
          6. Guarda como BMP 24 bits RGB (sin CLUT) para máxima compatibilidad.
             (Excepción: si es portada, guarda como JPG para compatibilidad del bookshelf).
        """
        try:
            img = Image.open(file_path)

            # 1. Imágenes decorativas minúsculas: eliminar directamente
            if img.width <= 15 or img.height <= 15:
                img.close()
                os.remove(file_path)
                return "deleted"

            # 2. Reducción de resolución
            img.thumbnail((self.max_width, self.max_height), Image.Resampling.LANCZOS)

            # 3. CORRECCIÓN CRÍTICA: aplanar canal Alpha antes de pasar a grises.
            if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1])  # Canal Alpha como máscara
                img = background

            # 4. Procesar según tipo:
            if is_cover:
                # Portada en escala de grises limpia (modo L) sin compresión destructiva en JPEG
                img = img.convert('L')
                out_path = Path(file_path).with_suffix('.jpg')
                img.save(out_path, 'JPEG', quality=95, optimize=True)
                self.cover_dimensions[Path(file_path).name] = img.size
            else:
                # Resto de imágenes: Floyd-Steinberg a 4 grises nativos en BMP 24-bits
                img = img.convert('L')
                pal_img = create_4gray_palette_image()
                img = img.quantize(palette=pal_img, dither=Image.Dither.FLOYDSTEINBERG)
                img = img.convert('RGB')
                out_path = Path(file_path).with_suffix('.bmp')
                img.save(out_path, 'BMP')

            img.close()
            
            # Borrar original si cambió la extensión
            if str(Path(file_path).resolve()) != str(Path(out_path).resolve()):
                os.remove(file_path)

            return "optimized"
        except Exception as e:
            logging.warning("[IMG SKIP] %s: %s", file_path, e)
            return "skipped"

    # ----------------------------------------------------------
    # HTML: purga de elementos pesados
    # ----------------------------------------------------------
    def _purge_html_soup(self, soup, cover_files=None):
        """Elimina scripts, estilos e iframes que el e-reader no puede manejar.
        También reescribe las referencias de imágenes a .bmp (salvo portadas)."""
        if cover_files is None:
            cover_files = set()

        for tag in soup(["script", "style", "iframe", "base", "canvas", "video", "audio"]):
            tag.decompose()

        for tag in soup.find_all(True):
            if tag.has_attr('style'):
                del tag['style']
            if tag.has_attr('class'):
                del tag['class']

        # Reescribir src de imágenes a .bmp (o .jpg si es portada)
        _IMG_EXTS = {'.jpg', '.jpeg', '.png', '.webp', '.gif', '.bmp'}
        for tag in soup.find_all('img'):
            src = tag.get('src', '')
            if Path(src).suffix.lower() in _IMG_EXTS:
                if Path(src).name in cover_files:
                    tag['src'] = str(Path(src).with_suffix('.jpg')).replace('\\', '/')
                else:
                    tag['src'] = str(Path(src).with_suffix('.bmp')).replace('\\', '/')
                    
        for tag in soup.find_all('image'):
            for attr in ('src', 'xlink:href', 'href'):
                val = tag.get(attr, '')
                if val and Path(val).suffix.lower() in _IMG_EXTS:
                    base_name = Path(val).name
                    if base_name in cover_files:
                        tag[attr] = str(Path(val).with_suffix('.jpg')).replace('\\', '/')
                        if base_name in self.cover_dimensions:
                            cw, ch = self.cover_dimensions[base_name]
                            tag['width'] = str(cw)
                            tag['height'] = str(ch)
                            svg_parent = tag.find_parent('svg')
                            if svg_parent:
                                if svg_parent.has_attr('viewbox'):
                                    del svg_parent['viewbox']
                                svg_parent['viewBox'] = f"0 0 {cw} {ch}"
                                svg_parent['width'] = "100%"
                                svg_parent['height'] = "100%"
                    else:
                        tag[attr] = str(Path(val).with_suffix('.bmp')).replace('\\', '/')

        return soup

    def _optimize_and_split_html(self, file_path, opf_modifier_queue, cover_files=None):
        """Purga el HTML. Si supera 300 KB lo divide en dos partes y anota el split para el OPF.
        Devuelve la lista de ficheros nuevos creados (para splitting iterativo en el llamador)."""
        T = self.T
        new_files = []
        try:
            file_size = os.path.getsize(file_path)

            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            soup = BeautifulSoup(content, HTML_PARSER)
            soup = self._purge_html_soup(soup, cover_files)

            # Si el archivo excede el tamaño crítico de memoria (medido tras la purga)
            purged_html = str(soup).encode('utf-8')
            if len(purged_html) > self.max_html_size and soup.body:
                children = list(soup.body.find_all(recursive=False))

                # Desempaquetar contenedores únicos si impiden el split
                while len(children) == 1 and children[0].name in ['div', 'section', 'article', 'main']:
                    children[0].unwrap()
                    children = list(soup.body.find_all(recursive=False))

                mid_point = len(children) // 2

                if mid_point > 0:
                    path_obj = Path(file_path)
                    part2_name = f"{path_obj.stem}_part2{path_obj.suffix}"
                    part2_path = path_obj.with_name(part2_name)

                    # CORRECCIÓN CRÍTICA: construir Part2 desde el HEAD original,
                    # luego mover nodos reales con extract() (no clonar la sopa entera).
                    head_tag  = soup.find('head')
                    head_html = str(head_tag) if head_tag else '<head></head>'
                    part2_soup = BeautifulSoup(
                        f'<?xml version="1.0" encoding="utf-8"?>'
                        f'<!DOCTYPE html><html xmlns="http://www.w3.org/1999/xhtml">'
                        f'{head_html}<body></body></html>',
                        HTML_PARSER
                    )

                    for child in children[mid_point:]:
                        extracted = child.extract()
                        part2_soup.body.append(extracted)

                    with open(part2_path, 'w', encoding='utf-8') as f2:
                        f2.write(str(part2_soup))

                    opf_modifier_queue.append((path_obj.name, part2_name))
                    print(T['SPLIT_MSG'].format(path_obj.name, part2_name))
                    # Encolar el fichero nuevo para un posible segundo split
                    new_files.append(str(part2_path))

            # Sobrescribir Parte 1 (ya sin la segunda mitad)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))

        except Exception as e:
            logging.warning("[HTML SKIP] %s: %s", file_path, e)

        return new_files

    # ----------------------------------------------------------
    # OPF: parchar manifiesto tras el splitting
    # ----------------------------------------------------------
    def _patch_opf_manifest(self, temp_dir, split_queue):
        """Busca el .opf y re-enlaza los _part2 generados por el split.
        Usa lxml.etree cuando está disponible para preservar namespaces XML."""
        if not split_queue:
            return

        for root_dir, _, files in os.walk(temp_dir):
            for file in files:
                if not file.endswith('.opf'):
                    continue

                opf_path = os.path.join(root_dir, file)

                try:
                    if _LXML_AVAILABLE:
                        import lxml.etree as etree
                        tree    = etree.parse(opf_path)
                        root_el = tree.getroot()
                        opf_ns  = root_el.nsmap.get(None, 'http://www.idpf.org/2007/opf')
                        ns      = f'{{{opf_ns}}}' if opf_ns else ''

                        manifest = root_el.find(f'{ns}manifest')
                        spine    = root_el.find(f'{ns}spine')

                        if manifest is not None and spine is not None:
                            for orig_filename, part2_filename in split_queue:
                                orig_item = None
                                for item in manifest:
                                    if Path(item.get('href', '')).name == orig_filename:
                                        orig_item = item
                                        break

                                if orig_item is not None:
                                    orig_href  = orig_item.get('href', orig_filename)
                                    part2_href = str(Path(orig_href).with_name(part2_filename)).replace('\\', '/')
                                    orig_id    = orig_item.get('id', 'item')
                                    part2_id   = f'{orig_id}_part2'

                                    new_item = etree.Element(f'{ns}item')
                                    new_item.set('id', part2_id)
                                    new_item.set('href', part2_href)
                                    new_item.set('media-type', orig_item.get(
                                        'media-type', 'application/xhtml+xml'))
                                    children = list(manifest)
                                    manifest.insert(children.index(orig_item) + 1, new_item)

                                    for itemref in list(spine):
                                        if itemref.get('idref') == orig_id:
                                            new_ref = etree.Element(f'{ns}itemref')
                                            new_ref.set('idref', part2_id)
                                            spine.insert(
                                                list(spine).index(itemref) + 1, new_ref)
                                            break

                        tree.write(opf_path, xml_declaration=True,
                                   encoding='UTF-8', pretty_print=True)

                    else:  # Fallback BeautifulSoup
                        with open(opf_path, 'r', encoding='utf-8') as f:
                            soup = BeautifulSoup(f.read(), 'xml')
                        manifest = soup.find('manifest')
                        spine    = soup.find('spine')
                        if manifest and spine:
                            for orig_filename, part2_filename in split_queue:
                                orig_item = None
                                for item in manifest.find_all('item'):
                                    if Path(item.get('href', '')).name == orig_filename:
                                        orig_item = item
                                        break
                                if orig_item:
                                    orig_href  = orig_item.get('href', orig_filename)
                                    part2_href = str(Path(orig_href).with_name(part2_filename)).replace('\\', '/')
                                    part2_id   = f"{orig_item.get('id', 'item')}_part2"
                                    new_el = soup.new_tag(
                                        'item', href=part2_href, id=part2_id,
                                        **{'media-type': orig_item.get(
                                            'media-type', 'application/xhtml+xml')})
                                    orig_item.insert_after(new_el)
                                    spine_item = spine.find(
                                        'itemref', idref=orig_item.get('id'))
                                    if spine_item:
                                        spine_item.insert_after(
                                            soup.new_tag('itemref', idref=part2_id))
                        with open(opf_path, 'w', encoding='utf-8') as f:
                            f.write(str(soup))

                except Exception as e:
                    logging.warning('[OPF ERROR] %s: %s', opf_path, e)

                return  # Solo hay 1 OPF por epub

    # ----------------------------------------------------------
    # OPF: actualizar hrefs de imágenes convertidas a BMP
    # ----------------------------------------------------------
    def _patch_opf_images(self, temp_dir, cover_files=None):
        """Actualiza el OPF: reemplaza extensiones de imagen por .bmp y
        fija el media-type a image/bmp en todos los <item> de imágenes
        (excepto las portadas, que se guardan como JPEG)."""
        if cover_files is None:
            cover_files = set()
            
        _IMG_EXTS = {'.jpg', '.jpeg', '.png', '.webp', '.gif', '.bmp'}

        for root_dir, _, files in os.walk(temp_dir):
            for file in files:
                if not file.endswith('.opf'):
                    continue
                opf_path = os.path.join(root_dir, file)
                try:
                    if _LXML_AVAILABLE:
                        import lxml.etree as etree
                        tree    = etree.parse(opf_path)
                        root_el = tree.getroot()
                        opf_ns  = root_el.nsmap.get(None, 'http://www.idpf.org/2007/opf')
                        ns      = f'{{{opf_ns}}}' if opf_ns else ''
                        manifest = root_el.find(f'{ns}manifest')
                        if manifest is not None:
                            for item in manifest:
                                href = item.get('href', '')
                                if Path(href).suffix.lower() in _IMG_EXTS:
                                    if Path(href).name in cover_files:
                                        item.set('href', str(Path(href).with_suffix('.jpg')).replace('\\', '/'))
                                        item.set('media-type', 'image/jpeg')
                                    else:
                                        item.set('href', str(Path(href).with_suffix('.bmp')).replace('\\', '/'))
                                        item.set('media-type', 'image/bmp')
                        tree.write(opf_path, xml_declaration=True,
                                   encoding='UTF-8', pretty_print=True)
                    else:
                        with open(opf_path, 'r', encoding='utf-8') as f:
                            soup = BeautifulSoup(f.read(), 'xml')
                        for item in soup.find_all('item'):
                            href = item.get('href', '')
                            if Path(href).suffix.lower() in _IMG_EXTS:
                                if Path(href).name in cover_files:
                                    item['href'] = str(Path(href).with_suffix('.jpg')).replace('\\', '/')
                                    item['media-type'] = 'image/jpeg'
                                else:
                                    item['href'] = str(Path(href).with_suffix('.bmp')).replace('\\', '/')
                                    item['media-type'] = 'image/bmp'
                        with open(opf_path, 'w', encoding='utf-8') as f:
                            f.write(str(soup))
                except Exception as e:
                    logging.warning('[OPF ERROR] %s: %s', opf_path, e)

                return  # Solo hay 1 OPF por epub

    # ----------------------------------------------------------
    # NCX: actualizar tabla de contenidos tras el splitting
    # ----------------------------------------------------------
    def _patch_ncx(self, temp_dir, split_queue):
        """Actualiza el toc.ncx añadiendo un navPoint para cada _part2 generado
        y renumera todos los playOrder de forma secuencial."""
        if not split_queue:
            return

        ncx_path = None
        for root_dir, _, files in os.walk(temp_dir):
            for file in files:
                if file.endswith('.ncx'):
                    ncx_path = os.path.join(root_dir, file)
                    break
            if ncx_path:
                break
        if not ncx_path:
            return

        try:
            if _LXML_AVAILABLE:
                import lxml.etree as etree
                tree    = etree.parse(ncx_path)
                root_el = tree.getroot()
                NCX_NS  = 'http://www.daisy.org/z3986/2005/ncx/'
                ns      = f'{{{NCX_NS}}}'

                for orig_filename, part2_filename in split_queue:
                    for nav_point in root_el.findall(f'.//{ns}navPoint'):
                        content_el = nav_point.find(f'{ns}content')
                        if content_el is None:
                            continue
                        src = content_el.get('src', '')
                        src_path = src.split('#')[0]
                        if Path(src_path).name != orig_filename:
                            continue

                        label_el   = nav_point.find(f'{ns}navLabel/{ns}text')
                        orig_label = label_el.text if label_el is not None else orig_filename

                        new_nav = etree.Element(f'{ns}navPoint')
                        new_nav.set('id', f"{nav_point.get('id', 'navPoint')}_part2")
                        lbl  = etree.SubElement(new_nav, f'{ns}navLabel')
                        txt  = etree.SubElement(lbl, f'{ns}text')
                        txt.text = f'{orig_label} (cont.)'
                        cnt  = etree.SubElement(new_nav, f'{ns}content')
                        cnt.set('src', str(Path(src).with_name(part2_filename)).replace('\\', '/'))

                        parent = nav_point.getparent()
                        parent.insert(list(parent).index(nav_point) + 1, new_nav)
                        break

                for i, np in enumerate(root_el.findall(f'.//{ns}navPoint'), start=1):
                    np.set('playOrder', str(i))

                tree.write(ncx_path, xml_declaration=True,
                           encoding='UTF-8', pretty_print=True)

            else:  # Fallback BeautifulSoup
                with open(ncx_path, 'r', encoding='utf-8') as f:
                    soup = BeautifulSoup(f.read(), 'xml')

                for orig_filename, part2_filename in split_queue:
                    for nav_point in soup.find_all('navPoint'):
                        content_el = nav_point.find('content')
                        if not content_el:
                            continue
                        src = content_el.get('src', '')
                        src_path = src.split('#')[0]
                        if Path(src_path).name != orig_filename:
                            continue

                        label_el   = nav_point.find('text')
                        orig_label = label_el.string if label_el else orig_filename

                        new_nav = soup.new_tag(
                            'navPoint', id=f"{nav_point.get('id', 'navPoint')}_part2")
                        lbl = soup.new_tag('navLabel')
                        txt = soup.new_tag('text')
                        txt.string = f'{orig_label} (cont.)'
                        lbl.append(txt)
                        new_nav.append(lbl)
                        cnt = soup.new_tag(
                            'content', src=str(Path(src).with_name(part2_filename)).replace('\\', '/'))
                        new_nav.append(cnt)
                        nav_point.insert_after(new_nav)
                        break

                for i, np in enumerate(soup.find_all('navPoint'), start=1):
                    np['playOrder'] = str(i)

                with open(ncx_path, 'w', encoding='utf-8') as f:
                    f.write(str(soup))

        except Exception as e:
            logging.warning('[NCX ERROR] %s: %s', ncx_path, e)

    # ----------------------------------------------------------
    # NAV (EPUB 3): actualizar tabla de contenidos nav.xhtml
    # ----------------------------------------------------------
    def _patch_nav(self, temp_dir, split_queue):
        """Actualiza nav.xhtml (EPUB 3) añadiendo enlaces para cada _part2 generado."""
        if not split_queue:
            return

        nav_candidates = []
        for root_dir, _, files in os.walk(temp_dir):
            for file in files:
                f_lower = file.lower()
                if f_lower in ('nav.xhtml', 'nav.html', 'toc.xhtml', 'toc.html'):
                    nav_candidates.append(os.path.join(root_dir, file))

        if not nav_candidates:
            return

        for nav_path in nav_candidates:
            try:
                with open(nav_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                # Solo modificar si realmente tiene navegación epub:type="toc" o etiqueta <nav>
                if '<nav' not in content.lower():
                    continue

                soup = BeautifulSoup(content, HTML_PARSER)
                modified = False

                for orig_filename, part2_filename in split_queue:
                    # Buscar enlaces <a href="...orig_filename...">
                    for a_tag in soup.find_all('a'):
                        href = a_tag.get('href', '')
                        href_path = href.split('#')[0]
                        if Path(href_path).name == orig_filename:
                            parent_li = a_tag.find_parent('li')
                            if parent_li:
                                # Clonar li
                                new_li = BeautifulSoup(str(parent_li), HTML_PARSER).find('li')
                                if new_li and new_li.find('a'):
                                    new_a = new_li.find('a')
                                    new_a['href'] = str(Path(href).with_name(part2_filename)).replace('\\', '/')
                                    new_a.string = f"{a_tag.get_text()} (cont.)"
                                    parent_li.insert_after(new_li)
                                    modified = True
                                    break

                if modified:
                    with open(nav_path, 'w', encoding='utf-8') as f:
                        f.write(str(soup))
            except Exception as e:
                logging.warning('[NAV ERROR] %s: %s', nav_path, e)

    # ----------------------------------------------------------
    # PIPELINE PRINCIPAL: 1 EPUB
    # ----------------------------------------------------------
    def process_single_epub(self, epub, current=1, total=1):
        """Orquesta la extracción, multiprocesamiento, split y reempaquetado de 1 epub."""
        T = self.T
        if self.dry_run:
            print(T['SIM_EPUB'].format(current, total, epub.name))
            return

        print(T['PROCESSING'].format(current, total, epub.name))
        opf_modifier_queue = []

        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temp_dir:
            try:
                # 1. Descomprimir
                with zipfile.ZipFile(epub, 'r') as zf:
                    zf.extractall(temp_dir)

                # 1b. Extraer portadas desde el OPF para mantenerlas como JPG
                cover_files = set()
                for root_dir, _, files in os.walk(temp_dir):
                    for file in files:
                        if file.endswith('.opf'):
                            with open(os.path.join(root_dir, file), 'r', encoding='utf-8') as f:
                                soup = BeautifulSoup(f.read(), 'xml')
                            meta_cover = soup.find('meta', attrs={'name': 'cover'})
                            if meta_cover:
                                cover_item = soup.find('item', id=meta_cover.get('content'))
                                if cover_item:
                                    cover_files.add(Path(cover_item.get('href', '')).name)
                            for item in soup.find_all('item'):
                                if 'cover-image' in item.get('properties', ''):
                                    cover_files.add(Path(item.get('href', '')).name)

                # Clasificar archivos por tipo
                image_tasks    = []
                html_tasks     = []
                fonts_to_delete = []

                for root_dir, _, files in os.walk(temp_dir):
                    for file in files:
                        full_path = os.path.join(root_dir, file)
                        ext = file.lower()

                        if ext.endswith(('.html', '.xhtml', '.htm')):
                            html_tasks.append(full_path)
                        elif ext.endswith(('.jpg', '.jpeg', '.png', '.webp', '.bmp', '.gif')):
                            image_tasks.append(full_path)
                        elif ext.endswith(('.ttf', '.otf', '.woff', '.woff2')):
                            fonts_to_delete.append(full_path)

                # Borrado de fuentes pesadas
                for font in fonts_to_delete:
                    try:
                        os.remove(font)
                    except OSError:
                        pass

                # 2. MULTIHILO: imágenes en paralelo (workers adaptados a la CPU del sistema)
                workers = min(8, os.cpu_count() or 2)
                
                def optimize_wrapper(path):
                    is_cover = Path(path).name in cover_files
                    self._optimize_image(path, is_cover)
                    
                with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
                    list(executor.map(optimize_wrapper, image_tasks))

                # 2b. Actualizar OPF: reflejar extensiones en el manifiesto
                self._patch_opf_images(temp_dir, cover_files)

                # 3. HTML: optimizar con splitting iterativo (procesa los _part2 recién creados)
                html_queue = list(html_tasks)
                while html_queue:
                    html_path = html_queue.pop(0)
                    nuevos = self._optimize_and_split_html(html_path, opf_modifier_queue, cover_files)
                    html_queue.extend(nuevos)

                # 4. Parchear OPF, toc.ncx (EPUB 2) y nav.xhtml (EPUB 3) si hubo splits
                self._patch_opf_manifest(temp_dir, opf_modifier_queue)
                self._patch_ncx(temp_dir, opf_modifier_queue)
                self._patch_nav(temp_dir, opf_modifier_queue)

                # 5. Empaquetar respetando el estándar EPUB (mimetype primero y sin compresión)
                out_name = f"{epub.stem}_{self.device_name}.epub"
                out_path = epub.parent / out_name

                with zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                    mimetype_path = os.path.join(temp_dir, 'mimetype')
                    if os.path.exists(mimetype_path):
                        zf.write(mimetype_path, 'mimetype', compress_type=zipfile.ZIP_STORED)

                    for root, _, files in os.walk(temp_dir):
                        for file in files:
                            if file == 'mimetype' and root == temp_dir:
                                continue
                            file_path = os.path.join(root, file)
                            arcname   = os.path.relpath(file_path, temp_dir)
                            zf.write(file_path, arcname)

                print(T['SAVED_OK'].format(out_name))

            except Exception as e:
                print(T['PROC_ERROR'].format(epub.name, e))

    # ----------------------------------------------------------
    # IMÁGENES: optimizador de fondos de pantalla
    # ----------------------------------------------------------
    def optimize_wallpapers(self, folder_path):
        """
        Optimiza imágenes sueltas (.jpg/.png/.bmp) como fondos de pantalla
        para el dispositivo activo (X3, X4 o X4p). Mismo pipeline que el EPUB:
          1. Descarta imágenes decorativas (<= 15 px).
          2. Reduce resolución al perfil del dispositivo (thumbnail LANCZOS).
          3. Aplana canal Alpha sobre fondo blanco.
          4. Convierte a escala de grises de 8 bits.
          5. Dithering Floyd-Steinberg cuantizado a los 4 grises nativos
             del panel E-Ink: #000000 / #555555 / #AAAAAA / #FFFFFF.
          6. Guarda como BMP 24 bits RGB (sin CLUT) con sufijo _X3 / _X4 / _X4p.
             No toca el fichero original.
        """
        T = self.T
        if not folder_path:
            print(T['INVALID_PATH'])
            return
        path = Path(folder_path)
        if not path.is_dir():
            print(T['INVALID_PATH'])
            return

        suffix = f"_{self.device_name}"

        image_exts = ('.jpg', '.jpeg', '.png', '.bmp', '.webp', '.gif')
        images = [
            f for f in path.iterdir()
            if f.is_file()
            and f.suffix.lower() in image_exts
            and not f.stem.endswith(('_X3', '_X4', '_X4p'))
        ]

        if not images:
            print(T['NO_IMAGES'])
            return

        print(T['FOUND_IMAGES'].format(len(images)))

        # Paleta de 4 grises nativos del panel E-Ink (igual que en _optimize_image)
        palette_img = create_4gray_palette_image()

        for idx, img_path in enumerate(sorted(images), start=1):
            try:
                img = Image.open(img_path)

                # 1. Descartar miniaturas decorativas
                if img.width <= 15 or img.height <= 15:
                    img.close()
                    print(f"[{idx}/{len(images)}]" + T['IMG_SKIPPED'].format(img_path.name))
                    continue

                # 2. Reducir al límite de pantalla del dispositivo
                img.thumbnail((self.max_width, self.max_height), Image.Resampling.LANCZOS)

                # 3. Aplanar canal Alpha sobre fondo blanco
                if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1])
                    img = background

                # 4. Escala de grises 8 bit
                img = img.convert('L')

                # 5. Dithering Floyd-Steinberg a los 4 grises nativos del panel
                #    NOTA: quantize(palette=...) requiere modo RGB en Pillow; convertimos antes.
                img = img.convert('RGB').quantize(palette=palette_img, dither=Image.Dither.FLOYDSTEINBERG)

                # 6. Guardar como BMP 24 bits RGB (sin CLUT, máxima compatibilidad)
                out_name = f"{img_path.stem}{suffix}.bmp"
                out_path = img_path.parent / out_name
                img.convert('RGB').save(str(out_path))
                img.close()

                print(f"[{idx}/{len(images)}]" + T['IMG_SAVED_OK'].format(out_name))

            except Exception as e:
                logging.warning("[WALLPAPER SKIP] %s: %s", img_path.name, e)
                print(f"[{idx}/{len(images)}]" + T['IMG_ERROR'].format(img_path.name, e))

        print(T['IMG_SUCCESS'])

    def run_wallpaper_optimization(self):
        """Flujo UI para optimizar imágenes sueltas como fondos de pantalla.
        Usa la carpeta de trabajo ya seleccionada (self.folder_path)."""
        T = self.T
        clear_screen()
        print_banner(T['BANNER_CONFIG'])
        if not self.folder_path or not Path(self.folder_path).is_dir():
            print(T['INVALID_PATH'])
            return
        self.optimize_wallpapers(self.folder_path)

    # ----------------------------------------------------------
    # OPTIMIZACIÓN: lote de EPUBs o archivo individual
    # ----------------------------------------------------------
    def run_optimization(self):
        T    = self.T
        path = Path(self.folder_path)
        if not path.exists():
            print(T['INVALID_PATH'])
            return

        # Si el usuario seleccionó un único archivo .epub
        if path.is_file():
            if path.suffix.lower() == '.epub':
                self.process_single_epub(path, current=1, total=1)
                print(T['SUCCESS_ALL'])
            else:
                print(T['INVALID_PATH'])
            return

        epubs = [e for e in path.glob('*.epub') if not e.stem.endswith(('_X3', '_X4', '_X4p'))]

        if not epubs:
            print(T['NO_EPUBS'])
            return

        print(T['FOUND_EPUBS'].format(len(epubs)))

        total = len(epubs)
        for idx, epub in enumerate(epubs, start=1):
            self.process_single_epub(epub, current=idx, total=total)

        print(T['SUCCESS_ALL'])

    # ----------------------------------------------------------
    # UI: selección de carpeta o archivo
    # ----------------------------------------------------------
    def select_folder(self):
        T = self.T
        clear_screen()
        print_banner(T['BANNER_CONFIG'])
        print(T['FOLDER_INTRO'])
        entered = input_path(T['FOLDER_PROMPT'].format(self.folder_path))
        if entered:
            self.folder_path = entered
        if not self.folder_path:
            self.folder_path = os.getcwd()
        save_config({'folder_path': str(self.folder_path)})

    # ----------------------------------------------------------
    # UI: menú interactivo
    # ----------------------------------------------------------
    def show_menu(self):
        T = self.T
        while True:
            clear_screen()
            print_banner(T['BANNER_MENU'])
            print(T['ACTIVE_FOLDER'].format(self.folder_path))
            print(T['ACTIVE_DEVICE'].format(self.device_name, self.max_width, self.max_height))

            sim_label = T['SIM_LABEL'] if self.dry_run else ""
            print(T['ACTIONS_HEADER'].format(sim_label))
            print(T['MENU_1'])
            print(T['MENU_2_ON'] if self.dry_run else T['MENU_2_OFF'])
            print(T['MENU_3'])
            print(T['MENU_4'])
            print(T['MENU_5'])
            print(T['MENU_0'])

            choice = input(T['SELECT_OPTION']).strip()

            if choice == '1':
                self.run_optimization()
                input(T['PRESS_ENTER'])
            elif choice == '2':
                self.dry_run = not self.dry_run
            elif choice == '3':
                self.select_folder()
            elif choice == '4':
                self.select_device()
                input(T['PRESS_ENTER'])
            elif choice == '5':
                self.run_wallpaper_optimization()
                input(T['PRESS_ENTER'])
            elif choice == '0':
                print(T['EXIT_MSG'])
                sys.exit(0)
            else:
                input(T['UNKNOWN_CMD'])

    # ----------------------------------------------------------
    # PUNTO DE ENTRADA INTERACTIVO
    # ----------------------------------------------------------
    def start(self):
        T = self.T
        try:
            saved_config = load_config()

            # Si ya se ha configurado anteriormente, saltamos directamente al menú
            if not saved_config.get('onboarding_done', False):
                clear_screen()
                print(T['LXML_ON'] if _LXML_AVAILABLE else T['LXML_OFF'])
                print()
                print(T['PROMO_START'])
                print(f"\n{T['PROMO_END']}")

                user_choice = input(T['CONTINUE_PROMPT']).strip().upper()
                if user_choice not in ('S', 'Y'):
                    print(T['GOODBYE'])
                    sys.exit(0)

                self.select_device()
                self.select_folder()
                save_config({'onboarding_done': True})

            self.show_menu()
        except KeyboardInterrupt:
            print(T['INTERRUPT'])
            sys.exit(0)


def main():
    parser = argparse.ArgumentParser(description="Optimizador de EPUBs para dispositivos Xteink (X3, X4, X4 Pro).")
    parser.add_argument("path", nargs="?", default=None, help="Ruta a una carpeta de EPUBs o a un archivo .epub individual.")
    parser.add_argument("--device", "-d", choices=["X3", "X4", "X4p"], default=None, help="Modelo objetivo (X3, X4, X4p).")
    parser.add_argument("--dry-run", action="store_true", help="Ejecutar en modo simulación sin modificar archivos.")

    args = parser.parse_args()

    lang = get_ui_language()
    T = TEXTS[lang]
    app = XteinkOptimizerApp(T)

    # Modo CLI no interactivo si se pasa argumento de ruta
    if args.path:
        target_path = Path(args.path.strip('"\'')).resolve()
        if not target_path.exists():
            print(f"[ERROR] Ruta no encontrada: {target_path}")
            sys.exit(1)

        app.folder_path = str(target_path)
        if args.device:
            app.device_name = args.device
            profile = DEVICE_PROFILES[app.device_name]
            app.max_width = profile['max_width']
            app.max_height = profile['max_height']

        app.dry_run = args.dry_run
        print(f"[CLI] Modo directo: {app.folder_path} | Dispositivo: Xteink {app.device_name} | Dry-run: {app.dry_run}")
        app.run_optimization()
    else:
        app.start()


if __name__ == "__main__":
    main()
