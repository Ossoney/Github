"""
PDFtoCBZ.py - Conversión y optimización inteligente de PDF a CBZ (Comic Book Zip).
Incluye:
 - Menú amigable completo TUI
 - Perfiles de dispositivo configurables
 - División de doble página (Double-page split) con orientación (LTR / RTL)
 - Modo simulación (Dry-Run) y modo desatendido (CLI)
 - Selector de carpetas gráfico (Tkinter) y de consola
 - Multiprocesamiento paralelo de páginas
 - Traslado seguro a ORIGINAL/
"""

import argparse
import concurrent.futures
import io
import locale
import logging
import os
import shutil
import sys
import tempfile
import time
import zipfile
from pathlib import Path
from typing import List, Optional, Tuple

import fitz  # PyMuPDF
import numpy as np
from PIL import Image, ImageEnhance

from common import (
    DEVICE_PROFILES,
    clear_screen,
    print_banner,
    select_folder_dialog,
    input_path_with_fallback,
    split_double_page_if_needed,
    is_blank_or_black_page,
)

# =========================================================
# LOGGER UNIFICADO
# =========================================================
BASE_DIR = Path(__file__).resolve().parent
LOG_PATH = BASE_DIR / 'PDFCBZtoEPUB.log'

logger = logging.getLogger("PDFtoCBZ")
logger.setLevel(logging.INFO)
if not logger.handlers:
    _fh = logging.FileHandler(str(LOG_PATH), encoding='utf-8')
    _fh.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(message)s'))
    _sh = logging.StreamHandler(sys.stdout)
    _sh.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(message)s'))
    logger.addHandler(_fh)
    logger.addHandler(_sh)

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
            "PDFtoCBZ optimiza tus cómics en PDF ahorrando espacio de almacenamiento\n"
            "al convertirlos en CBZ (Comic Book Zip) y acelerando la lectura.\n"
            "Los archivos originales se conservan intactos en la carpeta ORIGINAL/."
        ),
        'PROMO_END': (
            "---------------------------------------------------------------\n"
            "Si el programa te ha sido útil invítame a un café en paypal.me/ossoney.\n"
            "Envíame 1$ - 2$ - 3$ o lo que te apetezca.\n"
            "---------------------------------------------------------------"
        ),
        'CONTINUE_PROMPT': "\n¿Deseas continuar (S/N)?: ",
        'GOODBYE': "\nOperación cancelada. ¡Gracias por usar PDFtoCBZ!",
        'BANNER_MENU': "PDF TO CBZ - MENÚ PRINCIPAL",
        'BANNER_CONFIG': "PDF TO CBZ - CONFIGURACIÓN",
        'FOLDER_INTRO': "Selecciona la carpeta de PDFs ('g' para diálogo gráfico):",
        'FOLDER_PROMPT': "Ruta ('g' para diálogo, Enter para carpeta actual): ",
        'ACTIVE_FOLDER': "Carpeta activa: {}",
        'SIM_LABEL': " [SIMULACIÓN]",
        'ACTIONS_HEADER': "\nACCIONES DISPONIBLES{}:",
        'MENU_1': "Iniciar Conversión a CBZ",
        'MENU_2_ON': "Desactivar Modo Simulación (Dry-Run)",
        'MENU_2_OFF': "Activar Modo Simulación (Dry-Run)",
        'MENU_3': "Cambiar Carpeta",
        'MENU_4': "Incluir Subcarpetas: {}",
        'MENU_5': "Perfil Dispositivo: {}",
        'MENU_6': "Dividir Páginas Dobles: {}",
        'MENU_7': "Dirección Lectura: {}",
        'MENU_8': "Eliminar Páginas Vacías (B/N): {}",
        'MENU_0': "Salir",
        'SELECT_OPTION': "\nSelecciona una opción: ",
        'PRESS_ENTER': "\nPresiona ENTER para volver al menú...",
        'UNKNOWN_CMD': "Comando no reconocido. Presiona ENTER para continuar...",
        'EXIT_MSG': "\n¡Desconectando sistemas! Hasta luego.",
        'INVALID_PATH': "\nError: La ruta seleccionada no es válida.",
        'NO_FILES': "\nNo se encontraron archivos PDF en esta carpeta.",
        'FOUND_FILES': "\n[INFO] Se encontraron {} archivos PDF. Arrancando motores...",
        'PROCESSING': "\n → Procesando: {}",
        'SKIP_EXISTS': " → [SKIP] Ya existe: {}",
        'SAVED_OK': " → [OK] Guardado: {} ({:.1f} MB)",
        'MOVED_OK': " → [OK] Original trasladado a: ORIGINAL/{}",
        'SUCCESS_ALL': "\n → [COMPLETADO] Conversión terminada.",
        'SUMMARY_TITLE': "RESUMEN DE CONVERSIÓN",
        'ON': 'SÍ',
        'OFF': 'NO',
        'LTR': 'Occidental (Izq. a Der.)',
        'RTL': 'Manga (Der. a Izq.)',
    },
    'en': {
        'PROMO_START': (
            "PDFtoCBZ optimizes your PDF comics, saving storage space by converting\n"
            "them to CBZ (Comic Book Zip) and speeding up loading times.\n"
            "Original files are kept safe inside the ORIGINAL/ directory."
        ),
        'PROMO_END': (
            "---------------------------------------------------------------\n"
            "If the program was useful, buy me a coffee at paypal.me/ossoney.\n"
            "Send $1 - $2 - $3 or whatever you feel like.\n"
            "---------------------------------------------------------------"
        ),
        'CONTINUE_PROMPT': "\nDo you want to continue (Y/N)?: ",
        'GOODBYE': "\nOperation cancelled. Thank you for using PDFtoCBZ!",
        'BANNER_MENU': "PDF TO CBZ - MAIN MENU",
        'BANNER_CONFIG': "PDF TO CBZ - CONFIGURATION",
        'FOLDER_INTRO': "Select the PDF folder ('g' for GUI dialog):",
        'FOLDER_PROMPT': "Folder path ('g' for GUI dialog, Enter for current): ",
        'ACTIVE_FOLDER': "Active folder: {}",
        'SIM_LABEL': " [SIMULATION]",
        'ACTIONS_HEADER': "\nAVAILABLE ACTIONS{}:",
        'MENU_1': "Start Conversion to CBZ",
        'MENU_2_ON': "Disable Simulation Mode (Dry-Run)",
        'MENU_2_OFF': "Enable Simulation Mode (Dry-Run)",
        'MENU_3': "Change Folder",
        'MENU_4': "Include Subfolders: {}",
        'MENU_5': "Device Profile: {}",
        'MENU_6': "Split Double Pages: {}",
        'MENU_7': "Reading Direction: {}",
        'MENU_8': "Remove Blank Pages (B/W): {}",
        'MENU_0': "Exit",
        'SELECT_OPTION': "\nSelect an option: ",
        'PRESS_ENTER': "\nPress ENTER to return to menu...",
        'UNKNOWN_CMD': "Unrecognized command. Press ENTER to continue...",
        'EXIT_MSG': "\nShutting down systems! Goodbye.",
        'INVALID_PATH': "\nError: The selected path is not valid.",
        'NO_FILES': "\nNo PDF files found in this folder.",
        'FOUND_FILES': "\n[INFO] Found {} PDF files. Starting engines...",
        'PROCESSING': "\n → Processing: {}",
        'SKIP_EXISTS': " → [SKIP] Already exists: {}",
        'SAVED_OK': " → [OK] Saved: {} ({:.1f} MB)",
        'MOVED_OK': " → [OK] Original moved to: ORIGINAL/{}",
        'SUCCESS_ALL': "\n → [COMPLETE] Conversion finished.",
        'SUMMARY_TITLE': "CONVERSION SUMMARY",
        'ON': 'YES',
        'OFF': 'NO',
        'LTR': 'Western (Left-to-Right)',
        'RTL': 'Manga (Right-to-Left)',
    }
}

