# Guía de Instalación de Herramientas y Dependencias (Windows)

Esta guía detalla los programas externos y dependencias recomendadas para aprovechar al 100% todas las capacidades de la suite **PDFCBZtoEPUB** en Windows (OCR para escaneos, extracción de cómics CBR/RAR, visor gráfico, etc.).

---

## 1. Estado Actual de tu Equipo

| Componente | Tipo | Estado | Para qué sirve |
| :--- | :--- | :---: | :--- |
| **Python 3.14** | Intérprete | ✅ Instalado | Motor de ejecución de los scripts |
| **PyMuPDF (`fitz`)** | Librería Python | ✅ Instalado | Renderizado ultra-rápido de PDFs a imágenes y texto |
| **Pillow (`PIL`)** | Librería Python | ✅ Instalado | Procesamiento de imágenes (redimensión, autocrop, deskew) |
| **NumPy** | Librería Python | ✅ Instalado | Aceleración matemática de varianza, filtros y perfiles |
| **pytesseract** | Librería Python | ✅ Instalado | Puente entre Python y el motor Tesseract |
| **7-Zip / UnRAR** | Programa Windows | ✅ Instalado | Extracción automática de cómics en formato `.cbr` (RAR) |
| **Tesseract OCR (Motor binario)** | Programa Windows | ❌ **Pendiente** | Reconocimiento óptico de caracteres para PDFs escaneados |

---

## 2. Programas Recomendados en Windows

### A. Tesseract OCR (Recomendado para PDFs escaneados)
Permite que `PDFtoEPUB.py` convierta libros y documentos escaneados en **EPUB Reflowable** (texto real adaptable con búsqueda, cambio de tamaño de letra y modo oscuro).

#### Método 1: Vía Terminal (PowerShell / CMD) - El más rápido
Abre PowerShell y ejecuta:
```powershell
winget install UB-Mannheim.TesseractOCR
```

#### Método 2: Con Instalador Gráfico (.exe)
1. Descarga el instalador oficial de Windows mantenido por la Universidad de Mannheim:  
   👉 **[Descargar instalador de Tesseract para Windows (64-bit)](https://github.com/UB-Mannheim/tesseract/wiki)**  
   *(Selecciona la versión más reciente: `tesseract-ocr-w64-setup-5.x.x.exe`)*
2. Durante el asistente de instalación:
   - En la pantalla **"Choose Components"**, despliega **Additional language data** y asegúrate de marcar:
     - `Spanish` (para libros en español)
     - `English` (viene por defecto)
     - Cualquier otro idioma habitual de lectura (francés, catalán, gallego, alemán...).
3. Deja la ruta por defecto: `C:\Program Files\Tesseract-OCR`.
4. El programa `PDFtoEPUB.py` detectará automáticamente esta ruta sin necesidad de configurar variables de entorno.

---

### B. 7-Zip (Para descompresión de Cómics CBR)
Ya detectado en tu equipo (`C:\Program Files\7-Zip\7z.exe`).  
Si alguna vez reinstalas el sistema y necesitas instalarlo:
```powershell
winget install 7zip.7zip
```

---

### C. Calibre (Opcional - Lector y Visor de EPUBs en PC)
Permite inspeccionar y validar los archivos `.epub` generados directamente desde Windows.
```powershell
winget install Calibre.Calibre
```

---

## 3. Comandos Útiles de Verificación

Para comprobar que todo está listo, puedes ejecutar en tu terminal:

```powershell
# Comprobar versión de Python
python --version

# Comprobar motor Tesseract
& "C:\Program Files\Tesseract-OCR\tesseract.exe" --version

# Comprobar idiomas instalados en Tesseract
& "C:\Program Files\Tesseract-OCR\tesseract.exe" --list-langs
```
*(Deberían aparecer al menos `osd`, `eng` y `spa`).*
