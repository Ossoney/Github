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
CONCURRENCIA = 2          # Número de descargas simultáneas (reducido a 2 para evitar 503)
PAUSA_SEGURIDAD = 1.5     # Segundos de espera entre bloques (aumentado para menos rate-limiting)
REINTENTOS = 3            # Número máximo de reintentos por capítulo
BACKOFF_BASE = 2          # Segundos base para el backoff exponencial (2s, 4s, 8s...)
VOZ_HOMBRE = "es-ES-AlvaroNeural"
VOZ_MUJER  = "es-ES-ElviraNeural"

# --- LOGGING ---

LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "epub2mp3.log")

class TeeLogger:
    """Duplica sys.stdout a consola y fichero de log simultáneamente."""
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
    """Abre el TeeLogger e imprime cabecera de sesión."""
    tee = TeeLogger(LOG_FILE)
    ahora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n{'='*65}")
    print(f"  SESIÓN  {ahora}")
    print(f"{'='*65}")
    return tee


# --- UTILIDADES ---

def limpiar_nombre_archivo(nombre):
    """Elimina caracteres prohibidos y acorta si es muy largo."""
    nombre = re.sub(r'[\\/*?:"<>|]', "", nombre).strip()
    return nombre[:100]

def limpiar_texto(texto):
    texto = re.sub(r'http\S+', '', texto)
    texto = re.sub(r'\n\s*\d+\s*\n', '\n', texto)
    texto = re.sub(r'\s+', ' ', texto)
    return texto.strip()

def obtener_titulo_capitulo(soup):
    """Devuelve el título si existe, o None si no encuentra nada."""
    header = soup.find(['h1', 'h2', 'h3'])
    if header:
        titulo = header.get_text().strip()
        if len(titulo) > 50:
            titulo = titulo[:50] + "..."
        return titulo
    return None

def mostrar_intro():
    print("\n" + "="*65)
    print("EPUBtoMP3 es un programa freeware que convierte tus archivos EPUB")
    print("en archivos MP3. Es una conversión de tu libro o libros")
    print("electrónicos en audiolibros.")
    print("-" * 65)
    print("Si el programa te ha sido útil invítame a un café en:")
    print("paypal.me/ossoney")
    print("Envíame 1$ - 2$ - 3$ o lo que te apetezca.")
    print("=" * 65 + "\n")

# --- EXTRACCIÓN DE DATOS ---

def extraer_datos_epub(ruta_epub):
    book = epub.read_epub(ruta_epub)

    try:    titulo_libro = book.get_metadata('DC', 'title')[0][0]
    except: titulo_libro = "Sin Título"
    try:    autor = book.get_metadata('DC', 'creator')[0][0]
    except: autor = "Autor Desconocido"

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
    contador = 1
    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        soup = BeautifulSoup(item.get_body_content(), 'html.parser')
        texto_limpio = limpiar_texto(soup.get_text(separator='. '))

        if len(texto_limpio) > 200:
            titulo_detectado = obtener_titulo_capitulo(soup)

            if titulo_detectado:
                titulo_final = titulo_detectado
                es_titulo_real = True
            else:
                titulo_final = f"Capítulo {contador}"
                es_titulo_real = False

            capitulos.append({
                'indice': contador,
                'titulo': titulo_final,
                'tiene_titulo_real': es_titulo_real,
                'texto': texto_limpio
            })
            contador += 1

    return titulo_libro, autor, cover_data, capitulos

# --- ETIQUETADO SEGURO ---

def aplicar_tags_seguro(ruta, cap, titulo_libro, autor, cover_data):
    """Aplica tags ID3 al MP3. Devuelve True si tuvo éxito, False si falló."""
    if not ruta or not os.path.exists(ruta):
        return False
    if os.path.getsize(ruta) == 0:
        return False

    try:
        try:
            audio = MP3(ruta, ID3=ID3)
        except ID3NoHeaderError:
            audio = MP3(ruta)
            audio.add_tags()
        except Exception:
            audio = MP3(ruta)

        if audio.tags is None:
            try:
                audio.add_tags()
            except Exception:
                print(f"   ⚠️  No se pudieron añadir tags ID3 al cap {cap['indice']}.")
                return False

        audio.tags.add(TIT2(encoding=3, text=cap['titulo']))
        audio.tags.add(TPE1(encoding=3, text=autor))
        audio.tags.add(TALB(encoding=3, text=titulo_libro))
        audio.tags.add(TRCK(encoding=3, text=str(cap['indice'])))
        if cover_data:
            audio.tags.add(APIC(encoding=3, mime='image/jpeg', type=3, desc='Cover', data=cover_data))
        audio.save()
        return True

    except Exception as ex:
        print(f"   ⚠️  Error etiquetando cap {cap['indice']}: {ex}")
        return False