# 3 MODOS AUTOMÁTICOS
KCC_MODOS = {
    'normal': {'dpi': 1.4, 'calidad': 75},
    'alta': {'dpi': 1.6, 'calidad': 80},
    'pdf_like': {'extraer_original': True}
}

def detectar_problema_calidad(img: Image.Image, pdf_nombre: str) -> str:
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
    except Exception:
        return 'normal'

def modo_pdf_like(doc: fitz.Document, temp_dir: Path, npags: int) -> None:
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
                    except Exception: pass
            else:
                pix = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0))
                img = Image.open(io.BytesIO(pix.tobytes("ppm")))
                nombre = temp_dir / f"{contador:04d}.jpg"
                img.save(nombre, "JPEG", quality=95)
            contador += 1
        except Exception:
            pass

def optimizar_kcc_oasis(imagen: Image.Image, profile_key: str = 'default') -> Image.Image:
    if imagen.mode != 'RGB':
        imagen = imagen.convert('RGB')
    ancho_orig, alto_orig = imagen.size
    conf_profile = DEVICE_PROFILES.get(profile_key, DEVICE_PROFILES['default'])
    max_w = conf_profile['max_width']
    max_h = conf_profile['max_height']

    if ancho_orig > max_w or alto_orig > max_h:
        ratio = min(max_w / ancho_orig, max_h / alto_orig)
        nuevo_tam = (int(ancho_orig * ratio), int(alto_orig * ratio))
        img = imagen.resize(nuevo_tam, Image.Resampling.LANCZOS)
    else:
        img = imagen.copy()

    img = ImageEnhance.Contrast(img).enhance(1.10)
    img = ImageEnhance.Sharpness(img).enhance(1.05)

    try:
        img_array = np.array(img)
        diff = (np.mean(np.abs(img_array[:, :, 0].astype(float) - img_array[:, :, 1].astype(float))) +
                np.mean(np.abs(img_array[:, :, 1].astype(float) - img_array[:, :, 2].astype(float))))
        if diff < 5.0:
            img = img.convert('L')
    except Exception:
        pass
    return img

