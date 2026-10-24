# EPUBtoXteink Web 🌐

Aplicación web moderna y ligera para adaptar, reducir, comprimir y estabilizar libros electrónicos (EPUB) e imágenes para lectores de tinta electrónica **Xteink X3, X4 y X4 Pro**.

---

## ⚡ Novedades y Características

1. **Detección Automática de Idioma (Español / Inglés):**
   - Detecta automáticamente el idioma de tu navegador (`navigator.language`).
   - Si es español, muestra la interfaz y ayudas en **español**; si es cualquier otro idioma, cambia a **inglés**.
   - Incluye selector manual en la barra superior (`ES` / `EN`) por si el usuario desea cambiarlo al instante.

2. **Sistema de Cuentas, Límites y Créditos:**
   - **Usuario Anónimo (sin cuenta):** Dispone de **1 conversión gratuita al día**.
   - **Usuario Registrado / Logueado:** Dispone de **2 conversiones gratuitas al día**.
   - **Contador en Tiempo Real:** En la barra superior se muestra siempre el cupo diario restante y los créditos acumulados (ej. `Cuenta: 2/2 hoy + 100 créditos`).

3. **Recarga de Créditos con Tarjeta (Stripe Checkout):**
   - Integración con **Stripe** para procesar pagos seguros con tarjeta bancaria.
   - **Planes disponibles:**
     - **5 €:** 100 Conversiones completas.
     - **10 €:** 300 Conversiones completas (3 veces más valor).
   - Los créditos comprados no caducan y se van consumiendo automáticamente una vez agotado el cupo gratuito diario.
   - *Nota:* Puedes configurar tu clave secreta de Stripe mediante la variable de entorno `STRIPE_SECRET_KEY` o en `app.py`. Si no se configura una clave real, el sistema opera en modo de simulación directa para desarrollo.

4. **Subida en Lote (hasta 100 archivos):**
   - Arrastra hasta 100 libros o 100 imágenes a la vez.
   - Lista visual interactiva con el peso en MB y estado individual de cada elemento.
   - Descarga directa en un único archivo comprimido `Lote_Optimizado_Xteink.zip`.

5. **Motor E-Ink de Máxima Calidad:**
   - Portadas nítidas con recálculo de SVG `viewBox` para eliminar halos o imágenes estiradas.
   - Ilustraciones interiores en BMP 24b con Dithering Floyd-Steinberg a los 4 grises nativos.
   - Splitting iterativo de capítulos que superen los 300 KB para evitar cuelgues de RAM en el ESP32.

---

## 🚀 Cómo Iniciar el Servidor

### En Windows:
Haz doble clic sobre:
```text
run_server.bat
```
El servidor arrancará y tu navegador se abrirá automáticamente en `http://localhost:8080`.

### Desde la Terminal:
```bash
cd c:\Users\OscarSson\Videos\GitHub\Epub\EPUBtoXteinkWeb
python app.py
```
Accede en tu navegador a **`http://localhost:8080`**.
