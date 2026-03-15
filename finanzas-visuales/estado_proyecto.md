# Estado del Proyecto: Finanzas Visuales

## Descripción General y Política de Documentación

> **⚠️ IMPORTANTE:** El estado y la evolución de este proyecto se mantienen estrictamente a través de tres documentos centrales. *Cualquier cambio, nueva funcionalidad o proceso de despliegue debe actualizar obligatoriamente estos tres archivos:*
>
> 1. `caracteristicas.md` (Para funcionalidades y alcance)
> 2. `guia_acceso.md` (Para procesos de instalación y acceso)
> 3. `estado_proyecto.md` (Este documento, para el estado actual, UX y Changelog)

El proyecto **Finanzas Visuales** (v1.4.10) es una aplicación web de contabilidad personal diseñada bajo una arquitectura **"Local-First"**. Esto significa que los datos se almacenan directamente en el dispositivo del usuario utilizando IndexedDB, descartando el uso de bases de datos externas (como Supabase) para garantizar la máxima privacidad y velocidad.

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

Según la documentación (`CARACTERISTICAS.md` y `CHANGELOG.md`), la aplicación cuenta con un conjunto amplio de funcionalidades listas:

- **Dashboard Principal:** Resumen global, visualización histórica (6m, 12m, 24m y infinito) y filtrado de contexto.
- **Transacciones Integrales:**
  - Registro fácil de ingresos y gastos con notas, etiquetas (`#`) y estado de ánimo asociado.
  - Opción de **Transacciones Divididas** (Split Transactions).
  - Categorización jerárquica con íconos representativos.
- **Gestor de Wallets/Proyectos:** Soporte multi-cuenta, distinguiendo perfiles y bolsas de dinero.
- **Seguridad y Privacidad:**
  - Almacenamiento exclusivamente local.
  - Modo "Privacidad" (ocultar importes momentáneamente).
  - Zona de peligro (reinicio completo) y copias de seguridad (JSON y `.xlsx`).
- **Hábitos (Novedad):** Rastreador de rutinas con metas semanales, progreso visual, reordenación mediante arrastre (drag & drop), vista de 7 días completa y registro diario con efectos visuales tipo "explosión" de confeti.
- **Aspectos Visuales:** Adaptabilidad total en temas (10 paletas distintas incluyendo Mondrian), avatar propio y adaptación multilingüe.

## Cambios Recientes (Git)

Los últimos commits de la rama `main` enfocan la mejora en la manipulación de estados y correcciones clave:

1. `09aa4fc`: Mantener la cuenta seleccionada en el estado.
2. `30c3b63` / `8991edb`: Incorporación de la visualización de datos de tiempo "infinito" y arreglos en manejo de Excel.
3. `bcabbb3`: Soporte para importación general con archivos Excel.
4. `a480cf2`: Corrección de un de bug al borrar transacciones.

### Modificaciones Recientes (Ajustes de UI / UX)

- **Persistencia de Cuenta**: Se restauró la lógica para que al reiniciar la aplicación se mantenga activa la última cuenta (o proyecto) seleccionada.
- **Optimización Móvil**:
  - En el formulario de transacciones, la cuadrícula de categorías pasó de ser de 4 a 3 elementos por fila para mejorar la pulsación y usabilidad en dispositivos móviles. Los íconos también incrementaron su tamaño para facilitar la selección.
  - Las etiquetas (tags) aumentaron significativamente de tamaño tanto en el selector al crear movimientos como en el gestor de configuración (`TagManager`).
- **Etiquetas**: Se ordenó alfabéticamente la lista de etiquetas tanto en la configuración como en la selección al crear transacciones.
- **Transacciones**: Se habilitó la opción de marcar una transacción como "Recurrente" también al momento de editarla, no solo al crearla.
- **Cuentas y Proyectos**: Se simplificó la vista al eliminar el literal del tipo de cuenta, dejando visible únicamente el nombre y el saldo.
- **Calendario**: Se implementó el redondeo sin decimales en todos los saldos diarios mostrados en la cuadrícula.
- **Transacciones de Traspaso (v1.4.10)**:
  - Se añadió el tipo de transacción "Traspaso" para movimientos de fondos entre cuentas propias.
  - Interfaz dedicada que oculta categorías y permite elegir cuenta de origen y destino.
  - Lógica de balance balanceada (resta en origen, suma en destino).
  - Visualización distintiva en las listas con icono de doble flecha y color azul.
