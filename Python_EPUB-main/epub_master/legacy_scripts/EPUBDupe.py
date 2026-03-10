import os
import re
import shutil
from difflib import SequenceMatcher
from collections import defaultdict
from pathlib import Path
import locale 

# =========================================================
# CONSTANTES DE CONFIGURACIÓN
# =========================================================

UMBRAL_SIMILITUD = 0.85
CARPETA_DUPLICADOS = "POSIBLES_DUPLICADOS"
LOG_FILENAME = "log_proceso_epub_duplicados.txt"

# =========================================================
# FUNCIONES DE INTERFAZ Y LOCALIZACIÓN
# =========================================================

def obtener_idioma():
    """Detecta el idioma del sistema. Devuelve 'es' si es español, 'en' si no."""
    try:
        lang_code = locale.getlocale()[0]
    except:
        lang_code = os.environ.get('LANG', 'en_US')
        
    return 'es' if lang_code and lang_code.startswith('es') else 'en'

def obtener_texto(idioma):
    """Diccionario de todas las cadenas de texto del script."""
    if idioma == 'es':
        return {
            "MENSAJE_INICIO": """
---------------------------------------------------------------
EPUBDupe es un programa freeware que busca duplicados entre
tus archivos EPUB, te ofrece borrarlos y te ahorra espacio
de almacenamiento, haciendo más eficiente tu biblioteca.
No te preocupes, los archivos originales se mantienen.
---------------------------------------------------------------
Si el programa te ha sido útil invítame a un café en paypal.me/ossoney.
---------------------------------------------------------------
""",
            "PREGUNTA_CONTINUAR": "¿Desea continuar (S/N)? ",
            "MENSAJE_FIN": "\n---------------------------------------------------------------"
                         + "\nSi el programa te ha sido útil invítame a un café en paypal.me/ossoney."
                         + "\n---------------------------------------------------------------",
            "ADVERTENCIA_RESPUESTA_INVALIDA": "Respuesta no válida / Invalid answer. Por favor, escriba S/N o Y/N.",
            "PREGUNTA_CARPETA": "Introduce la ruta de la carpeta que contiene los archivos EPUB renombrados [enter para actual]: ",
            "ERROR_NO_DIR": "Error: La ruta '{}' no es un directorio válido.",
            "ERROR_NO_EPUBS": "Error: No se encontraron archivos EPUB en '{}'.",
            "INICIANDO_BUSQUEDA": "--- INICIANDO BÚSQUEDA DE DUPLICADOS ---",
            "NO_DUPLICADOS": "No se encontraron posibles duplicados (similitud de título > {}%).",
            "SE_ENCONTRARON": "Se encontraron {} grupos de posibles duplicados:",
            "GRUPO_DUPLICADOS": "{}. Grupo de Posibles Duplicados (Autor: {}):",
            "INSTRUCCIONES": "\n   Instrucciones:\n   - Escribe las letras de los archivos que quieres mover (ej: AB).\n   - Presiona ENTER para ignorar el grupo.",
            "ARCHIVOS_A_MOVER": "Archivos a mover (opciones: {} / ENTER): ",
            "GRUPO_IGNORADO_ENTER": "-> Grupo ignorado (ENTER).",
            "ADVERTENCIA_OPCION_INVALIDA": "Advertencia: Opción '{}' no válida. Ignorada.",
            "NO_SELECCION": "No se seleccionó ningún archivo válido para mover. Grupo ignorado.",
            "MOVIDO_DUPLICADOS": "Duplicado '{}' movido a {}",
            "ARCHIVO_MOVIDO": "-> Archivo '{}' movido para revisión.",
            "ERROR_MOVIENDO": "Error moviendo duplicado '{}': {}",
            "PROCESO_FINALIZADO": "Proceso de duplicados finalizado. Log guardado en: {}",
        }
    else: # Inglés
        return {
            "MENSAJE_INICIO": """
---------------------------------------------------------------
EPUBDupe is a freeware program that finds duplicates among
your EPUB files, offers to delete them, and saves you storage
space, making your library more efficient.
Don't worry, the original files are kept intact.
---------------------------------------------------------------
If the program has been useful to you, invite me for a 
coffee at paypal.me/ossoney. Send me 1$-2$-3$. Thanks.
---------------------------------------------------------------
""",
            "PREGUNTA_CONTINUAR": "Do you wish to continue (Y/N)? ",
            "MENSAJE_FIN": "\n---------------------------------------------------------------"
                         + "\nIf the program has been useful to you, invite me for a coffee at paypal.me/ossoney."
                         + "\n---------------------------------------------------------------",
            "ADVERTENCIA_RESPUESTA_INVALIDA": "Invalid answer / Respuesta no válida. Please type Y/N or S/N.",
            "PREGUNTA_CARPETA": "Enter the path of the folder containing the renamed EPUB files [enter for current]: ",
            "ERROR_NO_DIR": "Error: Path '{}' is not a valid directory.",
            "ERROR_NO_EPUBS": "Error: No EPUB files were found in '{}'.",
            "INICIANDO_BUSQUEDA": "--- INITIATING DUPLICATE SEARCH ---",
            "NO_DUPLICADOS": "No possible duplicates were found (title similarity > {}%).",
            "SE_ENCONTRARON": "{} groups of possible duplicates were found:",
            "GRUPO_DUPLICADOS": "{}. Possible Duplicates Group (Author: {}):",
            "INSTRUCCIONES": "\n   Instructions:\n   - Type the letters of the files you want to move (e.g., AB).\n   - Press ENTER to ignore the group.",
            "ARCHIVOS_A_MOVER": "Files to move (options: {} / ENTER): ",
            "GRUPO_IGNORADO_ENTER": "-> Group ignored (ENTER).",
            "ADVERTENCIA_OPCION_INVALIDA": "Warning: Option '{}' is not valid. Ignored.",
            "NO_SELECCION": "No valid files were selected to move. Group ignored.",
            "MOVIDO_DUPLICADOS": "Duplicate '{}' moved to {}",
            "ARCHIVO_MOVIDO": "-> File '{}' moved for review.",
            "ERROR_MOVIENDO": "Error moving duplicate '{}': {}",
            "PROCESO_FINALIZADO": "Duplicate process finished. Log saved at: {}",
        }

