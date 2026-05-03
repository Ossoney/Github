# Estado del Proyecto - Epub Biblio

## Estado de Desarrollo (Abril 2026) - Hitos Recientes

- [x] **Motor de PDF (Texto):** Implementado sistema de "Lista de Oro" para extracción de índices (TOC) inteligente. Soporta formatos modernos (`CHxxx`) y clásicos categorizados (`NOVELLA`).
- [x] **Unión de Párrafos:** Corregida la fragmentación inter-página. Los párrafos ahora fluyen continuamente a través de los saltos de página físicos.
- [x] **Limpieza de Ruido:** Eliminación automática de encabezados, pies de página y metadatos repetitivos de revistas (Headers/Footers).
- [x] **Estabilidad:** Normalización Unicode (NFKC) y soporte completo para UTF-8 en consola Windows, eliminando crashes por codificación.
- [x] **Detección de Historias:** Incrementada la precisión de detección de historias individuales en revistas de 1 a 15+ capítulos por ejemplar.

## Próximos Pasos (Hoja de Ruta)

### 1. Gestión de Perfiles y Usuarios (Nueva Prioridad)
- **Multi-perfil:** Crear una estructura de perfiles (estilo Netflix) para separar el progreso de lectura entre diferentes personas.
- **Autenticación:** Implementar sistema de login con **Usuario y Contraseña** para acceso seguro vía Tailscale.
- **Roles y Permisos:** Distinguir entre Administrador (gestión completa) y Lector (solo lectura y su propio progreso).
- **JWT (Tokens):** Implementar seguridad moderna para manejar sesiones sin fatiga de usuario.

### 2. Funcionalidades de Biblioteca
- **Marcar como Leído/Favorito:** Añadir estados a los libros de forma individual por perfil.
- **Edición de Metadatos:** Permitir correcciones de título/autor y cambio de portadas desde la interfaz web.
- **Bibliotecas Múltiples:** Soporte para gestionar carpetas separadas (ej: Cine ficción, General).
- **Agrupamiento Inteligente:** Detección automática de sagas y colecciones.

### 3. Mejoras Visuales
- **Modo Tablet/Horizontal:** Optimizar la rejilla de portadas para dispositivos de gran pantalla.
- **Animaciones de Transición:** Suavizar la entrada a la ficha del libro y al lector.

---
*Situación guardada en: 2026-04-14*
