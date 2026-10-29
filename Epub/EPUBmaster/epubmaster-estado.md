# EPUB Master Suite — Estado del Proyecto

> **Versión actual:** 2.2.0
> **Última actualización:** 2026-10-10
> **Estado general:** 🟢 Activo — Optimizado para bibliotecas masivas (75.000+ libros)

---

## 📦 Instalación

```bash
pip install -r requirements.txt
python EPUBMaster.py
```

### Dependencias (`requirements.txt`)

| Paquete | Versión mín. | Uso en el proyecto |
|---|---|---|
| `ebooklib` | `>=0.18` | Lectura de metadatos EPUB (usado como fallback de compatibilidad) |
| `Pillow` | `>=10.0.0` | Procesamiento y optimización multinúcleo de imágenes en EPUBs |

> **Nota:** El resto del proyecto usa únicamente la librería estándar de Python (`os`, `re`, `zipfile`, `shutil`, `difflib`, `pathlib`, `datetime`, `time`, `concurrent.futures`, `unicodedata`, `xml.etree`).

---

## ✅ Características Implementadas

### Módulo 1 — Renombrado Estructurado (`renamer.py`)
Estandariza nombres de archivos EPUB extrayendo metadatos Dublin Core del propio libro.

- **Formato de salida:** `Apellido, Nombre - Título.epub` o `VV.AA. - Título.epub`
- **Extracción ultrarrápida de metadatos:** Lectura directa del XML `content.opf` vía `zipfile` (15x a 40x más veloz que `ebooklib`, con fallback automático).
- **Procesamiento concurrente (`ThreadPoolExecutor`):** Indexación y análisis paralelo de archivos para bibliotecas masivas.
- **Normalización de autores varios integrada:** Detecta colectivos (`Varios Autores`, `VVAA`, `Autores varios`, `Various Authors`, etc.) tanto en metadatos como en el nombre del archivo, formatea limpiamente a `VV.AA. - Título.epub` y actualiza automáticamente sus metadatos internos (`content.opf`) a `VV.AA.`.
- **Corrección de apellidos compuestos:** Reemplazo inteligente de guiones y separadores para evitar uniones accidentales (`Pérez-Reverte` $\rightarrow$ `Pérez Reverte`).
- **Deduplicación de etiquetas y comentarios:** Evita duplicar notas entre paréntesis o corchetes presentes tanto en metadatos como en el nombre (`(Edición ilustrada)`).
- Preserva etiquetas adicionales del nombre original (`[v2]`, `[Calibre]`, `(Retail)`, etc.)
- Los archivos renombrados correctamente **se mantienen en la carpeta principal** con copia original en `ORIGINAL/`.
- Archivos sin metadatos suficientes $\rightarrow$ carpeta `DOUBT/`
- Compatible con modo Dry-Run.

---

### Módulo 2 — Optimización de Archivos (`optimizer.py`)
Reduce el tamaño de los EPUBs reprocesando su contenido interno.

- **Multiprocesamiento paralelo (`ProcessPoolExecutor`):** Aprovecha todos los núcleos de la CPU para comprimir múltiples libros en paralelo.
- Reescala imágenes a máximo **1000 px** de ancho (proporcional).
- Comprime imágenes al **75% de calidad JPEG** (con fallback a PNG si hay transparencia).
- Elimina comentarios HTML (`<!-- -->`) y CSS (`/* */`) innecesarios.
- **Eliminación inteligente de páginas vacías/lisas:** Detecta y purga páginas HTML sin texto ni imágenes o con solo un fondo sólido (blanco/negro), desvinculándolas limpiamente del `manifest`, `spine` y del índice de navegación NCX sin alterar la portada.
- Minifica espacios en blanco excesivos en HTML/CSS.
- Escribe el `mimetype` sin compresión (requerimiento de la especificación EPUB).
- Reemplazo atómico: solo sustituye el archivo si hay **ahorro real**.
- Muestra progreso en tiempo real y resumen con contadores y **ahorro total en MB**.
- Compatible con modo Dry-Run.

---

### Módulo 3 — Limpieza de Etiquetas de Idioma (`lang_cleaner.py`)
Detecta y gestiona archivos con etiquetas de idioma en el nombre.

- **Filtro inteligente anti-falsos positivos:** Whitelist de códigos ISO de idiomas válidos (`EN`, `ENG`, `FR`, `GL`, `GLG`, `IT`, etc.) descartando números romanos (`(II)`, `(III)`) y palabras comunes (`(NO)`, `(SIN)`, `(ESO)`).
- **Entrada múltiple por comas:** Permite introducir varias etiquetas a mover en una sola instrucción (ej: `EN, FR, [CAT]`).
- **Totalizador dinámico:** Muestra el recuento actualizado de las etiquetas restantes tras cada acción.
- Los archivos se **mueven** a `_BORRADOS_IDIOMA/` — **nunca se borran permanentemente**.
- Escaneo recursivo (incluye subcarpetas).
- Compatible con modo Dry-Run.

---

### Módulo 4 — Gestión de Duplicados (`dupe_finder.py`)
Identifica y gestiona duplicados a escala masiva (75.000+ libros).

