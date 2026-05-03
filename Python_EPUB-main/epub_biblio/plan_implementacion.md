# Plan de Desarrollo: Visor de Biblioteca EPUB

## 🏛️ Arquitectura Ligera
Para lograr que sea **muy visual y ligera**, utilizaremos el siguiente stack tecnológico:

1. **Backend (El Motor): Python + FastAPI**
   - **Por qué:** FastAPI es rapidísimo, ligero y se lleva excelente con el procesamiento de archivos. Reutilizará tus conocimientos previos de Python.
   - **Base de Datos:** **SQLite**. Archivo local, sin configuraciones complejas, perfecta para búsquedas instantáneas pero sin sobrecargar tu sistema.
2. **Frontend (La Vista): React + Vite**
   - **Por qué:** Vite compila en milisegundos y React nos permite crear una interfaz fluida, recargando solo lo necesario sin refrescar toda la página.
   - **Estilos:** CSS puro priorizando diseño limpio, modo oscuro y animaciones fluidas, tal como lo solicitaste.

## 🗂️ Estructura de Carpetas Propuesta

```text
epub_biblio/
│
├── backend/                # Motor en Python
│   ├── main.py             # Servidor web FastAPI
│   ├── epub_parser.py      # Tu lógica para extraer portadas y metadatos
│   ├── database.py         # Conexión local a SQLite
│   └── requirements.txt    # Dependencias (fastapi, uvicorn)
│
└── frontend/               # Interfaz visual
    ├── src/
    │   ├── components/     # Tarjetas de libros, barras de búsqueda
    │   ├── index.css       # Estilos globales y modo oscuro
    │   └── App.jsx         # Pantalla principal
    └── package.json
```

## 🚀 Fases de Implementación (Paso a Paso)

### Fase 1: Extractor y Backend Básico (Foco principal)
1. Crear el entorno de Python e instalar dependencias (`fastapi`, `uvicorn`).
2. Programar `epub_parser.py` para leer un `.epub`, sacar el Título, Autor y guardar físicamente la Portada.
3. Crear el puerto de nuestro servidor API (`/api/books`) para que envíe la lista de libros al frontend.

### Fase 2: Interfaz Visual (Frontend)
1. Iniciar un proyecto ligero con Vite (`npm create vite@latest`).
2. Crear la **Cuadrícula de Portadas** (Vista Principal) con un diseño visualmente atractivo.
3. Conectar el Frontend al Backend.

### Fase 3: Lectura e Interacción
1. Añadir barra de búsqueda instantánea.
2. Añadir funcionalidad de "Clic para abrir detalles" para leer el EPUB.
