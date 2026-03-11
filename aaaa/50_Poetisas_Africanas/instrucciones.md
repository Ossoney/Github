## Proyecto: 50 poetas del amor (en dominio público)

**Objetivo**: Recopilar 50 mejores poetisas del idioma o zona solicitados, con especialidad en el amor, con biografía sentimental + 5 de sus mejores poemas sobre amor, bilingües cada uno. Los 5 poemas si es posible, porque habrá alguna poetisa que no tenga 5 poemas.

### Parte 1: Generación inicial

Para **cada poeta** crear:

- **1 archivo .md**
- **Biografía**: Breve, enfocada en vida amorosa
- **10 poemas**: Primero en castellano y debajo en idioma original

**Salida**:

```
.md → /home/osso/Descargas/aaaa/poetas_idioma
```

*(o `poetisas_` si aplica)*

**Procesamiento:**

- Procesar **todos los poetas a la vez** sin pausas ni lotes, si es posible abarcar con calidad. Sinó, ofrecer lotes que permitan poemas completos e información completa.
- Siempre deja rastro de todo lo que haces en estado_proyecto.md para poder saber donde estamos y desde hay que continuar si hay algún problema o paramos.

**Control del script**:

- **Verificar** que todos los archivos se generaron correctamente.
- **Notificar** al usuario: "Completado - 50 poetisas generados correctamente"
**Esperar validación del usuario** antes de Parte 2.

### Parte 2: Filtro legal (dominio público)

**Regla**: Autoras fallecidos **antes de 1956** (>70 años).

**Pasos**:

1. **Identificar** poetas fallecidos ≥1956 → **Renombrar** archivos: `poeta_NO_DERECHOS.md/docx`
2. **Añadir** nuevos poetas (fallecidos <1956) hasta completar **50 válidos**
3. **Generar** .md de nuevos con mismo formato
4. **Verificar** todos los archivos en directorios correctos y que no haya autoras duplicadas.
5. **Notificar** al usuario: "Completado - 25 poetas dominio público + NO_DERECHOS marcados"

**No borrar** archivos `_NO_DERECHOS` (ejercicio teórico).
