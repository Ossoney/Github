import os
import sys
import time
from pathlib import Path

from pdf_modules.utils import (
    logger,
    get_system_language,
    clear_screen,
    print_banner,
    input_path,
    ask_yes_no,
    COMMON_TEXTS
)
from pdf_modules.dupe_finder import DupeFinderModule

# =========================================================
# CACHE DE DIAGNÓSTICO
# =========================================================

DIAGNOSTICS_CACHE_TTL = 30  # segundos

class PDFDupeApp:
    def __init__(self):
        self.lang = get_system_language()
        self.folder_path = None
        self.dry_run = False
        self.recursive = True

        # Módulo de duplicados
        self.dupe_finder = DupeFinderModule()

        # Cache de diagnóstico
        self._diag_cache = None
        self._diag_cache_time = 0

    def select_folder(self):
        clear_screen()
        print_banner("PDF DUPE FINDER - DETECTOR DE DUPLICADOS")
        print("Por favor, selecciona la carpeta donde tienes tu colección de libros PDF.")
        self.folder_path = input_path("Ruta de la carpeta (Enter para actual): ")
        logger.set_folder(self.folder_path)
        self._invalidate_cache()

    def _invalidate_cache(self):
        self._diag_cache = None
        self._diag_cache_time = 0

    def run_diagnostics(self):
        now = time.time()
        if self._diag_cache and (now - self._diag_cache_time) < DIAGNOSTICS_CACHE_TTL:
            clear_screen()
            print_banner("ANÁLISIS DE BIBLIOTECA PDF")
            modo_sub = " (Incluyendo subcarpetas)" if self.recursive else " (Solo carpeta raíz)"
            print(f"Directorio: {self.folder_path}{modo_sub}\n")
            stats_dupe = self._diag_cache
            print(f"Total PDFs analizados: {stats_dupe['total_files']}")
            print(f"Duplicados potenciales: ~{stats_dupe['needs_action']} {stats_dupe['description']}.")
            print("\n" + "-" * 65)
            return self._diag_cache

        clear_screen()
        print_banner("ANÁLISIS DE BIBLIOTECA PDF")
        modo_sub = " (Incluyendo subcarpetas)" if self.recursive else " (Solo carpeta raíz)"
        print(f"Directorio: {self.folder_path}{modo_sub}\n")

        print("Analizando biblioteca de libros...", end='\r')
        stats_dupe = self.dupe_finder.analyze(self.folder_path, recursive=self.recursive)
        print(" " * 65, end='\r')
        print(f"Total PDFs analizados: {stats_dupe['total_files']}")
        print(f"Duplicados potenciales: ~{stats_dupe['needs_action']} {stats_dupe['description']}.")
        print("\n" + "-" * 65)

        self._diag_cache = stats_dupe
        self._diag_cache_time = now
        return self._diag_cache

    def _show_dry_run_status(self):
        return " [MODO SIMULACIÓN ACTIVO]" if self.dry_run else ""

    def show_menu(self):
        while True:
            self.run_diagnostics()
            dry_status = self._show_dry_run_status()
            sub_status = "ACTIVADA" if self.recursive else "DESACTIVADA"
            print(f"\nACCIONES DISPONIBLES{dry_status}:")
            print(" [1] Buscar y Gestionar Duplicados (Auto + Revisión Asistida)")
            
            dry_label = "Desactivar" if self.dry_run else "Activar"
            print(f" [2] {dry_label} Modo Simulación (Dry Run)")
            print(f" [3] Alternar búsqueda en Subcarpetas (Actual: {sub_status})")
            print(" [4] Cambiar Carpeta de Trabajo")
            print(" [0] Salir")

            choice = input("\nSelecciona una opción: ").strip()

            if choice == '1':
                clear_screen()
                print_banner("GESTIÓN DE DUPLICADOS")
                self.dupe_finder.run(self.folder_path, dry_run=self.dry_run, recursive=self.recursive)
                self._invalidate_cache()
                input("\nPresione ENTER para continuar...")

            elif choice == '2':
                self.dry_run = not self.dry_run
                status_txt = "ACTIVADO (no se moverán archivos)" if self.dry_run else "DESACTIVADO (se moverán archivos)"
                print(f"\nModo Simulación {status_txt}")
                time.sleep(1.2)

            elif choice == '3':
                self.recursive = not self.recursive
                self._invalidate_cache()
                nuevo = "ACTIVADA (busca en todas las subcarpetas)" if self.recursive else "DESACTIVADA (solo carpeta raíz)"
                print(f"\nBúsqueda en subcarpetas {nuevo}")
                time.sleep(1.2)

            elif choice == '4':
                self.select_folder()

            elif choice == '0':
                clear_screen()
                print("Gracias por usar PDF Dupe Finder. ¡Hasta pronto!")
                logger.close()
                sys.exit(0)

            else:
                print("Opción no válida.")
                time.sleep(1)

def main():
    app = PDFDupeApp()
    try:
        app.select_folder()
        app.show_menu()
    except KeyboardInterrupt:
        print("\n\nOperación cancelada por el usuario.")
        logger.close()
        sys.exit(0)
    except Exception as e:
        import traceback
        print("\n" + "=" * 65)
        print("SE PRODUJO UN ERROR INESPERADO:")
        print("=" * 65)
        traceback.print_exc()
        input("\nPresione ENTER para salir...")
        logger.close()
        sys.exit(1)

if __name__ == "__main__":
    main()
