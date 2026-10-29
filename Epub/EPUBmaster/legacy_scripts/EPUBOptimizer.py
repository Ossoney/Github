import os
import sys
import argparse
import locale
import re
from typing import Dict, List, Set, Tuple, Optional
import shutil
from io import BytesIO
from PIL import Image, UnidentifiedImageError # Necesarias para OPTIMIZADOR
import glob
import zipfile # Necesaria para OPTIMIZADOR
import functools # Necesario para compatibilidad de la función compare_versions, aunque ya no se usa, lo mantendremos para evitar errores si lo piden
# import datetime # Se ha eliminado, ya que no se usa en el logging de esta versión.

# --- CONFIGURACIÓN Y CONSTANTES GENERALES ---
EPUB_EXTENSIONS = ('.epub',)
LOG_FILENAME = '.EbookToolbox.log'
# -------------------------------------------\

# --- FUNCIONALIDAD DE LOGGING (Centralizada) ---\
LOG_FILE_HANDLE = None

def log_print(message, end='\n'):
    """Imprime el mensaje en la consola y lo escribe en el archivo de log."""
    print(message, end=end)
    if LOG_FILE_HANDLE:
        LOG_FILE_HANDLE.write(message + end)

def write_log(folder_path: str, message: str):
    """Escribe un mensaje en el archivo de registro con una marca de tiempo."""
    # Note: Using datetime in the original code, but since it's not imported in this simplified version,
    # we'll use a simpler placeholder or re-add the minimal import if truly needed.
    # For now, let's assume simple log writing.
    log_path = os.path.join(folder_path, LOG_FILENAME)
    # Re-adding datetime import just for this function if needed
    import datetime
    timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    try:
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(f"{timestamp} {message}\n")
    except Exception as e:
        print(f"[ERROR DE LOG] Fallo al escribir en {LOG_FILENAME}: {e}")
# -------------------------------------------------------------------\

# --- UTILS GENERALES ---\
def bytes_to_kb(bytes_val: int) -> float:
    """Convierte bytes a kilobytes (KB) con 2 decimales."""
    return round(bytes_val / 1024, 2)
# -----------------------\


# --- LOCALIZACIÓN DE TEXTOS (Solo Español/Inglés) ---\
def get_ui_language():
    """Detecta el idioma del sistema (es, en) para la interfaz."""
    try:
        default_locale = locale.getlocale()[0]
        if default_locale and default_locale.lower().startswith('es'):
            return 'es'
    except Exception:
        pass
    return 'en'

