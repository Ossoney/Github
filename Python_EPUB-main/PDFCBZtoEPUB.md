# PDFCBZtoEPUB

## 📖 ¿Qué hace y para qué sirve?
`PDFCBZtoEPUB.py` es la "joya de la corona", un programa titánico y sumamente sofisticado diseñado para convertir archivos PDF y archivos de cómic (CBZ) en libros electrónicos puros y maleables en formato EPUB.

A diferencia de conversores genéricos, este script actúa como un **"escáner inteligente"**: detecta si un PDF es de texto, de imagen o de imagen con texto recuperable por OCR, y aplica el pipeline óptimo en cada caso.

---

## ⚙️ Modos de Conversión

### 1. PDF de Texto → EPUB Reflowable
Para PDFs nativos con texto vectorial (novelas, papers, documentos).
- Extrae texto enriquecido con negrita, cursiva y jerarquía de encabezados.
- Detecta capítulos usando **TOC nativo** (si existe) o **heurísticas** (tamaño de fuente, patrones de texto, Golden List para revistas).
- Extracción de texto **paralela** con `ThreadPoolExecutor` (cada hilo abre su propio `fitz.Document` para ser thread-safe). Acelera PDFs de 200+ páginas.
- Incluye imágenes embebidas del PDF en el EPUB.
- Genera índice de navegación (TOC) interactivo.

### 2. PDF de Imagen → EPUB Fixed-Layout (FXL)
Para PDFs de cómics, revistas escaneadas o documentos con layout complejo.
- Procesamiento **paralelo de páginas** con `ProcessPoolExecutor` (multi-núcleo real, anti-GIL).
- Detección automática de color vs. blanco/negro por página (perfiles `OPT_SCAN_COLOR` / `OPT_SCAN_BW`).
- Passthrough JPEG: si la imagen ya es pequeña y eficiente, se copia sin recodificar (cero pérdida generacional).
- Auto-cropping de márgenes blancos con `ImageChops.difference`.

### 3. PDF de Imagen → EPUB Reflowable por OCR *(nuevo, automático)*
Se activa automáticamente cuando se detecta un PDF de imagen **y Tesseract está instalado**.
- **Test de viabilidad** (rápido, ~2 seg): OCR de la primera página a 150 DPI. Si extrae ≥ 150 caracteres → OCR viable.
- **OCR completo** a 300 DPI con `ProcessPoolExecutor` (hasta 6 núcleos en paralelo).
- Detección de capítulos en el texto extraído: patrones explícitos ("Capítulo X", "Chapter X"...) + heurística ALL-CAPS.
- Produce un EPUB reflowable con TOC, buscable y navegable.
- Si Tesseract no está instalado o la calidad es insuficiente → fallback transparente al modo FXL.

### 4. CBZ → EPUB Fixed-Layout
Para archivos de cómic en formato ZIP.
- Viewport calculado por **moda** de las 8 primeras páginas (evita que una doble-página distorsione el layout).
- Optimización paralela de imágenes con `ProcessPoolExecutor`.
- Lee metadatos de `ComicInfo.xml` si existe (título, autor, número).
- Passthrough JPEG para imágenes ya optimizadas.

---

## 📦 Librerías Necesarias

```bash
pip install PyMuPDF Pillow
pip install numpy          # opcional, acelera detección B/N
pip install pytesseract    # opcional, activa el modo OCR automático
```

| Librería | Rol | Obligatoria |
|---|---|---|
| `PyMuPDF (fitz)` | Deconstruir PDFs, extraer texto e imágenes | ✅ Sí |
| `Pillow (PIL)` | Manipulación y compresión de imágenes | ✅ Sí |
| `numpy` | Detección rápida de imágenes B/N | ⬜ Opcional |
| `pytesseract` | Wrapper Python para Tesseract OCR | ⬜ Opcional |

### Para activar OCR (modo 3)
Además de `pip install pytesseract`, se necesita el **binario nativo de Tesseract**:

