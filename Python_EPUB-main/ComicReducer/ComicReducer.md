# ComicReducer

## 📖 ¿Qué hace y para qué sirve?
`ComicReducer.py` es una utilidad especializada y rápida creada para los puristas del cómic digital. Su objetivo principal es tomar archivos de cómics pesados (en formatos estandarizados CBR o CBZ) y reducir drásticamente su tamaño de almacenamiento sin percibir pérdida visual de calidad.

Es la solución ideal para quienes tienen colecciones inmensas de cómics en discos duros o tablets y necesitan liberar espacio urgentemente. El programa transforma las imágenes interiores a formatos mucho más eficientes (WebP) y reduce dimensiones titánicas a tamaños amigables y legibles para cualquier pantalla moderna.

## ⚙️ Funciones Principales

- **`extract_comic(input_file, temp_folder)`**: El punto de partida. Se encarga de abrir y desempaquetar el contenido del CBR o CBZ en una carpeta temporal segura. Primero intenta abrirlo como ZIP (muchos CBR son simplemente ZIP renombrados); si falla, delega en **7-Zip** para manejar RAR y cualquier otro formato.
- **`process_single_image(image_path, target_height, quality)`**: El motor visual del programa. Toma la imagen extraída y realiza tres pasos vitales: 
  1. La redimensiona (Downscaling) si su altura excede el `target_height` (por defecto 1600px), usando el suave algoritmo Lanczos para evitar bordes dentados.
  2. Analiza matemáticamente si la imagen es en blanco y negro puro; de ser así, descarta los colores guardando la imagen en escala de grises.
  3. Convierte la imagen al formato súper eficiente `WebP`.
- **`optimize_comic(input_file, target_height, quality)`**: Orquesta el flujo de un cómic en su totalidad. Llama a la extracción, procesa todas las imágenes detectadas a través de hilos concurrentes para mayor velocidad, y luego utiliza `pack_comic` para volver a empaquetarlo. Finaliza calculando y reportando los Megabytes exactos que te ha hecho ahorrar.
- **`obtener_todos_comics(...)` y Manejo de Directorios**: Dispone de menús interactivos donde el usuario puede seleccionar carpetas detectadas automáticamente (por índice o rango como `1-5`), introducir rutas absolutas o relativas manualmente, e incluso decidir si incluir subcarpetas en el proceso.
- **Resultado Totalizador**: Al terminar una sesión, imprime en pantalla un balance detallado: cantidad de cómics exitosos, omitidos, fallidos, peso total original vs nuevo, y porcentaje de espacio liberado en tu disco.

## 📦 Librerías Necesarias
Para utilizar el programa, necesitas instalar lo siguiente en tu terminal:

```bash
pip install Pillow numpy tqdm
```

- **`Pillow` (PIL)**: Librería fundamental que ejecuta la magia de abrir la imagen original, redimensionarla proporcionalmente y exportarla en el nuevo y ligero formato WebP.
- **`numpy`**: Permite calcular las diferencias de color entre los píxeles de una imagen de forma hiperveloz para detectar automáticamente si el cómic se encuentra en blanco y negro.
- **`tqdm`**: Muestra amigables barras de progreso animadas en la consola mientras se optimizan las imágenes.

> ⚠️ **Requisito externo**: Para procesar archivos `.cbr` (RAR), instala **[7-Zip](https://www.7-zip.org)** (gratuito). El programa lo detecta automáticamente en su ruta estándar de Windows.

## ✨ Ventajas Relevantes
- **Redimensionado Inteligente**: Al fijar un límite de altura de 1600px (ideal para tablets como iPad o Galaxy Tab), evita que las imágenes tengan dimensiones absurdamente grandes (como 4000px) que solo consumen espacio inútil sin brindar más nitidez en pantallas normales.
- **Compresión WebP**: El uso del códec WebP con método de compresión 6 ofrece una reducción de peso monumental comparado al típico JPEG, reteniendo mucha más calidad en colores y texturas.
- **Velocidad Multiproceso**: En lugar de modificar página por página de forma secuencial, utiliza todos los núcleos de tu procesador (ProcessPoolExecutor) para optimizar un montón de páginas al unísono.
- **Protección Original**: Nunca sobreescribe el cómic que tienes; genera uno nuevo en la misma carpeta con el sufijo `_optimized.cbz` para que puedas verificar que se ve excelente antes de borrar el original.
