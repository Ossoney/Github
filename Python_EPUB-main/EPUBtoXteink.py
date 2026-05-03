import sys
import os
import zipfile
import logging
import locale
import builtins
import concurrent.futures
from pathlib import Path
import tempfile

# =========================================================
# LOGGER: externalizado a Documentos para evitar bloat en Git
# =========================================================
DOCUMENTS_DIR = Path.home() / "Documents" / "Epubbiblio"
DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)
LOG_PATH = DOCUMENTS_DIR / 'EPUBtoXteink.log'

logging.basicConfig(
    filename=str(LOG_PATH),
    level=logging.INFO,
    format='%(asctime)s | %(message)s',
    encoding='utf-8'
)

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
# LOCALIZACIÓN
# =========================================================

def get_ui_language():
    """Devuelve 'es' si el sistema está en español, 'en' en el resto de casos."""
    try:
        default_locale = locale.getlocale()[0]
        if default_locale and default_locale.lower().startswith('es'):
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

        # Selección de carpeta
        'FOLDER_INTRO':  "Selecciona la carpeta donde guardas tus EPUB.",
        'FOLDER_PROMPT': "Ruta de la carpeta (Enter para usar la actual): ",

        # Menú
        'ACTIVE_FOLDER':  "Carpeta activa: {}",
        'SIM_LABEL':      " [ESTADO DE SIMULACIÓN]",
        'ACTIONS_HEADER': "\nACCIONES DISPONIBLES{}:",
        'MENU_1':         " [1] Iniciar Optimización Híper-acelerada (Multihilo + Splitting de RAM)",
        'MENU_2_ON':      " [2] Desactivar Modo Simulación (Dry-Run)",
        'MENU_2_OFF':     " [2] Activar Modo Simulación (Dry-Run)",
        'MENU_3':         " [3] Cambiar Carpeta de Biblioteca",
        'MENU_0':         " [0] Salir",
        'SELECT_OPTION':  "\nSelecciona una opción: ",
        'PRESS_ENTER':    "\nPresiona ENTER para volver al menú...",
        'UNKNOWN_CMD':    "Comando no reconocido. Presiona ENTER para continuar...",
        'EXIT_MSG':       "\n¡Desconectando sistemas! Hasta luego.",

        # Procesamiento
        'INVALID_PATH':  "\nError: La ruta seleccionada no es válida.",
        'NO_EPUBS':      "\nNo se encontraron archivos EPUB originales en esta carpeta.",
        'FOUND_EPUBS':   "\n[INFO] Se encontraron {} libros. Arrancando motores...",
        'SUCCESS_ALL':   "\n -> [ÉXITO TOTAL] Optimización terminada.",
        'SIM_EPUB':      "[SIMULACIÓN] Optimizaría usando Multihilo y Splitting: {}",
        'PROCESSING':    "\n -> Procesando: {}",
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

        # Folder selection
        'FOLDER_INTRO':  "Select the folder where your EPUBs are stored.",
        'FOLDER_PROMPT': "Folder path (press Enter to use current): ",

        # Menu
        'ACTIVE_FOLDER':  "Active folder: {}",
        'SIM_LABEL':      " [SIMULATION MODE]",
        'ACTIONS_HEADER': "\nAVAILABLE ACTIONS{}:",
        'MENU_1':         " [1] Start Hyper-Accelerated Optimization (Multithreading + RAM Splitting)",
        'MENU_2_ON':      " [2] Disable Simulation Mode (Dry-Run)",
        'MENU_2_OFF':     " [2] Enable Simulation Mode (Dry-Run)",
        'MENU_3':         " [3] Change Library Folder",
        'MENU_0':         " [0] Exit",
        'SELECT_OPTION':  "\nSelect an option: ",
        'PRESS_ENTER':    "\nPress ENTER to return to the menu...",
        'UNKNOWN_CMD':    "Unknown command. Press ENTER to continue...",
        'EXIT_MSG':       "\nShutting down! Goodbye.",

        # Processing
        'INVALID_PATH':  "\nError: The selected path is not valid.",
        'NO_EPUBS':      "\nNo original EPUB files found in this folder.",
        'FOUND_EPUBS':   "\n[INFO] Found {} books. Starting engines...",
        'SUCCESS_ALL':   "\n -> [COMPLETE] Optimization finished.",
        'SIM_EPUB':      "[SIMULATION] Would optimize using Multithreading and Splitting: {}",
        'PROCESSING':    "\n -> Processing: {}",
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
        self.folder_path = None
        self.dry_run = False

        self.max_width  = 758
        self.max_height = 1024

        # Tamaño crítico a partir del cual el lector crashea (~300 KB)
        self.max_html_size = 300 * 1024

    # ----------------------------------------------------------
    # IMAGEN: Grises + Alpha flatten + Resize + Floyd-Steinberg
    # ----------------------------------------------------------
    def _optimize_image(self, file_path):
        """
        Pipeline completo de imagen para e-readers:
          1. Elimina miniaturas decorativas (<= 15 px).
          2. Reduce resolución al máximo del dispositivo.
          3. Aplana canal Alpha sobre fondo blanco (evita fondo negro).
          4. Convierte a escala de grises de 8 bits.
          5. Aplica dithering Floyd-Steinberg a 16 niveles de gris
             para mejorar el contraste en pantallas E-Ink.
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
            #    Sin esto, PNGs con transparencia se renderizan con fondo negro.
            if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1])  # Canal Alpha como máscara
                img = background

            # 4. Convertir a escala de grises de 8 bit
            img = img.convert('L')

            # 5. Dithering Floyd-Steinberg a 16 niveles de gris.
            #    quantize() descompone la imagen en la paleta más cercana usando F-S.
            #    Convirtiendo de vuelta a 'L' obtenemos grises suaves sin pérdida de bits.
            img = img.quantize(colors=16, dither=Image.Dither.FLOYDSTEINBERG).convert('L')

            img.save(file_path, optimize=True, quality=80)
            img.close()
            return "optimized"
        except Exception:
            return "skipped"

    # ----------------------------------------------------------
    # HTML: purga de elementos pesados
    # ----------------------------------------------------------
    def _purge_html_soup(self, soup):
        """Elimina scripts, estilos e iframes que el e-reader no puede manejar."""
        for tag in soup(["script", "style", "iframe", "base", "canvas", "video", "audio"]):
            tag.decompose()

        for tag in soup.find_all(True):
            if tag.has_attr('style'):
                del tag['style']
            if tag.has_attr('class'):
                del tag['class']
        return soup

    def _optimize_and_split_html(self, file_path, opf_modifier_queue):
        """Purga el HTML. Si supera 300 KB lo divide en dos partes y anota el split para el OPF."""
        T = self.T
        try:
            file_size = os.path.getsize(file_path)

            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            soup = BeautifulSoup(content, HTML_PARSER)
            soup = self._purge_html_soup(soup)

            # Si el archivo excede el tamaño crítico de memoria del dispositivo
            if file_size > self.max_html_size and soup.body:
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

            # Sobrescribir Parte 1 (ya sin la segunda mitad)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))

        except Exception:
            pass

    # ----------------------------------------------------------
    # OPF: parchar manifiesto tras el splitting
    # ----------------------------------------------------------
    def _patch_opf_manifest(self, temp_dir, split_queue):
        """Busca el .opf y re-enlaza los capítulos _part2 generados por el split."""
        if not split_queue:
            return

        for root, _, files in os.walk(temp_dir):
            for file in files:
                if not file.endswith('.opf'):
                    continue

                opf_path = os.path.join(root, file)

                try:
                    with open(opf_path, 'r', encoding='utf-8') as f:
                        soup = BeautifulSoup(f.read(), 'xml')

                    manifest = soup.find('manifest')
                    spine    = soup.find('spine')

                    if manifest and spine:
                        for orig_filename, part2_filename in split_queue:
                            # CORRECCIÓN CRÍTICA: buscar por nombre final del href
                            # para funcionar aunque sea "Text/capitulo.xhtml"
                            orig_item = None
                            for item in manifest.find_all('item'):
                                href = item.get('href', '')
                                if Path(href).name == orig_filename:
                                    orig_item = item
                                    break

                            if orig_item:
                                orig_href  = orig_item.get('href', orig_filename)
                                part2_href = str(Path(orig_href).with_name(part2_filename))
                                part2_id   = f"{orig_item.get('id', 'item')}_part2"

                                new_manifest_el = soup.new_tag(
                                    'item',
                                    href=part2_href,
                                    id=part2_id,
                                    **{'media-type': orig_item.get('media-type', 'application/xhtml+xml')}
                                )
                                orig_item.insert_after(new_manifest_el)

                                spine_item = spine.find('itemref', idref=orig_item.get('id'))
                                if spine_item:
                                    new_spine_el = soup.new_tag('itemref', idref=part2_id)
                                    spine_item.insert_after(new_spine_el)

                    with open(opf_path, 'w', encoding='utf-8') as f:
                        f.write(str(soup))

                except Exception:
                    pass

                return  # Solo hay 1 OPF por epub

    # ----------------------------------------------------------
    # PIPELINE PRINCIPAL: 1 EPUB
    # ----------------------------------------------------------
    def process_single_epub(self, epub):
        """Orquesta la extracción, multiprocesamiento, split y reempaquetado de 1 epub."""
        T = self.T
        if self.dry_run:
            print(T['SIM_EPUB'].format(epub.name))
            return

        print(T['PROCESSING'].format(epub.name))
        opf_modifier_queue = []

        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temp_dir:
            try:
                # 1. Descomprimir
                with zipfile.ZipFile(epub, 'r') as zf:
                    zf.extractall(temp_dir)

                # Clasificar archivos por tipo
                image_tasks    = []
                html_tasks     = []
                fonts_to_delete = []

                for root, _, files in os.walk(temp_dir):
                    for file in files:
                        full_path = os.path.join(root, file)
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

                # 2. MULTIHILO: imágenes en paralelo (8 workers)
                with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
                    list(executor.map(self._optimize_image, image_tasks))

                # 3. HTML: optimizar y detectar capítulos gigantes
                for html_path in html_tasks:
                    self._optimize_and_split_html(html_path, opf_modifier_queue)

                # 4. Parchear el OPF si hubo splits
                self._patch_opf_manifest(temp_dir, opf_modifier_queue)

                # 5. Empaquetar respetando el estándar EPUB (mimetype primero y sin compresión)
                out_name = f"{epub.stem}_Xteink.epub"
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
    # OPTIMIZACIÓN: lote de EPUBs
    # ----------------------------------------------------------
    def run_optimization(self):
        T    = self.T
        path = Path(self.folder_path)
        if not path.is_dir():
            print(T['INVALID_PATH'])
            return

        epubs = [e for e in path.glob('*.epub') if not e.stem.endswith('_Xteink')]

        if not epubs:
            print(T['NO_EPUBS'])
            return

        print(T['FOUND_EPUBS'].format(len(epubs)))

        for epub in epubs:
            self.process_single_epub(epub)

        print(T['SUCCESS_ALL'])

    # ----------------------------------------------------------
    # UI: selección de carpeta
    # ----------------------------------------------------------
    def select_folder(self):
        T = self.T
        clear_screen()
        print_banner(T['BANNER_CONFIG'])
        print(T['FOLDER_INTRO'])
        self.folder_path = input_path(T['FOLDER_PROMPT'])
        if not self.folder_path:
            self.folder_path = os.getcwd()

    # ----------------------------------------------------------
    # UI: menú interactivo
    # ----------------------------------------------------------
    def show_menu(self):
        T = self.T
        while True:
            clear_screen()
            print_banner(T['BANNER_MENU'])
            print(T['ACTIVE_FOLDER'].format(self.folder_path))

            sim_label = T['SIM_LABEL'] if self.dry_run else ""
            print(T['ACTIONS_HEADER'].format(sim_label))
            print(T['MENU_1'])
            print(T['MENU_2_ON'] if self.dry_run else T['MENU_2_OFF'])
            print(T['MENU_3'])
            print(T['MENU_0'])

            choice = input(T['SELECT_OPTION']).strip()

            if choice == '1':
                self.run_optimization()
                input(T['PRESS_ENTER'])
            elif choice == '2':
                self.dry_run = not self.dry_run
            elif choice == '3':
                self.select_folder()
            elif choice == '0':
                print(T['EXIT_MSG'])
                sys.exit(0)
            else:
                input(T['UNKNOWN_CMD'])

    # ----------------------------------------------------------
    # PUNTO DE ENTRADA
    # ----------------------------------------------------------
    def start(self):
        T = self.T
        try:
            clear_screen()

            # Aviso del motor HTML (diferido aquí para que salga en el idioma correcto)
            print(T['LXML_ON'] if _LXML_AVAILABLE else T['LXML_OFF'])
            print()

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


if __name__ == "__main__":
    lang = get_ui_language()
    T    = TEXTS[lang]
    app  = XteinkOptimizerApp(T)
    app.start()
