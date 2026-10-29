"""
------------------------------------------------------------------------------
GUÍA DE INSTALACIÓN DE DEPENDENCIAS
------------------------------------------------------------------------------
Para que el programa funcione, abre tu terminal y ejecuta:

[WINDOWS]
pip install ebooklib beautifulsoup4 edge-tts tqdm mutagen

[LINUX / MACOS]
pip3 install ebooklib beautifulsoup4 edge-tts tqdm mutagen
------------------------------------------------------------------------------
"""

import sys
import asyncio
import re
import os
import datetime

# --- VERIFICACIÓN DE DEPENDENCIAS ---
try:
    import ebooklib
    from ebooklib import epub
    from bs4 import BeautifulSoup
    import edge_tts
    from tqdm import tqdm
    from mutagen.mp3 import MP3
    from mutagen.id3 import ID3, TIT2, TPE1, APIC, TRCK, TALB, ID3NoHeaderError
except ImportError as e:
    print(f"\n❌ ERROR: Falta la librería '{e.name}'. Instálala con pip.")
    sys.exit(1)

# --- CONFIGURACIÓN GLOBAL ---
CONCURRENCIA = 2          
PAUSA_SEGURIDAD = 0.3     
REINTENTOS = 3            
BACKOFF_BASE = 2          

# Voces por idioma (puedes añadir más)
VOCES = {
    "es": {"H": "es-ES-AlvaroNeural", "M": "es-ES-ElviraNeural"},
    "en": {"H": "en-US-GuyNeural",    "M": "en-US-AvaNeural"},
    "gl": {"H": "gl-ES-RoiNeural",    "M": "gl-ES-SabelaNeural"},
    "default": {"H": "es-ES-AlvaroNeural", "M": "es-ES-ElviraNeural"}
}

MAX_CARACTERES_CAPITULO = 20000  # Límite para fragmentación

# --- LOGGING ---
# (Se mantiene igual que el anterior)
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "epub2mp3.log")

class TeeLogger:
    def __init__(self, filepath):
        self._consola = sys.stdout
        self._log     = open(filepath, "a", encoding="utf-8", buffering=1)
        sys.stdout    = self
    def write(self, texto):
        self._consola.write(texto)
        self._log.write(texto)
    def flush(self):
        self._consola.flush()
        self._log.flush()
    def close(self):
        sys.stdout = self._consola
        self._log.close()

def iniciar_log():
    tee = TeeLogger(LOG_FILE)
    ahora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n{'='*65}\n  SESIÓN  {ahora}\n{'='*65}")
    return tee

# --- UTILIDADES ---

def limpiar_nombre_archivo(nombre):
    nombre = re.sub(r'[\\/*?:"<>|]', "", nombre).strip()
    return nombre[:100]

# Clases CSS habituales en EPUBs para números de página
_CLASES_PAGINA = re.compile(
    r'\b(page[\-_]?num(ber)?|pagenum|page[\-_]?break|pagination|'
    r'pgnum|folio|page[\-_]?ref|sigla)\b',
    re.IGNORECASE
)

def eliminar_numeracion_paginas(soup):
    """Elimina marcadores de número de página del árbol HTML antes de get_text().

    Estrategia (por orden de fiabilidad):
    1. Atributo EPUB3 estándar:  epub:type="pagebreak"
    2. Atributo ARIA:            role="doc-pagebreak"
    3. Clases CSS típicas:       pagenum, page-number, folio, etc.
    4. Atributo id que empiece por 'page' seguido de dígitos (p. ej. id="page42")
    """
    for tag in soup.find_all(True):
        eliminar = False

        # 1. epub:type="pagebreak"  (EPUB3 estándar)
        epub_type = tag.get('epub:type', '') or tag.get('type', '')
        if 'pagebreak' in epub_type.lower():
            eliminar = True

        # 2. role="doc-pagebreak"  (ARIA / EPUB Accessibility)
        if not eliminar and 'doc-pagebreak' in tag.get('role', '').lower():
            eliminar = True

        # 3. Clase CSS con patrón de número de página
        if not eliminar:
            clases = ' '.join(tag.get('class', []))
            if _CLASES_PAGINA.search(clases):
                eliminar = True

        # 4. id="pageXX" o id="pg42"
        if not eliminar:
            tag_id = tag.get('id', '')
            if re.match(r'^p(age?|g)?\d+$', tag_id, re.IGNORECASE):
                eliminar = True

        if eliminar:
            tag.decompose()

    return soup

