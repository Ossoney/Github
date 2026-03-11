#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera 100 poetisas eróticas/apasionadas - Proyecto 'El Hilo Rojo'
Sigue instrucciones.md: biografía sentimental + 10 poemas bilingües
Usa google.genai (nueva librería)
"""

import os
import time
import google.genai as genai

API_KEY = os.environ.get("GEMINI_API_KEY", "")
if not API_KEY:
    raise ValueError(
        "Falta GEMINI_API_KEY. Ejecuta con:\n"
        "  GEMINI_API_KEY='tu_clave' python3 generar_poetisas_eroticas.py"
    )

client = genai.Client(api_key=API_KEY)

OUTPUT_DIR = "/home/osso/Descargas/aaaa/poetisas_eroticas"
os.makedirs(OUTPUT_DIR, exist_ok=True)

ESTADO_FILE = "/home/osso/Descargas/aaaa/estado_poetisas_eroticas.md"

# ============================================================
# 100 POETISAS apasionadas que escribieron poesía erótica
# Formato: (num, nombre, nacimiento, muerte, país, idioma, no_derechos)
# no_derechos = True si fallecida >= 1956 o aún vive
# ============================================================
POETISAS = [
    # ── GRECIA CLÁSICA ──────────────────────────────────────────────────
    ("001", "Safo de Lesbos", "610 aC", "570 aC", "Grecia", "griego arcaico", False),
    ("002", "Erina de Telos", "360 aC", "352 aC", "Grecia", "griego antiguo", False),

    # ── ROMA CLÁSICA ─────────────────────────────────────────────────────
    ("003", "Sulpicia de Roma", "40 aC", "10 dC", "Roma", "latín", False),

    # ── CHINA IMPERIAL ───────────────────────────────────────────────────
    ("004", "Yu Xuanji", "844", "868", "China", "chino clásico", False),
    ("005", "Xue Tao", "768", "831", "China", "chino clásico", False),
    ("006", "Li Qingzhao", "1084", "1151", "China", "chino clásico", False),
    ("007", "Zhu Shuzhen", "1063", "1110", "China", "chino clásico", False),

    # ── JAPÓN CLÁSICO ────────────────────────────────────────────────────
    ("008", "Izumi Shikibu", "976", "1030", "Japón", "japonés clásico", False),
    ("009", "Ono no Komachi", "825", "900", "Japón", "japonés clásico", False),

    # ── INDIA MEDIEVAL ───────────────────────────────────────────────────
    ("010", "Mirabai", "1498", "1546", "India", "hindi/rajasthani", False),
    ("011", "Mahadevi Akka", "1130", "1160", "India", "canarés", False),
    ("012", "Lalleshwari (Lal Ded)", "1320", "1392", "India", "cachemiri", False),
    ("013", "Andal", "800", "841", "India", "tamil clásico", False),

    # ── PERSIA / ORIENTE MEDIO ───────────────────────────────────────────
    ("014", "Mahsati Ganjavi", "1089", "1159", "Azerbaiyán/Persia", "persa clásico", False),
    ("015", "Rabia al-Adawiyya", "714", "801", "Irak/Siria", "árabe clásico", False),

    # ── EUROPA MEDIEVAL ──────────────────────────────────────────────────
    ("016", "Beatriz de Día (La Comtessa)", "1140", "1175", "Provenza", "occitano", False),
    ("017", "María de Francia", "1160", "1215", "Francia/Inglaterra", "francés antiguo", False),
    ("018", "Hadewijch de Amberes", "1200", "1248", "Países Bajos", "holandés medio", False),
    ("019", "Mechthild de Magdeburgo", "1207", "1282", "Alemania", "alemán medieval", False),
    ("020", "Hildegarda de Bingen", "1098", "1179", "Alemania", "latín medieval", False),

    # ── RENACIMIENTO ─────────────────────────────────────────────────────
    ("021", "Gaspara Stampa", "1523", "1554", "Italia", "italiano", False),
    ("022", "Veronica Franco", "1546", "1591", "Italia", "italiano", False),
    ("023", "Louise Labé", "1524", "1566", "Francia", "francés", False),
    ("024", "Sor Juana Inés de la Cruz", "1648", "1695", "México", "español", False),
    ("025", "María de Zayas y Sotomayor", "1590", "1661", "España", "español", False),

    # ── SIGLO XVII-XVIII ─────────────────────────────────────────────────
    ("026", "Aphra Behn", "1640", "1689", "Inglaterra", "inglés", False),
    ("027", "Lady Mary Wortley Montagu", "1689", "1762", "Inglaterra", "inglés", False),
    ("028", "Anne Bradstreet", "1612", "1672", "Nueva Inglaterra/EEUU", "inglés", False),
    ("029", "Mary Wollstonecraft", "1759", "1797", "Inglaterra", "inglés", False),
    ("030", "Sor Violante do Céu", "1607", "1693", "Portugal/Brasil", "portugués/español", False),

    # ── ROMANTICISMO (XIX) ───────────────────────────────────────────────
    ("031", "Carolina Coronado", "1820", "1911", "España", "español", False),
    ("032", "Rosalía de Castro", "1837", "1885", "España/Galicia", "gallego/español", False),
    ("033", "Gertrudis Gómez de Avellaneda", "1814", "1873", "Cuba/España", "español", False),
    ("034", "Emily Brontë", "1818", "1848", "Inglaterra", "inglés", False),
    ("035", "Elizabeth Barrett Browning", "1806", "1861", "Inglaterra", "inglés", False),
    ("036", "Christina Rossetti", "1830", "1894", "Inglaterra", "inglés", False),
    ("037", "Emily Dickinson", "1830", "1886", "EEUU", "inglés", False),
    ("038", "Adah Isaacs Menken", "1835", "1868", "EEUU", "inglés", False),
    ("039", "Renée Vivien", "1877", "1909", "Francia/Inglaterra", "francés", False),
    ("040", "Anna de Noailles", "1876", "1933", "Francia", "francés", False),
    ("041", "Luisa Pérez de Zambrana", "1837", "1922", "Cuba", "español", False),
    ("042", "Marceline Desbordes-Valmore", "1786", "1859", "Francia", "francés", False),
    ("043", "Lucie Delarue-Mardrus", "1874", "1945", "Francia", "francés", False),
    ("044", "Rachilde (Marguerite Vallette-Eymery)", "1860", "1953", "Francia", "francés", False),
    ("045", "Edith Södergran", "1892", "1923", "Finlandia", "sueco", False),

    # ── ENTRE SIGLOS XIX-XX ──────────────────────────────────────────────
    ("046", "Delmira Agustini", "1886", "1914", "Uruguay", "español", False),
    ("047", "María Eugenia Vaz Ferreira", "1875", "1924", "Uruguay", "español", False),
    ("048", "Alfonsina Storni", "1892", "1938", "Argentina", "español", False),
    ("049", "Julia de Burgos", "1914", "1953", "Puerto Rico", "español", False),
    ("050", "Florbela Espanca", "1894", "1930", "Portugal", "portugués", False),
    ("051", "Amy Lowell", "1874", "1925", "EEUU", "inglés", False),
    ("052", "Edna St. Vincent Millay", "1892", "1950", "EEUU", "inglés", False),
    ("053", "Sara Teasdale", "1884", "1933", "EEUU", "inglés", False),
    ("054", "Elinor Wylie", "1885", "1928", "EEUU", "inglés", False),
    ("055", "Radclyffe Hall", "1880", "1943", "Inglaterra", "inglés", False),
    ("056", "Sigrid Undset", "1882", "1949", "Noruega", "noruego", False),
    ("057", "Zinaida Hippius", "1869", "1945", "Rusia", "ruso", False),
    ("058", "Marina Tsvetáyeva", "1892", "1941", "Rusia", "ruso", False),
    ("059", "Colette", "1873", "1954", "Francia", "francés", False),
    ("060", "Else Lasker-Schüler", "1869", "1945", "Alemania", "alemán", False),
    ("061", "Charlotte Mew", "1869", "1928", "Inglaterra", "inglés", False),
    ("062", "Yosano Akiko", "1878", "1942", "Japón", "japonés", False),
    ("063", "Malak Abd al-Aziz", "1898", "1940", "Egipto", "árabe", False),
    ("064", "Clara Sandoval", "1895", "1950", "Colombia", "español", False),

    # ── SIGLO XX - NO_DERECHOS (fallecidas >= 1956 o vivas) ──────────────
    ("065", "Natalie Barney", "1876", "1972", "EEUU/Francia", "francés/inglés", True),
    ("066", "Juana de Ibarbourou", "1892", "1979", "Uruguay", "español", True),
    ("067", "H.D. (Hilda Doolittle)", "1886", "1961", "EEUU", "inglés", True),
    ("068", "Dorothy Parker", "1893", "1967", "EEUU", "inglés", True),
    ("069", "Djuna Barnes", "1892", "1982", "EEUU", "inglés", True),
    ("070", "Vita Sackville-West", "1892", "1962", "Inglaterra", "inglés", True),
    ("071", "Sylvia Townsend Warner", "1893", "1978", "Inglaterra", "inglés", True),
    ("072", "Anna Ajmátova", "1889", "1966", "Rusia", "ruso", True),
    ("073", "Gabriela Mistral", "1889", "1957", "Chile", "español", True),
    ("074", "Dulce María Loynaz", "1902", "1997", "Cuba", "español", True),
    ("075", "Clara Lair", "1895", "1973", "Puerto Rico", "español", True),
    ("076", "Magda Portal", "1900", "1989", "Perú", "español", True),
    ("077", "Forugh Farrojzad", "1934", "1967", "Irán", "persa", True),
    ("078", "Nazik al-Mala'ika", "1923", "2007", "Irak", "árabe", True),
    ("079", "Halina Poświatowska", "1935", "1967", "Polonia", "polaco", True),
    ("080", "Nelly Sachs", "1891", "1970", "Alemania/Suecia", "alemán", True),
    ("081", "Ingeborg Bachmann", "1926", "1973", "Austria", "alemán", True),
    ("082", "Marguerite Yourcenar", "1903", "1987", "Francia/Bélgica", "francés", True),
    ("083", "Sophia de Mello Breyner Andresen", "1919", "2004", "Portugal", "portugués", True),
    ("084", "Ping Xin (Bing Xin)", "1900", "1999", "China", "chino", True),
    ("085", "Anne Sexton", "1928", "1974", "EEUU", "inglés", True),
    ("086", "Sylvia Plath", "1932", "1963", "EEUU", "inglés", True),
    ("087", "Adrienne Rich", "1929", "2012", "EEUU", "inglés", True),
    ("088", "Audre Lorde", "1934", "1992", "EEUU", "inglés", True),
    ("089", "Sharon Olds", "1942", "vive", "EEUU", "inglés", True),
    ("090", "Erica Jong", "1942", "vive", "EEUU", "inglés", True),
    ("091", "Nikki Giovanni", "1943", "vive", "EEUU", "inglés", True),
    ("092", "Olga Broumas", "1949", "vive", "Grecia/EEUU", "inglés/griego", True),
    ("093", "Concha Méndez", "1898", "1986", "España/México", "español", True),
    ("094", "Luisa Carnés", "1905", "1964", "España/México", "español", True),
    ("095", "Nathalie Sarraute", "1900", "1999", "Francia", "francés", True),
    ("096", "Fumiko Hayashi", "1903", "1975", "Japón", "japonés", True),
    ("097", "Berta Lask", "1878", "1967", "Alemania", "alemán", True),
    ("098", "Magda Iguarán de Correa", "1899", "1968", "Colombia", "español", True),
    ("099", "Anne Spencer", "1882", "1975", "EEUU", "inglés", True),
    ("100", "Kathleen Raine", "1908", "2003", "Inglaterra", "inglés", True),
]


def generar_poetisa(num, nombre, nacimiento, muerte, pais, idioma, no_derechos):
    """Genera el archivo .md para una poetisa usando Gemini."""

    muerte_str = muerte if muerte else "vive"

    prompt = f"""Eres una experta en literatura erótica y apasionada universal.

