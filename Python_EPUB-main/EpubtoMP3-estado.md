# EPUBtoMP3 — Estado del proyecto

**Fecha de revisión:** 2026-03-31  
**Archivo principal:** `EPUBtoMP3.py`

---

## ¿Qué es EPUBtoMP3?

EPUBtoMP3 es un programa de línea de comandos en Python que convierte libros electrónicos
en formato `.epub` en audiolibros en formato `.mp3`, utilizando el motor de síntesis de
voz de Microsoft Edge TTS (neural, sin coste).

Está pensado para procesar colecciones completas de libros de forma desatendida: se le
indica una carpeta, elige qué libros convertir, y genera automáticamente los MP3 con sus
metadatos (título, autor, carátula, número de pista) listos para usar en cualquier
reproductor de audio.

---

## Funcionalidades

### Conversión EPUB → MP3
- Extrae el texto de cada capítulo del EPUB usando `ebooklib` y `BeautifulSoup`.
- Filtra contenido irrelevante (URLs, líneas vacías, espacios redundantes).
- Convierte cada capítulo en un archivo MP3 independiente con numeración ordenada.
- Descarta capítulos con menos de 200 caracteres (páginas de créditos, índices, etc.).

### Voces en español (Microsoft Neural TTS)
- **Hombre:** Álvaro (`es-ES-AlvaroNeural`)
- **Mujer:** Elvira (`es-ES-ElviraNeural`)
- Selector interactivo al inicio del proceso.

### Control de velocidad
- Normal (`+0%`), Rápida (`+10%`), Muy Rápida (`+25%`).
- Selector interactivo al inicio del proceso.

### Metadatos ID3 automáticos
- Escribe en cada MP3: título del capítulo, autor, álbum (título del libro) y número de pista.
- Incrusta la portada del libro (cover) si está disponible en el EPUB.

### Nomenclatura inteligente de archivos
- Si el capítulo tiene título propio: `001 - Título Capítulo - Nombre Libro.mp3`
- Si no tiene título: `001 - Nombre Libro.mp3`

### Procesado en lote
- Puede convertir un único libro o todos los EPUBs de una carpeta en una sola pasada.

### Descarga concurrente
- Descarga varios capítulos en paralelo (configurable: 2, 3 o 4 hilos) para acelerar el proceso.

### Dependencias
```
ebooklib  beautifulsoup4  edge-tts  tqdm  mutagen
```
Instalación: `pip install ebooklib beautifulsoup4 edge-tts tqdm mutagen`

---

## Diagnóstico previo

### Error recurrente observado

```
❌ Fallo descarga cap X: 503, message='Invalid response status',
   url='wss://speech.platform.bing.com/...'
```

El error `503` proviene del servidor de Microsoft Edge TTS (WebSocket). No es un bug
del código en sí, sino una respuesta del servidor que indica rechazo temporal por
sobrecarga o rate-limiting. Con 3 hilos simultáneos y pausa de solo 0.5s, el script
golpeaba el servidor demasiado agresivamente.

---

## Problemas identificados

| Prioridad | Problema | Descripción |
|-----------|----------|-------------|
| 🔴 Alta | Sin reintentos | Al primer `503`, el capítulo se perdía definitivamente (`return None`) |
| 🔴 Alta | Sin reanudación | Al relanzar, volvía a procesar todo desde cero aunque ya hubiera MP3s |
| 🟡 Media | Pausa insuficiente | `PAUSA_SEGURIDAD = 0.5s` era demasiado corta con 3 hilos |
| 🟡 Media | Concurrencia fija | `CONCURRENCIA = 3` hardcodeada, sin opción para el usuario |
| 🟢 Baja | Sin log de fallidos | No quedaba registro de qué capítulos no se generaron |
| 🟢 Baja | Etiquetado silencioso | Los errores en los tags ID3 se tragaban con `except: pass` |
| 🟢 Baja | Carpeta mal ubicada | La carpeta de salida se creaba en `os.getcwd()`, no junto al EPUB |

---

## Mejoras implementadas

### 1. Reintentos con backoff exponencial
- Hasta **3 reintentos** por capítulo antes de marcarlo como fallido.
- Esperas crecientes: **2s → 4s → 8s** entre intentos.
- Borra el archivo parcial antes de reintentar para evitar MP3s corruptos.

```python
REINTENTOS = 3
BACKOFF_BASE = 2   # → 2**1=2s, 2**2=4s, 2**3=8s
```

### 2. Reanudación automática (idempotencia)
- Antes de descargar, comprueba si el `.mp3` ya existe y tiene contenido (`size > 0`).
- Si existe, lo salta directamente.
- Al inicio de cada libro muestra: `✅ Ya hechos: X | ⏳ Pendientes: Y`

### 3. Pausa de seguridad aumentada
- De `0.5s` → **`1.5s`** entre capítulos.

### 4. Concurrencia configurable e interactiva
- Reducida por defecto de 3 → **2 hilos**.
- Nuevo menú al inicio para elegir 2, 3 o 4 hilos, con advertencia sobre el riesgo de 503.

### 5. Log de capítulos fallidos al final del libro
- Tras procesar cada libro, si algún capítulo no se pudo generar ni tras los reintentos:
  ```
  ⚠️  La voz dormida: 1 capítulo(s) NO convertido(s): [2]
  ```

### 6. Advertencias visibles en el etiquetado ID3
- `aplicar_tags_seguro` ahora devuelve `True/False`.
- Imprime aviso en consola si el etiquetado falla, en lugar de silenciarlo.

### 7. Carpeta de salida relativa al EPUB
- La carpeta de destino se crea en el mismo directorio que el archivo EPUB procesado,
  independientemente de desde dónde se ejecute Python.

---

## Configuración actual

```python
CONCURRENCIA   = 2      # configurable en el menú (2/3/4)
PAUSA_SEGURIDAD = 1.5   # segundos entre capítulos
REINTENTOS     = 3      # reintentos por capítulo
BACKOFF_BASE   = 2      # segundos base para el backoff (exponencial)
VOZ_HOMBRE     = "es-ES-AlvaroNeural"
VOZ_MUJER      = "es-ES-ElviraNeural"
```

---

## Nota futura

Si los 503 persisten en capítulos concretos incluso tras los 3 reintentos, una posible
mejora adicional sería **alternar la voz** (Álvaro ↔ Elvira) en cada reintento, ya que
el servidor TTS de Microsoft puede tratar diferente las distintas voces.
