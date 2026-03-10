import sys
from epub_modules.utils import logger, get_system_language, clear_screen, print_banner, input_path
from epub_modules.renamer import RenamerModule
from epub_modules.optimizer import OptimizerModule
from epub_modules.lang_cleaner import LangCleanerModule
from epub_modules.dupe_finder import DupeFinderModule

class EPUBMasterApp:
    def __init__(self):
        self.lang = get_system_language()
        self.folder_path = None
        
        # Modules
        self.renamer = RenamerModule()
        self.optimizer = OptimizerModule()
        self.cleaner = LangCleanerModule()
        self.dupe_finder = DupeFinderModule()

    def select_folder(self):
        clear_screen()
        print_banner("EPUB MASTER SUITE - CONFIGURACIÓN")
        print("Por favor, selecciona la carpeta donde tienes tu biblioteca de libros.")
        self.folder_path = input_path("Ruta de la carpeta (Enter para actual): ")
        logger.set_folder(self.folder_path)

    def run_diagnostics(self):
        clear_screen()
        print_banner("ANÁLISIS DE BIBLIOTECA")
        print(f"Analizando: {self.folder_path}\n")
        
        # Ejecutar análisis rápidos
        # Usamos límites razonables para feedback rápido
        print("1. Analizando nombres de archivos...", end='\r')
        stats_rename = self.renamer.analyze(self.folder_path, limit=200)
        print(f"1. Nombres:    Detectados ~{stats_rename['needs_action']} {stats_rename['description']}.")
        
        print("2. Buscando duplicados...", end='\r')
        stats_dupe = self.dupe_finder.analyze(self.folder_path, limit=200)
        print(f"2. Duplicados: Detectados ~{stats_dupe['needs_action']} {stats_dupe['description']}.")
        
        print("3. Escaneando idiomas...", end='\r')
        stats_lang = self.cleaner.analyze(self.folder_path, limit=500)
        print(f"3. Idiomas:    Detectados ~{stats_lang['needs_action']} {stats_lang['description']}.")
        
        print("4. Comprobando optimización...", end='\r')
        stats_opt = self.optimizer.analyze(self.folder_path, limit=20)
        print(f"4. Optimizar:  Detectados ~{stats_opt['needs_action']} {stats_opt['description']}.")
        
        print("\n" + "-"*60)

    def show_menu(self):
        while True:
            self.run_diagnostics()
            print("\nACCIONES DISPONIBLES:")
            print(" [1] Renombrar Archivos (Formato: Apellido, Nombre - Titulo)")
            print(" [2] Gestionar Duplicados")
            print(" [3] Limpiar Idiomas (Borrar [EN], [FR], etc.)")
            print(" [4] Optimizar EPUBs (Reducir tamaño)")
            print(" [5] Cambiar Carpeta")
            print(" [0] Salir")
            
            choice = input("\nSelecciona una opción: ").strip()
            
            if choice == '1':
                self.renamer.run(self.folder_path)
            elif choice == '2':
                self.dupe_finder.run(self.folder_path)
            elif choice == '3':
                self.cleaner.run(self.folder_path)
            elif choice == '4':
                self.optimizer.run(self.folder_path)
            elif choice == '5':
                self.select_folder()
            elif choice == '0':
                print("¡Hasta luego!")
                logger.close()
                sys.exit(0)
            else:
                input("Opción no válida. Enter para continuar...")
            
            if choice in ['1', '2', '3', '4']:
                input("\nOperación completada. Presiona ENTER para volver al menú...")

    def start(self):
        try:
            clear_screen()
            print("-" * 63)
            print("EPUB Master Suite es un programa freeware que unifica tus herramientas")
            print("de gestión de libros electrónicos: Renombrado, Optimización,")
            print("Limpieza de idiomas y búsqueda de Duplicados.")
            print("-" * 63)
            print("Si el programa te ha sido útil invítame a un café en paypal.me/ossoney.")
            print("-" * 63 + "\n")
            
            self.select_folder()
            self.show_menu()
        except KeyboardInterrupt:
            print("\n\nSalida forzada por el usuario.")
            logger.close()
            sys.exit(0)

if __name__ == "__main__":
    app = EPUBMasterApp()
    app.start()
