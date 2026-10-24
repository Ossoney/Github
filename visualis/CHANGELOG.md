# 📜 Changelog - VISUALIS

## [1.4.39] - 2026-10-15

### Added

- **Sistema Local de Logging de Eventos y Errores (`visualis.log`)**:
  - Implementado endpoint API interno en Next.js (`/api/log`) para registrar eventos y excepciones en tiempo de ejecución.
  - Generación y persistencia directa en el archivo `visualis.log` en la carpeta raíz del proyecto (`C:\Users\OscarSson\Videos\GitHub\visualis\`).
  - Módulo cliente `lib/logger.js` con métodos `logger.info`, `logger.warn` y `logger.error`.
  - Capturador global de errores (`window.onerror` y `unhandledrejection`) configurado en `ClientLayout.jsx` para registrar automáticamente cualquier fallo de ejecución en el cliente.
  - Exclusión de `visualis.log` y `*.log` en `.gitignore` para preservar la limpieza del repositorio.

## [1.4.38] - 2026-10-11

### Added

- **Nuevas Apariencias Artísticas de Vanguardia: Futurismo Dinámico y Fauvismo Salvaje**:
  - **Sustitución de "Noche Estrellada" (`sky`) por "Futurismo Dinámico" (`futurism`)**:
    - Inspirado en las vanguardias del Futurismo y el diseño aerodinámico contemporáneo.
    - Fondo de grafito técnico oscuro con sutiles vectores diagonales de fuerza a 135°.
    - Botones principales en **Cobalto Cinético** (`#0066ff`) con destellos degradados a cyan, bordes activos con brillo de propulsión y balances de ingresos en **Cyan Láser** (`#00f0ff`) para máxima visibilidad táctica.
  - **Sustitución de "Eclipse Dorado" (`gold`) por "Fauvismo Salvaje" (`fauvism`)**:
    - Inspirado en la fiera exaltación del color puro sin inhibiciones (Matisse, Derain).
    - Fondo ciruela volcánico oscuro con tarjetas en violeta profundo enmarcadas en **Amarillo Cadmio Solar** puro (`#ffb703`).
    - Sombras desplazadas en **Azul Ultramar Francés** (`#2040d0`), botones enérgicos de amarillo anaranjado y contrastes intensos para una experiencia sensorial viva.
  - **Compatibilidad y Migración Transparente**:
    - Redirección automática de configuraciones previas (`sky` -> `futurism`, `gold` -> `fauvism`).
    - Actualizado el tema por defecto de la aplicación a `futurism`.
    - Traducciones integradas en los 5 idiomas oficiales de la aplicación (`es`, `en`, `gl`, `eu`, `ca`).

## [1.4.37] - 2026-10-11

### Added

- **Nuevas Apariencias Artísticas de Alto Impacto: Bauhaus y Brutalismo Ácido**:
  - **Sustitución de "Cielo Ártico" por "Bauhaus Constructivista" (`bauhaus`)**:
    - Estética de vanguardia arquitectónica de 1920. Fondo en blanco yeso crudo con cuadrícula técnica milimétrica, esquinas puras, bordes negros rotundos y sombras sólidas de bloque. Botones en rojo cinabrio (`#d62828`), acentos en azul cobalto (`#003049`) y máxima legibilidad tipográfica.
  - **Sustitución de "Horizonte Ámbar" por "Brutalismo Ácido" (`brutalist`)**:
    - Estética underground industrial y brutalismo web de alto voltaje. Fondo en negro carbón profundo con acentos e hipercontrastes en verde eléctrico fósforo **Toxic Volt** (`#ccff00`), bordes rotundos, sombras desplazadas sin difuminar y textos de balances ultravisibles.
  - **Migración y Compatibilidad Automática**: Las preferencias previas de usuarios que tenían seleccionados los temas claros anteriores (`light-sky`, `light-warm`) se redirigen de forma transparente hacia los nuevos temas artísticos sin inconsistencias visuales.
  - **Internacionalización**: Nuevas claves añadidas en los 5 idiomas (`es`, `en`, `gl`, `eu`, `ca`).

## [1.4.36] - 2026-10-01

### Added

- **Métrica de Gasto, Ingreso y Balance Diario Medio**:
  - Sustituida la tarjeta abstracta de "Tendencia (+X%)" por la media diaria exacta calculada sobre los días naturales del periodo analizado (`Gasto diario`, `Ingreso diario` o `Balance diario` en `XX,XX € / día`).
  - Proporciona una métrica aterrizada y realista del ritmo de vida financiero cotidiano.
- **Restauración y Cobertura Total Multiidioma (i18n)**:
  - Completadas y sincronizadas todas las 271 claves de traducción en los 5 idiomas soportados: **Galego**, **Català**, **Euskara**, **English** y **Español**.
  - Corregido el problema por el cual menús, barra lateral de configuración, títulos y ayudas volvían a mostrarse en castellano al seleccionar Gallego u otros idiomas autonómicos.
  - Traducidos al 100% todos los textos del panel de insights históricos y cabeceras gráficas.

## [1.4.35] - 2026-10-01

### Added

- **Escalas Claras y Visualización Interactiva en Gráficos Históricos (6m / 12m / 24m / ∞)**:
  - **Eje Y con Escalas en Euros**: Ahora los gráficos de evolución mensual incorporan referencias numéricas en el lateral izquierdo (`0 €`, valores medios y techo de escala máxima con redondeo inteligente). En el gráfico de Balance Neto, el eje es bidireccional mostrando valores positivos, línea cero y negativos.
  - **Cabecera Contextual Descriptiva**: Título explicativo según el tipo consultado (*Evolución mensual de Ingresos*, *Evolución mensual de Gastos*, *Evolución mensual del Balance Neto*) con subtítulo que aclara la escala en euros.
  - **Interacción Táctil y Hover**: Al deslizar el dedo o pasar el ratón sobre cualquier mes, se proyecta una guía vertical y un punto resaltado, mostrando el mes y el importe exacto en la cabecera del gráfico al instante.
  - **Insignia de Récord Mensual**: Distintivo visual flotante permanente sobre el mes pico (`Máx: X.XXX €`) para identificar de inmediato el mes de mayor movimiento financiero sin tener que pulsar en cada punto.
  - **Canvas Ampliado**: Mayor altura y espaciado lateral para una lectura gráfica espaciosa y descansada en dispositivos móviles y de escritorio.

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
