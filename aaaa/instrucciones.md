## Proyecto: 25 poetas del amor (en dominio público)

**Objetivo**: Recopilar 25 mejores poetas del idioma solicitado, con especialidad en el amor, con biografía sentimental + 10 de sus mejores poemas sobre amor, bilingües cada uno.

### Parte 1: Generación inicial

Para **cada poeta** crear:

- **1 archivo .md**
- **Biografía**: Breve, enfocada en vida amorosa
- **10 poemas**: Tabla bilingüe (original | traducción) por poema

**Salida**:

```
.md → /home/osso/Descargas/aaaa/poetas_idioma
```
*(o `poetisas_` si aplica)*

**Procesamiento:**

- Procesar **todos los poetas a la vez** sin pausas ni lotes.
- Siempre deja rastro de todo lo que haces en estado_proyecto.md para poder saber donde estamos y desde hay que continuar si hay algún problema o paramos.

**Control del script**:

- **Verificar** que todos los archivos se generaron correctamente.
- **Notificar** al usuario: "Completado - 25 poetas generados correctamente"
**Esperar validación del usuario** antes de Parte 2.

### Parte 2: Filtro legal (dominio público)

**Regla**: Autores fallecidos **antes de 1956** (>70 años).

**Pasos**:

1. **Identificar** poetas fallecidos ≥1956 → **Renombrar** archivos: `poeta_NO_DERECHOS.md/docx`
2. **Añadir** nuevos poetas (fallecidos <1956) hasta completar **25 válidos**
3. **Generar** .md de nuevos con mismo formato
4. **Verificar** todos los archivos en directorios correctos
5. **Notificar** al usuario: "Completado - 25 poetas dominio público + NO_DERECHOS marcados"

**No borrar** archivos `_NO_DERECHOS` (ejercicio teórico).
