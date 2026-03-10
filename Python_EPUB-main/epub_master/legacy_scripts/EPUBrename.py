import os
import re
import shutil
from ebooklib import epub
from pathlib import Path
import locale 

# =========================================================
# CONSTANTES DE CONFIGURACIÓN
# =========================================================

CARPETA_DONE = "DONE"
CARPETA_DOUBT = "DOUBT"
LOG_FILENAME = "log_proceso_epub_renombrado.txt"

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
EPUBRename es un programa freeware que normaliza los nombres de 
tus archivos EPUB, dando formato APELLIDO, NOMBRE - LIBRO. Revisa 
los megadatos del libro electrónico y hace más eficiente tu biblioteca.
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
            "PREGUNTA_CARPETA": "Introduce la ruta de la carpeta con los EPUBs a analizar [enter para actual]: ",
            "INICIANDO_PROCESO": "--- INICIANDO PROCESO DE RENOMBRADO ---",
            "RENOMBRADO_COPIADO": "Archivo '{}' renombrado y copiado a DONE como '{}'",
            "MOVIDO_DOUBT": "Archivo '{}' movido a DOUBT por nombre no claro",
            "ERROR_COPIA": "Error copiando '{}': {}",
            "PROCESO_FINALIZADO": "Proceso de renombrado finalizado. Log guardado en: {}",
        }
    else: # Inglés
        return {
            "MENSAJE_INICIO": """
---------------------------------------------------------------
EPUBRename is a freeware program that standardizes the names of 
your EPUB files, using the format SURNAME, FIRST NAME - BOOK TITLE. 
It checks the ebook's metadata and makes your library more efficient.
Don't worry, the original files are kept intact.
---------------------------------------------------------------
If the program has been useful to you, invite me for a coffee at paypal.me/ossoney.
---------------------------------------------------------------
""",
            "PREGUNTA_CONTINUAR": "Do you wish to continue (Y/N)? ",
            "MENSAJE_FIN": "\n---------------------------------------------------------------"
                         + "\nIf the program has been useful to you, invite me for a coffee at paypal.me/ossoney."
                         + "\n---------------------------------------------------------------",
            "ADVERTENCIA_RESPUESTA_INVALIDA": "Invalid answer / Respuesta no válida. Please type Y/N or S/N.",
            "PREGUNTA_CARPETA": "Enter the path of the folder containing the EPUBs to analyze [enter for current]: ",
            "INICIANDO_PROCESO": "--- INITIATING RENAME PROCESS ---",
            "RENOMBRADO_COPIADO": "File '{}' renamed and copied to DONE as '{}'",
            "MOVIDO_DOUBT": "File '{}' moved to DOUBT due to unclear name",
            "ERROR_COPIA": "Error copying '{}': {}",
            "PROCESO_FINALIZADO": "Rename process finished. Log saved at: {}",
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

def obtener_metadatos(epub_path):
    # ... (Código de obtener_metadatos se mantiene igual)
    try:
        book = epub.read_epub(str(epub_path)) 
        title = ""
        author = ""
        if book.get_metadata('DC', 'title'):
            title = book.get_metadata('DC', 'title')[0][0]
        if book.get_metadata('DC', 'creator'):
            author = book.get_metadata('DC', 'creator')[0][0]
        return title.strip(), author.strip()
    except Exception as e:
        # Se mantiene en español/inglés simple ya que es un mensaje de advertencia específico de la librería
        print(f"Warning: Could not read metadata for '{epub_path.name}'. Error: {e}")
        return None, None

def separar_informacion_adicional(nombre_archivo):
    # ... (Código de separar_informacion_adicional se mantiene igual)
    base = re.sub(r"[\[\(].*?[\]\)]", "", nombre_archivo).strip()
    base_escapada = re.escape(base)
    
    extras_izquierda_texto = ""
    extras_izquierda_match = re.search(r"^(.*?)" + base_escapada, nombre_archivo)
    if extras_izquierda_match:
        extras_izquierda_texto = " ".join(re.findall(r"[\[\(].*?[\]\)]", extras_izquierda_match.group(1))).strip()

    extras_derecha_texto = ""
    extras_derecha_match = re.search(base_escapada + r"(.*?)$", nombre_archivo)
    if extras_derecha_match:
        extras_derecha_texto = " ".join(re.findall(r"[\[\(].*?[\]\)]", extras_derecha_match.group(1))).strip()
        
    return base, extras_izquierda_texto, extras_derecha_texto

def invertir_nombre_apellido(nombre_completo):
    # ... (Código de invertir_nombre_apellido se mantiene igual)
    partes = nombre_completo.split()
    if len(partes) > 1:
        apellido = partes[-1]
        nombre = " ".join(partes[:-1])
        return f"{apellido}, {nombre}"
    else:
        return nombre_completo

def limpiar_nombre_archivo(nombre):
    # ... (Código de limpiar_nombre_archivo se mantiene igual)
    return re.sub(r'[\\/:"*?<>|_\-]+', '', nombre)

def construir_nombre_formato(autor, titulo, extras_izq, extras_der):
    # ... (Código de construir_nombre_formato se mantiene igual)
    autor_formateado = invertir_nombre_apellido(autor) if autor else None
    titulo = titulo if titulo else None
    
    if not autor_formateado or not titulo:
        return None
    
    autor_limpio = limpiar_nombre_archivo(autor_formateado)
    titulo_limpio = limpiar_nombre_archivo(titulo)

    nombre_central = f"{autor_limpio} - {titulo_limpio}"
    
    nuevo_nombre = ""
    if extras_izq:
        nuevo_nombre += f"{extras_izq} "
        
    nuevo_nombre += nombre_central
    
    if extras_der:
        nuevo_nombre += f" {extras_der}"
    
    nuevo_nombre += ".epub"
    return nuevo_nombre

def preguntar_carpeta(textos):
    """
    Solicita la ruta de la carpeta de origen. La ruta del LOG es la carpeta actual.
    """
    log_dir = Path(os.getcwd()) 
    
    carpeta_a_procesar = input(textos["PREGUNTA_CARPETA"]).strip()
    if not carpeta_a_procesar:
        carpeta_a_procesar = os.getcwd()
        
    return Path(carpeta_a_procesar), log_dir

# =========================================================
# FUNCIÓN PRINCIPAL DE RENOMBRADO
# =========================================================

def main():
    idioma = obtener_idioma()
    textos = obtener_texto(idioma)
    
    if not mostrar_mensaje_inicio(idioma, textos):
        mostrar_mensaje_fin(idioma, textos)
        return

    carpeta_path, log_dir = preguntar_carpeta(textos)
    done_path = carpeta_path / CARPETA_DONE
    doubt_path = carpeta_path / CARPETA_DOUBT
    log_path = log_dir / LOG_FILENAME

    done_path.mkdir(exist_ok=True)
    doubt_path.mkdir(exist_ok=True)

    epubs = [f for f in carpeta_path.glob("*.epub") if f.name != LOG_FILENAME]

    log_lines = [f"--- INICIO DEL PROCESO DE RENOMBRADO en {carpeta_path} ---"]
    
    print(f"\n--- {textos['INICIANDO_PROCESO']} ---")

    for archivo_path in epubs:
        archivo_nombre = archivo_path.name
        
        # NOTE: El mensaje de advertencia dentro de obtener_metadatos no está traducido
        titulo, autor = obtener_metadatos(archivo_path) 

        base_nombre, extras_izq, extras_der = separar_informacion_adicional(archivo_path.stem) 
        
        if not titulo or not autor:
            if "-" in base_nombre:
                partes = base_nombre.split("-", 1)
                autor = autor or partes[0].strip()
                titulo = titulo or partes[1].strip()
        
        nuevo_nombre = construir_nombre_formato(autor, titulo, extras_izq, extras_der)
        
        if nuevo_nombre:
            destino = done_path / nuevo_nombre
            log_message = textos['RENOMBRADO_COPIADO'].format(archivo_nombre, nuevo_nombre)
        else:
            destino = doubt_path / archivo_nombre
            log_message = textos['MOVIDO_DOUBT'].format(archivo_nombre)

        try:
            shutil.copy2(archivo_path, destino)
            log_lines.append(log_message)
            print(log_message)
        except Exception as e:
            error_message = textos['ERROR_COPIA'].format(archivo_nombre, e)
            log_lines.append(error_message)
            print(error_message)

    log_lines.append("--- PROCESO DE RENOMBRADO FINALIZADO ---")
    
    with log_path.open('a', encoding='utf-8') as log_file: 
        log_file.write("\n".join(log_lines))

    print(textos['PROCESO_FINALIZADO'].format(log_path))
    
    mostrar_mensaje_fin(idioma, textos)


if __name__ == "__main__":
    main()