# --- CORE ASÍNCRONO (WORKER) CON REINTENTOS ---

async def tarea_capitulo(sem, cap, carpeta_salida, voz, velocidad, titulo_libro, autor, cover_data):
    """Descarga un capítulo con reintentos y backoff exponencial."""

    libro_seguro = limpiar_nombre_archivo(titulo_libro)

    if cap['tiene_titulo_real']:
        cap_seguro  = limpiar_nombre_archivo(cap['titulo'])
        nombre_base = f"{cap['indice']:03d} - {cap_seguro} - {libro_seguro}"
    else:
        nombre_base = f"{cap['indice']:03d} - {libro_seguro}"

    nombre_archivo = f"{nombre_base}.mp3"
    ruta_completa  = os.path.join(carpeta_salida, nombre_archivo)

    # ── MEJORA: Saltar si ya existe y tiene contenido ──────────────────────
    if os.path.exists(ruta_completa) and os.path.getsize(ruta_completa) > 0:
        return ruta_completa   # capítulo ya convertido, nada que hacer

    async with sem:
        # ── MEJORA: Reintentos con backoff exponencial ─────────────────────
        ultimo_error = None
        for intento in range(1, REINTENTOS + 1):
            try:
                communicate = edge_tts.Communicate(cap['texto'], voz, rate=velocidad)
                await communicate.save(ruta_completa)
                await asyncio.sleep(PAUSA_SEGURIDAD)
                break   # éxito → salir del bucle de reintentos
            except Exception as e:
                ultimo_error = e
                # Borrar archivo parcial si existe
                if os.path.exists(ruta_completa):
                    try:
                        os.remove(ruta_completa)
                    except OSError:
                        pass

                if intento < REINTENTOS:
                    espera = BACKOFF_BASE ** intento   # 2s, 4s, 8s…
                    print(f"\n   ⚠️  Cap {cap['indice']} intento {intento}/{REINTENTOS} fallido. "
                          f"Reintentando en {espera:.0f}s... ({e})")
                    await asyncio.sleep(espera)
                else:
                    print(f"\n❌ Fallo definitivo cap {cap['indice']} tras {REINTENTOS} intentos: {ultimo_error}")
                    return None

    aplicar_tags_seguro(ruta_completa, cap, titulo_libro, autor, cover_data)
    return ruta_completa

# --- GESTOR DE CONVERSIÓN ---

async def convertir_libro(ruta_epub, velocidad, voz_elegida):
    print(f"\n📚 Analizando: {os.path.basename(ruta_epub)}...")

    try:
        titulo_libro, autor, cover_data, capitulos = extraer_datos_epub(ruta_epub)
    except Exception as e:
        print(f"❌ Error leyendo EPUB: {e}")
        return

    # ── MEJORA: carpeta relativa al directorio del EPUB, no al cwd ─────────
    directorio_epub = os.path.dirname(os.path.abspath(ruta_epub))
    nombre_carpeta  = limpiar_nombre_archivo(f"{autor} - {titulo_libro}")
    carpeta_salida  = os.path.join(directorio_epub, nombre_carpeta)

    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)

    # Contar cuántos capítulos ya están hechos (reanudación)
    ya_hechos = sum(
        1 for cap in capitulos
        if os.path.exists(os.path.join(
            carpeta_salida,
            _nombre_mp3(cap, titulo_libro)
        )) and os.path.getsize(os.path.join(
            carpeta_salida,
            _nombre_mp3(cap, titulo_libro)
        )) > 0
    )
    pendientes = len(capitulos) - ya_hechos

    print(f"   📂 Destino: {carpeta_salida}/")
    print(f"   📑 Capítulos: {len(capitulos)} | ✅ Ya hechos: {ya_hechos} | ⏳ Pendientes: {pendientes} | 🚀 Hilos: {CONCURRENCIA}")

    if pendientes == 0:
        print(f"   ℹ️  Todos los capítulos ya estaban convertidos. Nada que hacer.\n")
        return

    sem    = asyncio.Semaphore(CONCURRENCIA)
    tareas = [
        tarea_capitulo(sem, cap, carpeta_salida, voz_elegida, velocidad, titulo_libro, autor, cover_data)
        for cap in capitulos
    ]

    fallidos = []
    pbar = tqdm(total=len(tareas), unit="cap", leave=False)
    for coro, cap in zip(asyncio.as_completed(tareas), capitulos):
        resultado = await coro
        if resultado is None:
            fallidos.append(cap['indice'])
        pbar.update(1)

    pbar.close()

    # ── MEJORA: Resumen de capítulos fallidos ──────────────────────────────
    if fallidos:
        print(f"   ⚠️  {titulo_libro}: {len(fallidos)} capítulo(s) NO convertido(s): {fallidos}")
    else:
        print(f"   ✅ {titulo_libro} completado.\n")

