# EPUBtoMP3 — Estado del proyecto

**Última actualización:** Mayo 2026
**Archivo principal:** `EPUBtoMP3.py`

---

## Funcionalidades Recientes (Mayo 2026)

### 🧩 Fragmentación de Capítulos Largos
- Se ha implementado un límite de **20,000 caracteres** por bloque de audio.
- Los capítulos que superan este límite se dividen en partes con formato de dos dígitos (`p01`, `p02`, etc.) para garantizar una correcta ordenación alfabética y secuencial en reproductores de audio.
- El corte se realiza de forma inteligente buscando puntos y finales de frase.

### 🌍 Gestión de Idioma (Detección o Forzado)
- El script lee el metadato `DC:language` del EPUB.
- Soporta mapeo dinámico de voces (Español, Inglés y Gallego configurados).
- Voces en Gallego integradas: `gl-ES-RoiNeural` (Hombre) y `gl-ES-SabelaNeural` (Mujer).
- Menú interactivo al inicio que permite dejar la detección en **Automático** o **Forzar** Gallego, Español o Inglés manualmente aunque el EPUB no tenga los metadatos correctos.

### 🎙️ Alternancia de Voz en Reintentos
- Si un intento de descarga falla, el siguiente reintento cambia automáticamente el género de la voz (Hombre ↔ Mujer).
- Esto ayuda a evadir límites temporales del servidor TTS de Microsoft.

### 🛡️ Verificación de Integridad (Anti-Corrupción)
- Tras generar cada MP3, se valida mediante `mutagen` que el archivo sea legible y tenga una duración mayor a 0.
- Si el archivo es inválido, se elimina automáticamente y se lanza un reintento.

---

## Configuración Técnica Actualizada

```python
CONCURRENCIA   = 2      # Recomendado 2 para evitar errores 503
REINTENTOS     = 3      # Intentos totales por cada fragmento
LIMITE_CHARS   = 20000  # Caracteres máximos por archivo MP3
```

## Próximos Pasos (Opcional)
- [ ] Soporte para más idiomas (Francés, Alemán, etc.).
- [ ] Normalización de volumen mediante `ffmpeg` tras la conversión.
- [ ] Interfaz gráfica simple (GUI) para evitar la consola.
