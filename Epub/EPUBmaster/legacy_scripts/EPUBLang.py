import os
import sys
import argparse
import locale
import re
import shutil
import datetime
from collections import defaultdict
from typing import Dict, List, Set, Tuple, Optional

# --- CONFIGURACIÓN E CONSTANTES XERAIS ---
EPUB_EXTENSIONS = ('.epub',)
LOG_FILENAME = '.EPUBTagCleaner.log'

# Etiquetas de idioma a buscar (se usan en mayúsculas para la búsqueda).
LANGUAGE_TAGS: Set[str] = {"[CA]", "[EO]", "[EN]", "[GAL]"} 

# ------------------------------------------\

# --- FUNCIONALIDADE DE LOGGING ---
LOG_FILE_HANDLE = None

def log_print(message, end='\n'):
    """Imprime a mensaxe na consola e escríbea no arquivo de log."""
    print(message, end=end)
    if LOG_FILE_HANDLE:
        LOG_FILE_HANDLE.write(message + end)

def write_log(folder_path: str, message: str):
    """Escribe unha mensaxe no arquivo de rexistro coa marca de tempo."""
    log_path = os.path.join(folder_path, LOG_FILENAME)
    timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    try:
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(f"{timestamp} {message}\n")
    except Exception:
        pass # Non imprimir erro de log na consola para manter a limpeza.
# ----------------------------------\

# --- LOCALIZACIÓN DE TEXTOS ---\
def get_ui_language():
    """Detecta o idioma do sistema (es, en) para a interface."""
    try:
        default_locale = locale.getlocale()[0]
        if default_locale and default_locale.lower().startswith('es'):
            return 'es'
    except Exception:
        pass
    return 'en'