- **Windows**: descargar instalador desde [github.com/UB-Mannheim/tesseract](https://github.com/UB-Mannheim/tesseract/wiki). Seleccionar el paquete de idioma **"spa"** (español) durante la instalación.
- **Linux**: `sudo apt install tesseract-ocr tesseract-ocr-spa`
- **macOS**: `brew install tesseract`

> Si Tesseract no está disponible, el programa funciona con normalidad usando el modo FXL como siempre.

---

## ✨ Pipeline de Optimización de Imágenes

| Perfil | Uso | Max Ancho | Calidad |
|---|---|---|---|
| `OPT_COMIC` | CBZ color | 1600 px | 82 |
| `OPT_SCAN_COLOR` | PDF imagen color | 1200 px | 72 |
| `OPT_SCAN_BW` | PDF imagen B/N | 950 px | 45 |
| `OPT_TEXT` | Imágenes en PDFs de texto | 1000 px | 75 |

- **Auto-detección B/N**: Si `numpy` está disponible, usa diferencia media entre canales RGB. Sin numpy, muestrea una miniatura 50×50 px (eficiente en RAM).
- **Comparación inteligente**: Si la imagen optimizada es mayor que el original, se usa el original.
- **Compresión EPUB**: ZIP nivel 9 para XHTML/CSS (5–15% menos que el nivel por defecto).

---

## 🔍 Decisión Automática de Modo OCR

```
PDF de imagen detectado
    │
    ├─ pytesseract no instalado → modo FXL (imagen) + aviso
    │
    └─ pytesseract instalado
            │
            ├─ OCR página 1 @ 150 DPI (test ~2s)
            │
            ├─ < 150 chars → calidad insuficiente → modo FXL
            │
            └─ ≥ 150 chars → OCR viable
                    │
                    └─ OCR paralelo 300 DPI (hasta 6 núcleos)
                            → EPUB reflowable con TOC
```

**Cuándo activa OCR (resultados excelentes):**
- Novelas o libros escaneados a ≥ 300 DPI
- Papers académicos de una sola columna
- PDFs nativo-imagen con texto limpio

**Cuándo cae al modo FXL (OCR sería malo):**
- Cómics / manga (test de calidad falla → < 150 chars)
- Escaneos de baja calidad o muy inclinados
- Revistas con layout de 2 columnas (OCR mezclaría columnas)

---

## 📊 Metadatos en el EPUB Generado

El EPUB siempre incluye en su OPF:
- `dc:title` — del PDF o nombre del archivo
- `dc:creator` — del PDF o de `ComicInfo.xml` (CBZ)
- `dc:language` — del PDF (mapeado desde metadatos) o `es` por defecto

---

## 🗂️ Gestión de Archivos

Al finalizar la conversión:
- El EPUB se guarda junto al archivo original.
- El original se mueve a `ORIGINAL/` (manteniendo la estructura de subcarpetas si se procesan subcarpetas).
- Se muestra un **resumen final** con MB originales, MB de EPUB y % de ahorro por tipo (PDF Texto / PDF Imagen / CBZ).

---

## 🛠️ Historial de Mejoras (v2026-05)

### Bugs corregidos
- Fuga de `fitz.Document` en `convert_pdf_image_to_epub` cuando ocurría una excepción.
- Bug de precedencia de operadores en la unión de párrafos entre páginas (podía fusionar párrafos incorrectamente).
- `bare except:` reemplazados por `except Exception:` en todos los workers (Ctrl+C ahora siempre funciona).

### Rendimiento
- `_is_grayscale_image` fallback sin numpy: de `list(img.getdata())` (RAM completa) a `img.resize(50,50)` (muestreo eficiente).
- Extracción de texto paralela con `ThreadPoolExecutor` en `detect_chapters_from_pdf`.
- Viewport de CBZ calculado por moda de las 8 primeras páginas.
- `pack_epub`: compresión ZIP nivel 9.

### Nuevas funciones
- **OCR automático** (`convert_pdf_ocr_to_epub`, `_ocr_page_worker`, `_split_ocr_text_into_chapters`, `_test_ocr_quality`, `_pdf_lang_to_tesseract`).
- `generate_opf_fxl` y `generate_opf_reflowable` ahora aceptan `author` y `language`.
- `generate_cover_xhtml` acepta el nombre del archivo de portada.

### Localización
- Todas las cadenas de texto están en el diccionario bilingüe `TEXTS` (es/en). Eliminados los últimos mensajes hardcodeados en español.
