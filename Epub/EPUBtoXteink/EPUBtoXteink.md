# EPUBtoXteink

## 📖 ¿Qué hace y para qué sirve?
``EPUBtoXteink.py`` es una potente utilidad de optimización creada para adaptar libros electrónicos (EPUBs) de gran tamaño o con mucho formato, para que sean perfectamente legibles en lectores de tinta electrónica (e-readers) con hardware muy limitado, como los modelos **Xteink X3** y **Xteink X4 / X4 Pro**.

Los lectores de tinta electrónica de gama baja suelen congelarse, sufrir cuelgues por falta de RAM, o no mostrar bien las imágenes en color. Este programa soluciona todo eso al purgar el código innecesario, dividir los capítulos inmensos, y procesar todas las imágenes en el formato óptimo para cada dispositivo. Genera un nuevo archivo **``_X3.epub``**, **``_X4.epub``** o **``_X4p.epub``** (según el modelo elegido) sumamente ligero y estable, preservando siempre el original.

### 📱 Perfiles de Dispositivo Soportados

| Modelo | Selección | Pantalla | Resolución (portrait) | PPI | RAM / CPU | Sufijo |
|--------|-----------|----------|-----------------------|-----|-----------|--------|
| **Xteink X3** | [1] | 3.7" | 480 × 640 px | ≈250 | 128 MB / ESP32 | `_X3` |
| **Xteink X4** | [2] | 4.3" | 480 × 800 px | ≈220 | 128 MB / ESP32-S3R8 | `_X4` |
| **Xteink X4 Pro** | [3] | 4.3" | 480 × 800 px | ≈220 | 128 MB / ESP32-S3R8 | `_X4p` |

Al arrancar, el programa pregunta tu modelo y carga el perfil de resolución correcto. El umbral de splitting (300 KB) es idéntico en todos los modelos por compartir la misma restricción de RAM por página.

## ⚙️ Funciones Principales

- **``_optimize_image(file_path)``**: Núcleo de procesamiento visual. Pipeline de 6 pasos:
  1. Elimina imágenes decorativas diminutas (≤ 15 px).
  2. Redimensiona al máximo de la pantalla del dispositivo (X3: 480×640 px, X4: 480×800 px).
  3. Aplana canal Alpha sobre fondo blanco (evita fondos negros en PNGs transparentes).
  4. Convierte a escala de grises de 8 bits.
  5. Aplica **Dithering Floyd-Steinberg cuantizado a los 4 niveles de gris nativos del panel** E-Ink: negro ``#000000``, gris oscuro ``#555555``, gris claro ``#AAAAAA``, blanco ``#FFFFFF``. Cuantizar aquí (en el PC) evita que el ESP32 consuma RAM haciéndolo en tiempo real.
  6. Guarda como **BMP 24 bits RGB** — el formato más compatible con todos los firmwares del X4 Pro (CrossPoint, CrossInk y oficial). El formato 24 bits elimina la tabla de paleta (CLUT) que causaba colores invertidos. Los 4 valores RGB posibles coinciden exactamente con los 4 estados físicos del panel.

  El fichero original (.jpg, .png, .webp, etc.) se elimina automáticamente tras crear el .bmp.

- **``select_device()``**: Selector de modelo al inicio y desde la opción [4] del menú. Carga el perfil de resolución correcto para que las imágenes se adapten con precisión al hardware real.

- **``_purge_html_soup(soup)``**: Limpia el HTML interno del libro eliminando scripts, CSS pesados, iframes, audios y clases de estilo. **También reescribe todos los atributos ``src`` de ``<img>`` y ``<image>`` para apuntar a los nuevos ficheros ``.bmp``**, incluyendo elementos SVG con ``xlink:href``.

- **``_optimize_and_split_html(file_path, opf_modifier_queue)``**: Si un capítulo HTML supera 300 KB, lo divide en dos partes. El proceso es **iterativo**: si la parte resultante sigue siendo demasiado grande, vuelve a dividirse hasta que todos los fragmentos quedan bajo el umbral. Evita cuelgues de RAM en el e-reader.

