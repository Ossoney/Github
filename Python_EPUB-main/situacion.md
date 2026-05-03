# Situación Actual del Proyecto (Python_EPUB)
*Documento de estado para retomar el trabajo en el futuro.*

Este documento resume las últimas optimizaciones, cambios arquitectónicos y documentaciones realizadas a lo largo de la suite de herramientas. El objetivo principal ha sido estandarizar, documentar y llevar al límite el rendimiento de todos los scripts.

---

## 1. 📖 Documentación Global (Los Manuales)
Se ha generado un archivo `.md` (Markdown) para cada uno de los programas principales del repositorio. Estos documentos actúan como pequeños manuales de usuario y referencias técnicas. Si en el futuro dudas de qué hace un script o qué librerías necesita, solo tienes que leer su `.md`:
- `EPUBtoMP3.md`
- `EPUBtoXteink.md`
- `PDFtoCBZ.md`
- `PDFCBZtoEPUB.md`
- `ComicReducer.md`

---

## 2. ⚡ Optimizaciones en Código (Scripts Tocados)

### `ComicReducer.py` (Antes comicreducer.py)
- **Renombrado**: Se cambió el nombre a *CamelCase* para mantener consistencia visual con el resto de las herramientas (como `PDFtoCBZ.py`). El archivo original en minúsculas fue eliminado.
- **Resultado Totalizador**: Se modificó la lógica interna para que, en lugar de terminar abruptamente, recopile datos durante toda la sesión. Al finalizar, imprime un resumen estadístico detallado: número de cómics procesados, cuántos se omitieron (porque ya existían), cuántos fallaron, y lo más importante: **el total exacto de Megabytes que se ahorraron en el disco duro.**
- **Claridad de guardado**: El menú ahora avisa claramente al usuario que los cómics reducidos se guardan en la *misma carpeta* que el original pero añadiendo `_optimized.cbz`.

### `PDFCBZtoEPUB.py` (El Titán)
Se solicitó que este programa fuese **más rápido, más potente y perfecto**, pero respetando la arquitectura de un solo archivo. Se inyectaron modificaciones "quirúrgicas" de alto rendimiento:
1. **Multiprocesamiento (Anti-GIL)**: La fase de conversión de imágenes masivas en CBZs se modificó para usar `ProcessPoolExecutor` nativo (aprovechando los núcleos de la CPU al máximo) en lugar de `ThreadPoolExecutor`, lo que aniquila los tiempos de espera largos.
2. **Auto-Cropping Automático**: Se inyectó código que utiliza la función matemática `ImageChops.difference` para detectar y recortar milimétricamente cualquier margen completamente blanco o liso alrededor de las páginas de los cómics antes de optimizarlas. Esto permite maximizar el tamaño del contenido en pantallas de e-readers.
3. **Flujo Lazy Loading (Gestión de RAM)**: Originalmente, el script leía **todas** las páginas de un archivo ZIP y las guardaba en la memoria RAM antes de mandarlas a procesar, lo cual podía colgar computadoras con archivos CBZ de más de 1 GB. Se modificó el bucle para extraer temporalmente "crudos" al disco, procesarlos y luego borrar el crudo; logrando que el consumo de memoria RAM se mantenga bajo y estable de principio a fin.
4. **Passthrough Respetado**: Se validó y unificó la lógica que permite trasladar JPGs originales sin re-codificarlos si estos ya cumplen con los requisitos de tamaño, garantizando pérdida "cero".

---

## 3. 🎯 Siguientes Pasos Sugeridos
Si en el futuro deseas retomar y mejorar el proyecto, aquí hay algunas ideas de donde partir:
- **Testing en Entornos Aislados**: Correr una batería de pruebas con archivos masivos (Ej: Un CBZ de 2GB) a través de `PDFCBZtoEPUB.py` para asegurar que el `ProcessPoolExecutor` y el borrado de disco temporal actúan de forma perfecta en tu SO.
- **Tesseract OCR**: Implementar OCR (Reconocimiento Óptico de Caracteres) opcional en `PDFCBZtoEPUB.py` para PDFs que sean 100% imágenes pero contengan revistas (poder detectar los títulos de capítulos de una imagen rasterizada).
- **Consolidación de requirements**: Actualmente la dependencia `edge-tts` está en el MP3, `lxml` en Xteink, etc. Podría crearse un gran archivo `requirements.txt` global unificado para facilitar la instalación del entorno virtual en el futuro.
