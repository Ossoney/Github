# PDFtoEPUB

## 📖 ¿Qué hace y para qué sirve?
`PDFtoEPUB.py` es un conversor inteligente que analiza la naturaleza de tus archivos PDF (texto puro, imágenes escaneadas o cómics) y determina la mejor forma de transformarlos en libros electrónicos (EPUB).

A diferencia de los conversores básicos, este programa no trata todos los PDFs igual. Utiliza heurísticas y, si es posible, Reconocimiento Óptico de Caracteres (OCR) para obtener el resultado más limpio y navegable.

---

## ⚙️ Modos de Conversión Automáticos

### 1. Modo PDF de Texto → EPUB Reflowable
Si el PDF contiene texto seleccionable (novelas, documentos, papers), el script:
- Extrae el texto conservando **negritas y cursivas**.
- Detecta capítulos usando el índice interno (TOC) o una heurística basada en expresiones regulares (`Capítulo X`, `Parte Y`, etc.).
- Produce un EPUB "Reflowable" adaptativo, donde puedes cambiar el tamaño de letra en tu e-reader.

### 2. Modo PDF de Imagen (Escáner) → EPUB Fixed-Layout
Si el programa detecta que el PDF está compuesto puramente por imágenes a toda página (ej: un cómic en formato PDF o una revista escaneada a baja calidad):
- Extrae cada página en alta resolución.
- Aplica compresión inteligente (si la página es B/N, la pasa a escala de grises para ahorrar espacio).
- Empaqueta todo en un EPUB de formato fijo (Fixed-Layout).

### 3. Modo OCR Automático (¡La Magia!)
Si detecta un PDF de imagen, pero reconoce que tiene suficiente calidad de texto y **tienes Tesseract instalado**:
- Extrae el texto de las imágenes en paralelo utilizando todos los núcleos de tu CPU.
- Estructura los capítulos.
- Transforma ese PDF de fotos inerte en un EPUB Reflowable vivo y maleable.
- (Hace un pequeño "test de viabilidad" primero; si la calidad es mala, vuelve al modo 2 automáticamente).

---

## 📦 Librerías Necesarias

Para que el programa funcione, necesitas instalar las siguientes dependencias en Python:

```bash
pip install PyMuPDF Pillow
```

### Opcionales (Altamente Recomendadas)
```bash
pip install numpy          # Para que la detección de B/N sea fulminante
pip install pytesseract    # Para activar el modo OCR
```

> **IMPORTANTE PARA EL OCR:** `pytesseract` es solo un puente. Necesitas tener instalado el motor **Tesseract OCR** en tu sistema operativo (con el paquete de idioma español/inglés). 
> - En Windows: Descarga el [instalador de UB-Mannheim](https://github.com/UB-Mannheim/tesseract/wiki).
> - En Linux: `sudo apt install tesseract-ocr tesseract-ocr-spa`.

---

## 🚀 Optimizaciones Bajo el Capó

1. **Multiprocesamiento**: Tanto en la extracción de texto, optimización de imágenes y pasadas de OCR, el script emplea `ProcessPoolExecutor` y `ThreadPoolExecutor` para saturar tu CPU y hacer el trabajo rápido.
2. **Protección del Original**: Cuando termina, el PDF original no se borra, sino que se reubica automáticamente en una subcarpeta segura llamada `ORIGINAL/`.
3. **Lazy Memory**: Utiliza directorios temporales de disco (`tempfile`) para generar la estructura del EPUB, evitando colapsar la RAM de tu ordenador cuando conviertes archivos masivos.