def mostrar_mensaje_inicio(idioma, textos):
    """Muestra el mensaje inicial y pregunta si desea continuar."""
    print(textos["MENSAJE_INICIO"])
    
    while True:
        respuesta = input(textos["PREGUNTA_CONTINUAR"]).strip().upper()
        if respuesta == 'S' or respuesta == 'Y':
            return True
        elif respuesta == 'N':
            return False
        else:
            print(textos["ADVERTENCIA_RESPUESTA_INVALIDA"])

def mostrar_mensaje_fin(idioma, textos):
    """Muestra el mensaje final de donación."""
    print(textos["MENSAJE_FIN"])

# =========================================================
# FUNCIONES DE AYUDA (Mantenidas)
# =========================================================

def preguntar_carpeta_escanear(textos):
    """
    Solicita la ruta de la carpeta a escanear. La ruta del LOG es la carpeta actual.
    """
    log_dir = Path(os.getcwd()) 
    
    carpeta_a_escanear = input(textos["PREGUNTA_CARPETA"]).strip()
    if not carpeta_a_escanear:
        carpeta_a_escanear = os.getcwd()
        
    return Path(carpeta_a_escanear), log_dir

def comparar_titulos(titulo1, titulo2, umbral=UMBRAL_SIMILITUD):
    return SequenceMatcher(None, titulo1.lower(), titulo2.lower()).ratio() >= umbral

# =========================================================
# FUNCIÓN PRINCIPAL DE DUPLICADOS
# =========================================================