Crea un documento Markdown completo y detallado sobre la poetisa ERÓTICA:
**{nombre}** ({nacimiento} – {muerte_str}) — {pais} — idioma original: {idioma}

El documento debe seguir este formato EXACTO:

---

# {nombre}
*({nacimiento} – {muerte_str}) · {pais}*

## Biografía sentimental y erótica

[Escribe 5-7 párrafos DETALLADOS sobre su vida amorosa, sus amantes, su sensualidad,
sus obsesiones eróticas, escándalos, relaciones, y cómo todo eso se reflejó en su poesía.
Sé apasionado, literario, específico. Mínimo 500 palabras. Sin censuras.]

---

## Sus 10 mejores poemas eróticos y apasionados

Para cada poema, usa esta tabla bilingüe:

### Poema 1: [Título del poema]

| {idioma.upper()} (original) | ESPAÑOL (traducción) |
|:---|:---|
| [verso 1 completo] | [traducción verso 1] |
| [verso 2 completo] | [traducción verso 2] |
| ... | ... |

### Poema 2: [Título del poema]
(etc. hasta el poema 10)

---

INSTRUCCIONES CRÍTICAS:
1. Los 10 poemas deben ser los MÁS ERÓTICOS, SENSUALES y APASIONADOS de su obra conocida.
2. Incluir poemas que hablen explícitamente de deseo sexual, cuerpo, placer, lujuria o amor carnal.
3. Cada poema debe estar COMPLETO (todos sus versos reales, no extractos, no inventados).
4. La columna izquierda de la tabla = texto ORIGINAL en {idioma} (en su escritura/alfabeto nativo).
5. La columna derecha = traducción literaria al español.
6. La biografía debe ser EXPLÍCITA sobre su erotismo y vida amorosa, sin eufemismos.
7. Cita obras, fechas y títulos reales cuando se conozcan.
8. Si no quedan poemas eróticos documentados, usa sus poemas más pasionales/sensuales.
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )
        contenido = response.text
    except Exception as e:
        print(f"  ERROR generando {nombre}: {e}")
        return False

    # Nota legal si aplica
    if no_derechos:
        contenido += (
            "\n\n---\n\n"
            "> ⚠️ **NOTA LEGAL**: Esta poetisa falleció en o después de 1956 (o sigue viva). "
            "Sus obras pueden **no** estar en dominio público. "
            "Este archivo es un ejercicio teórico-literario únicamente.\n"
        )

    # Nombre de archivo
    nombre_archivo = (nombre
        .replace(" ", "_")
        .replace("(", "")
        .replace(")", "")
        .replace("'", "")
        .replace(".", "")
        .replace(",", "")
        .replace("/", "-")
    )
    if no_derechos:
        filename = f"{num}_{nombre_archivo}_NO_DERECHOS.md"
    else:
        filename = f"{num}_{nombre_archivo}.md"

    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(contenido)

    print(f"  ✅ [{num}] {nombre} → {filename}")
    return filename