TEXTS = {
    'es': {
        # MENSAXES PROMOCIONAIS NOVOS
        'PROMO_START': """+---------------------------------------------------------------+
EPUBLang es un programa freeware que optimiza tu biblioteca EPUB
mostrándote los archivos en idiomas distintos al español, por si
quieres borrarlos y ahorrar espacio de almacenamiento.
[CA]-catalán, [EO]-euskera, [FR]-francés, [EN]-inglés.
+---------------------------------------------------------------+""",
        'PROMO_END': """---------------------------------------------------------------
Si el programa te ha sido útil invítame a un café en paypal.me/ossoney.
Envíame 1$ - 2$ - 3$ o lo que te apetezca.
---------------------------------------------------------------""",
        'CONTINUE_PROMPT': "\n¿Deseas continuar con la detección y borrado de idiomas (S/N)?: ",
        'GOODBYE_MESSAGE': "Operación cancelada. ¡Gracias por usar EPUBTagCleaner!",

        # MENSAXES DE CARPETA
        'STARTING_MESSAGE': "Iniciando EPUBTagCleaner...",
        'FOLDER_PROMPT': "Ruta de la carpeta a procesar: ",
        'FOLDER_DEFAULT': "Dejar vacío para procesar la carpeta actual (./): ",
        'PATH_ERROR': "Error: La ruta '{}' no es un directorio válido.",
        'NO_EPUB_FILES': "No se encontraron archivos .epub en la carpeta: {}",
        
        # MENSAXES DO MÓDULO (LINGUAXE)
        'M3_TITLE': "--- INICIANDO DEPURADOR DE IDIOMAS ---",
        'M3_TAGS_SEARCH': "Etiquetas de idioma a buscar: {}",
        'M3_SCAN_TOTAL': "Archivos escaneados en total:",
        'M3_FILES_WITH_TAGS': "Archivos con etiquetas:",
        'M3_TAGS_FOUND_TITLE': "--- ETIQUETAS ENCONTRADAS ---",
        'M3_GROUP_TITLE': "\n--- Archivos con la etiqueta [{}] ({} archivos) ---",
        # CORRECCIÓN AQUÍ: Quitamos el (S/N) de la traducción original
        'M3_ASK_DELETE': "\n¿Deseas ELIMINAR permanentemente TODOS los {} archivos con la etiqueta [{}]?: ", 
        'M3_ENTER_TAG': "Introduce la etiqueta (ej: EN) que deseas borrar, o 'N' para cancelar: ",
        'M3_INVALID_TAG': "Etiqueta no válida. Por favor, introduce una de las etiquetas mostradas.",
        'M3_DELETE_CONFIRMED': "BORRADO INICIADO: Eliminando {} archivos para la etiqueta {}.",
        'M3_DELETE_CANCELED': "Eliminación cancelada. Los archivos se mantienen intactos.",
        'M3_DELETING_FILE': "  - Borrando: {}",
        'M3_DELETE_ERROR': "  [ERROR] No se pudo borrar: {}",
        'M3_DELETE_SUCCESS': "✅ ¡Eliminación completada! Se borraron {} archivos con la etiqueta {}.",
        'M3_PROCESS_COMPLETE': "Proceso terminado.",
    },
    'en': {
        # PROMOTIONAL MESSAGES (English translation)
        'PROMO_START': """+---------------------------------------------------------------+
EPUBLang is a freeware program that optimizes your EPUB library
by showing you files in languages ​​other than Spanish, in case
you want to delete them and save storage space.
[CA]-Catalan, [EO]-Basque, [FR]-French, [EN]-English.
+---------------------------------------------------------------+""",
        'PROMO_END': """---------------------------------------------------------------
If the program was useful, invite me for a coffee at paypal.me/ossoney.
Send $1 - $2 - $3 or whatever you feel like.
---------------------------------------------------------------""",
        'CONTINUE_PROMPT': "\nDo you want to continue with language detection and deletion (Y/N)?: ",
        'GOODBYE_MESSAGE': "Operation canceled. Thank you for using EPUBTagCleaner!",

        # FOLDER MESSAGES
        'STARTING_MESSAGE': "Starting EPUBLang...",
        'FOLDER_PROMPT': "Path to the folder to process: ",
        'FOLDER_DEFAULT': "Leave empty to process the current folder (./): ",
        'PATH_ERROR': "Error: Path '{}' is not a valid directory.",
        'NO_EPUB_FILES': "No .epub files found in the folder: {}",

        # MODULE MESSAGES (LANGUAGE CLEANER)
        'M3_TITLE': "--- STARTING LANGUAGE CLEANER ---",
        'M3_TAGS_SEARCH': "Language tags to search for: {}",
        'M3_SCAN_TOTAL': "Total files scanned:",
        'M3_FILES_WITH_TAGS': "Files with tags:",
        'M3_TAGS_FOUND_TITLE': "--- FOUND TAGS ---",
        'M3_GROUP_TITLE': "\n--- Files with tag [{}] ({} files) ---",
        # CORRECCIÓN AQUÍ: Quitamos el (Y/N) de la traducción original
        'M3_ASK_DELETE': "\nDo you want to permanently DELETE ALL {} files with tag [{}]?: ",
        'M3_ENTER_TAG': "Enter the tag (e.g., EN) you want to delete, or 'N' to cancel: ",
        'M3_INVALID_TAG': "Invalid tag. Please enter one of the displayed tags.",
        'M3_DELETE_CONFIRMED': "DELETION STARTED: Deleting {} files for tag {}.",
        'M3_DELETE_CANCELED': "Deletion canceled. Files remain intact.",
        'M3_DELETING_FILE': "  - Deleting: {}",
        'M3_DELETE_ERROR': "  [ERROR] Could not delete: {}",
        'M3_DELETE_SUCCESS': "✅ Deletion complete! Deleted {} files with tag {}.",
        'M3_PROCESS_COMPLETE': "Process finished.",
    }
}
# --------------------------------\


# --- FUNCIONALIDAD CENTRAL DE DETECCIÓN Y BORRADO ---