- **``_patch_opf_images(temp_dir)``**: Tras convertir las imágenes a BMP, actualiza el manifiesto OPF reemplazando todos los ``href`` de imágenes por sus equivalentes ``.bmp`` y fijando el ``media-type`` a ``image/bmp``. Usa ``lxml.etree`` cuando está disponible (fallback a BeautifulSoup).

- **``_patch_opf_manifest(...)``**: Tras dividir capítulos, reescribe el OPF añadiendo los nuevos ``_part2`` en el orden correcto. Usa **``lxml.etree``** nativo para preservar namespaces XML con total fidelidad.

- **``_patch_ncx(...)``**: Actualiza el **``toc.ncx``** (tabla de contenidos EPUB 2): inserta un ``navPoint`` "(cont.)" por cada capítulo dividido y renumera todos los ``playOrder`` secuencialmente. Usa ``lxml.etree`` o BeautifulSoup como fallback.

- **``_patch_nav(...)``**: Actualiza el archivo de navegación **``nav.xhtml`` / ``toc.xhtml``** (estándar EPUB 3): inserta los nuevos enlaces de lista ``<li>`` "(cont.)" para mantener la tabla de contenidos interactiva sincronizada.

- **``process_single_epub(epub)``**: Orquesta el flujo completo de un libro: extracción, procesado multihilo de imágenes, actualización del OPF de imágenes, limpieza y splitting de HTML, parcheo del OPF, NCX y NAV, y reempaquetado en EPUB estándar.

## 🚀 Uso por Línea de Comandos (CLI) y Persistencia
Además del menú interactivo, el programa permite ejecutar optimizaciones directas por terminal:
```bash
# Optimizar una carpeta completa
python EPUBtoXteink.py "C:\MisLibros" --device X4p

# Optimizar un único archivo EPUB
python EPUBtoXteink.py "C:\MisLibros\libro.epub" --device X4p

# Simulación (Dry-Run) sin modificar archivos
python EPUBtoXteink.py "C:\MisLibros\libro.epub" --dry-run
```
El programa almacena automáticamente en **``config.json``** la última carpeta y el modelo seleccionado, permitiendo entrar de inmediato al menú interactivo en los siguientes arranques sin preguntas repetitivas.

## 📦 Librerías Necesarias
```bash
pip install beautifulsoup4 Pillow lxml
```

- **``beautifulsoup4``**: Navega y modifica los archivos ``.html`` y ``.xml`` internos del EPUB.
- **``Pillow`` (PIL)**: Redimensionamiento, aplanado Alpha, dithering Floyd-Steinberg y conversión a BMP 24 bits.
- **``lxml``**: *Opcional pero altamente recomendado*. Parser HTML/XML ultrarrápido; también usado de forma nativa para el parcheo del OPF y del NCX preservando namespaces XML.

## ✨ Ventajas Relevantes
- **BMP 24 bits — Máxima Compatibilidad**: Imágenes en BMP sin tabla de paleta (CLUT), RGB 24 bits. Compatible con CrossPoint, CrossInk y firmware oficial sin riesgo de colores invertidos.
- **4 Grises Nativos del Panel**: El dithering se cuantiza a los 4 niveles físicos exactos del panel E-Ink. El ESP32 recibe la imagen lista para pintar sin gastar RAM en re-cuantizar.
- **Optimización por Dispositivo**: Resolución adaptada automáticamente al modelo (X3 o X4 / X4 Pro) con perfil independiente por pantalla.
- **Procesamiento Multihilo**: Imágenes procesadas en paralelo con ``min(8, CPU cores)`` hilos.
- **Prevención Anti-Crashes**: División iterativa de capítulos — ningún fragmento supera 300 KB sin importar el tamaño original.
- **OPF y NCX coherentes**: Manifiesto y tabla de contenidos siempre sincronizados tras splitting y conversión de imágenes.
- **Preservación del Original**: Siempre crea un fichero nuevo (``_XteinkX3.epub`` o ``_XteinkX4.epub``) sin tocar el original.
- **Bilingüe y Dry-Run**: Interfaz en español o inglés según el sistema. Modo simulación para verificar antes de aplicar.