- **Embudo de indexación O(1):** Agrupación instantánea por claves canónicas normalizadas (sin tildes, signos ni etiquetas) que resuelve la inmensa mayoría de duplicados en 2-3 segundos.
- **Pre-filtro de longitud matemático:** Descarta en $O(1)$ libros que difieren en más de un 15% de longitud antes de aplicar `SequenceMatcher`.
- **Auto-resolución exclusiva por versión:** Si dos o más libros tienen exactamente el mismo nombre y la **única** diferencia es la versión (ej: `(r1.0)` vs `(r2.0)` o con/sin versión), conserva automáticamente la versión más avanzada y mueve las antiguas a `POSIBLES_DUPLICADOS/`.
- **Control manual estricto para el resto:** Cualquier diferencia de título, edición o extras pasa a revisión manual asistida con visualización de tamaño en KB y contador de progreso (`Grupo X de Y`).
- **Comando de pausa rápida `[S]`:** Permite pausar la revisión en cualquier momento y volver al menú sin perder el trabajo realizado.

---

### Módulo 5 — Estadísticas de Biblioteca (`stats.py`)
Genera un informe completo de la biblioteca **sin modificar ningún archivo**.

- Optimizado con lector rápido de metadatos para inspeccionar la muestra sin saturar disco.
- Total de EPUBs y recuento en subcarpetas.
- Tamaño total, promedio, libro más grande y más pequeño.
- Distribución por tamaño: ligeros (<1 MB) / normales (1–10 MB) / pesados (>10 MB).
- Autores únicos detectados por nombre de archivo.
- Archivos con nombre incorrecto y con etiquetas de idioma detectadas.
- Estimación de libros sin metadatos Dublin Core.
- Recomendaciones automáticas sobre qué módulo ejecutar.

---

### Función transversal — Modo Simulación / Dry-Run
Activa/desactiva desde el menú con la opción `[6]`.

- Muestra con exactitud qué archivos se moverían o renombrarían **sin tocar ningún archivo en disco**.

---

## 🗂️ Estructura del Proyecto

```
EPUBmaster/
├── EPUBMaster.py              ← Punto de entrada. Menú y orquestación
├── requirements.txt           ← Dependencias pip
├── epubmaster-estado.md       ← Documento de estado y arquitectura
├── epubmaster.log             ← Log de sesiones (generado automáticamente)
└── epub_modules/
    ├── utils.py               ← Logger, helpers UI, extractor de metadatos rápido
    ├── renamer.py             ← Módulo 1: Renombrado concurrente y normalización VV.AA.
    ├── optimizer.py           ← Módulo 2: Optimización paralela multinúcleo
    ├── lang_cleaner.py        ← Módulo 3: Limpieza de idiomas con whitelist
    ├── dupe_finder.py         ← Módulo 4: Duplicados con embudo O(1) y auto-versión
    └── stats.py               ← Módulo 5: Estadísticas de biblioteca
```

### Carpetas generadas durante el uso

| Carpeta | Módulo | Contenido |
|---|---|---|
| `ORIGINAL/` | Renamer | Copias de seguridad de los archivos originales antes de renombrarse |
| `DOUBT/` | Renamer | Archivos sin metadatos suficientes |
| `_BORRADOS_IDIOMA/` | LangCleaner | Archivos movidos por etiqueta de idioma |
| `POSIBLES_DUPLICADOS/` | DupeFinder | Libros duplicados movidos (manuales o versiones anteriores) |

---

## 🔧 Historial de Versiones

### v2.2.0 — 2026-10-10 (Versión Actual)
- 🚀 **Escalabilidad masiva para 75.000 libros:**
  - Rediseño del motor de duplicados (`dupe_finder.py`) con embudo de claves canónicas $O(1)$ y prefiltro de longitud.
  - Implementación de lector ligero de metadatos XML/OPF (`get_epub_metadata_fast`) eliminando el cuello de botella de `ebooklib`.
  - Paralelización multinúcleo en `optimizer.py` con `ProcessPoolExecutor`.
  - Extracción concurrente de metadatos en `renamer.py` con `ThreadPoolExecutor`.
- ⭐ **Auto-resolución estricta por versión:** Detección de duplicados idénticos que solo varían en revisión/versión (`(r1.0)` vs `(r2.0)`), conservando la más reciente y reservando la decisión manual para el resto.
- ⭐ **Normalización de obras colectivas a `VV.AA.`:** Detección de múltiples variantes (`Varios Autores`, `VVAA`, `Colectivo`...) y nombrado unificado a `VV.AA. - Título.epub`.
- 🛠️ **Deduplicación precisa de comentarios y paréntesis:** Corrección de duplicados accidentales como `(Edición ilustrada) (Edicion ilustrada)`.
- 🛠️ **Corrección de apellidos juntados:** Eliminado el bug que fusionaba apellidos con guiones (`Pérez-Reverte` $\rightarrow$ `Pérez Reverte`).
- 🛠️ **Mejoras de usabilidad en limpieza de idiomas:** Soporte para entrada múltiple por comas (`EN, FR`) y whitelist de códigos ISO para eliminar falsos positivos como números romanos y palabras comunes.
- 🛠️ **Mejoras en asistente de duplicados:** Visualización de tamaño en KB por opción, indicador de progreso `Grupo X de Y` y comando rápido `[S]` para pausar la sesión.

### v2.1.0 — 2026-04-06
- ✅ Fix: Corrección de crasheos silenciosos en `Logger`.
- ✅ Fix: Exclusión de carpetas internas de trabajo en escaneos recursivos.
- ✅ Fix: Limpieza de temporales `.opt` tras errores en optimización.
- ✅ Mejora: Renombrado en raíz con respaldo en `ORIGINAL/`.

### v2.0.0 — 2026-03-31
- ✅ Nuevo módulo: Estadísticas de biblioteca (`stats.py`).
- ✅ Nuevo: Modo Simulación / Dry-Run (opción `[6]`).
- ✅ Fix crítico: Reemplazo de borrado definitivo por carpetas de seguridad.
