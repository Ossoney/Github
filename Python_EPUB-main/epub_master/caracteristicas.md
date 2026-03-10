# EPUB Master Suite

**EPUB Master Suite** es una aplicación de línea de comandos (CLI) desarrollada en Python, diseñada como una herramienta "todo en uno" (freeware) para la gestión, limpieza y organización de bibliotecas de libros electrónicos, específicamente en formato EPUB.

## Características Principales

La aplicación se estructura en base a 4 módulos principales que procesan automáticamente los archivos de una carpeta seleccionada por el usuario:

### 1. Renombrado Estructurado (`renamer.py`)
Analiza y estandariza los nombres de los archivos EPUB para mantener una biblioteca uniforme y fácil de explorar. 
- **Formato de salida:** `Apellido, Nombre - Título.epub`

### 2. Optimización de Archivos (`optimizer.py`)
Analiza la estructura de los archivos EPUB y los procesa con el objetivo de reducir su tamaño de almacenamiento sin comprometer el contenido.

### 3. Limpieza de Etiquetas de Idioma (`lang_cleaner.py`)
Detecta y elimina las etiquetas de idioma o códigos de país incrustados en los nombres de los archivos (común en libros descargados de internet).
- **Ejemplo de limpieza:** Elimina textos como `[EN]`, `[FR]`, `(ES)`, entre otros.

### 4. Gestión de Duplicados (`dupe_finder.py`)
Escanea la biblioteca para identificar y agrupar libros electrónicos duplicados, permitiendo al usuario decidir mantener la mejor versión y eliminar copias redundantes para ahorrar espacio.

## Interfaz y Flujo de Uso

- **Diagnóstico Automático:** Al definir una ruta de carpeta, el programa realiza un escaneo rápido preliminar de los archivos contenidos para estimar visualmente cuántos de ellos necesitan renombrado, optimización, limpieza o si existen duplicados.
- **Menú Interactivo CLI:** A través de un menú numérico en la terminal, el usuario puede ejecutar cualquiera de las cuatro tareas disponibles individualmente, o retroceder para cambiar la carpeta de trabajo, garantizando un flujo de trabajo sencillo y controlado.