# Función auxiliar para calcular el nombre de archivo de un capítulo
def _nombre_mp3(cap, titulo_libro):
    libro_seguro = limpiar_nombre_archivo(titulo_libro)
    if cap['tiene_titulo_real']:
        cap_seguro  = limpiar_nombre_archivo(cap['titulo'])
        nombre_base = f"{cap['indice']:03d} - {cap_seguro} - {libro_seguro}"
    else:
        nombre_base = f"{cap['indice']:03d} - {libro_seguro}"
    return f"{nombre_base}.mp3"

# --- MENÚS ---

def pedir_voz():
    print("\n🗣️  SELECTOR DE VOZ")
    print("1. Hombre (Álvaro) - Default")
    print("2. Mujer (Elvira)")
    opcion = input("Elige opción (1-2): ").strip()
    if opcion == "2":
        return VOZ_MUJER
    return VOZ_HOMBRE

def pedir_velocidad():
    print("\n⚡ SELECTOR DE VELOCIDAD")
    print("1. Normal (0%)")
    print("2. Rápida (+10%)")
    print("3. Muy Rápida (+25%)")
    opcion = input("Elige opción (1-3): ").strip()
    if opcion == "2": return "+10%"
    if opcion == "3": return "+25%"
    return "+0%"

def pedir_concurrencia():
    print("\n🔀 HILOS SIMULTÁNEOS (más hilos = más rápido pero más errores 503)")
    print("1. 2 hilos - Estable (recomendado)")
    print("2. 3 hilos - Rápido")
    print("3. 4 hilos - Agresivo")
    opcion = input("Elige opción (1-3, Enter para 1): ").strip()
    if opcion == "2": return 3
    if opcion == "3": return 4
    return 2

def seleccionar_archivos():
    ruta_actual = os.getcwd()
    ruta_input  = input(f"\n📂 Ruta (Enter para '{ruta_actual}'): ").strip()
    ruta_carpeta = ruta_input if ruta_input else ruta_actual

    if not os.path.exists(ruta_carpeta):
        sys.exit("❌ La ruta no existe.")

    archivos = [f for f in os.listdir(ruta_carpeta) if f.lower().endswith(".epub")]
    if not archivos:
        sys.exit("❌ No hay archivos .epub aquí.")

    print(f"\nLibros en '{os.path.abspath(ruta_carpeta)}':")
    for i, f in enumerate(archivos):
        print(f"{i+1}. {f}")

    opcion = input("\n[A] Todos | [Nº] Uno específico: ").strip().upper()

    if opcion == 'A':
        return [os.path.join(ruta_carpeta, f) for f in archivos]
    try:
        idx = int(opcion)
        if 1 <= idx <= len(archivos):
            return [os.path.join(ruta_carpeta, archivos[idx-1])]
    except Exception:
        pass
    sys.exit("❌ Opción inválida.")

# --- MAIN ---

async def main():
    global CONCURRENCIA
    tee = iniciar_log()
    try:
        mostrar_intro()

        libros       = seleccionar_archivos()
        voz          = pedir_voz()
        velocidad    = pedir_velocidad()
        CONCURRENCIA = pedir_concurrencia()

        print(f"\n🚀 Iniciando proceso...")
        for libro in libros:
            await convertir_libro(libro, velocidad, voz)

        print("🎉 ¡TODO FINALIZADO! 🎉")
    finally:
        tee.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Detenido por usuario.")
        print(f"   Log guardado en: {LOG_FILE}")