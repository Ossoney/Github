# CHATwas — Simplificador de conversaciones de WhatsApp

**Versión:** 1.2 | Mayo 2026  
**Sin dependencias externas** — solo librería estándar de Python 3.10+

---

## ¿Qué hace?

Toma el archivo `.txt` exportado de WhatsApp y lo simplifica automáticamente:

| Operación | Descripción |
|---|---|
| 👤 **Detecta participantes** | Extrae todos los nombres de las cabeceras y los reduce a su inicial |
| 🗑️ **Elimina líneas vacías** | Borra líneas donde el mensaje está en blanco |
| 🖼️ **Elimina multimedia** | Borra líneas con `<Multimedia omitido>` |
| 🔇 **Elimina mensajes borrados** | Borra `Eliminaste este mensaje.` y `Se eliminó este mensaje.` |
| ⚙️ **Elimina mensajes de sistema** | Borra la línea inicial de cifrado y similares |
| ✏️ **Elimina "Se editó"** | Quita el fragmento `<Se editó este mensaje.>` del texto |

---

## Uso

```bash
python CHATwas.py
```

El programa muestra un menú interactivo:

1. **Selecciona la carpeta** donde está el `.txt` (o pulsa Enter para el directorio actual)
2. **Elige el archivo** de la lista numerada
3. **Confirma el nombre** del archivo de salida (por defecto añade `_limpio` al nombre)
4. El script muestra los **participantes detectados** y su inicial asignada
5. Procesa y muestra un **resumen estadístico**

El archivo original **no se modifica** — siempre se crea un archivo nuevo.

---

## Formato esperado

El script reconoce el formato estándar de exportación de WhatsApp:

```
31/8/25, 20:47 - Los mensajes y las llamadas están cifrados de extremo a extremo...
18/5/26, 22:23 - Óscar S.: Hola
18/5/26, 22:24 - Rebeca: ¿Qué tal?
18/5/26, 22:25 - Óscar S.: 
18/5/26, 22:26 - CDN Rebeca: <Multimedia omitido>
18/5/26, 22:27 - Óscar S.: Bien <Se editó este mensaje.>
```

Resultado tras procesar:

```
18/5/26, 22:23 - O.: Hola
18/5/26, 22:24 - R.: ¿Qué tal?
18/5/26, 22:27 - O.: Bien
```

> El patrón de cabecera acepta variaciones de fecha (`D/M/AA`, `DD/MM/AAAA`, etc.)  
> Los prefijos de operador como `CDN` se ignoran al calcular la inicial.

---

## Log

Cada sesión queda registrada en `CHATwas.log` junto al script, con marca de tiempo y estadísticas.

---

## Cómo funciona la detección de nombres

El script hace una primera pasada sobre el archivo y extrae todos los nombres únicos que aparecen antes del `:` en cada cabecera. Para cada nombre calcula su inicial (ignorando prefijos como `CDN`, y normalizando tildes: `Ó → O`). No hay nada que configurar — funciona con cualquier chat.

---

## Sugerencias de mejora futura

- Modo **procesado por lotes** (varios `.txt` a la vez)
- Opción de **redactar también las fechas** para anonimización completa
- Exportación a **formato Markdown** con cabeceras por fecha