def actualizar_estado(poetisas_completadas):
    """Actualiza el archivo de estado del proyecto."""
    total = len(poetisas_completadas)
    ok_count = sum(1 for p in poetisas_completadas if p[8])
    nd_count = sum(1 for p in poetisas_completadas if p[8] and p[6])
    valid_count = sum(1 for p in poetisas_completadas if p[8] and not p[6])

    lineas = [
        "# Estado: Proyecto 100 Poetisas Eróticas y Apasionadas\n\n",
        f"**Directorio**: `poetisas_eroticas/`  \n",
        f"**Total generadas**: {ok_count}/{total}  \n",
        f"**Dominio público** (fallecidas < 1956): {valid_count}  \n",
        f"**NO_DERECHOS** (fallecidas ≥ 1956 o viven): {nd_count}  \n\n",
        "| # | Poetisa | País | Idioma | Archivo | Estado |\n",
        "|:--|:--------|:-----|:-------|:--------|:-------|\n",
    ]
    for item in poetisas_completadas:
        num, nombre, nac, mue, pais, idioma, no_der, filename, ok = item
        estado = "✅ Creado" if ok else "❌ Error"
        if no_der and ok:
            estado += " ⚠️ NO_DERECHOS"
        lineas.append(f"| {num} | {nombre} ({nac}–{mue}) | {pais} | {idioma} | `{filename}` | {estado} |\n")

    with open(ESTADO_FILE, "w", encoding="utf-8") as f:
        f.writelines(lineas)


