# Guía de Despliegue y PWA

Esta guía detalla cómo llevar tu aplicación **Finanzas Visuales** en tu móvil y cómo desplegarla en internet.

## 1. Despliegue en Vercel (Gratis)

La forma más sencilla de tener tu app accesible desde cualquier lugar es usar Vercel.

1. **Crea una cuenta en Vercel**: Ve a [vercel.com](https://vercel.com) y regístrate (puedes usar tu cuenta de GitHub).
2. **Nuevo Proyecto**:
    * Haz clic en "Add New..." > "Project".
    * Selecciona tu repositorio de GitHub `finanzas-visuales`.
    * Dale a "Import".
3. **Configuración**:
    * Vercel detectará automáticamente que es un proyecto Next.js.
    * No necesitas cambiar nada en "Build and Output Settings".
    * Haz clic en **"Deploy"**.
4. **¡Listo!**: En unos minutos, Vercel te dará una URL (ejemplo: `https://finanzas-visuales.vercel.app`).

## 2. Instalación en el Móvil (PWA)

Una vez desplegada, puedes instalarla en tu móvil para que parezca una App nativa (sin barra de navegador, pantalla completa, icono en inicio).

### En iPhone (iOS)

1. Abre Safari y ve a tu URL de Vercel.
2. Toca el botón **Compartir** (cuadrado con flecha hacia arriba).
3. Busca y selecciona **"Añadir a la pantalla de inicio"**.
4. Confirma el nombre y dale a "Añadir".

### En Android (Chrome)

1. Abre Chrome y ve a tu URL de Vercel.
2. Toca los **tres puntos** (menú) arriba a la derecha.
3. Selecciona **"Añadir a pantalla de inicio"** o "Instalar aplicación".

## 3. Sincronización de Datos (Importante)

Tu aplicación sigue una filosofía **"Local-First"**. Esto significa que los datos (tus gastos, ingresos, etc.) se guardan **dentro de tu dispositivo** (en el navegador), no en una nube centralizada.

* **Consecuencia**: Los datos que metas en el ordenador NO aparecerán automáticamente en el móvil, y viceversa.
* **Solución (Backup)**: Próximamente habilitaremos una función para "Exportar Copia de Seguridad" en un archivo y "Restaurar" en otro dispositivo, para que puedas pasar tus datos manualmente si lo necesitas.

### Recomendación

Usa el móvil para el día a día (añadir gastos rápidos) y el ordenador para revisiones mensuales o ajustes de presupuesto, sincronizando manualmente cuando sea necesario mediante la función de Backup.
