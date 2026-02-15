# 📱 Guía de Acceso y Despliegue: Finanzas Visuales

Esta aplicación está diseñada con una arquitectura **"Local-First"**. Esto significa que tus datos viven **exclusivamente en el dispositivo** donde la usas (tu ordenador, tu móvil, tu tablet). No hay una nube central que sincronice todo automáticamente por defecto.

---

## 🏠 Opción 1: Acceso en Casa (Red WiFi Local)

Ideal para probar la app en tu móvil sin configurar servidores. Solo funciona si ambos dispositivos están conectados al mismo WiFi.

### Pasos

1. **En tu PC (Servidor):**
    * Abre la terminal en la carpeta del proyecto.
    * Ejecuta el comando: `npm run dev`
    * Asegúrate de que la terminal muestre: `ready - started server on 0.0.0.0:3000, url: http://localhost:3000`
    * **Averigua tu IP Local:**
        * Abre otra terminal (PowerShell o CMD).
        * Escribe `ipconfig` y pulsa Enter.
        * Busca la línea **"Dirección IPv4"** bajo tu adaptador WiFi o Ethernet. (Ejemplo: `192.168.1.45`)

2. **En tu Móvil (Cliente):**
    * Conéctate al **mismo WiFi** que el PC.
    * Abre tu navegador (Chrome, Safari).
    * Escribe en la barra de direcciones: `http://TU_IP_LOCAL:3000`
        * *Ejemplo: `http://192.168.1.45:3000`*

### ⚠️ Importante sobre los Datos

Al entrar desde el móvil, verás la aplicación **vacía**. Esto es normal.

* Los datos del PC están en el PC.
* Los datos del móvil se guardarán en el móvil.
* **Para mover datos:** Usa la opción **Exportar** (en PC) -> Envíate el archivo Excel al móvil -> Usa la opción **Importar** (en Móvil - *Próximamente*).

---

## 🌍 Opción 2: Acceso desde Cualquier Lugar (Despliegue)

Si quieres usar la app fuera de casa o compartirla, necesitas subirla a internet. La forma más sencilla y gratuita es **Vercel**.

### Pasos para Desplegar

1. **Sube tu código a GitHub:**
    * Asegúrate de que tus últimos cambios estén subidos a tu repositorio.

2. **Crea una cuenta en Vercel:**
    * Ve a [vercel.com](https://vercel.com) y regístrate con tu cuenta de GitHub.

3. **Importar Proyecto:**
    * En Vercel, pulsa "Add New..." -> "Project".
    * Selecciona tu repositorio `finanzas-visuales`.
    * Dale a **Deploy**.

4. **¡Listo!:**
    * Vercel te dará una URL pública (ejemplo: `finanzas-visuales.vercel.app`).
    * Puedes entrar desde cualquier lugar del mundo.

### 💡 Nota sobre Persistencia

Aunque la web esté en internet, los datos **siguen siendo locales** en cada dispositivo.

* Si entras desde el móvil de tu pareja, verás otros datos (o cero datos).
* Si borras la caché del navegador, podrías perder los datos (¡usa la Exportación de seguridad regularmente!).

---

## 🚀 Instalación como App Nativa (PWA)

Para una mejor experiencia en móvil (sin barra de navegador y pantalla completa):

1. Abre la app en el navegador de tu móvil (ya sea por WiFi local o Vercel).
2. **Android (Chrome):** Menú (3 puntos) -> "Instalar aplicación" o "Añadir a pantalla de inicio".
3. **iOS (Safari):** Botón Compartir -> "Añadir a la pantalla de inicio".

La app aparecerá en tu menú como una aplicación normal.