def main():
    print("=" * 60)
    print("GENERANDO 100 POETISAS ERÓTICAS Y APASIONADAS")
    print("=" * 60)
    print(f"Directorio de salida: {OUTPUT_DIR}")
    print()

    completadas = []
    errores = []

    for poetisa in POETISAS:
        num, nombre, nac, mue, pais, idioma, no_der = poetisa
        tag = "⚠️ NO_DERECHOS" if no_der else "✓ Dominio público"
        print(f"[{num}/100] {nombre} ({pais}) [{tag}]...")

        filename = generar_poetisa(num, nombre, nac, mue, pais, idioma, no_der)
        ok = bool(filename)
        if not filename:
            filename = f"{num}_ERROR.md"
            errores.append(nombre)

        completadas.append((num, nombre, nac, mue, pais, idioma, no_der, filename, ok))

        # Guardar estado tras cada poetisa
        actualizar_estado(completadas)

        # Pausa corta para no saturar la API
        time.sleep(1.5)

    print()
    print("=" * 60)
    ok_total = len(completadas) - len(errores)
    print(f"COMPLETADO: {ok_total}/100 generadas correctamente")
    if errores:
        print(f"ERRORES ({len(errores)}): {', '.join(errores)}")
    print(f"Estado guardado en: {ESTADO_FILE}")
    print("=" * 60)


if __name__ == "__main__":
    main()
