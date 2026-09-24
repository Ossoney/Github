# 📜 Changelog - VISUALIS

## [1.4.34] - 2026-09-24

### Added

- **Nuevas Apariencias Artísticas de Alto Contraste**: Estreno de **Cyberpunk Neón** (fondo noche abisal, bordes cian láser con resplandor y botones con degradado neón) y **Ukiyo-e Gran Ola** (estética de xilografía japonesa sobre papel washi, azul índigo de Hokusai y bermellón Torii).
- **Subcategorías en Transacciones Recurrentes**: Selector jerárquico dinámico para clasificar ingresos y gastos fijos mensuales con subcategorías específicas (ej. *Suministros > Luz*).
- **Iconos Inteligentes y Reserva**: Detección semántica automática para nuevas categorías (*Electricidad, Automóvil, Deporte, Viajes, Alquiler...*) y catálogo extendido de iconos de reserva.
- **Acceso Directo a Novedades**: Botón "Ver novedades de la versión" en Configuración > Versión/Ayuda para abrir la ventana de novedades en cualquier momento.
- **Identificador de Versión en Configuración**: Distintivo con la versión actual (v1.4.34) visible en la cabecera y barra lateral de Configuración.

### Fixed

- **Tema Eclipse Dorado (`gold`)**: Reparadas las variables CSS faltantes en `app/globals.css` y añadidas las traducciones multiidioma completas.


### Changed

- **UX/Accesibilidad**: Aumentado el tamaño de la fuente base (`text-xs` a `text-sm`) en el selector de categorías, carteras y modo desglose dentro del formulario de transacciones para mejorar la lectura rápida y usabilidad continuada.

### Fixed

- **Modo Pop Art**: Solucionado un problema visual ("cajas negras") donde fondos muy oscuros ocultaban los textos negros en el formulario de transacciones. Se ha ajustado la paleta para este tema utilizando fondos vibrantes (cyan, amarillo, blanco) con alto contraste según la estética arte pop.

## [1.4.25] - 2026-03-23

### Added

- **Nuevas Apariencias**: Incorporación de los temas **Mondrian Style**, **Art Déco** y **Pop Art**.
- **Sistema de Diseño Neoplástico**: Implementación de bordes marcados y colores primarios en el tema Mondrian para una experiencia visual única.
- **Mensaje de Inicio**: Sistema de notificaciones de bienvenida para informar sobre nuevas versiones y características.

### Fixed

- **Corrupción de Traducciones**: Restauración completa del sistema de internacionalización (i18n.js) y corrección de typos en el diccionario español.
- **Sincronización de Brackets**: Ajuste de cierres de objetos en el núcleo de traducciones.
- **Mejoras en Habit Tracker**: Ajuste de visualización de rachas y consistencia.

## [1.3.05] - 2026-03-15

### Added

- **Habit Tracker**: Seguimiento de hábitos con efectos de partículas y drag & drop.
- **Vista de Calendario**: Visualización mensual de ingresos y gastos.
- **Modo Privacidad**: Ofuscación de saldos sensibles.
- **Transacciones Divididas**: Soporte para múltiples categorías en un solo ticket.
