# EPUB Master Suite — Estado del Proyecto

> **Versión actual:** 2.1.0
> **Última actualización:** 2026-04-06
> **Estado general:** 🟢 Activo — En desarrollo

---

## 📦 Instalación

```bash
pip install -r requirements.txt
python EPUBMaster.py
```

### Dependencias (`requirements.txt`)

| Paquete | Versión mín. | Uso en el proyecto |
|---|---|---|
| `ebooklib` | `>=0.18` | Lectura y escritura de archivos EPUB — extrae metadatos Dublin Core (`title`, `creator`) del interior del libro |
| `Pillow` | `>=10.0.0` | Procesamiento y optimización de imágenes dentro de los EPUBs (reescalado, recompresión JPEG/PNG) |

> **Nota:** El resto del proyecto usa únicamente la librería estándar de Python (`os`, `re`, `zipfile`, `shutil`, `difflib`, `pathlib`, `datetime`, `time`).

---

## ✅ Características Implementadas

### Módulo 1 — Renombrado Estructurado (`renamer.py`)
Estandariza nombres de archivos EPUB extrayendo metadatos Dublin Core del propio libro.

- **Formato de salida:** `Apellido, Nombre - Título.epub`
- Lee metadatos DC (`title`, `creator`) del interior del EPUB con `ebooklib`
- Fallback: si no hay metadatos, intenta extraer autor y título del propio nombre del archivo
- Preserva etiquetas adicionales del nombre original (`[v2]`, `[Calibre]`, `(Retail)`, etc.)
- Los archivos renombrados correctamente **se mantienen en la carpeta principal**.
- Se crea una copia de seguridad del original intocado en la carpeta `ORIGINAL/`.
- Archivos sin metadatos suficientes → carpeta `DOUBT/`
- Compatible con modo Dry-Run

---

### Módulo 2 — Optimización de Archivos (`optimizer.py`)
Reduce el tamaño de los EPUBs reprocesando su contenido interno.

- Reescala imágenes a máximo **1000 px** de ancho (proporcional)
- Comprime imágenes al **75% de calidad JPEG** (con fallback a PNG si hay transparencia)
- Elimina comentarios HTML (`<!-- -->`) y CSS (`/* */`) innecesarios
- Minifica espacios en blanco excesivos en HTML/CSS
- Escribe el `mimetype` sin compresión (requerimiento de la especificación EPUB)
- Solo reemplaza el archivo si hay **ahorro real**; si no, descarta el temporal
- Muestra resumen con contadores: optimizados / sin cambios / errores y **ahorro total en MB**
- Compatible con modo Dry-Run (estima ahorro por archivo sin modificar nada)

---

### Módulo 3 — Limpieza de Etiquetas de Idioma (`lang_cleaner.py`)
Detecta y gestiona archivos con etiquetas de idioma en el nombre.

- Detecta patrones `[XX]` y `(XX)` de 2-3 letras (ej: `[EN]`, `(FR)`, `[GAL]`)
- Muestra resumen: qué etiquetas hay y cuántos archivos afectan
- Los archivos se **mueven** a `_BORRADOS_IDIOMA/` — **nunca se borran permanentemente**
- El usuario puede revisar y eliminar manualmente esa carpeta cuando esté seguro
- Escaneo recursivo (incluye subcarpetas)
- Compatible con modo Dry-Run

---

### Módulo 4 — Gestión de Duplicados (`dupe_finder.py`)
Identifica posibles libros duplicados por similitud de título y autor.

- Agrupa libros por autor (normalizado) para reducir comparaciones innecesarias
- Compara títulos con `SequenceMatcher` (umbral: **85% de similitud**)
- Muestra grupos de candidatos para que el usuario decida qué conservar
- Los seleccionados se mueven a `POSIBLES_DUPLICADOS/`
- Solo escanea la carpeta raíz (aún sin soporte recursivo)

---

### Módulo 5 — Estadísticas de Biblioteca (`stats.py`) ⭐ *Nuevo en v2.0*
Genera un informe completo de la biblioteca **sin modificar ningún archivo**.

- Total de EPUBs y cuántos están en subcarpetas
- Tamaño total, promedio, libro más grande y más pequeño
- Distribución por tamaño: ligeros (<1 MB) / normales (1–10 MB) / pesados (>10 MB)
- Número de autores únicos detectados por nombre de archivo
- Archivos con nombre incorrecto (no siguen el formato estándar)
- Archivos con etiquetas de idioma detectadas
- Estimación de libros sin metadatos DC (sobre muestra configurable)
- **Recomendaciones automáticas** indicando qué módulo usar

---

### Función transversal — Modo Simulación / Dry-Run ⭐ *Nuevo en v2.0*
Activa/desactiva desde el menú con la opción `[6]`.

- Cuando está **activo**, todas las operaciones (renombrar, mover, optimizar) muestran
  exactamente qué harían **sin tocar ningún archivo**
- El estado se muestra visiblemente en el encabezado del menú
- Diseñado para revisar una biblioteca grande antes de ejecutar cambios masivos

---

### Sistema — Caché de Diagnóstico ⭐ *Nuevo en v2.0*
Mejora de rendimiento interna en el menú principal.

