# Role: Senior Dev - Expenless-Inspired Finance App

# Design Philosophy (The Expenless Way)
- Speed First: El formulario de entrada de gastos debe aparecer por defecto o estar a un toque de distancia.
- Wallet System: La app debe permitir gestionar diferentes "bolsillos" (Cash, Card, Savings).
- Visual Feedback: Usa barras de progreso para presupuestos mensuales. Si el gasto supera el 80%, el color cambia a naranja; si supera el 100%, a rojo.

# Technical Requirements
1. Data Export: El botón de exportación debe generar un Excel con columnas claras: Fecha, Categoría, Cuenta, Descripción, Monto.
2. Local First: Los datos deben persistir en el dispositivo (LocalStorage o IndexedDB) para que la app funcione sin internet, igual que Expenless.
3. Simple Icons: Usa una librería como 'Lucide-React' para asignar iconos a las categorías (ej: 'utensils' para comida).
4. - Nos interesa que la app sea muy visual y muy ligera, que se ejecute muy rápido.

# Dashboard Layout
- Superior: Balance total y selector de cuenta.
- Centro: Gráfico de donut con distribución por categoría.
- Inferior: Lista de transacciones recientes con scroll infinito.


