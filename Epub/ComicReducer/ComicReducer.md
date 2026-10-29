# ComicReducer

## 📖 ¿Qué hace y para qué sirve?
`ComicReducer.py` es una utilidad especializada y rápida creada para la optimización de cómics y libros ilustrados digitales. Su objetivo es tomar archivos de cómics pesados (**CBR, CBZ y documentos PDF**) y reducir drásticamente su tamaño de almacenamiento sin percibir pérdida visual de calidad.

Es la solución ideal para liberar espacio en discos duros, tablets o e-readers. El programa transforma las imágenes interiores al eficiente formato **WebP** y adapta las dimensiones de las páginas para pantallas modernas de forma paralela.

---

## 🚀 Nuevas Funcionalidades Integradas

1. **Perfiles Predefinidos de Optimización**:
   - `[1]` **Habitual / Equilibrado**: 1600px de altura, Calidad 80 (por defecto, balance óptimo).
   - `[2]` **Tablet / iPad HD**: 2048px de altura, Calidad 85 (máxima nitidez).
   - `[3]` **Móvil / E-Reader**: 1280px de altura, Calidad 75 (pantallas compactas).
   - `[4]` **Ultra Ahorro / Ligero**: 1080px de altura, Calidad 65 (mínimo peso).
   - `[5]` **Sin Reescalar**: Mantiene la resolución original, aplicando únicamente conversión a WebP (Calidad 80).

2. **Opción ON/OFF para Eliminar el Archivo Original**:
   - Disponible en el menú interactivo, en la GUI y mediante el flag CLI `--delete-original`.
   - Garantiza que el archivo nuevo se haya generado correctamente antes de eliminar el original.

3. **Soporte Completo para Archivos PDF**:
   - Permite procesar archivos `.pdf` directamente (extrae sus páginas en alta resolución mediante `pymupdf` y las empaqueta en `.cbz` optimizado).

4. **Preservación Total de Metadatos**:
   - Mantiene intactos archivos `ComicInfo.xml` y cualquier otro metadato presente en el archivo comprimido.

5. **Tratamiento Inteligente de Páginas Dobles (Double-Page Spreads)**:
   - Detecta si una imagen es apaisada/doble página (`width > height`) y ajusta dinámicamente el límite de ancho para evitar que se reduzca excesivamente respecto a las páginas simples.

6. **Auto-recorte (Auto-crop) de Bordes**:
   - Opción conmutable para recortar márgenes homogéneos blancos o negros escaneados en los bordes de las páginas.

7. **Eliminación Conmutable de Páginas Vacías (Blancas / Negras)**:
   - Opción `ON/OFF` (desactivada por defecto) que detecta y elimina páginas interiores vacías, blancas o negras producidas en el escaneado.
   - **Protección de seguridad**: Nunca elimina la primera página (portada) ni la última página (contraportada).

8. **Interfaz Gráfica (GUI) y Acceso Directo Drag & Drop**:
   - **GUI**: Ejecutable con `python ComicReducer.py --gui` o haciendo doble clic en `ComicReducer_DragDrop.bat`. Dispone de selector de archivos/carpetas, selector de perfil, conmutadores y barra de progreso gráfica.
   - **Arrastrar y Soltar**: Arrastra uno o varios archivos `.cbz`, `.cbr`, `.pdf` o carpetas enteras sobre `ComicReducer_DragDrop.bat` para procesarlos de inmediato.

---

## ⚙️ Uso por Línea de Comandos (CLI)

```bash
# Modo interactivo clásico
python ComicReducer.py

# Interfaz gráfica (GUI)
python ComicReducer.py --gui

# Procesar un archivo individual con perfil específico
python ComicReducer.py "mi_comic.cbr" --profile 2

# Procesar con auto-recorte y eliminación del original
python ComicReducer.py "manga.pdf" --autocrop --delete-original

# Procesar una carpeta y todas sus subcarpetas
python ComicReducer.py "D:\Comics" --subfolders --profile 1
```

---

## 📦 Librerías Necesarias

```bash
pip install Pillow numpy tqdm pymupdf
```

- **`Pillow` (PIL)**: Conversión y reescalado Lanczos a WebP.
- **`numpy`**: Detección vectorial ultrarrápida de imágenes en blanco y negro.
- **`tqdm`**: Barras de progreso en la consola.
- **`pymupdf` (fitz)**: Extracción y renderizado de páginas de documentos PDF.
- **`7-Zip` (externo)**: Necesario para descomprimir cómics `.cbr` (formato RAR).