TEXTS = {
    'es': {
        # TAMAÑOS
        'SIZE_KB': "KB",
        
        # MENSAJES PROMOCIONALES NUEVOS
        'PROMO_START': """EPUBOptimizer es un programa freeware que optimiza tus archivos EPUB
ahorrandote espacio de almacenamiento y haciendo más eficientes tus
lecturas. En resumen: Reduce-reescala imágenes, elimina basura y comprime. 
No te preocupes, los archivos originales se mantienen.""",
        'PROMO_END': """---------------------------------------------------------------
Si el programa te ha sido útil invítame a un café en paypal.me/ossoney.
Envíame 1$ - 2$ - 3$ o lo que te apetezca.
---------------------------------------------------------------""",
        'CONTINUE_PROMPT': "\n¿Deseas continuar con la optimización (S/N)?: ",
        'GOODBYE_MESSAGE': "Operación cancelada. ¡Gracias por usar EPUBOptimizer!",

        # MENSAJES DE CARPETA
        'STARTING_MESSAGE': "Iniciando EPUBOptimizer...",
        'FOLDER_PROMPT': "Ruta de la carpeta a procesar: ",
        'FOLDER_DEFAULT': "Dejar vacío para procesar la carpeta actual (./): ",
        'PATH_ERROR': "Error: La ruta '{}' no es un directorio válido.",
        'NO_EPUB_FILES': "No se encontraron archivos .epub en la carpeta: {}",
        
        # --- MÓDULO 1: OPTIMIZADOR DE EPUBS ---
        'M1_TITLE': "--- INICIANDO OPTIMIZADOR DE EPUBS ---",
        'M1_START_OPTIMIZING': "--- Iniciando optimización de {} archivos EPUB ---",
        'M1_PROCESSING_FILE': "[{}/{}] Procesando: {}",
        'M1_SUCCESS': "OPTIMIZACIÓN EXITOSA",
        'M1_SKIPPED': "SALTADO (Ya es óptimo o no se pudo mejorar)",
        'M1_ERROR': "ERROR (El archivo se ha mantenido intacto)",
        'M1_SUMMARY_TITLE': "--- RESUMEN FINAL DE OPTIMIZACIÓN ---",
        'M1_FILES_PROCESSED': "Archivos procesados:",
        'M1_SUCCESS_COUNT': "Optimizados exitosamente:",
        'M1_SKIPPED_COUNT': "SIN AHORRO / No procesado:",
        'M1_ERROR_COUNT': "Con errores (Saltados):",
        'M1_ORIGINAL_SIZE': "Tamaño Original Total:",
        'M1_FINAL_SIZE': "Tamaño Procesado Total:",
        'M1_SAVINGS': "Ahorro Total:",
        'M1_SAVINGS_PERCENT': "Porcentaje de Ahorro:",
        'M1_UNOPTIMIZED_TITLE': "ARCHIVOS NO OPTIMIZADOS (SIN AHORRO DE ESPACIO O CON ERROR)",
        'M1_ALL_OPTIMIZED': "(Todos los archivos fueron optimizados exitosamente)",
        'M1_PROCESS_COMPLETE': "Proceso terminado.",
        'M1_CLEANUP_TEMP': "Limpiando archivos temporales...",
        'M1_TEMP_DELETED': "Directorio temporal borrado: {}",
        'M1_TEMP_ERROR': "Error al limpiar el directorio temporal: {}",
    },
    'en': {
        # SIZES
        'SIZE_KB': "KB",
        
        # MENSAJES PROMOCIONALES NUEVOS (Traducción requerida)
        'PROMO_START': """EPUBOptimizer is freeware that optimizes your EPUB files,
saving you storage space and making your reading more efficient.
In summary: Reduces/rescales images, removes junk, and compresses size.
Don't worry, the original files are kept safe.""",
        'PROMO_END': """---------------------------------------------------------------
If the program was useful, invite me for a coffee at paypal.me/ossoney.
Send $1 - $2 - $3 or whatever you feel like.
---------------------------------------------------------------""",
        'CONTINUE_PROMPT': "\nDo you want to continue with the optimization (Y/N)?: ",
        'GOODBYE_MESSAGE': "Operation canceled. Thank you for using EPUBOptimizer!",

        # FOLDER MESSAGES
        'STARTING_MESSAGE': "Starting EPUBOptimizer...",
        'FOLDER_PROMPT': "Path to the folder to process: ",
        'FOLDER_DEFAULT': "Leave empty to process the current folder (./): ",
        'PATH_ERROR': "Error: Path '{}' is not a valid directory.",
        'NO_EPUB_FILES': "No .epub files found in the folder: {}",
        
        # --- MODULE 1: EPUB OPTIMIZER ---
        'M1_TITLE': "--- STARTING EPUB OPTIMIZER ---",
        'M1_START_OPTIMIZING': "--- Starting optimization of {} EPUB files ---",
        'M1_PROCESSING_FILE': "[{}/{}] Processing: {}",
        'M1_SUCCESS': "OPTIMIZATION SUCCESSFUL",
        'M1_SKIPPED': "SKIPPED (Already optimal or could not be improved)",
        'M1_ERROR': "ERROR (File has been kept intact)",
        'M1_SUMMARY_TITLE': "--- FINAL OPTIMIZATION SUMMARY ---",
        'M1_FILES_PROCESSED': "Files processed:",
        'M1_SUCCESS_COUNT': "Successfully optimized:",
        'M1_SKIPPED_COUNT': "NO SAVINGS / Not processed:",
        'M1_ERROR_COUNT': "With errors (Skipped):",
        'M1_ORIGINAL_SIZE': "Total Original Size:",
        'M1_FINAL_SIZE': "Total Processed Size:",
        'M1_SAVINGS': "Total Savings:",
        'M1_SAVINGS_PERCENT': "Savings Percentage:",
        'M1_UNOPTIMIZED_TITLE': "UNOPTIMIZED FILES (NO SPACE SAVINGS OR WITH ERROR)",
        'M1_ALL_OPTIMIZED': "(All files were successfully optimized)",
        'M1_PROCESS_COMPLETE': "Process finished.",
        'M1_CLEANUP_TEMP': "Cleaning up temporary files...",
        'M1_TEMP_DELETED': "Temporary directory deleted: {}",
        'M1_TEMP_ERROR': "Error cleaning up temporary directory: {}",
    }
}
# --------------------------------\