def find_tagged_files(folder_path: str) -> Tuple[int, int, Dict[str, List[str]]]:
    """Busca archivos .epub con etiquetas de idioma (ej: [CA]) y los agrupa, buscando recursivamente."""
    
    results: Dict[str, List[str]] = defaultdict(list)
    total_scanned = 0
    files_with_tags = 0
    
    # Lista de etiquetas completas para búsqueda (ej: "[CA]", "[EN]")
    known_tags = LANGUAGE_TAGS
    
    # os.walk busca recursivamente en todas las subcarpetas.
    for root, _, files in os.walk(folder_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            
            # 1. Comprobar la extensión .epub (insensible a mayúsculas/minúsculas)
            if os.path.splitext(filename)[1].lower() in EPUB_EXTENSIONS:
                total_scanned += 1
                
                found_tag = None
                
                # 2. Buscar si alguna de las etiquetas conocidas existe en el nombre.
                for tag in known_tags:
                    if tag in filename:
                        # Hemos encontrado una etiqueta conocida
                        found_tag = tag
                        break # Salir tan pronto como se encuentre una etiqueta
                
                if found_tag:
                    files_with_tags += 1
                    # Almacenamos la ruta completa del archivo y usamos la etiqueta encontrada (ej: "[CA]")
                    results[found_tag].append(file_path)
                        
    return total_scanned, files_with_tags, results

def display_results(results: Dict[str, List[str]], T: Dict[str, str]):
    """Muestra las etiquetas y los archivos encontrados."""
    
    if not results:
        return

    log_print("\n" + "="*50)
    log_print(T['M3_TAGS_FOUND_TITLE'])
    log_print("="*50)
    
    for tag, file_list in sorted(results.items()):
        # Utiliza el nombre sin corchetes para el título (ej: EN)
        tag_display = tag.strip('[]') 
        log_print(T['M3_GROUP_TITLE'].format(tag_display, len(file_list)))
        for file_path in file_list:
            log_print(f"  - {os.path.basename(file_path)}")
    log_print("="*50)

def ask_and_delete_language_tag(folder_path: str, results: Dict[str, List[str]], T: Dict[str, str]):
    """Pregunta qué etiqueta borrar y ejecuta la eliminación."""
    
    available_tags = {tag.strip('[]').upper() for tag in results.keys()}
    
    while True:
        target_tag_input = input(T['M3_ENTER_TAG']).strip().upper()
        
        if target_tag_input == 'N':
            write_log(folder_path, T['M3_DELETE_CANCELED'])
            log_print(T['M3_DELETE_CANCELED'])
            return
        
        target_tag = f"[{target_tag_input}]"
        
        if target_tag in results:
            break
        
        log_print(T['M3_INVALID_TAG'])
        log_print(f"Tags disponibles: {', '.join(sorted(available_tags))}")

    # Confirmación de borrado
    files_to_delete = results[target_tag]
    total_to_delete = len(files_to_delete)
    
    # Se añade (S/N) o (Y/N) según el idioma para la confirmación
    confirmation_char = 'S' if get_ui_language() == 'es' else 'Y'

    # Corrección: Simplificamos el prompt para que solo añada el sufijo (S/N) una vez
    prompt_suffix = f"({confirmation_char}/N): " 

    user_confirmation = input(T['M3_ASK_DELETE'].format(total_to_delete, target_tag_input) + prompt_suffix).strip().upper()
    
    if user_confirmation == confirmation_char:
        write_log(folder_path, T['M3_DELETE_CONFIRMED'].format(total_to_delete, target_tag))
        log_print(T['M3_DELETE_CONFIRMED'].format(total_to_delete, target_tag))
        
        deleted_count = 0
        
        for file_path in files_to_delete:
            filename = os.path.basename(file_path)
            log_print(T['M3_DELETING_FILE'].format(filename))
            try:
                os.remove(file_path)
                deleted_count += 1
                write_log(folder_path, f"BORRADO EXITOSO: {filename}")
            except Exception as e:
                log_print(T['M3_DELETE_ERROR'].format(filename))
                write_log(folder_path, f"ERROR AL BORRAR {filename}: {e}")
                
        final_log = T['M3_DELETE_SUCCESS'].format(deleted_count, target_tag)
        log_print(final_log)
        write_log(folder_path, final_log)
        
    else:
        log_print(T['M3_DELETE_CANCELED'])
        write_log(folder_path, T['M3_DELETE_CANCELED'])


def run_tag_cleaner_module(folder_path: str, T: Dict[str, str]):
    """Función principal del Depurador de Idiomas."""
    
    # --- DEPURACIÓN: Verifica la ruta que se está procesando ---
    log_print(f"\n[DEBUG] Ruta de procesamiento ABSOLUTA: {folder_path}")
    if not os.path.isdir(folder_path):
        log_print(f"[DEBUG] ERROR: {folder_path} NO ES UN DIRECTORIO VÁLIDO.")
        return 
    # -----------------------------------------------------------

    # 1. Inicialización de log
    global LOG_FILE_HANDLE
    log_file_path = os.path.join(folder_path, LOG_FILENAME)
    try:
        if LOG_FILE_HANDLE: LOG_FILE_HANDLE.close()
        LOG_FILE_HANDLE = open(log_file_path, 'a', encoding='utf-8') 
        write_log(folder_path, f"\n{T['M3_TITLE']}")
    except Exception as e:
        print(f"[ERROR] No se pudo abrir el archivo de log: {e}")
        LOG_FILE_HANDLE = None
    
    log_print(T['M3_TITLE'])
    write_log(folder_path, T['M3_TAGS_SEARCH'].format(LANGUAGE_TAGS))
    
    try:
        # 2. Ejecutar la búsqueda y agrupar los resultados
        total_scanned, files_with_tags, results = find_tagged_files(folder_path)
        
        # 3. Resumen
        log_print("\n" + "="*50)
        log_print(f"{T['M3_SCAN_TOTAL']:<25} {total_scanned} archivos")
        log_print(f"{T['M3_FILES_WITH_TAGS']:<25} {files_with_tags} archivos")
        log_print("="*50)
        
        if total_scanned == 0:
            log_print(T['NO_EPUB_FILES'].format(folder_path))
            return
            
        if not results:
            log_print(f"No se encontraron etiquetas de idioma {LANGUAGE_TAGS} en los {total_scanned} archivos .epub escaneados.")
            return
            
        # 4. Mostrar resultados y preguntar por borrado
        display_results(results, T)
        ask_and_delete_language_tag(folder_path, results, T)
        
    except Exception as e:
        log_print(f"[ERROR FATAL] Fallo en el módulo: {e}")
        write_log(folder_path, f"[ERROR FATAL] {e}")
    finally:
        log_print(f"\n{T['M3_PROCESS_COMPLETE']}")
        write_log(folder_path, T['M3_PROCESS_COMPLETE'])
        
        # Cerrar log
        if LOG_FILE_HANDLE:
            LOG_FILE_HANDLE.close()
            LOG_FILE_HANDLE = None


# --- LÓGICA PRINCIPAL DEL PROGRAMA ---
def main():
    
    # 1. Detección de idioma y textos
    LANG = get_ui_language()
    T = TEXTS[LANG]
    
    # 2. Imprimir el nuevo banner promocional de inicio
    print(T['PROMO_START'])
    print(T['PROMO_END'])
    
    # 3. Preguntar si desea continuar (S/N)
    user_choice = input(T['CONTINUE_PROMPT']).strip().upper()
    
    if user_choice not in ('S', 'Y'):
        print(T['GOODBYE_MESSAGE'])
        sys.exit(0) # Salir del programa

    # 4. Configuración de ruta
    parser = argparse.ArgumentParser(description=T['STARTING_MESSAGE'])
    parser.add_argument('folder', nargs='?', default='.', help=T['FOLDER_PROMPT'])
    args = parser.parse_args()

    folder_path = os.path.abspath(args.folder)
    
    if args.folder == '.':
        prompt_msg = T['FOLDER_PROMPT'] + T['FOLDER_DEFAULT']
        user_input = input(prompt_msg).strip()
        if user_input:
            folder_path = os.path.abspath(user_input)
    
    if not os.path.isdir(folder_path):
        print(T['PATH_ERROR'].format(folder_path))
        sys.exit(1)

    # 5. Ejecutar el limpiador de etiquetas (única función)
    run_tag_cleaner_module(folder_path, T)
    
    # 6. Imprimir banner de finalización
    print(T['PROMO_END'])


if __name__ == "__main__":
    main()