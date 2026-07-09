# 📱 Guía de Acceso, Instalación y Despliegue: Finanzas Visuales

Esta aplicación está diseñada con una arquitectura **"Local-First"**. Esto significa que tus datos viven **exclusivamente en el dispositivo** donde la usas (tu ordenador, tu móvil, tu tablet). No hay una nube central que sincronice todo automáticamente.

---

## 🏠 1. Acceso Local (Red WiFi en casa)

Ideal para probar la app en tu móvil sin configurar servidores externos. Funciona si ambos dispositivos están conectados a la misma red WiFi.

### Servidor (Tu Ordenador)

1. Abre la terminal en la carpeta del proyecto.
2. Ejecuta el comando: `npm run dev`
3. Asegúrate de que el servidor escuche, verás una URL como `http://localhost:3000`.
4. Averigua tu IP Local (en Windows, abre otra terminal y escribe `ipconfig`). Busca tu "Dirección IPv4" (Ejemplo: `192.168.1.45`).

### Cliente (Tu Móvil)

1. Conéctate al **mismo WiFi**.
2. Abre el navegador (Chrome, Safari) y entra en: `http://TU_IP_LOCAL:3000` (siguiendo el ejemplo: `http://192.168.1.45:3000`).

---

## 🌍 2. Despliegue Público (Vercel)

Si quieres usar la app fuera de casa desde cualquier lugar o compartirla, puedes subirla a internet de forma gratuita con Vercel.

1. **Sube el código a GitHub**: Asegúrate de que tus últimos cambios estén en el repositorio principal.
2. **Crea una cuenta en [Vercel](https://vercel.com)** (puedes iniciar sesión con GitHub).
3. **Importar Proyecto**: En el dashboard de Vercel, pulsa "Add New..." -> "Project". Selecciona tu repositorio `visualis` y dale a **Deploy**.
4. ¡Listo! Vercel te proporcionará una URL pública (ejemplo: `https://visualis.vercel.app`).

---

## 🚀 3. Instalación como App Nativa (PWA en el Móvil)

Una vez que tengas acceso a tu URL (local o la de Vercel), puedes "instalar" la aplicación en tu móvil para que luzca y funcione como una aplicación nativa (sin barra de navegador, ocupando toda la pantalla y con icono en inicio).

### En Android (Chrome)

1. Abre Chrome y dirígete a tu URL de Vercel.
2. Toca los **tres puntos** (menú arriba a la derecha).
3. Selecciona **"Instalar aplicación"** o **"Añadir a pantalla de inicio"**.

### En iPhone (iOS - Safari)

1. Abre Safari y dirígete a tu URL.
2. Toca el botón **Compartir** (el icono de un cuadrado con flecha hacia arriba).
3. Busca y selecciona **"Añadir a la pantalla de inicio"**.

---

## ⚠️ 4. Gestión de Datos y Sincronización

Recuerda siempre el principio **"Local-First"**:

- **Los datos del ordenador se quedan en el ordenador** y los del móvil en el móvil.
- Entrar a la misma URL web desde el móvil no mostrará mágicamente los datos de tu ordenador; la aplicación aparecerá inicialmente vacía.
- **Copias de Seguridad / Sincronización Manual**: Usa la configuración de la app para **"Exportar"** tus datos (se genera un archivo). Envíate ese archivo a tu otro dispositivo y usa la opción análoga para **"Importar"** y restaurar todo el ecosistema.
- Recomendación: Usa tu dispositivo principal (ej. el móvil) para anotar el día a día y exporta el archivo hacia el ordenador cuando quieras hacer revisiones minuciosas o visualizar el historial a pantalla completa.
