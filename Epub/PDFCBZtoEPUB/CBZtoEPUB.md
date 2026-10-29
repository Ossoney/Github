# CBZtoEPUB

## 📖 ¿Qué hace y para qué sirve?
`CBZtoEPUB.py` es un programa especializado y rápido diseñado para convertir archivos de cómic (CBZ) en libros electrónicos puros y maleables en formato EPUB Fixed-Layout.

## ⚙️ Funciones Principales

### CBZ → EPUB Fixed-Layout
Para archivos de cómic en formato ZIP (CBZ).
- Viewport calculado por **moda** de las 8 primeras páginas (evita que una doble-página distorsione el layout).
- Optimización paralela de imágenes con `ProcessPoolExecutor` (multi-núcleo real).
- Detección automática de páginas en blanco y negro para mayor compresión.
- Passthrough JPEG: si la imagen ya es pequeña y eficiente, se copia sin recodificar (cero pérdida generacional).
- Auto-cropping de márgenes blancos con `ImageChops.difference`.
- Lee metadatos de `ComicInfo.xml` si existe (título, autor, número de serie).

---

## 📦 Librerías Necesarias

```bash
pip install Pillow
pip install numpy          # opcional, acelera detección B/N
```

| Librería | Rol | Obligatoria |
|---|---|---|
| `Pillow (PIL)` | Manipulación y compresión de imágenes | ✅ Sí |
| `numpy` | Detección rápida de imágenes B/N | ⬜ Opcional |

---

## ✨ Pipeline de Optimización de Imágenes

- **Resolución Máxima**: 1600x2400 píxeles.
- **Auto-detección B/N**: Si `numpy` está disponible, usa diferencia media entre canales RGB. Sin numpy, muestrea una miniatura 50×50 px (eficiente en RAM).
- **Comparación inteligente**: Si la imagen optimizada resulta ser de mayor peso que el original, se conserva el original siempre que sea válido.
- **Compresión EPUB**: ZIP nivel 9 para XHTML/CSS (5–15% menos que el nivel por defecto).

---

## 📊 Metadatos en el EPUB Generado

El EPUB siempre incluye en su OPF:
- `dc:title` — del nombre del archivo o del `ComicInfo.xml` si existe.
- `dc:creator` — del `ComicInfo.xml` si se encuentra.

---

## 🗂️ Gestión de Archivos

Al finalizar la conversión:
- El EPUB se guarda junto al archivo original.
- El archivo CBZ original se mueve a una carpeta `ORIGINAL/` (manteniendo la estructura de subcarpetas si se procesaron).
- Se muestra un **resumen final** con MB originales, MB de EPUB y el % de espacio ahorrado.
