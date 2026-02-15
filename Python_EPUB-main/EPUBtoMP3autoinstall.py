#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
================================================================================
EPUB TO MP3 CONVERTER (Auto-Install Edition)
================================================================================
Autor:       vibe coding de Oscar S. con Gemini
Descripción: Conversor de EPUB a MP3.
             Incluye gestión automática de dependencias y bypass de 
             protección PEP 668 en Linux (Debian/Ubuntu).
================================================================================
"""

import sys
import subprocess
import os
import platform
import asyncio
import re

# --- 1. GESTOR DE DEPENDENCIAS AUTOMÁTICO ---

def instalar_y_reiniciar():
    """
    Instala las librerías faltantes y reinicia el script.
    Maneja específicamente el error de entorno gestionado en Linux.
    """
    librerias = ['ebooklib', 'beautifulsoup4', 'edge-tts', 'tqdm', 'mutagen']
    sistema = platform.system()
    
    print("\n" + "!"*80)
    print("⚠️  FALTAN LIBRERÍAS NECESARIAS.")
    print(f"⏳ Iniciando instalación automática en {sistema}...")
    print("!"*80 + "\n")

    # Comando base de pip
    cmd = [sys.executable, "-m", "pip", "install"] + librerias

    try:
        # Intento 1: Instalación estándar
        subprocess.check_call(cmd)
    except subprocess.CalledProcessError:
        # Si falla en Linux, es probable que sea por el bloqueo PEP 668
        if sistema == "Linux":
            print("\n🔒 Detectado bloqueo de entorno gestionado (Debian/Ubuntu).")
            print("🔓 Aplicando corrección (--break-system-packages)...")
            try:
                # Intento 2: Forzar instalación
                cmd_force = cmd + ["--break-system-packages"]
                subprocess.check_call(cmd_force)
            except subprocess.CalledProcessError as e:
                print(f"\n❌ Error fatal instalando dependencias: {e}")
                sys.exit(1)
        else:
            print("\n❌ Error instalando dependencias. Revisa tu conexión a internet.")
            sys.exit(1)

    print("\n✅ Dependencias instaladas correctamente.")
    print("🔄 Reiniciando el programa para aplicar cambios...\n")
    
    # Reiniciamos el script automáticamente
    os.execv(sys.executable, [sys.executable] + sys.argv)

# Verificación inicial de importaciones
try:
    import ebooklib
    from ebooklib import epub
    from bs4 import BeautifulSoup
    import edge_tts
    from tqdm import tqdm
    from mutagen.mp3 import MP3
    from mutagen.id3 import ID3, TIT2, TPE1, APIC, TRCK, TALB, ID3NoHeaderError
except ImportError:
    instalar_y_reiniciar()

# --- SI LLEGAMOS AQUÍ, TODO ESTÁ LISTO ---

# --- CONFIGURACIÓN GLOBAL ---
CONCURRENCIA = 3          
PAUSA_SEGURIDAD = 0.5     
VOZ_HOMBRE = "es-ES-AlvaroNeural"
VOZ_MUJER = "es-ES-ElviraNeural"

# --- UTILIDADES ---

def limpiar_nombre_archivo(nombre):
    nombre = re.sub(r'[\\/*?:"<>|]', "", nombre).strip()
    return nombre[:100]

def limpiar_texto(texto):
    texto = re.sub(r'http\S+', '', texto)
    texto = re.sub(r'\n\s*\d+\s*\n', '\n', texto)
    texto = re.sub(r'\s+', ' ', texto)
    return texto.strip()

def obtener_titulo_capitulo(soup):
    header = soup.find(['h1', 'h2', 'h3'])
    if header:
        titulo = header.get_text().strip()
        if len(titulo) > 50: titulo = titulo[:50] + "..."
        return titulo
    return None

def mostrar_intro():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n" + "="*65)
    print("  EPUBtoMP3: Conversor Freeware de Libros Electrónicos a Audio")
    print(f"  Sistema: {platform.system()} | Dependencias: OK")
    print("-" * 65)
    print("  Si este software te resulta útil, considera invitarme a un café:")
    print("  ☕ Paypal: paypal.me/ossoney")
    print("  (Tu apoyo mantiene este código actualizado)")
    print("=" * 65 + "\n")

# --- EXTRACCIÓN ---

def extraer_datos_epub(ruta_epub):
    try:
        book = epub.read_epub(ruta_epub)
    except Exception as e:
        raise RuntimeError(f"Error leyendo archivo: {e}")
    
    try: titulo_libro = book.get_metadata('DC', 'title')[0][0]
    except: titulo_libro = "Sin Título"
    try: autor = book.get_metadata('DC', 'creator')[0][0]
    except: autor = "Autor Desconocido"

    cover_data = None
    cover_item = book.get_item_with_id('cover')
    if not cover_item:
        for item in book.get_items_of_type(ebooklib.ITEM_IMAGE):
            if 'cover' in item.get_name().lower():
                cover_item = item; break
    if cover_item: cover_data = cover_item.get_content()

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

# --- PROCESAMIENTO ---

def aplicar_tags_seguro(ruta, cap, titulo_libro, autor, cover_data):
    if not ruta or not os.path.exists(ruta): return
    if os.path.getsize(ruta) == 0: return 

    try:
        try: audio = MP3(ruta, ID3=ID3)
        except ID3NoHeaderError: audio = MP3(ruta); audio.add_tags()
        except: audio = MP3(ruta)

        if audio.tags is None:
            try: audio.add_tags()
            except: pass

        if audio.tags is not None:
            audio.tags.add(TIT2(encoding=3, text=cap['titulo']))
            audio.tags.add(TPE1(encoding=3, text=autor))
            audio.tags.add(TALB(encoding=3, text=titulo_libro))
            audio.tags.add(TRCK(encoding=3, text=str(cap['indice'])))
            if cover_data:
                audio.tags.add(APIC(encoding=3, mime='image/jpeg', type=3, desc=u'Cover', data=cover_data))
            audio.save()
    except Exception:
        pass

async def tarea_capitulo(sem, cap, carpeta_salida, voz, velocidad, titulo_libro, autor, cover_data):
    libro_seguro = limpiar_nombre_archivo(titulo_libro)
    
    if cap['tiene_titulo_real']:
        cap_seguro = limpiar_nombre_archivo(cap['titulo'])
        nombre_base = f"{cap['indice']:03d} - {cap_seguro} - {libro_seguro}"
    else:
        nombre_base = f"{cap['indice']:03d} - {libro_seguro}"
        
    nombre_archivo = f"{nombre_base}.mp3"
    ruta_completa = os.path.join(carpeta_salida, nombre_archivo)
    
    async with sem:
        try:
            communicate = edge_tts.Communicate(cap['texto'], voz, rate=velocidad)
            await communicate.save(ruta_completa)
            await asyncio.sleep(PAUSA_SEGURIDAD)
        except Exception as e:
            print(f"\n❌ Error descargando cap {cap['indice']}: {e}")
            return None

    aplicar_tags_seguro(ruta_completa, cap, titulo_libro, autor, cover_data)
    return ruta_completa

async def convertir_libro(ruta_epub, velocidad, voz_elegida):
    print(f"\n📚 Analizando: {os.path.basename(ruta_epub)}...")
    
    try:
        titulo_libro, autor, cover_data, capitulos = extraer_datos_epub(ruta_epub)
    except Exception as e:
        print(f"❌ Error crítico leyendo EPUB: {e}")
        return
    
    nombre_carpeta = limpiar_nombre_archivo(f"{autor} - {titulo_libro}")
    if not os.path.exists(nombre_carpeta):
        os.makedirs(nombre_carpeta)
    
    print(f"   📂 Destino: {nombre_carpeta}/")
    print(f"   📑 Capítulos detectados: {len(capitulos)}")
    print(f"   🚀 Modo Turbo: {CONCURRENCIA} hilos")

    sem = asyncio.Semaphore(CONCURRENCIA)
    tareas = []
    
    for cap in capitulos:
        task = tarea_capitulo(sem, cap, nombre_carpeta, voz_elegida, velocidad, titulo_libro, autor, cover_data)
        tareas.append(task)
    
    pbar = tqdm(total=len(tareas), unit="cap", leave=False, desc="Procesando")
    for f in asyncio.as_completed(tareas):
        await f
        pbar.update(1)
        
    pbar.close()
    print(f"   ✅ Libro completado: {titulo_libro}\n")

# --- MENÚS ---

def pedir_voz():
    print("\n🗣️  SELECTOR DE VOZ")
    print("1. Hombre (Álvaro) - Default")
    print("2. Mujer (Elvira)")
    opcion = input("   > Elige opción (1-2): ").strip()
    if opcion == "2": return VOZ_MUJER
    return VOZ_HOMBRE

def pedir_velocidad():
    print("\n⚡ SELECTOR DE VELOCIDAD")
    print("1. Normal (0%)")
    print("2. Rápida (+10%)")
    print("3. Muy Rápida (+25%)")
    opcion = input("   > Elige opción (1-3): ").strip()
    if opcion == "2": return "+10%"
    if opcion == "3": return "+25%"
    return "+0%"

def seleccionar_archivos():
    ruta_actual = os.getcwd()
    ruta_input = input(f"\n📂 Ruta (Enter para '{ruta_actual}'): ").strip()
    ruta_carpeta = ruta_input if ruta_input else ruta_actual
    
    if not os.path.exists(ruta_carpeta):
        sys.exit("❌ La ruta no existe.")
        
    archivos = [f for f in os.listdir(ruta_carpeta) if f.lower().endswith(".epub")]
    if not archivos:
        sys.exit("❌ No hay archivos .epub aquí.")
        
    print(f"\nLibros encontrados en: {os.path.abspath(ruta_carpeta)}")
    for i, f in enumerate(archivos):
        print(f"{i+1}. {f}")
        
    opcion = input("\n[A] Todos | [Nº] Uno específico: ").strip().upper()
    
    if opcion == 'A':
        return [os.path.join(ruta_carpeta, f) for f in archivos]
    try:
        idx = int(opcion)
        if 1 <= idx <= len(archivos):
             return [os.path.join(ruta_carpeta, archivos[idx-1])]
    except:
         pass
    sys.exit("❌ Opción inválida.")

# --- MAIN ---

async def main():
    mostrar_intro()
    libros = seleccionar_archivos()
    voz = pedir_voz()
    velocidad = pedir_velocidad()
    
    print(f"\n🚀 Iniciando proceso para {len(libros)} libro(s)...")
    for libro in libros:
        await convertir_libro(libro, velocidad, voz)
        
    print("🎉 ¡TODO FINALIZADO! Gracias por usar EPUBtoMP3. 🎉")

if __name__ == "__main__":
    try:
        if platform.system() == 'Windows':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Proceso detenido manualmente.")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")