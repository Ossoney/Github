# Estado del Proyecto: Finanzas Visuales

## Descripción General y Política de Documentación

> **⚠️ IMPORTANTE:** El estado y la evolución de este proyecto se mantienen estrictamente a través de tres documentos centrales. *Cualquier cambio, nueva funcionalidad o proceso de despliegue debe actualizar obligatoriamente estos tres archivos:*
>
> 1. `caracteristicas.md` (Para funcionalidades y alcance)
> 2. `guia_acceso.md` (Para procesos de instalación y acceso)
> 3. `estado_proyecto.md` (Este documento, para el estado actual, UX y Changelog)

El proyecto **Finanzas Visuales** (v1.4.26) es una aplicación web de contabilidad personal diseñada bajo una arquitectura **"Local-First"**. Esto significa que los datos se almacenan directamente en el dispositivo del usuario utilizando IndexedDB, descartando el uso de bases de datos externas para garantizar la máxima privacidad y velocidad.

## Tecnologías Principales

- **Framework Ocupado:** Next.js 14 (App Router) con React 18
- **Estilos:** Tailwind CSS
- **Gestión de Estado:** Zustand (para el store local)
- **Base de Datos Local (IndexedDB):** Dexie.js (y `dexie-react-hooks`)
- **Iconografía:** Lucide React
- **Animaciones:** Framer Motion
- **Manejo de Fechas:** `date-fns`
- **Importación/Exportación:** `xlsx` (para manejo de Excel)
- **PWA:** Sí, utiliza `@ducanh2912/next-pwa` para instalarse como una aplicación progresiva.

## Estado Actual y Funcionalidades

- **Dashboard Principal:** Resumen global, visualización histórica (6m, 12m, 24m y infinito) y filtrado de contexto.
- **Transacciones Integrales:** Registro con notas, etiquetas (`#`), estado de ánimo, transacciones divididas y calculadora integrada.
- **Gestor de Wallets/Proyectos:** Soporte multi-cuenta y traspasos entre cuentas propias.
- **Seguridad y Privacidad:** Almacenamiento exclusivamente local, modo privacidad y copias de seguridad (JSON/Excel).
- **Hábitos:** Rastreador de rutinas con metas semanales, efectos visuales y recordatorios inteligentes.
- **Personalización Visual:** 11 temas artísticos (incluyendo **Mondrian** y **Pop Art**) y perfiles personalizados.

## Modificaciones Recientes (v1.4.26)

### 1. Lectura y Accesibilidad UX
Se ha incrementado el tamaño de la fuente (`text-xs` a `text-sm`) en el selector de categorías, carteras y modo desglose del formulario de transacciones, haciendo la lectura mucho más cómoda durante el uso continuado de la app.

### 2. Corrección del Tema Pop Art
Se solucionó un problema de "cajas negras" en el tema **Pop Art** reajustando por completo `globals.css`. Los fondos ahora mapean correctamente a tonos vibrantes (blanco, cian, amarillo) y se fuerza un color de viñeta negra u oscura en previsualizadores (placeholders) asegurando contraste.

### 3. Restauración del Núcleo i18n
Se ha reconstruido el sistema de internacionalización tras una corrupción de archivos, corrigiendo errores de sintaxis y typos en el diccionario español (ej. "Botón Nuclear", "Importación").

### 2. Nuevas Apariencias Artísticas

- **Pop Art**: Estética vibrante con colores saturados y estilo cómic.

### 3. Optimización de Mensajes de Inicio

- El componente `WhatsNewModal` ha sido actualizado para informar dinámicamente sobre la versión 1.4.25, permitiendo el estreno inmediato del tema Mondrian.

### 4. Mantenimiento General

- Corrección de la duplicidad de iconos en categorías importadas.
- Ajuste de desplazamiento (scroll) en la vista de hábitos para dispositivos móviles.
- Sincronización de cierres de brackets en el motor de carga de traducciones.

## Historial de Versiones (Changelog Recopilado)

### [1.4.26] - 2026-04-06 - Mejoras Visuales (UX)
- **Mejora**: Aumento del tamaño de fuente en categorización y wallets dentro del formulario de transacción para mejorar legibilidad.
- **Fix**: Reparación de los colores base (`bg-slate-800`, `900`, `950`) en el tema **Pop Art** para eliminar cajas oscuras que ocultaban el texto.

### [1.4.25] - 2026-03-23 - Estilo Artístico y Estabilidad

- **Añadido**: Tema **Pop Art** con su correspondiente paleta de colores y traducciones.
- **Añadido**: Mensaje de bienvenida de versión 1.4.25 destacando el neoplasticismo y estilos geométricos.
- **Mejora**: Restauración completa de `lib/i18n.js` y corrección de errores tipográficos en español.
- **Mejora**: Ajuste de scroll en móvil para el Habit Tracker.
- **Mejora**: Asignación automática de iconos a categorías sin imagen tras importación.

### [1.4.10] - Recordatorios y Traspasos

- **Añadido**: Sistema de **Recordatorios de Hábitos** con notificaciones PWA.
- **Añadido**: Funcionalidad de **Traspasos entre cuentas** propia.

### [1.3.05] - Mondrian y UI Premium

- **Añadido**: Tema *Estilo Mondrian* y nuevo módulo de **Seguimiento de Hábitos** con efectos de confeti.
- **Añadido**: Componente de aviso de actualizaciones (`WhatsNewModal`).
- **Mejora**: Rediseño del panel de ayuda interna.