def limpiar_texto(texto):
    texto = re.sub(r'http\S+', '', texto)
    # Fallback: número solo rodeado de espacios/puntuación (lo que escape al HTML)
    texto = re.sub(r'(?<![^\s.])\b\d{1,4}\b(?![^\s.])', '', texto)
    texto = re.sub(r'\s+', ' ', texto)
    return texto.strip()

def obtener_titulo_capitulo(soup):
    header = soup.find(['h1', 'h2', 'h3'])
    if header:
        titulo = header.get_text().strip()
        return titulo[:50] + "..." if len(titulo) > 50 else titulo
    return None

def fragmentar_texto(texto, limite=MAX_CARACTERES_CAPITULO):
    """Divide un texto largo en partes respetando los puntos finales."""
    if len(texto) <= limite:
        return [texto]
    
    partes = []
    while len(texto) > 0:
        if len(texto) <= limite:
            partes.append(texto)
            break
        
        # Buscar el último punto antes del límite
        corte = texto.rfind('. ', 0, limite)
        if corte == -1: corte = limite # Si no hay punto, cortar a saco
        
        partes.append(texto[:corte+1].strip())
        texto = texto[corte+1:].strip()
    return partes

def verificar_audio_valido(ruta):
    """Verifica si el MP3 tiene cabeceras válidas y duración."""
    try:
        audio = MP3(ruta)
        return audio.info.length > 0
    except Exception:
        return False

# --- EXTRACCIÓN DE DATOS ---

def extraer_datos_epub(ruta_epub):
    book = epub.read_epub(ruta_epub)

    try:    titulo_libro = book.get_metadata('DC', 'title')[0][0]
    except: titulo_libro = "Sin Título"
    try:    autor = book.get_metadata('DC', 'creator')[0][0]
    except: autor = "Autor Desconocido"
    try:    idioma = book.get_metadata('DC', 'language')[0][0][:2].lower()
    except: idioma = "es"

    cover_data = None
    cover_item = book.get_item_with_id('cover')
    if not cover_item:
        for item in book.get_items_of_type(ebooklib.ITEM_IMAGE):
            if 'cover' in item.get_name().lower():
                cover_item = item
                break
    if cover_item:
        cover_data = cover_item.get_content()

    capitulos = []
    contador_global = 1
    # Usar el spine para respetar el orden de lectura definido en el EPUB
    spine_ids = [item_id for item_id, _ in book.spine]
    items_ordenados = [book.get_item_with_id(item_id) for item_id in spine_ids]
    items_ordenados = [it for it in items_ordenados if it is not None]
    for item in items_ordenados:
        soup = BeautifulSoup(item.get_body_content(), 'html.parser')
        eliminar_numeracion_paginas(soup)                          # ← antes de get_text()
        texto_limpio = limpiar_texto(soup.get_text(separator='. '))

        if len(texto_limpio) > 200:
            titulo_detectado = obtener_titulo_capitulo(soup)
            partes = fragmentar_texto(texto_limpio)
            
            for sub_idx, sub_texto in enumerate(partes):
                # Si hay fragmentación, añadir "Parte XX" al título con 2 dígitos
                sufijo = f" (Parte {sub_idx+1:02d})" if len(partes) > 1 else ""
                
                if titulo_detectado:
                    titulo_final = f"{titulo_detectado}{sufijo}"
                    es_titulo_real = True
                else:
                    titulo_final = f"Capítulo {contador_global}{sufijo}"
                    es_titulo_real = False

                capitulos.append({
                    'indice': contador_global,
                    'sub_indice': sub_idx + 1 if len(partes) > 1 else None,
                    'titulo': titulo_final,
                    'tiene_titulo_real': es_titulo_real,
                    'texto': sub_texto
                })
            contador_global += 1

    return titulo_libro, autor, cover_data, idioma, capitulos

# --- CORE ASÍNCRONO ---