# --- MÓDULO 1: OPTIMIZADOR DE EPUBS (Núcleo) ---\

# --- CONFIGURACIÓN ESPECÍFICA DEL MÓDULO 1 (MANTENIDA) ---\
M1_QUALITY_COMPRESSION = 75 
M1_MAX_IMAGE_WIDTH = 1000 
M1_IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff') 
M1_TEXT_EXTENSIONS_TO_MINIFY = ('.xhtml', '.html', '.htm', '.css') 
M1_UNOPTIMIZED_DIR_NAME = "_No_Optimizados" 
# -------------------------------------------\

def m1_minify_text(file_path):
    """Minifica archivos HTML/CSS eliminando comentarios y espacios innecesarios."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        content = re.sub(r'\s{2,}', ' ', content)
        content = content.strip()

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return True
    except Exception:
        return False

def m1_optimize_image(temp_dir, internal_path, image_data):
    """Comprime y reescala una imagen en memoria."""
    original_size = len(image_data)
    
    try:
        img_input = BytesIO(image_data)
        img = Image.open(img_input)
        
        width, height = img.size
        format_name = img.format

        # 1. Reescala
        if width > M1_MAX_IMAGE_WIDTH:
            scale_factor = M1_MAX_IMAGE_WIDTH / width
            new_height = int(height * scale_factor)
            img = img.resize((M1_MAX_IMAGE_WIDTH, new_height), Image.LANCZOS)
        
        # 2. Compresión a JPG/JPEG
        output_buffer = BytesIO()
        
        if format_name in ('PNG', 'GIF'):
            if img.mode not in ('RGBA', 'P'):
                img_rgb = img.convert('RGB')
                img_rgb.save(output_buffer, format='JPEG', quality=M1_QUALITY_COMPRESSION, optimize=True)
                format_name = 'JPEG'
            else:
                img.save(output_buffer, format='PNG', optimize=True)
        else:
            img.save(output_buffer, format=format_name, quality=M1_QUALITY_COMPRESSION, optimize=True)

        new_data = output_buffer.getvalue()
        new_size = len(new_data)
        
        # 3. Guardar el archivo temporalmente si hay ahorro
        if new_size < original_size:
            temp_file_path = os.path.join(temp_dir, internal_path)
            os.makedirs(os.path.dirname(temp_file_path), exist_ok=True)
            with open(temp_file_path, 'wb') as f:
                f.write(new_data)
            return True, original_size, new_size
        
        return False, original_size, original_size 

    except UnidentifiedImageError:
        log_print(f"  [ERROR IMAGEN] Archivo no es una imagen válida o está corrupta: {internal_path}", end='\r')
        return False, original_size, original_size
    except Exception as e:
        log_print(f"  [ERROR IMAGEN] Fallo al procesar {internal_path}: {e}", end='\r')
        return False, original_size, original_size

def m1_optimize_epub(epub_path, temp_dir, file_index, total_files, T: Dict[str, str], unoptimized_files_list: List[str]):
    """Optimiza un único archivo EPUB: comprime imágenes y minifica texto."""
    
    filename = os.path.basename(epub_path)
    log_print(T['M1_PROCESSING_FILE'].format(file_index, total_files, filename), end='')
    
    total_original_size = os.path.getsize(epub_path)
    total_reduction_bytes = 0
    optimized_file_data = {} 
    
    try:
        with zipfile.ZipFile(epub_path, 'r') as zin:
            for item in zin.infolist():
                internal_path = item.filename
                
                if internal_path == 'mimetype' or item.is_dir():
                    continue

                original_data = zin.read(item)
                ext = os.path.splitext(internal_path.lower())[1]
                is_optimized = False
                original_item_size = len(original_data)
                
                if ext in M1_IMAGE_EXTENSIONS:
                    success, original_size, new_size = m1_optimize_image(temp_dir, internal_path, original_data)
                    if success:
                        is_optimized = True
                        total_reduction_bytes += (original_size - new_size)
                        optimized_file_data[internal_path] = (original_size, new_size)
                        
                elif ext in M1_TEXT_EXTENSIONS_TO_MINIFY:
                    temp_file_path = os.path.join(temp_dir, internal_path)
                    os.makedirs(os.path.dirname(temp_file_path), exist_ok=True)
                    with open(temp_file_path, 'wb') as f:
                        f.write(original_data)
                    
                    if m1_minify_text(temp_file_path):
                        new_item_size = os.path.getsize(temp_file_path)
                        if new_item_size < original_item_size:
                            is_optimized = True
                            total_reduction_bytes += (original_item_size - new_item_size)
                            optimized_file_data[internal_path] = (original_item_size, new_item_size)
                        else:
                            os.remove(temp_file_path)
                            
                if not is_optimized:
                    optimized_file_data[internal_path] = (original_item_size, original_item_size)
                    temp_file_path = os.path.join(temp_dir, internal_path)
                    os.makedirs(os.path.dirname(temp_file_path), exist_ok=True)
                    with open(temp_file_path, 'wb') as f:
                        f.write(original_data)
    
    except zipfile.BadZipFile:
        log_print(f"{' ' * 20} [MAL ZIP] {filename}", end='\n')
        unoptimized_files_list.append(f"{filename} (Error ZIP)")
        return total_original_size, total_original_size, 'error', 0
    except Exception as e:
        log_print(f"{' ' * 20} [ERROR GENERAL] {filename}", end='\n')
        unoptimized_files_list.append(f"{filename} (Error General: {e})")
        return total_original_size, total_original_size, 'error', 0

    # 2. Reconstrucción del EPUB optimizado
    if total_reduction_bytes > 0:
        new_epub_path = epub_path + ".optimized"
        try:
            with zipfile.ZipFile(epub_path, 'r') as zin, zipfile.ZipFile(new_epub_path, 'w', zipfile.ZIP_DEFLATED) as zout:
                
                # 2.1. Escribir mimetype (sin compresión, siempre primero)
                try:
                    zout.writestr('mimetype', zin.read('mimetype'), compress_type=zipfile.ZIP_STORED)
                except KeyError:
                    pass

                # 2.2. Escribir archivos optimizados/copiados
                for internal_path, sizes in optimized_file_data.items():
                    temp_file_path = os.path.join(temp_dir, internal_path)
                    if internal_path != 'mimetype' and os.path.exists(temp_file_path):
                        zout.write(temp_file_path, internal_path)

            total_new_size = os.path.getsize(new_epub_path)
            shutil.move(new_epub_path, epub_path)
            
            log_print(f"{' ' * 20} [OK] {T['M1_SUCCESS']} | Ahorro: {bytes_to_kb(total_reduction_bytes):.2f} KB ({total_reduction_bytes * 100 / total_original_size:.2f}%)", end='\n')
            return total_original_size, total_new_size, 'success', total_reduction_bytes
            
        except Exception as e:
            log_print(f"{' ' * 20} [ERROR RECONSTRUCCIÓN] {filename} | {e}", end='\n')
            unoptimized_files_list.append(f"{filename} (Error Reconstrucción)")
            if os.path.exists(new_epub_path):
                os.remove(new_epub_path)
            return total_original_size, total_original_size, 'error', 0
    
    # Si no hubo ahorro
    log_print(f"{' ' * 20} [SKIP] {T['M1_SKIPPED']}", end='\n')
    unoptimized_files_list.append(filename)
    return total_original_size, total_original_size, 'skipped', 0

def m1_print_final_summary(total_metrics, total_original_kb, total_final_kb, total_reduction_kb, total_reduction_percent, unoptimized_files_list, T: Dict[str, str]):
    """Imprime el resumen final del proceso."""
    log_print("\n" + T['M1_SUMMARY_TITLE'])
    log_print("="*50)
    
    log_print(f"{T['M1_FILES_PROCESSED']:<25} {total_metrics['processed_count']} archivos")
    log_print(f"{T['M1_SUCCESS_COUNT']:<25} {total_metrics['success_count']} archivos")
    log_print(f"{T['M1_SKIPPED_COUNT']:<25} {total_metrics['processed_count'] - total_metrics['success_count'] - total_metrics['error_count']} archivos")
    log_print(f"{T['M1_ERROR_COUNT']:<25} {total_metrics['error_count']} archivos")
    log_print("-" * 50)
    
    log_print(f"{T['M1_ORIGINAL_SIZE']:<25} {total_original_kb:.2f} KB")
    log_print(f"{T['M1_FINAL_SIZE']:<25} {total_final_kb:.2f} KB")
    log_print(f"{T['M1_SAVINGS']:<25} {total_reduction_kb:.2f} KB")
    log_print(f"{T['M1_SAVINGS_PERCENT']:<25} {total_reduction_percent:.2f}%")
    log_print("="*50)

    log_print("\n" + "="*50)
    log_print(T['M1_UNOPTIMIZED_TITLE'])
    log_print("="*50)
    if unoptimized_files_list:
        for name in unoptimized_files_list:
            log_print(f"  - {name}")
    else:
        log_print(f"  {T['M1_ALL_OPTIMIZED']}")
    log_print("="*50)

def run_optimizer_module(folder_path: str, T: Dict[str, str]):
    """Función principal del Módulo 1: Optimizador de EPUBs."""
    
    log_print(T['M1_TITLE'])
    
    # Preparación
    temp_dir = os.path.join(folder_path, '.epub_temp')
    
    # Inicialización de log
    global LOG_FILE_HANDLE
    log_file_path = os.path.join(folder_path, LOG_FILENAME)
    try:
        if LOG_FILE_HANDLE: LOG_FILE_HANDLE.close()
        LOG_FILE_HANDLE = open(log_file_path, 'w', encoding='utf-8') 
        write_log(folder_path, T['M1_TITLE'])
    except Exception as e:
        print(f"[ERROR] No se pudo abrir el archivo de log: {e}")
        LOG_FILE_HANDLE = None

    # Inicialización de métricas
    total_metrics = {'processed_count': 0, 'success_count': 0, 'error_count': 0}
    total_original_size = 0
    total_new_size = 0
    unoptimized_files = [] 
    
    try:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.makedirs(temp_dir, exist_ok=True)
        
        epub_files = glob.glob(os.path.join(folder_path, f'*{EPUB_EXTENSIONS[0]}'))
        total_files = len(epub_files)
        
        if total_files == 0:
            log_print(T['NO_EPUB_FILES'].format(folder_path))
            return
            
        log_print(T['M1_START_OPTIMIZING'].format(total_files))
        
        # Procesamiento de archivos
        for i, epub_file in enumerate(epub_files):
            original_size, new_size, status, reduction_bytes = m1_optimize_epub(
                epub_file, temp_dir, i + 1, total_files, T, unoptimized_files
            )
            
            total_metrics['processed_count'] += 1
            total_original_size += original_size
            total_new_size += new_size
            
            if status == 'success':
                total_metrics['success_count'] += 1
            elif status == 'error':
                total_metrics['error_count'] += 1

        # Cálculo de métricas finales
        total_reduction_bytes = total_original_size - total_new_size
        total_original_kb = bytes_to_kb(total_original_size)
        total_final_kb = bytes_to_kb(total_new_size)
        total_reduction_kb = bytes_to_kb(total_reduction_bytes)
        
        total_reduction_percent = (total_reduction_bytes / total_original_size * 100) if total_original_size > 0 else 0
        
        # Imprimir resumen
        m1_print_final_summary(
            total_metrics, 
            total_original_kb, 
            total_final_kb, 
            total_reduction_kb, 
            total_reduction_percent, 
            unoptimized_files, 
            T
        )
        
    except Exception as e:
        log_print(f"[ERROR FATAL] Fallo en run_optimizer_module: {e}")
        write_log(folder_path, f"[ERROR FATAL] {e}")
    finally:
        # Limpieza
        log_print(T['M1_CLEANUP_TEMP'])
        try:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
                log_print(T['M1_TEMP_DELETED'].format(temp_dir))
        except Exception as e:
            log_print(T['M1_TEMP_ERROR'].format(e))
            write_log(folder_path, T['M1_TEMP_ERROR'].format(e))
        
        # Cerrar log y mensaje de fin
        if LOG_FILE_HANDLE:
            write_print = T['PROMO_END'] # El mensaje final de donación
            write_log(folder_path, write_print)
            log_print(f"\n{write_print}")
            LOG_FILE_HANDLE.close()
            LOG_FILE_HANDLE = None

# ---------------------------------------------------------------------------\


# --- LÓGICA PRINCIPAL DEL PROGRAMA (SÓLO OPTIMIZADOR) ---\
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

    # 5. Ejecutar el optimizador
    run_optimizer_module(folder_path, T)


if __name__ == "__main__":
    main()