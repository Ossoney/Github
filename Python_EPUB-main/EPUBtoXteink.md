# EPUBtoXteink

## 📖 ¿Qué hace y para qué sirve?
`EPUBtoXteink.py` es una potente utilidad de optimización creada para adaptar libros electrónicos (EPUBs) de gran tamaño o con mucho formato, para que sean perfectamente legibles en lectores de tinta electrónica (e-readers) con hardware muy limitado, como los modelos Xteink X3/X4. 

Los lectores de tinta electrónica antiguos o de gama baja suelen congelarse, sufrir cuelgues por falta de RAM, o no mostrar bien las imágenes en color. Este programa soluciona todo eso al purgar el código innecesario, dividir los capítulos inmensos, y procesar todas las imágenes en una escala de grises optimizada, generando un nuevo archivo `_Xteink.epub` sumamente ligero y estable.

## ⚙️ Funciones Principales

- **`_optimize_image(file_path)`**: Es el núcleo de procesamiento visual. Toma cada imagen del libro y le aplica un pipeline de optimización: borra imágenes minúsculas innecesarias, aplana los canales Alpha (para evitar fondos negros), reduce la resolución al límite soportado por el e-reader (758x1024), y convierte todo a escala de grises usando la técnica *Dithering Floyd-Steinberg* a 16 colores. Esto mejora inmensamente el contraste y la nitidez en pantallas e-ink.
- **`_purge_html_soup(soup)`**: Limpia por completo el HTML interno del libro. Elimina de un plumazo scripts, CSS pesados, iframes, audios y clases de estilo que el hardware limitado no puede procesar, dejando el contenido en su forma más pura y ligera.
- **`_optimize_and_split_html(file_path, opf_modifier_queue)`**: ¡La salvación para la memoria RAM! Si detecta un capítulo HTML que pesa más de 300 KB, lo divide físicamente en dos partes. Esto evita que el e-reader intente cargar todo el capítulo a la vez en su pequeña memoria y termine crasheando (colapsando).
- **`_patch_opf_manifest(...)`**: Tras haber dividido los capítulos pesados, esta función reescribe inteligentemente el archivo OPF (el "mapa" o índice interno del EPUB), añadiendo los nuevos capítulos divididos en su orden correcto para que la transición en el e-reader sea imperceptible.
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
- **Procesamiento Híbrido y Multihilo**: Al procesar las imágenes usando 8 hilos en paralelo (Threadpool), el programa funciona de manera ultrarrápida, aprovechando al máximo la CPU del usuario.
- **Dithering Floyd-Steinberg**: Las imágenes no solo se pasan a blanco y negro; el dithering simula sombras y gradientes utilizando patrones de puntos, haciendo que las imágenes se vean impresionantes incluso en pantallas sin colores.
- **Prevención Anti-Crashes**: La división automática de capítulos (RAM Splitting) asegura que no exista ningún libro que tu e-reader no pueda abrir o pasar de página de forma fluida.
- **Preservación del Original**: Nunca destruye tu archivo original, siempre crea uno nuevo con la terminación `_Xteink.epub`.
- **Detección de idioma y Modo Simulación**: Se adapta a tu idioma y te permite probar el proceso (Dry-Run) antes de aplicar cambios a tu biblioteca real.