- **Refinamiento de Hábitos y Notificaciones (v1.4.10)**:
  - **Recordatorios Inteligentes**: Sistema de notificaciones PWA con interruptor On/Off personalizado.
  - **Modal de Permisos**: Ventana elegante de pre-autorización para solicitar permisos de notificación con estética acorde a la app.
  - **Internacionalización**: Traducción completa de estadísticas (Rachas, Mejores marcas) y días de la semana en todos los idiomas (ES, EN, GL, EU, CA).
  - **Persistencia en Excel/JSON**: Los hábitos y sus logs ahora se incluyen en todos los sistemas de copia de seguridad y exportación.
  - **Reordenación**: Capacidad de reordenar hábitos mediante *Drag & Drop*.
  - **Vista de 7 Días**: El registro rápido ahora muestra los últimos 7 días completos.
  - **Micro-interacciones**: Efecto de "explosión" de confeti al completar hábitos.
- **Resumen y Balances**:
  - Se retiraron los decimales de la pantalla inicial en las variables de Ingresos, Gastos y Balance Total, así como en los desgloses por categoría.
  - En el historial (6m, 12m, 24m, ∞) se eliminaron las estadísticas de "Mejor mes" y "Peor mes" y se retiraron los decimales en todos los reportes de saldo.
- **Calculadora Integrada**: Se incorporó un componente en el propio flujo de transacciones (tanto en monto global como dividido) para hacer cálculos ágiles de recibos de forma rápida sin cambiar de app.
- **Temas Visuales**:
  - Se han rediseñado por completo las 9 paletas de colores en `globals.css` priorizando el contraste premium estilo SaaS/OLED.
  - Se sustituyeron 3 temas menos usados por **versiones claras (Light Mode)**: *Claro Cielo, Claro Menta y Claro Cálido*, ajustando correctamente las paletas Zinc y Stone invertidas para su total legibilidad.
  - Se incorporó el nuevo tema **"Estilo Mondrian"**, con un contraste máximo tipo *De Stijl*, esquinas ortogonales, fondos negros puros y colores primarios saturados.
- **Novedades Dinámicas**: Se implementó un sistema (`WhatsNewModal`) para mostrar un popup atractivo e interactivo con "Lo Nuevo" únicamente cuando el usuario actualiza a una nueva versión, con opción de aplicar cambios (como el tema) directamente desde ahí.
- **Centro de Ayuda y Prestaciones**: Rediseño completo de la vista de ayuda interna de la aplicación (ahora "Conoce Visualis"), abandonando las listas de texto plano por un un layout de tarjetas con brillos *glassmorphism*, estructurado, muy atractivo visualmente.

## Próximos Posibles Pasos

La arquitectura inicial parece estar completa y robusta en cuanto a gestión de cliente. Cualquier expansión futura dependerá en la optimización de los listados extensos, sincronización en la nube (si fuera necesaria mediante backup P2P) o la incorporación de notificaciones nativas dado que la PWA ya está implementada.

---

## Historial de Versiones (Changelog Recopilado)

### [1.4.10] - Recordatorios y Traspasos

- **Añadido**: Sistema de **Recordatorios de Hábitos** con notificaciones PWA y modal de permisos premium.
- **Añadido**: Nueva funcionalidad de **Traspasos entre cuentas**, permitiendo mover dinero sin afectar al flujo de ingresos/gastos globales.
- **Añadido**: Los hábitos ahora se guardan en los archivos JSON y Excel de copia de seguridad.
- **Mejora**: Traducción completa de todas las etiquetas de hábitos y días de la semana en todos los idiomas.
- **Mejora**: Integración de avisos de versión (`WhatsNewModal`) automáticos para destacar novedades.

### [1.3.05] - Mondrian y UI Premium

- **Añadido**: Tema *Estilo Mondrian* con un agresivo contraste basado en negro, líneas blancas y colores primarios puros.
- **Añadido**: Nuevo módulo de **Seguimiento de Hábitos** (Habit Tracker) con:
  - Metas semanales y anillos de progreso reactivos.
  - Vista completa de los últimos 7 días.
  - Sistema de reordenación por arrastre.
  - Efectos visuales de confeti/explosión al completar tareas.
  - Mini heatmap de consistencia de 21 días optimizado para móvil.
- **Añadido**: Nuevo componente de aviso automarzido de actualizaciones (`WhatsNewModal`).
- **Mejora**: Rediseño estético y de estructura del panel de ayuda y prestaciones (`VersionHelp.jsx`).

### [1.1.31] - Base del Local-First

- **Añadido**: Arquitectura Local-First con IndexedDB (vía Dexie.js) para máxima velocidad y privacidad.
- **Añadido**: Sistema de cuentas (Wallets), alertas visuales para presupuestos, exportación e importación en Excel y JSON.
- **Añadido**: Modo de privacidad para ocultar importes en pantalla rápidamente.
- **Añadido**: Transacciones divididas (Split Transactions).
- **Añadido**: Contexto inteligente aplicado (el botón de añadir se adapta a si estás visualizando ingresos o gastos).
- **Añadido**: Historiales con "Intervalos Inteligentes" para no ofrecer reportes de 2 años si la cuenta recién fue creada.
- **Cambio**: Abandono de dependencias de backend externo (Supabase) enfocándose completamente a PWA y respuesta rápida de UI.
