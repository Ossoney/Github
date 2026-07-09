# EPUBtoMP3 — Estado del proyecto

**Última actualización:** Mayo 2026
**Archivo principal:** `EPUBtoMP3.py`

---

## Funcionalidades Recientes (Mayo 2026)

### 🧩 Fragmentación de Capítulos Largos
- Se ha implementado un límite de **20,000 caracteres** por bloque de audio.
- Los capítulos que superan este límite se dividen en partes (`p1`, `p2`, etc.).
- El corte se realiza de forma inteligente buscando puntos y finales de frase.

### 🌍 Detección Automática de Idioma
- El script lee el metadato `DC:language` del EPUB.
- Soporta mapeo dinámico de voces (Español e Inglés configurados).
- Evita que libros en inglés se lean con acento español y viceversa.

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
