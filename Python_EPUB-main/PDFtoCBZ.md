# PDFtoCBZ Optimizer

## 📖 ¿Qué hace y para qué sirve?
`PDFtoCBZ.py` es una potente herramienta diseñada específicamente para los amantes de los cómics digitales. Su función principal es transformar pesados archivos PDF (que a menudo contienen imágenes o escaneos de alta resolución sin comprimir) en el formato nativo para cómics `CBZ` (Comic Book Zip). 

Al realizar esta conversión, el programa optimiza, comprime y reescala automáticamente todas las páginas del cómic. El resultado es un archivo mucho más ligero, ágil a la hora de cargarse en visores de cómics (como CDisplayEx, Perfect Viewer, etc.) o e-readers, y visualmente nítido.

## ⚙️ Funciones Principales

- **`detectar_problema_calidad(img, pdf_nombre)`**: Esta es la mente analítica del programa. Analiza una página de muestra del PDF midiendo su varianza (contraste y detalles) y su nivel de gris. Con base en estos datos matemáticos, decide automáticamente si el PDF tiene una calidad pobre, media o normal, y asigna el "Modo de Calidad" adecuado (`normal`, `alta`, o `pdf_like`).
- **`convertir_pdf_kcc(pdf_path)`**: Es el flujo principal de trabajo por cada PDF. Extrae las páginas una a una usando una resolución en PPP (DPI) específica según el modo detectado. Si el PDF original crece en tamaño tras la conversión (algo que no debería pasar), la función aplica un mecanismo de "Fail-Safe", aborta, y utiliza automáticamente el protocolo `PDF-LIKE` para asegurar la reducción de peso.
- **`optimizar_kcc_oasis(imagen)`**: Una función que trata cada imagen individualmente emulando los perfiles óptimos del lector Kindle Oasis (KCC). Ajusta el contraste (+10%), aplica un poco de nitidez extra (+5%) y recorta/reescala de ser necesario. Además, auto-detecta si la imagen es en Blanco y Negro; si lo es, elimina por completo los canales de color (convirtiendo la imagen a modo 'L'), lo cual reduce el peso de la imagen significativamente sin perder ningún detalle.
- **`modo_pdf_like(doc, temp_dir, npags)`**: Este es el modo de rescate o "Lossless". Si el PDF ya estaba muy optimizado o era puro texto/imágenes con problemas al rasterizarse, esta función en lugar de "tomarle fotos" a las páginas, extrae la imagen binaria original exacta que está embebida en el PDF sin tocarle un solo píxel, asegurando que el cómic conserve toda su calidad intrínseca.
- **`crear_zip_desde_temp(...)`**: Una vez que todas las imágenes han sido optimizadas y guardadas en una carpeta temporal, esta función las empaqueta metódicamente en el formato de deflación ZIP nivel 9, pero con la extensión final `.cbz`.

## 📦 Librerías Necesarias
Para que este programa funcione correctamente, necesitas ejecutar en tu terminal:

```bash
pip install PyMuPDF Pillow numpy
```

- **`PyMuPDF` (fitz)**: Es la librería estrella para manejar documentos PDF. Es extremadamente rápida renderizando y extrayendo las imágenes del archivo original.
- **`Pillow` (PIL)**: Utilizada para todo el procesamiento visual (mejorar contraste, nitidez, reescalado con algoritmo Lanczos y conversión a escala de grises).
- **`numpy`**: Imprescindible para hacer cálculos matemáticos ultra veloces sobre los arrays de píxeles de las imágenes (ej. calcular la varianza y la diferencia entre canales RGB para detectar páginas en B/N).

## ✨ Ventajas Relevantes
- **Optimización Automática Inteligente**: No necesitas configurar resoluciones o perfiles; el script auto-analiza el cómic y decide el DPI y el ratio de compresión perfecto para cada caso.
- **Auto-detección de Blanco y Negro**: Al eliminar los canales RGB en páginas que en realidad no los necesitan (cómics en blanco y negro o manga), ahorras hasta un 60% más de espacio.
- **Fail-Safe (Protocolo de seguridad de tamaño)**: Es imposible que el script genere un CBZ más pesado que el PDF original. Si detecta un crecimiento de MB, reinicia todo y extrae las imágenes en su formato original.
- **Detección Automática de Idioma**: Sus menús y reportes de la terminal cambian su idioma automáticamente dependiendo del sistema operativo (Soporta Inglés y Español nativo).
- **Fácil uso por carpetas (Batch Processing)**: Puedes seleccionar múltiples carpetas, e incluso sus subcarpetas, y el programa procesará automáticamente cientos de PDFs sin que tengas que intervenir.