async def tarea_capitulo(sem, cap, carpeta_salida, voz_base, velocidad, titulo_libro, autor, cover_data, idioma):
    libro_seguro = limpiar_nombre_archivo(titulo_libro)
    
    # Nombre de archivo dinámico (p01, p02...)
    sub = f"p{cap['sub_indice']:02d}" if cap.get('sub_indice') else ""
    if cap['tiene_titulo_real']:
        cap_seguro = limpiar_nombre_archivo(cap['titulo'])
        nombre_archivo = f"{cap['indice']:03d}{sub} - {cap_seguro} - {libro_seguro}.mp3"
    else:
        nombre_archivo = f"{cap['indice']:03d}{sub} - {libro_seguro}.mp3"
    
    ruta_completa = os.path.join(carpeta_salida, nombre_archivo)

    if os.path.exists(ruta_completa) and verificar_audio_valido(ruta_completa):
        return ruta_completa

    async with sem:
        voces_disponibles = VOCES.get(idioma, VOCES["default"])
        # Alternancia de voz: si la base es M, la alterna es H
        voz_alterna = voces_disponibles["H"] if voz_base == voces_disponibles["M"] else voces_disponibles["M"]
        
        for intento in range(1, REINTENTOS + 1):
            # Alternar voz en intentos pares
            voz_actual = voz_base if intento % 2 != 0 else voz_alterna
            
            try:
                communicate = edge_tts.Communicate(cap['texto'], voz_actual, rate=velocidad)
                await communicate.save(ruta_completa)
                
                # Verificación de integridad tras descargar
                if verificar_audio_valido(ruta_completa):
                    break  # ← libera el slot inmediatamente
                else:
                    raise Exception("Audio generado corrupto o vacío")
                    
            except Exception as e:
                if os.path.exists(ruta_completa): os.remove(ruta_completa)
                if intento < REINTENTOS:
                    espera = BACKOFF_BASE ** intento
                    print(f"\n   ⚠️  Cap {cap['indice']}{sub} fallo ({e}). Reintento {intento}/{REINTENTOS} con voz {'Alterna' if intento % 2 == 0 else 'Original'} en {espera}s...")
                    await asyncio.sleep(espera)
                else:
                    print(f"\n❌ Fallo definitivo cap {cap['indice']}{sub}: {e}")
                    return None

    # Pausa FUERA del semáforo: no bloquea otros hilos
    await asyncio.sleep(PAUSA_SEGURIDAD)
    aplicar_tags_seguro(ruta_completa, cap, titulo_libro, autor, cover_data)
    return ruta_completa

# --- GESTOR DE CONVERSIÓN ---

async def convertir_libro(ruta_epub, velocidad, genero_voz, idioma_forzado=None, sem=None):
    print(f"\n📚 Analizando: {os.path.basename(ruta_epub)}...")

    try:
        titulo_libro, autor, cover_data, idioma_detectado, capitulos = extraer_datos_epub(ruta_epub)
    except Exception as e:
        print(f"❌ Error leyendo EPUB: {e}"); return

    # Usar idioma forzado si se seleccionó, o el detectado por defecto
    idioma = idioma_forzado or idioma_detectado
    modo_idioma = f"{idioma} (Forzado)" if idioma_forzado else f"{idioma} (Detectado)"

    # Elegir voz base según género e idioma seleccionado
    voz_base = VOCES.get(idioma, VOCES["default"])[genero_voz]
    
    directorio_epub = os.path.dirname(os.path.abspath(ruta_epub))
    carpeta_salida  = os.path.join(directorio_epub, limpiar_nombre_archivo(f"{autor} - {titulo_libro}"))
    if not os.path.exists(carpeta_salida): os.makedirs(carpeta_salida)

    print(f"   🌐 Idioma: {modo_idioma} | 📑 Segmentos: {len(capitulos)} | 🎙️ Voz: {voz_base}")

    sem = sem or asyncio.Semaphore(CONCURRENCIA)

    async def tarea_con_info(cap):
        resultado = await tarea_capitulo(sem, cap, carpeta_salida, voz_base, velocidad, titulo_libro, autor, cover_data, idioma)
        return cap, resultado

    fallidos = []
    pbar = tqdm(total=len(capitulos), unit="seg", leave=False)
    for coro in asyncio.as_completed([tarea_con_info(cap) for cap in capitulos]):
        try:
            cap, resultado = await coro
            sub = f"p{cap['sub_indice']:02d}" if cap.get('sub_indice') else ""
            if resultado is None:
                fallidos.append(f"{cap['indice']}{sub}")
        except Exception as e:
            fallidos.append("?")
        pbar.update(1)
    pbar.close()

    if fallidos: print(f"   ⚠️  {titulo_libro}: Errores en: {fallidos}")
    else: print(f"   ✅ {titulo_libro} completado.\n")

