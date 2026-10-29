"""
main.py - Lanzador y Centro de Control de la Suite PDFCBZtoEPUB.
Permite ejecutar de forma unificada:
 1. Cómic (CBZ / CBR) → EPUB Fixed-Layout
 2. PDF (Cómics / Libros) → CBZ Optimizer
 3. PDF (Texto / Escáner) → EPUB Inteligente
 O invocar el modo CLI desatendido para automatizaciones masivas.
"""

import argparse
import os
import sys
from pathlib import Path

from common import (
    clear_screen,
    print_banner,
    select_folder_dialog,
    input_path_with_fallback,
    DEVICE_PROFILES,
)
import CBZtoEPUB
import PDFtoCBZ
import PDFtoEPUB

def show_main_menu():
    folder = os.getcwd()
    while True:
        clear_screen()
        print_banner("PDFCBZ TO EPUB - CENTRO DE CONTROL")
        print(f" Carpeta activa actual: {folder}\n")
        print(" ╔══════════════════════════════════════════════════════════╗")
        print(" ║  [ 1 ]  Cómics (CBZ / CBR) ➔ EPUB Fixed-Layout           ║")
        print(" ║  [ 2 ]  PDFs Cómics ➔ CBZ Optimizer                      ║")
        print(" ║  [ 3 ]  PDFs Libros / Escáner ➔ EPUB Inteligente         ║")
        print(" ╟──────────────────────────────────────────────────────────╢")
        print(" ║  [ 4 ]  Cambiar carpeta activa                           ║")
        print(" ║  [ 5 ]  Ver registro de actividad (PDFCBZtoEPUB.log)     ║")
        print(" ╟──────────────────────────────────────────────────────────╢")
        print(" ║  [ 0 ]  Salir                                            ║")
        print(" ╚══════════════════════════════════════════════════════════╝")

        opt = input("\nSelecciona una opción: ").strip()

        if opt == '1':
            lang = CBZtoEPUB.get_ui_language()
            app = CBZtoEPUB.CBZtoEPUBApp(CBZtoEPUB.TEXTS[lang], folder=folder)
            app.show_menu()
        elif opt == '2':
            lang = PDFtoCBZ.get_ui_language()
            app = PDFtoCBZ.PDFtoCBZApp(PDFtoCBZ.TEXTS[lang], folder=folder)
            app.show_menu()
        elif opt == '3':
            lang = PDFtoEPUB.get_ui_language()
            app = PDFtoEPUB.PDFtoEPUBApp(PDFtoEPUB.TEXTS[lang], folder=folder)
            app.show_menu()
        elif opt == '4':
            clear_screen()
            print_banner("CAMBIAR CARPETA ACTIVA")
            print("Introduce la ruta o escribe 'g' para abrir el explorador de carpetas:")
            nueva = input_path_with_fallback("Ruta ('g' para diálogo, Enter para mantener): ", allow_dialog=True)
            if nueva and Path(nueva).is_dir():
                folder = nueva
        elif opt == '5':
            clear_screen()
            print_banner("ÚLTIMOS REGISTROS (PDFCBZtoEPUB.log)")
            log_p = Path(__file__).resolve().parent / "PDFCBZtoEPUB.log"
            if log_p.exists():
                lines = log_p.read_text(encoding='utf-8', errors='replace').splitlines()
                for line in lines[-25:]:
                    print(f" {line}")
            else:
                print(" Aún no existe el archivo de log.")
            input("\nPresiona ENTER para volver al menú...")
        elif opt == '0':
            print("\n¡Hasta pronto!")
            sys.exit(0)
        else:
            input("\nOpción no válida. Presiona ENTER para continuar...")

def main():
    parser = argparse.ArgumentParser(description="PDFCBZtoEPUB - Suite Integral de Conversión de Libros y Cómics")
    parser.add_argument("-t", "--task", choices=["cbz2epub", "pdf2cbz", "pdf2epub"], help="Tarea a realizar en modo CLI")
    parser.add_argument("-i", "--input", help="Carpeta de origen con los archivos a procesar")
    parser.add_argument("-p", "--profile", choices=list(DEVICE_PROFILES.keys()), default="default", help="Perfil de dispositivo de destino")
    parser.add_argument("--subfolders", action="store_true", help="Incluir subcarpetas recursivamente")
    parser.add_argument("--split-double", action="store_true", help="Dividir páginas dobles")
    parser.add_argument("--direction", choices=["ltr", "rtl"], default="ltr", help="Dirección de lectura: ltr u rtl")
    parser.add_argument("--remove-blank", action="store_true", default=True, help="Eliminar páginas en blanco o en negro (activado por defecto)")
    parser.add_argument("--no-remove-blank", dest="remove_blank", action="store_false", help="No eliminar páginas en blanco o en negro")
    parser.add_argument("--dry-run", action="store_true", help="Modo simulación sin escribir cambios en disco")

    args = parser.parse_args()

    if args.task and args.input:
        folder = args.input
        if args.task == "cbz2epub":
            lang = CBZtoEPUB.get_ui_language()
            app = CBZtoEPUB.CBZtoEPUBApp(
                CBZtoEPUB.TEXTS[lang], folder=folder, profile=args.profile, dry_run=args.dry_run,
                subfolders=args.subfolders, split_double=args.split_double, reading_dir=args.direction,
                remove_blank=args.remove_blank
            )
            app.run_conversion()
        elif args.task == "pdf2cbz":
            lang = PDFtoCBZ.get_ui_language()
            app = PDFtoCBZ.PDFtoCBZApp(
                PDFtoCBZ.TEXTS[lang], folder=folder, profile=args.profile, dry_run=args.dry_run,
                subfolders=args.subfolders, split_double=args.split_double, reading_dir=args.direction,
                remove_blank=args.remove_blank
            )
            app.run_conversion()
        elif args.task == "pdf2epub":
            lang = PDFtoEPUB.get_ui_language()
            app = PDFtoEPUB.PDFtoEPUBApp(
                PDFtoEPUB.TEXTS[lang], folder=folder, profile=args.profile, dry_run=args.dry_run,
                subfolders=args.subfolders, split_double=args.split_double, reading_dir=args.direction,
                remove_blank=args.remove_blank
            )
            app.run_conversion()
    else:
        show_main_menu()

if __name__ == "__main__":
    main()
