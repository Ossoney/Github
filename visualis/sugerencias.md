# Sugerencias y Mejoras

- [x] Añadir en Configuración la opción "Versión/Ayuda" al final de la lista.
- [x] Al pulsar "Versión/Ayuda", mostrar el texto completo de las características (contenido de `CARACTERISTICAS.md`).
- [x] Incorporar una línea de texto con un email de contacto para sugerencias/quejas en "Versión/Ayuda".
- [x] Añadir sección de donaciones "Invítame a un café" con enlace a PayPal (<https://paypal.me/ossoney>) en "Versión/Ayuda", traducido a todos los idiomas.
- [ ] **Metas de Ahorro**: Fijar objetivos (ej. "Coche") y ver progreso.
- [x] **Vista de Calendario**: Ver gastos e ingresos diarios en un calendario mensual (con botón "Volver").
- [ ] **Adjuntos y Recibos**: Adjuntar fotos/PDFs a las transacciones.
- [x] **Modo Privacidad**: Botón para ocultar/difuminar importes sensibles.
- [ ] **Gestión de Deudas**: Control de préstamos a/de amigos.
- [x] **Transacciones Divididas**: Asignar múltiples categorías a un solo movimiento (Wizard).
- [ ] **Listas de Compra**: Checklist que convierte items en gastos.
- [ ] **Atajos de Teclado**: Teclas rápidas para desktop.
- [ ] **Suscripciones Recurrentes**: Panel para cargos fijos (Netflix, Alquiler) y alertas.
- [x] **Presupuestos (Budgets)**: Límites de gasto por categoría con barras de progreso.
- [x] **Filtrado por Cuenta**: Capacidad de ver todo el dashboard filtrado por una cuenta/proyecto específico.
- [x] **Histórico Total (∞)**: Opción para ver todo el historial de datos sin límites de meses.
- [x] **Backup Manual**: Exportación completa a JSON y Excel (ya funcional).
- [ ] **Sincronización Automática**: Conexión directa con Google Drive/Dropbox para guardado automático.
- [ ] **Importación Bancaria**: Carga de extractos CSV/Excel.
- [ ] **Búsqueda Global**: Buscador rápido (Ctrl+K) de transacciones y ajustes.
- [ ] **Modo Zen**: Vista simplificada solo con "Disponible hoy".
- [x] **Gasto Emocional**: Registrar cómo te sentiste al gastar (😍/😐/😰) y análisis mensual.
- [ ] **Forecasting (Futuro)**: Proyección de saldo basada en gastos previos.
- [ ] **Resumen Mensual Visual**: Estilo "Stories" con lo destacado del mes.
- [ ] **Input por Voz (IA)**: Crear transacciones hablando.
- [ ] **Seguimiento de Salud (Peso)**: Gráficos de tendencia, importación/exportación (CSV/JSON) y sinergias con gastos en alimentación.

- [ ] **Gamificación de Metas**: Visuales que se colorean al ahorrar.

## 🔐 Autenticación y Sincronización Multi-Dispositivo (Posible Futuro)

> **Estado**: Idea evaluada — No iniciada. Requiere decisión arquitectónica previa.

Se ha analizado la viabilidad de añadir login (usuario + contraseña) para poder acceder a los datos desde cualquier dispositivo. Actualmente la app es **Local-First** (IndexedDB), por lo que cada dispositivo tiene sus propios datos.

### Opción A — Supabase Completo ⭐⭐⭐ (Media-Alta complejidad)
- Migrar toda la lógica de datos de Dexie.js → Supabase (PostgreSQL en la nube).
- Autenticación real con email/contraseña mediante `@supabase/supabase-js`.
- Sincronización en tiempo real entre dispositivos.
- **Nota**: Ya existe `supabase_schema.sql` en el proyecto como base de partida.
- **Esfuerzo estimado**: ~2-3 sesiones largas. Mayor riesgo de regresiones.
- **Resultado**: Login real, datos en la nube, acceso total desde cualquier dispositivo.

### Opción B — Solución Híbrida ⭐⭐ (Media complejidad)
- Mantener Local-First pero añadir sincronización manual contra un backend ligero (Supabase Storage, GitHub Gist, etc.).
- Al abrir la app, se descarga el último backup de la nube y se fusiona.
- **Esfuerzo estimado**: ~1 sesión. Bajo riesgo de romper lo existente.
- **Limitación**: No es tiempo real; funciona como backup automático en la nube.

### Consideraciones antes de implementar
- [ ] Decidir si los datos pasan a ser "del servidor" o se mantiene la filosofía local.
- [ ] Evaluar el plan gratuito de Supabase (500 MB, 50.000 filas — más que suficiente).
- [ ] Definir política de privacidad si los datos salen del dispositivo.

---

## Ideas de Sistemas de Diseño y Apariencias Futuras

Puedes tomar Mondrian como referencia de “sistema de diseño” (bloques, color plano, líneas negras) y luego elegir otros estilos igual de icónicos y legibles para UI.

### Estilos muy geométricos / gráficos

- **Bauhaus**: geometría pura, tipografía sans, paleta primaria+negro/gris; encaja muy bien con grids, layouts modulares y botones claros.
- [ ] **Art déco**: formas escalonadas, diagonales, dorados, contrastes fuertes; perfecto para “premium”, tarjetas, cabeceras con ornamento controlado.
- **Op art**: patrones ópticos y repetitivos, blanco y negro o bicolor; ideal para fondos o loaders, mejor usarlo con moderación para no marear.
- **Constructivismo ruso**: diagonales, bloques rojos/negros, tipografía fuerte; buenísimo para pantallas tipo “dashboard” o mensajes de acción.

### Estilos de color muy reconocibles

- **Fauvismo**: colores muy saturados y algo “salvajes”, contraste alto; puede inspirar tu paleta más que la forma de los componentes.
- [x] **Pop art**: colores planos chillones, bordes marcados, iconografía de cultura popular; perfecto para iconos, ilustraciones de onboarding y vacíos de contenido.
- **Minimalismo**: súper limpio, mucho espacio en blanco, casi monocromo con uno o dos acentos; muy usable para productividades y apps serias.

### Estilos con “atmósfera”

- **Surrealismo**: composiciones oníricas, elementos fuera de contexto; lo usaría en ilustraciones de portada, no tanto en la UI en sí para no romper la claridad.
- **Impresionismo / postimpresionismo**: pinceladas visibles, texturas de color; encaja bien en fondos suaves, headers degradados o ilustraciones, más que en botones.
- **Estética retrofuturista / synthwave**: neones, degradados morado‑cian, grillas; ideal para apps de música, gaming, dashboards “ciberpunk”.

### Estilos pensados para digital / UI

- **Pixel art**: cuadrícula clara, paleta limitada, sensación de videojuego clásico; perfecto para iconos, avatares o modos de “tema retro”.
- **Cartoon / ilustración infantil**: formas simples, contorno, expresividad; muy usable para explicar funciones complejas de forma amigable.
- **“Arquitectura futurista” / tech**: líneas limpias, vidrio, neón sutil; se traduce bien en tarjetas con bordes suaves, sombras ligeras y acentos eléctricos.

*Un truco útil: define un sistema (grid, radios, sombras, tipografía) neutro y luego crea “skins” de tema Mondrian, Bauhaus, Pop Art, Pixel, etc., solo cambiando color, textura e ilustraciones.*
