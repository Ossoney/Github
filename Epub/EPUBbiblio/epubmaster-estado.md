# Epub Master / Epub Biblio — Estado del Proyecto

> **Proyecto:** Epub Biblio (Web Suite de Gestión, Visualización y Lectura de EPUBs)  
> **Última actualización:** 04 de Octubre de 2026  
> **Estado general:** 🟢 Activo, Estable y en Producción Local / LAN  
> **Tecnologías:** Python 3.14 (FastAPI, SQLAlchemy, Uvicorn) + React 18 (Vite 8) + SQLite (WAL mode)

---

## 📊 Estado Actual del Catálogo y Colecciones

- **Total de libros registrados:** ~74.888 volúmenes.
- **Cobertura de portadas:** **99.6%** (74.601 libros con portada visible).
  - *Rescate masivo completado:* Se recuperaron y extrajeron 1.121 carátulas directamente desde el interior de los archivos `.epub` que carecían de imagen previa.
  - *Erótica y Adultos:* 100% de carátulas presentes (2.684 libros cubiertos).
- **Rutas de datos persistentes:**
  - Base de datos SQLite: `C:\Users\OscarSson\Documents\Epubbiblio\biblio.db`
  - Almacén de portadas extraídas: `C:\Users\OscarSson\Documents\Epubbiblio\covers\`
  - Configuración y ajustes: `C:\Users\OscarSson\Documents\Epubbiblio\settings.json`
  - Copias de seguridad de versiones: `C:\Users\OscarSson\Documents\Epubbiblio\backups\`

---

## 🏛️ Sistema de Bibliotecas y Orden de Afinidad Literaria

El desplegable principal de bibliotecas está organizado de forma natural por afinidad temática y cuenta con líneas separadoras (`──────────────`) entre bloques:

1. **Catálogo General**
   - 📚 *Todas las bibliotecas*
   - 🏛️ *Biblioteca Principal* (Catálogo completo, 80.888 libros)
2. **Narrativa, Historia y Acción**
   - 🏛️ *Novela y Narrativa Contemporánea* (13.017 libros)
   - 🏛️ *Novela Histórica* (6.951 libros)
   - 🏛️ *Aventuras y Acción* (6.202 libros)
3. **Misterio, Suspense y Terror**
   - 🏛️ *Policial y Novela Negra* (7.079 libros)
   - 🏛️ *Intriga, Suspense y Thriller* (9.454 libros)
   - 🏛️ *Terror* (3.579 libros)
4. **Ficción Especulativa**
   - 🏛️ *Ciencia Ficción* (6.358 libros)
   - ⭐ *Ciencia Ficción (VIP)* (947 libros selectos — carpeta propia `C:\Arquivo XeralOss\RECOPILACIONES\CI&FI`)
   - 🏛️ *Fantasía* (5.697 libros)
5. **Romance y Adultos**
   - 🏛️ *Novela Romántica* (13.624 libros)
   - 🔞 *Erótica y Adultos* (2.793 libros) — *cuenta con tema rosa distintivo*
6. **Formas Breves, Poesía, Teatro y Humor**
   - 🏛️ *Relatos y Cuentos Cortos* (5.353 libros)
   - 🏛️ *Poesía* (845 libros)
   - 🏛️ *Teatro* (549 libros)
   - 🏛️ *Humor y Sátira* (2.569 libros)
7. **Lectores Jóvenes**
   - 🏛️ *Infantil y Juvenil* (4.009 libros)
8. **No Ficción, Pensamiento y Divulgación**
   - 🏛️ *Biografías, Memorias y Crónicas* (3.936 libros)
   - 🏛️ *Ensayo, Filosofía y Pensamiento* (7.295 libros)
   - 🏛️ *Divulgación y Ciencia* (6.279 libros)

---

## ⭐ Sistema Híbrido de Valoraciones y Reseñas

El sistema integra un cálculo híbrido inteligente de puntuación:

1. **Prioridad 1 — Valoraciones Propias (Comunidad/Lectores):**
   - Los usuarios pueden valorar de 1 a 5 estrellas y dejar comentarios desde el modal del libro.
   - Si existen votos de lectores locales, esta puntuación tiene prioridad absoluta sobre cualquier fuente externa.
2. **Prioridad 2 — Open Library (Comunitaria Externa con Búsqueda Multi-Estrategia):**
   - Si el libro no tiene valoraciones internas, se consulta Open Library en cascada inteligente de 4 niveles para maximizar hallazgos:
     - 🎯 **Nivel 1 (ISBN Exacto):** Si el EPUB contiene metadatos de ISBN (10 o 13 dígitos), consulta directa por ISBN. 100% infalible y exacto sin importar cómo esté nombrado el archivo.
     - 🔍 **Nivel 2 (Título + Autor Limpio):** Normalizado, sin corchetes de sagas ni signos que rompan la sintaxis Lucene.
     - 📖 **Nivel 3 (Solo Título):** Si no hubo resultado con autor (por diferencias en nombres de autor).
     - 🧩 **Nivel 4 (Palabras Clave Esenciales + Apellido):** Si el título contiene subtítulos largos o ediciones conmemorativas, toma las 2 o 3 palabras nucleares más el apellido del autor (ej. *"BLACKWATER I. La riada"* localiza con éxito *"La Riada McDowell"*).
   - **Descarga automática de carátulas ausentes:** Si un libro carece de imagen de portada física en su EPUB, al consultar Open Library (tanto al abrir *Valorar*, pulsar *Consultar*, o en la sincronización global) se descarga y guarda físicamente la carátula oficial en el servidor, actualizándola en la tarjeta al instante.
   - **Consulta en vivo:** Al abrir la ficha de un libro no sincronizado, el backend consulta Open Library en ese instante en segundo plano y actualiza la tarjeta al vuelo.
   - **Botón manual:** En el modal de opiniones existe el botón `🔄 Consultar Open Library` para forzar la actualización de cualquier título.
   - **Sincronización masiva en segundo plano:** Desde *Admin ➔ Mantenimiento*, una tarea en background recorre el catálogo progresivamente sin saturar ni ralentizar la biblioteca.
3. **Ordenación:**
   - La opción de ordenación **"Mejor valorados ⭐"** posiciona primero los libros con mayor puntuación (desempatando por novedades más recientes).

---

## 🛡️ Panel de Administración y Mantenimiento

- **Monitor de Escaneo en Segundo Plano en Vivo:**
  - Barra de progreso porcentual fluida que informa de:
    - `Archivos analizados de X totales`.
    - `Nuevos libros incorporados a la biblioteca` en tiempo real.
    - Archivo EPUB procesándose en cada instante.
    - Botón `Detener Escaneo` para pausar o cancelar de forma limpia si es necesario.
  - **Indicador activo en la barra superior:** Si hay un escaneo en marcha, aparece un botón animado `⚡ X%` en la cabecera que permite abrir el monitor con un solo clic.
  - Al terminar el escaneo, la biblioteca, el catálogo y las estadísticas se actualizan automáticamente en pantalla sin recargar.
- **Escaneo Inteligente:**
  - El botón `⚡ Escanear` solo se muestra en aquellas bibliotecas que disponen de una carpeta física configurada en disco (Biblioteca Principal y ⭐ Ciencia Ficción VIP).
  - Las bibliotecas basadas en etiquetas de género muestran el distintivo informativo `🏷️ Colección temática`.
- **Protección de Bibliotecas del Sistema:**
  - Las bibliotecas esenciales (ID 1 y 2) están protegidas contra borrado accidental.
- **Gestión de Incidencias y Reportes:**
  - En el modal de *Valorar*, los lectores tienen un acceso directo para reportar incidencias: *"Si detectas que el libro no pertenece al género o cualquier otra incidencia, explícamelo e intentaré subsanarlo cuanto antes"*.
  - En el panel de **Admin**, la nueva pestaña **🚨 Incidencias** muestra los mensajes en tiempo real, permitiendo al Administrador Master revisar los avisos y marcarlos como resueltos con un botón (*✓ Resolver*).
- **Gestión de Usuarios y Roles:**
  - Rol **Master** (acceso completo a configuración, mantenimiento y todas las colecciones).
  - Rol **Lector** (acceso únicamente a las bibliotecas asignadas por el administrador, marcadores personales y opiniones).

---

## 🎨 Experiencia de Usuario y Visualización

- **Escalador de Portadas Responsivo:**
  - Selector con 5 niveles en escritorio: 110px, 135px, 160px, 190px y 220px.
- **Tarjetas Giratorias 3D:**
  - Anverso: Portada con efecto de profundidad y gradiente de reserva si no hay carátula.
  - Reverso: Título, autor, valoración ⭐ con conteo, etiquetas, sinopsis con scroll y botones de acción rápida (*Leer* y *Valorar*).
- **Lector Integrado:**
  - Motor `ReactReader` para lectura fluida directamente en el navegador sin apps externas.
- **Búsqueda Ultra-Rápida con SQLite FTS5 (Full-Text Search):**
  - Motor de búsqueda indexado mediante tabla virtual `books_fts` (`unicode61 remove_diacritics 2`) con disparadores (triggers) en tiempo real para inserciones, actualizaciones y borrados.
  - El tiempo de respuesta de búsqueda sobre más de 80.000 libros se ha reducido de ~2.000 ms a **< 50 ms**, eliminando bloqueos y encolamiento de consultas en tiempo real.
- **Ordenación Directa en Base de Datos (Backend SQL):**
  - La ordenación (`Mejor valorados ⭐`, `A-Z`, `Z-A`, `Más antiguos`, `Más recientes`) se ejecuta ahora a nivel de base de datos con índices dedicados (`ix_books_external_rating`, `ix_books_title`, `ix_books_author`).
  - Esto garantiza que al seleccionar "Mejor valorados", el sistema evalúa y devuelve los mejores de la totalidad del catálogo (80.000+ libros) y no solo de los primeros 1.000 en memoria.
- **Vigía en Tiempo Real Multi-Carpeta (Watchdog Multicarpeta):**
  - Módulo con escucha simultánea de todas las carpetas configuradas en las bibliotecas (ej. `Epublibre` y `CI&FI VIP`):
    - `on_created`: Auto-incorpora y clasifica nuevos EPUBs tan pronto se guardan en cualquiera de las carpetas vigiladas.
    - `on_deleted`: Elimina automáticamente el libro de la base de datos si su archivo EPUB se borra físicamente de cualquiera de las carpetas, manteniendo el catálogo 100% sincronizado con el disco.

---

## 🚀 Puesta en Marcha y Servicios

### Backend (FastAPI)
```powershell
cd backend
venv\Scripts\activate
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend (Vite Dev Server)
```powershell
cd frontend
npm run dev -- --host
```

### Build para Producción
```powershell
cd frontend
npm run build
```
*(FastAPI sirve automáticamente los archivos compilados en `frontend/dist` en la raíz `http://localhost:8000/`)*.