# --- ETIQUETADO SEGURO ---

def aplicar_tags_seguro(ruta, cap, titulo_libro, autor, cover_data):
    if not ruta or not os.path.exists(ruta): return False
    try:
        try: audio = MP3(ruta, ID3=ID3)
        except ID3NoHeaderError:
            audio = MP3(ruta)
            audio.add_tags()
        if audio.tags is None: audio.add_tags()

        audio.tags.add(TIT2(encoding=3, text=cap['titulo']))
        audio.tags.add(TPE1(encoding=3, text=autor))
        audio.tags.add(TALB(encoding=3, text=titulo_libro))
        audio.tags.add(TRCK(encoding=3, text=str(cap['indice'])))
        if cover_data:
            audio.tags.add(APIC(encoding=3, mime='image/jpeg', type=3, desc='Cover', data=cover_data))
        audio.save()
        return True
    except Exception as ex:
        print(f"   ⚠️  Error tags cap {cap['indice']}: {ex}")
        return False

# --- MENÚS Y MAIN ---

def pedir_idioma():
    print("\n🌐 IDIOMA DE LECTURA:")
    print("1. Automático (detectar según EPUB) - Default")
    print("2. Gallego (gl)")
    print("3. Español (es)")
    print("4. Inglés (en)")
    op = input("Elige (1-4): ").strip()
    if op == "2": return "gl"
    if op == "3": return "es"
    if op == "4": return "en"
    return None

def pedir_genero_voz():
    print("\n🗣️  SELECTOR DE VOZ")
    print("1. Hombre (H) - Default\n2. Mujer (M)")
    return "M" if input("Elige (1-2): ").strip() == "2" else "H"

async def main():
    global CONCURRENCIA
    tee = iniciar_log()
    try:
        print("\n" + "="*65 + "\nEPUBtoMP3 - Conversión Inteligente con Fragmentación\n" + "="*65)
        libros = seleccionar_archivos()
        idioma_forzado = pedir_idioma()
        genero = pedir_genero_voz()
        velocidad = pedir_velocidad()
        CONCURRENCIA = pedir_concurrencia()

        # Semáforo global compartido: controla el total de conexiones
        # simultáneas a edge-tts independientemente de cuántos libros corran
        sem = asyncio.Semaphore(CONCURRENCIA)
        await asyncio.gather(*[
            convertir_libro(libro, velocidad, genero, idioma_forzado, sem)
            for libro in libros
        ])
        print("\n🎉 ¡PROCESO COMPLETADO! 🎉")
    finally:
        tee.close()

def pedir_velocidad():
    print("\n⚡ VELOCIDAD: 1. Normal | 2. Rápida (+10%) | 3. Muy Rápida (+25%)")
    op = input("Elige (1-3): ").strip()
    return "+10%" if op=="2" else "+25%" if op=="3" else "+0%"

def pedir_concurrencia():
    print("\n🔀 HILOS: 1. 2 (Estable) | 2. 4 | 3. 6 | 4. 8 (Máximo)")
    op = input("Elige (1-4): ").strip()
    return 4 if op=="2" else 6 if op=="3" else 8 if op=="4" else 2

def seleccionar_archivos():
    ruta = input(f"\n📂 Ruta (Enter para actual): ").strip() or os.getcwd()
    if not os.path.exists(ruta): sys.exit("❌ Error: Ruta no existe.")
    archivos = [f for f in os.listdir(ruta) if f.lower().endswith(".epub")]
    if not archivos: sys.exit("❌ No hay EPUBs.")
    for i, f in enumerate(archivos): print(f"{i+1}. {f}")
    op = input("\n[A] Todos | [Nº] Uno: ").strip().upper()
    if op == 'A': return [os.path.join(ruta, f) for f in archivos]
    try: return [os.path.join(ruta, archivos[int(op)-1])]
    except: sys.exit("❌ Opción inválida.")

if __name__ == "__main__":
    try: asyncio.run(main())
    except KeyboardInterrupt: print("\n🛑 Detenido por usuario.")