def encontrar_duplicados_y_preguntar(scan_path, log_lines, textos):
    print(f"\n--- {textos['INICIANDO_BUSQUEDA']} ---")
    
    archivos_escanear = [f for f in scan_path.glob("*.epub")]
    libros_por_autor = defaultdict(list)
    
    patron_extraccion = re.compile(r"^(?:\[.*?\]\s*|\(.*?\)s*)*(.*?) - (.*?)(?:\s*\[.*?\]|\s*\(.*?\))*\.epub$", re.IGNORECASE)

    info_libros = []
    
    for archivo_path in archivos_escanear:
        archivo_nombre = archivo_path.name
        match = patron_extraccion.match(archivo_nombre)
        if match:
            autor_formato = match.group(1).strip()
            titulo_base = match.group(2).strip()
            
            autor_base = autor_formato 
            
            info_libros.append({
                'path_completo': archivo_path,
                'nombre_archivo': archivo_nombre,
                'autor_base': autor_base,
                'titulo_base': titulo_base,
            })
            libros_por_autor[autor_base].append(info_libros[-1])

    grupos_duplicados = []
    
    for autor, libros in libros_por_autor.items():
        if len(libros) < 2:
            continue
            
        libros_sin_agrupar = list(libros)
        
        while libros_sin_agrupar:
            libro_principal = libros_sin_agrupar.pop(0)
            grupo_actual = {libro_principal['nombre_archivo']}
            
            i = 0
            while i < len(libros_sin_agrupar):
                libro_a_comparar = libros_sin_agrupar[i]
                
                if comparar_titulos(libro_principal['titulo_base'], libro_a_comparar['titulo_base']):
                    grupo_actual.add(libro_a_comparar['nombre_archivo'])
                    libros_sin_agrupar.pop(i)
                else:
                    i += 1

            if len(grupo_actual) > 1:
                grupos_duplicados.append(list(grupo_actual))

    if not grupos_duplicados:
        print(textos['NO_DUPLICADOS'].format(UMBRAL_SIMILITUD * 100))
        return 

    print(textos['SE_ENCONTRARON'].format(len(grupos_duplicados)))
    
    duplicados_path = scan_path / CARPETA_DUPLICADOS
    duplicados_path.mkdir(exist_ok=True)
    
    for i, grupo in enumerate(grupos_duplicados):
        autor_del_grupo = [l['autor_base'] for l in info_libros if l['nombre_archivo'] == grupo[0]][0] if grupo else "Unknown"
        
        print(textos['GRUPO_DUPLICADOS'].format(i+1, autor_del_grupo))
        
        opciones_validas = []
        nombres_ordenados = sorted(grupo) 
        
        for j, nombre in enumerate(nombres_ordenados):
            letra = chr(ord('A') + j)
            print(f"   {letra}) {nombre}")
            opciones_validas.append(letra)
        
        print(textos['INSTRUCCIONES'])
        
        eleccion = input(textos['ARCHIVOS_A_MOVER'].format(', '.join(opciones_validas))).strip().upper()
        
        archivos_a_mover = []
        
        if not eleccion:
            print(textos['GRUPO_IGNORADO_ENTER'])
            log_lines.append(f"Grupo de duplicados ignorado (ENTER).")
            continue
        
        for letra in eleccion:
            if letra in opciones_validas:
                indice = ord(letra) - ord('A')
                nombre_archivo = nombres_ordenados[indice]
                archivos_a_mover.append(nombre_archivo)
            else:
                print(textos['ADVERTENCIA_OPCION_INVALIDA'].format(letra))

        if not archivos_a_mover:
            print(textos['NO_SELECCION'])
            log_lines.append(f"Grupo de duplicados ignorado (selección inválida).")
            continue
        
        for nombre_archivo in archivos_a_mover:
            ruta_origen = scan_path / nombre_archivo 
            ruta_destino = duplicados_path / nombre_archivo
            try:
                ruta_origen.rename(ruta_destino)
                log_lines.append(textos['MOVIDO_DUPLICADOS'].format(nombre_archivo, CARPETA_DUPLICADOS))
                print(textos['ARCHIVO_MOVIDO'].format(nombre_archivo))
            except Exception as e:
                log_lines.append(textos['ERROR_MOVIENDO'].format(nombre_archivo, e))
                print(textos['ERROR_MOVIENDO'].format(nombre_archivo, e))


def main_duplicados():
    idioma = obtener_idioma()
    textos = obtener_texto(idioma)
    
    if not mostrar_mensaje_inicio(idioma, textos):
        mostrar_mensaje_fin(idioma, textos)
        return

    scan_path, log_dir = preguntar_carpeta_escanear(textos)
    log_path = log_dir / LOG_FILENAME 

    if not scan_path.is_dir():
        print(textos['ERROR_NO_DIR'].format(scan_path))
        mostrar_mensaje_fin(idioma, textos)
        return

    if not list(scan_path.glob("*.epub")):
        print(textos['ERROR_NO_EPUBS'].format(scan_path))
        mostrar_mensaje_fin(idioma, textos)
        return

    log_lines = [f"\n--- INICIO DEL PROCESO DE BÚSQUEDA DE DUPLICADOS en {scan_path} ---"]
    
    encontrar_duplicados_y_preguntar(scan_path, log_lines, textos)
    
    log_lines.append("--- PROCESO DE BÚSQUEDA DE DUPLICADOS FINALIZADO ---")

    with log_path.open('a', encoding='utf-8') as log_file: 
        log_file.write("\n".join(log_lines))

    print(textos['PROCESO_FINALIZADO'].format(log_path))
    
    mostrar_mensaje_fin(idioma, textos)

if __name__ == "__main__":
    main_duplicados()