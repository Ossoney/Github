# EPUBtoMP3

## 📖 ¿Qué hace y para qué sirve?
`EPUBtoMP3.py` es un script en Python diseñado para transformar libros electrónicos en formato EPUB en audiolibros completos en formato MP3. Funciona extrayendo el texto de cada capítulo del libro y utilizando las voces neuronales de Microsoft Edge (Text-To-Speech) para generar archivos de audio de alta calidad. 

Es la herramienta perfecta para quienes prefieren escuchar sus libros electrónicos mientras conducen, caminan o realizan otras actividades, creando audiolibros realistas y separados por capítulos de forma totalmente automática.

## ⚙️ Funciones Principales

- **`extraer_datos_epub(ruta_epub)`**: Abre el archivo EPUB original y extrae toda su información vital: título, autor, imagen de portada (cover) y el texto de cada uno de sus capítulos. Se encarga de limpiar el HTML para obtener un texto puro y fluido.
- **`tarea_capitulo(...)`**: Es el "motor" o "worker" de conversión. Descarga el audio generado para un capítulo específico. Incluye un sistema inteligente de reintentos (backoff exponencial) en caso de que haya cortes de conexión o limitaciones de la red.
- **`convertir_libro(ruta_epub, velocidad, voz_elegida)`**: Orquesta la conversión de un libro entero. Gestiona la creación de la carpeta de salida (nombrada con Autor y Título), salta los capítulos que ya hayan sido convertidos previamente (ideal por si se interrumpe el proceso) y lanza múltiples hilos de descarga simultánea para acelerar el trabajo.
- **`aplicar_tags_seguro(...)`**: Incrusta metadatos ID3 en cada archivo MP3 generado. Esto asegura que, al abrir el audio en un reproductor de música o del coche, aparezca la carátula original del libro, el nombre del capítulo, el artista (autor) y el álbum (título del libro).
- **`seleccionar_archivos()`**: Proporciona una interfaz interactiva de consola para que el usuario pueda elegir si convertir un solo libro de la carpeta actual o todos a la vez.

## 📦 Librerías Necesarias
Para que el programa funcione correctamente, necesitas instalar las siguientes dependencias mediante la terminal:

```bash
pip install ebooklib beautifulsoup4 edge-tts tqdm mutagen
```

- **`ebooklib`**: Para leer e inspeccionar el interior del archivo `.epub`.
- **`beautifulsoup4`**: Para limpiar las etiquetas HTML del libro y extraer únicamente el texto a leer.
- **`edge-tts`**: La librería estrella; se conecta a los servidores de Microsoft Edge para generar las voces neuronales (voces muy naturales y expresivas).
- **`tqdm`**: Muestra una barra de progreso visual en la consola.
- **`mutagen`**: Permite incrustar la carátula y los metadatos ID3 directamente dentro de los archivos MP3 finales.

## ✨ Ventajas Relevantes
- **Voces Neuronales**: Al usar `edge-tts`, las voces suenan muy humanas y fluidas, a diferencia de los antiguos sistemas TTS robóticos.
- **Multihilo (Descarga Concurrente)**: Procesa varios capítulos a la vez, reduciendo el tiempo de espera.
- **Tolerancia a fallos**: Si se corta internet o se interrumpe el script, al volver a iniciarlo saltará automáticamente los MP3 que ya están terminados.
- **Etiquetado perfecto**: Tus audiolibros lucirán como álbumes de música profesionales en cualquier reproductor gracias al auto-etiquetado con carátulas.
