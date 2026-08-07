# EPUBtoXteink

## 📖 ¿Qué hace y para qué sirve?
`EPUBtoXteink.py` es una potente utilidad de optimización creada para adaptar libros electrónicos (EPUBs) de gran tamaño o con mucho formato, para que sean perfectamente legibles en lectores de tinta electrónica (e-readers) con hardware muy limitado, como los modelos **Xteink X3** y **Xteink X4 / X4 Pro**.

Los lectores de tinta electrónica antiguos o de gama baja suelen congelarse, sufrir cuelgues por falta de RAM, o no mostrar bien las imágenes en color. Este programa soluciona todo eso al purgar el código innecesario, dividir los capítulos inmensos, y procesar todas las imágenes en una escala de grises optimizada. Genera un nuevo archivo **`_XteinkX3.epub`** o **`_XteinkX4.epub`** (según el modelo elegido) sumamente ligero y estable, preservando siempre el original.

### 📱 Perfiles de Dispositivo Soportados

| Modelo | Pantalla | Resolución | PPI | RAM / CPU |
|--------|----------|------------|-----|-----------|
| **Xteink X3** | 3.7" | 480 × 640 px | ≈250 | 128 MB / ESP32 |
| **Xteink X4 / X4 Pro** | 4.3" | 480 × 800 px | ≈220 | 128 MB / ESP32 |

Al arrancar, el programa te pregunta por tu modelo. Las imágenes se redimensionan al límite exacto de la pantalla de tu dispositivo. El umbral de splitting de capítulos (300 KB) es idéntico en ambos, ya que comparten la misma RAM y procesador.

## ⚙️ Funciones Principales

- **`_optimize_image(file_path)`**: Es el núcleo de procesamiento visual. Toma cada imagen del libro y le aplica un pipeline de optimización: borra imágenes minúsculas innecesarias, aplana los canales Alpha (para evitar fondos negros), **reduce la resolución al límite exacto de la pantalla del dispositivo seleccionado** (X3: 480×640 px, X4 / X4 Pro: 480×800 px), y convierte todo a escala de grises usando la técnica *Dithering Floyd-Steinberg* a 16 colores. Esto mejora inmensamente el contraste y la nitidez en pantallas e-ink.
- **`select_device()`**: Presenta al usuario un selector de modelo (X3 o X4 / X4 Pro) al inicio del programa y al pulsar la opción [4] del menú. Carga el perfil correcto de resolución de pantalla para el dispositivo elegido, garantizando que las imágenes se adapten con precisión al hardware real sin desperdiciar memoria.
- **`_purge_html_soup(soup)`**: Limpia por completo el HTML interno del libro. Elimina de un plumazo scripts, CSS pesados, iframes, audios y clases de estilo que el hardware limitado no puede procesar, dejando el contenido en su forma más pura y ligera.
- **`_optimize_and_split_html(file_path, opf_modifier_queue)`**: ¡La salvación para la memoria RAM! Si detecta un capítulo HTML que pesa más de 300 KB, lo divide físicamente en dos partes. El proceso es **iterativo**: si la parte resultante sigue siendo demasiado grande, vuelve a dividirse hasta que todos los fragmentos están por debajo del umbral. Esto evita que el e-reader intente cargar todo el capítulo a la vez en su pequeña memoria y termine crasheando (colapsando).
- **`_patch_opf_manifest(...)`**: Tras haber dividido los capítulos pesados, esta función reescribe inteligentemente el archivo OPF (el "mapa" o índice interno del EPUB), añadiendo los nuevos capítulos divididos en su orden correcto. Usa **`lxml.etree`** de forma nativa cuando está disponible para preservar namespaces XML con total fidelidad.
- **`_patch_ncx(...)`**: Complementa al parcheo del OPF actualizando el **`toc.ncx`** (tabla de contenidos de EPUB 2). Para cada capítulo dividido, inserta un nuevo `navPoint` etiquetado como "(cont.)" justo después del original y renumera todos los `playOrder` de forma secuencial. Garantiza que la navegación del índice en el e-reader sea continua e imperceptible.
- **`process_single_epub(epub)`**: Orquesta todo el flujo de trabajo en un único libro. Extrae sus entrañas, lanza múltiples hilos de procesamiento para sus imágenes, limpia el HTML, parchea el manifiesto y lo vuelve a empaquetar respetando los estrictos estándares del formato EPUB.

## 📦 Librerías Necesarias
Asegúrate de instalar las siguientes dependencias mediante la terminal:

```bash
pip install beautifulsoup4 Pillow lxml
```

- **`beautifulsoup4`**: Esencial para navegar y modificar los archivos `.html` y `.xml` internos del EPUB sin romper su estructura.
- **`Pillow` (PIL)**: La librería gráfica que se encarga del redimensionamiento, aplanado y de la aplicación del *dithering* Floyd-Steinberg en las imágenes.
- **`lxml`**: *Opcional pero altamente recomendado*. Es un motor ("parser") de procesamiento HTML y XML extremadamente rápido que acelera drásticamente la purga y el split de los libros si está instalado.

## ✨ Ventajas Relevantes
- **Optimización por Dispositivo**: El programa pregunta al arranque si tu lector es un X3 o un X4 / X4 Pro y ajusta automáticamente los límites de resolución de imagen a la pantalla real de cada modelo. El archivo resultante (e.g. `_XteinkX3.epub`) queda identificado claramente para evitar mezclas.
- **Procesamiento Híbrido y Multihilo**: Al procesar las imágenes usando 8 hilos en paralelo (Threadpool), el programa funciona de manera ultrarrápida, aprovechando al máximo la CPU del usuario.
- **Dithering Floyd-Steinberg**: Las imágenes no solo se pasan a blanco y negro; el dithering simula sombras y gradientes utilizando patrones de puntos, haciendo que las imágenes se vean impresionantes incluso en pantallas sin colores.
- **Prevención Anti-Crashes**: La división automática de capítulos (RAM Splitting) asegura que no exista ningún libro que tu e-reader no pueda abrir o pasar de página de forma fluida.
- **Preservación del Original**: Nunca destruye tu archivo original, siempre crea uno nuevo con la terminación `_XteinkX3.epub` o `_XteinkX4.epub` según el modelo seleccionado.
- **Detección de idioma y Modo Simulación**: Se adapta a tu idioma y te permite probar el proceso (Dry-Run) antes de aplicar cambios a tu biblioteca real.