- El análisis rápido inicial (Dashboard) se cachea **30 segundos**
- En bibliotecas grandes, evita reabrir decenas de ZIPs en cada vuelta al menú
- El caché se invalida automáticamente tras ejecutar cualquier operación

---

## 🗂️ Estructura del Proyecto

```
epub_master/
├── EPUBMaster.py              ← Punto de entrada. Menú y orquestación
├── requirements.txt           ← Dependencias pip
├── epubmaster-estado.md       ← Este archivo
├── epubmaster.log             ← Log de sesiones (generado automáticamente)
└── epub_modules/
    ├── utils.py               ← Logger, helpers de UI, detección de idioma
    ├── renamer.py             ← Módulo 1: Renombrado
    ├── optimizer.py           ← Módulo 2: Optimización
    ├── lang_cleaner.py        ← Módulo 3: Limpieza de idiomas
    ├── dupe_finder.py         ← Módulo 4: Duplicados
    └── stats.py               ← Módulo 5: Estadísticas (nuevo)
```

### Carpetas generadas durante el uso

| Carpeta | Módulo | Contenido |
|---|---|---|
| `ORIGINAL/` | Renamer | Copias de seguridad de los archivos originales antes de renombrarse |
| `DOUBT/` | Renamer | Archivos sin metadatos suficientes |
| `_BORRADOS_IDIOMA/` | LangCleaner | Archivos movidos por etiqueta de idioma |
| `POSIBLES_DUPLICADOS/` | DupeFinder | Posibles copias duplicadas |

---

## 🔧 Bugs Corregidos en v2.0

| Bug | Módulo | Descripción |
|---|---|---|
| ✅ Borrado permanente | `lang_cleaner` | `unlink()` reemplazado por `move()` a carpeta segura |
| ✅ Duplicación de archivos | `renamer` | `copy2()` reemplazado por `move()` |
| ✅ Extras perdidos | `renamer` | `[v2]`, `[Calibre]` etc. ahora se preservan en el nombre final |
| ✅ `temp_dir` zombi | `optimizer` | Eliminado directorio temporal nunca usado (procesado en memoria) |
| ✅ Sin resumen detallado | `optimizer` | Ahora muestra ok/skip/error y % de ahorro por archivo |

---

## 🚧 Pendiente / Roadmap

### Prioridad Alta
- [ ] **Editor de Metadatos** — Permitir editar manualmente título/autor en el XML interno de los EPUBs en `DOUBT/`, cerrando el ciclo completo sin herramientas externas
- [ ] **Soporte Recursivo en Renamer/Optimizer** — Procesar subdirectorios (por autor, género...) no solo la raíz

### Prioridad Media
- [ ] **Backup Automático** — Crear snapshot `.zip` con los archivos afectados antes de cada operación destructiva, con opción de gestión desde el menú
- [ ] **Detección de duplicados por hash** — Complementar la comparación por similitud de nombre con hash MD5 del contenido para mayor precisión

### Prioridad Baja
- [ ] **Extractor de Portadas** — Extraer imágenes de portada a una carpeta `_PORTADAS/` para revisión visual
- [ ] **Compatibilidad con más formatos** — Soporte básico para `.mobi` / `.azw3` en el renombrado

---

## 📝 Historial de Versiones

### v2.1.0 — 2026-04-06
- ✅ Fix crítico: `Logger` provocaba crasheos silenciosos forzando el cierre en el menú de operaciones.
- ✅ Fix: `lang_cleaner` y `stats` ya no escanean ni cuentan los libros que fueron movidos a subcarpetas de seguridad (como `_BORRADOS_IDIOMA/` o `ORIGINAL/`).
- ✅ Fix: `optimizer` elimina archivos temporales `.opt` si se produce un error y muestra resumen detallado de fallos al final.
- ✅ Mejora: `renamer` ahora deja los archivos listos en la carpeta raíz y hace backup en `ORIGINAL/` (reemplazando el antiguo `DONE/`).
- ✅ Mejora: Interfaz (flujo visual entre el caché del menú principal y los módulos) corregida y envuelta en un control de excepciones para nunca salir de la aplicación bruscamente.

### v2.0.0 — 2026-03-31
- ✅ Nuevo módulo: Estadísticas de biblioteca (`stats.py`)
- ✅ Nuevo: Modo Simulación / Dry-Run (opción `[6]` en menú)
- ✅ Fix crítico: `lang_cleaner` ya no borra archivos permanentemente
- ✅ Fix crítico: `renamer` mueve en lugar de copiar (elimina duplicados en raíz)
- ✅ Fix: Etiquetas extras `[v2]`, `[Calibre]` se preservan correctamente
- ✅ Fix: Eliminado `temp_dir` muerto en `optimizer`
- ✅ Mejora: Caché de diagnóstico (30 seg) para evitar re-escaneo constante
- ✅ Mejora: `optimizer` muestra resumen con % de ahorro por archivo
- ✅ Añadido `requirements.txt`

### v1.0.0 — 2026-03-01
- 🎉 Primera versión unificada
- Módulos: Renamer, Optimizer, LangCleaner, DupeFinder
- Refactorización de los 4 scripts legacy monolíticos (`EPUBrename.py`, `EPUBOptimizer.py`, `EPUBLang.py`, `EPUBDupe.py`)
