# 🌟 VISUALIS v1.3.05 (Marzo 2026) - Guía de Funcionalidades

Visualis es una aplicación de gestión financiera personal diseñada para ser privada, potente y visualmente atractiva. A continuación se detallan todas sus capacidades:

## 📊 1. Gestión Financiera Principal

### **Dashboard (Tablero de Control)**

* **Resumen Global**: Visualización inmediata del Patrimonio Neto total y balance mensual.
* **Filtrado por Cuenta**: Las tarjetas de la parte superior permiten filtrar **todo el dashboard** (estadísticas, desgloses, actividad y presupuestos) por una cuenta o proyecto específico.
* **Selector Temporal e Histórico**: Navegación entre meses y opciones de histórico (6m, 12m, 24m) que aparecen según disponibilidad de datos.
* **Histórico Completo (∞)**: Opción para visualizar automáticamente todo el historial disponible desde la primera transacción.
* **Actividad Reciente**: Listado dinámico de las últimas operaciones realizadas, filtrado según la cuenta seleccionada.
* **Resumen de Cuentas**: Estado y gestión de todas las cuentas/proyectos activos.
* **Estadísticas Contextuales**: Las medias de ingresos y gastos se ocultan inteligentemente según la vista activa para evitar ruido visual.

### **Transacciones (Ingresos y Gastos)**

* **Registro Detallado**: Permite registrar cantidad, fecha, cuenta origen/destino, categoría, descripción, notas, etiquetas y **Estado de Ánimo**.
* **Gasto Emocional**: Registra cómo te sentiste al realizar un gasto (😍, 🙂, 😐, 😰, 😠) para entender tus patrones de comportamiento.
* **Edición y Borrado**: Control total para modificar o eliminar cualquier movimiento pasado.
* **Buscador Avanzado**: Filtros potentes por texto, rango de fechas, tipo, categoría o cuenta.
* **Calculadora Integrada**: Posibilidad de realizar operaciones matemáticas (sumas, restas, multiplicación, división) directamente desde el campo de importe, ideal para calcular tickets desglosados sin salir de la app.
* **Transacciones Divididas**: Capacidad de dividir un gasto único en múltiples categorías (ej. compra en hipermercado dividida en Alimentación y Limpieza). Cada línea dividida también incluye soporte de calculadora integrada.
* **Contexto Inteligente**: El botón de añadir transacción detecta automáticamente si estás viendo ingresos o gastos.

## 🗂️ 2. Estructura Organizativa

### **Cuentas y Proyectos (Wallets)**

* **Multi-cuenta**: Gestión ilimitada de cuentas (Efectivo, Banco, Ahorros, Tarjetas, Proyectos específicos).
* **Tipos de Cuenta**: Clasificación visual para distinguir entre liquidez y ahorros.

### **Categorización Inteligente**

* **Sistema Jerárquico**: Categorías Principales (ej. Alimentación) y Subcategorías (ej. Supermercado, Restaurante).
* **Iconos y Colores**: Cada categoría tiene su propio icono y color para rápida identificación visual.
* **Personalización**: Posibilidad de crear, editar y eliminar categorías según las necesidades del usuario.

### **Etiquetas (#Tags)**

* **Clasificación Transversal**: Permite agrupar gastos de diferentes categorías bajo un mismo concepto (ej. `#Vacaciones2024`, `#BodaAlberto`).
* **Gestión de Etiquetas**: Panel dedicado para crear y administrar etiquetas.

## 🔄 3. Planificación y Automatización

### **Presupuestos (Budgets)**

* **Límites Mensuales**: Establecimiento de techos de gasto por categoría (ej. Máximo 200€ en Ocio al mes).
* **Seguimiento Visual**: Barras de progreso que indican porcentaje gastado vs disponible.
* **Alertas Visuales**: Indicadores de color cuando te acercas o excedes el límite.

### **Transacciones Recurrentes**

* **Automatización**: Configuración de ingresos o gastos fijos (Nómina, Alquiler, Netflix, etc.).
* **Frecuencia Estándar**: Generación automática mensual el día elegido.
* **Gestión**: Panel para activar/desactivar recurrencias sin borrarlas.

## 📈 4. Seguimiento de Hábitos (Habit Tracker)

* **Construcción de Rutinas**: Permite definir metas semanales para nuevos hábitos (ej. Ejercicio 3 veces/semana).
* **Vista de 7 Días**: Cuadrícula interactiva que muestra la semana completa para marcar el cumplimiento con un solo clic y feedback visual inmediato.
* **Efectos Premium**: Animaciones de partículas tipo "explosión" al completar una tarea diaria para reforzar el hábito positivamente.
* **Reordenación Dinámica**: Capacidad de organizar tus hábitos por importancia mediante arrastre directo (Drag & Drop).
* **Progreso Dinámico**: Anillos de progreso que muestran el avance real vs la meta establecida para la semana.
* **Historial de Consistencia**: Mini-mapas de calor integrados que muestran los últimos 21 días de actividad de un vistazo.
* **Personalización**: Cada hábito puede tener su propio color identificativo.

## 🎨 5. Personalización y Experiencia (UX)

### **Identidad Visual y Temas**

Sistema de temas completo que cambia toda la paleta de colores de la aplicación:

* 🌌 **Noche Estrellada** (Azul Oscuro/Plata)
* 🌕 **Eclipse Dorado** (Negro/Oro)
* 🌲 **Bosque Profundo** (Verde/Pizarra)
* 🔮 **Nebulosa Púrpura** (Violeta/Deep)
* 🦾 **Futuro Neón** (Cyberpunk)
* 🍷 **Vino Selecto** (Burdeos)
* 🌤️ **Claro Cielo** (Clásico y Brillante)
* 🌱 **Claro Menta** (Tonos Zinc y Verde Esmeralda)
* 🌅 **Claro Cálido** (Tonos Marfil y Pálidos Rojos)

### **Perfil de Usuario**

* **Avatar y Nombre**: Personalización de la identidad del usuario.
* **Personalización de Inicio**: Opción para cambiar el título de la app a "Las finanzas de [Nombre]".

### **Internacionalización (i18n)**

Soporte completo multi-idioma:

* 🇪🇸 Español
* 🇬🇧 English
* 🏳️ Gallego
* 🏳️ Euskera

## 🔒 6. Datos y Privacidad

### **Privacidad Local (Local First)**

* **Sin Nube Externa**: Todos los datos se almacenan en el navegador del usuario (IndexedDB). No viajan a servidores externos, garantizando máxima privacidad.

### **Copias de Seguridad (Backup)**

* **Exportación JSON**: Generación de un archivo completo con toda la base de datos (cuentas, movimientos, configuración) para migrar entre dispositivos.
* **Restauración**: Capacidad de importar copias de seguridad previas.
* **Exportación a Excel**: Descarga de datos en formato `.xlsx` para análisis externos detallados.

### **Seguridad de Datos**

* **Zona de Peligro**: Funcionalidad "Botón Nuclear" para reinicio de fábrica (borrado seguro de todos los datos locales).

### **Modo Privacidad**

* **Ocultación de saldos**: Botón en la cabecera (icono de ojo) que permite ofuscar todos los importes sensibles de la aplicación con un solo clic, ideal para usar la app en público.