def _procesar_pagina_pdf_worker(args):
    pdf_path_str, page_idx, dpi_usar, calidad_usar, out_file_str, profile_key, split_double, reading_dir, remove_blank, is_protected = args
    try:
        doc = fitz.open(pdf_path_str)
        pagina = doc.load_page(page_idx)
        pix = pagina.get_pixmap(matrix=fitz.Matrix(dpi_usar, dpi_usar))
        img = Image.open(io.BytesIO(pix.tobytes("ppm")))
        doc.close()

        # Si se solicita eliminar páginas vacías y no está protegida como portada
        if remove_blank and not is_protected and is_blank_or_black_page(img):
            return True, True  # processed, is_blank

        sub_images = [img]
        if split_double:
            sub_images = split_double_page_if_needed(img, reading_direction=reading_dir)

        out_base = Path(out_file_str)
        if len(sub_images) == 1:
            img_opt = optimizar_kcc_oasis(sub_images[0], profile_key=profile_key)
            img_opt.save(out_base, "JPEG", quality=calidad_usar, optimize=True)
        else:
            for part_idx, sub_img in enumerate(sub_images, 1):
                if remove_blank and not is_protected and is_blank_or_black_page(sub_img):
                    continue
                part_out = out_base.parent / f"{out_base.stem}_{part_idx}.jpg"
                img_opt = optimizar_kcc_oasis(sub_img, profile_key=profile_key)
                img_opt.save(part_out, "JPEG", quality=calidad_usar, optimize=True)
        return True, False
    except Exception:
        return False, False

def crear_zip_desde_temp(temp_dir: Path, cbz_path: Path):
    imgs = sorted(list(temp_dir.glob("*.*")))
    if not imgs: return False
    with zipfile.ZipFile(cbz_path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for img in imgs:
            zf.write(img, img.name)
    return True

def convertir_pdf_kcc(pdf_path: Path, profile_key: str = 'default',
                      split_double: bool = False, reading_dir: str = 'ltr',
                      remove_blank: bool = True) -> Tuple[Optional[Path], float]:
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

        modo = 'normal'
        if npags > 0:
            try:
                pagina_test = doc.load_page(0)
                pix_test = pagina_test.get_pixmap(matrix=fitz.Matrix(1.5, 1.5))
                img_test = Image.open(io.BytesIO(pix_test.tobytes("ppm")))
                modo = detectar_problema_calidad(img_test, pdf_path.name)
            except Exception:
                pass

        logger.info(f"   🎯 Modo seleccionado: {modo.upper()}")

        if modo == 'pdf_like':
            modo_pdf_like(doc, temp_dir, npags)
        else:
            conf = KCC_MODOS[modo]
            dpi_usar = conf['dpi']
            calidad_usar = conf['calidad']
            tasks = [
                (str(pdf_path), i, dpi_usar, calidad_usar, str(temp_dir / f"{i+1:04d}.jpg"),
                 profile_key, split_double, reading_dir, remove_blank, (i == 0))
                for i in range(npags)
            ]
            workers = max(2, min(os.cpu_count() or 4, 8))
            with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
                res = list(executor.map(_procesar_pagina_pdf_worker, tasks))
            blank_count = sum(1 for _, was_blank in res if was_blank)
            if blank_count > 0:
                logger.info(f"   🗑️  {blank_count} páginas vacías eliminadas (en blanco/negro)")

        if not crear_zip_desde_temp(temp_dir, cbz_path):
            doc.close(); doc = None
            return None, 0

        # FAIL-SAFE: Si resulta mayor que el original
        tam_final = cbz_path.stat().st_size
        if tam_final > tam_original and modo != 'pdf_like':
            diff_mb = (tam_final - tam_original) / (1024 * 1024)
            logger.warning(f"⚠️ RESULTADO MÁS GRANDE (+{diff_mb:.1f}MB). Activando protocolo PDF-Like...")
            cbz_path.unlink()
            shutil.rmtree(temp_dir)
            temp_dir = Path(tempfile.mkdtemp(prefix="cbz_retry_"))
            modo_pdf_like(doc, temp_dir, npags)
            crear_zip_desde_temp(temp_dir, cbz_path)
            tam_final = cbz_path.stat().st_size
            modo = "PDF-LIKE (RETRY)"

        doc.close(); doc = None
        tam_orig_mb = tam_original / (1024 * 1024)
        tam_final_mb = tam_final / (1024 * 1024)
        variacion_pct = ((tam_final - tam_original) / tam_original * 100) if tam_original > 0 else 0
        tiempo = time.time() - inicio

        logger.info(f"✅ {tam_orig_mb:.1f} -> {tam_final_mb:.1f}MB ({variacion_pct:+.1f}%) [{modo.upper()}] [{tiempo:.1f}s]")
        return cbz_path, variacion_pct

    except Exception as e:
        logger.error(f"❌ ERROR: {e}")
        if cbz_path.exists():
            try: os.remove(cbz_path)
            except Exception: pass
        return None, 0
    finally:
        if doc is not None:
            try: doc.close()
            except Exception: pass
        shutil.rmtree(temp_dir, ignore_errors=True)

# =========================================================
# APLICACIÓN INTERACTIVA
# =========================================================
class PDFtoCBZApp:
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
        self.metrics = {'total': 0, 'exitos': 0, 'ahorro': 0.0, 'moved': 0}

    def scan_files(self) -> List[Path]:
        p = Path(self.folder_path)
        if self.include_subfolders:
            return sorted(list(p.rglob("*.pdf")))
        return sorted(list(p.glob("*.pdf")))

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

        todos = self.scan_files()
        if not todos:
            print(T['NO_FILES'])
            return

        print(T['FOUND_FILES'].format(len(todos)))
        self.metrics = {'total': len(todos), 'exitos': 0, 'ahorro': 0.0, 'moved': 0}

        for pdf in todos:
            cbz_target = pdf.with_suffix('.cbz')
            if cbz_target.exists():
                print(T['SKIP_EXISTS'].format(cbz_target.name))
                continue

            if self.dry_run:
                orig_size = pdf.stat().st_size
                print(f"[SIMULACIÓN] {pdf.name} (PDF → CBZ)")
                print(f"    ↳ Perfil: {DEVICE_PROFILES.get(self.profile, {}).get('name')}")
                print(f"    ↳ Dobles: {T['ON'] if self.split_double else T['OFF']} | Dirección: {self.reading_direction.upper()}")
                try: rel = pdf.relative_to(self.folder_path)
                except Exception: rel = Path(pdf.name)
                print(f"    ↳ Traslado: ORIGINAL/{rel}")
                self.metrics['exitos'] += 1
                continue

            cbz_path, variacion = convertir_pdf_kcc(
                pdf, profile_key=self.profile,
                split_double=self.split_double, reading_dir=self.reading_direction,
                remove_blank=self.remove_blank
            )
            if cbz_path and cbz_path.exists():
                self.metrics['exitos'] += 1
                self.metrics['ahorro'] += (variacion * -1)
                try:
                    base_path = Path(self.folder_path)
                    try: rel = pdf.relative_to(base_path)
                    except ValueError: rel = Path(pdf.name)
                    dest = base_path / 'ORIGINAL' / rel
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(pdf), str(dest))
                    print(T['MOVED_OK'].format(rel))
                    self.metrics['moved'] += 1
                except Exception as e:
                    print(f"   ⚠️ Error trasladando archivo: {e}")

        print("\n" + "=" * 60)
        print(f"🎉 COMPLETADO: {self.metrics['exitos']}/{len(todos)} CBZ creados")
        if self.metrics['exitos'] > 0 and not self.dry_run:
            print(f"📊 Reducción media: {self.metrics['ahorro']/self.metrics['exitos']:.1f}%")
        print("=" * 60)

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
    parser = argparse.ArgumentParser(description="PDF to CBZ Optimizer")
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
        app = PDFtoCBZApp(
            T, folder=args.input, profile=args.profile, dry_run=args.dry_run,
            subfolders=args.subfolders, split_double=args.split_double, reading_dir=args.direction,
            remove_blank=args.remove_blank
        )
        app.run_conversion()
    else:
        app = PDFtoCBZApp(T)
        app.start()

if __name__ == "__main__":
    main()
