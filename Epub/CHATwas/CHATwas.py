"""
==============================================================================
  CHATwas — Simplificador de conversaciones de WhatsApp en .txt
==============================================================================
  Toma el archivo .txt exportado de WhatsApp y lo simplifica:
    · Reduce cada participante a su inicial (detección automática)
    · Elimina líneas de multimedia, mensajes borrados y sistema
    · Limpia el texto «Se editó este mensaje»
  Sin dependencias externas. Solo librería estándar de Python.
  Uso: python CHATwas.py
==============================================================================
"""

import sys
import os
import re
import datetime
import unicodedata
import io

# Forzar UTF-8 en la consola de Windows (evita UnicodeEncodeError con emojis)
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# ---------------------------------------------------------------------------
# CONFIGURACIÓN
# ---------------------------------------------------------------------------

VERSION = "1.2  |  Mayo 2026"

# Patrón de cabecera de mensaje WhatsApp:
#   DD/M/AA, HH:MM - Nombre: [texto]
# Grupo 1 captura el nombre exacto (todo lo que hay entre " - " y ":").
PATRON_CABECERA = re.compile(
    r"^(\d{1,2}/\d{1,2}/\d{2,4},\s+\d{1,2}:\d{2}\s+-\s+)(.+?):\s*"
)
#   grupo 1 ─ prefijo de fecha/hora    grupo 2 ─ nombre del participante

# Líneas de sistema de WhatsApp: tienen timestamp pero NO tienen «Nombre: »
# Ejemplo: «31/8/25, 20:47 - Los mensajes y las llamadas están cifrados…»
PATRON_SISTEMA = re.compile(
    r"^\d{1,2}/\d{1,2}/\d{2,4},\s+\d{1,2}:\d{2}\s+-\s+"
)

# Textos "vacíos" que hacen que la línea entera deba borrarse
MENSAJES_VACIAR = {
    "",                          # mensaje en blanco (tras la cabecera)
    "<Multimedia omitido>",
    "\u200e<Multimedia omitido>",  # variante con carácter invisible LRM
    "Eliminaste este mensaje.",
    "Se eliminó este mensaje.",
}

# Fragmentos inline que se eliminan (se borra solo el fragmento, no la línea)
FRAGMENTOS_BORRAR = [
    " <Se editó este mensaje.>",
    "\u200e<Se editó este mensaje.>",   # variante con carácter invisible
    "<Se editó este mensaje.>",
]

# Prefijos no-nombre que WhatsApp añade a algunos contactos (ej: "CDN Rebeca")
PREFIJOS_NO_NOMBRE = ("CDN ", "cdn ")

# ---------------------------------------------------------------------------
# LOGGING (igual que el resto de scripts del proyecto)
# ---------------------------------------------------------------------------

LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "CHATwas.log")

class TeeLogger:
    def __init__(self, filepath):
        self._consola = sys.stdout
        self._log     = open(filepath, "a", encoding="utf-8", buffering=1)
        sys.stdout    = self
    def write(self, texto):
        self._consola.write(texto)
        self._log.write(texto)
    def flush(self):
        self._consola.flush()
        self._log.flush()
    def close(self):
        sys.stdout = self._consola
        self._log.close()

def iniciar_log():
    tee = TeeLogger(LOG_FILE)
    ahora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n{'='*65}\n  SESIÓN  {ahora}\n{'='*65}")
    return tee

# ---------------------------------------------------------------------------
# DETECCIÓN AUTOMÁTICA DE PARTICIPANTES
# ---------------------------------------------------------------------------

def _sin_tildes(texto: str) -> str:
    """Devuelve el texto con los diacríticos eliminados."""
    return "".join(
        c for c in unicodedata.normalize("NFD", texto)
        if unicodedata.category(c) != "Mn"
    )

def nombre_a_inicial(nombre: str) -> str:
    """
    Calcula la inicial de un nombre tal como aparece en la cabecera.
    Elimina prefijos de operador/grupo ('CDN ') y devuelve la primera
    letra del nombre real seguida de punto.

    Ejemplos:
        'CDN Rebeca'  → 'R.'
        'Óscar S.'    → 'O.'
        'María José'  → 'M.'
    """
    n = nombre
    for prefijo in PREFIJOS_NO_NOMBRE:
        if n.startswith(prefijo):
            n = n[len(prefijo):]
            break
    primera_raw = n.strip()[0].upper() if n.strip() else "?"
    # Normalizar la inicial: quitar tilde (Ó → O, Á → A, etc.)
    primera = _sin_tildes(primera_raw)
    return primera + "."

def detectar_participantes(lineas: list[str]) -> dict[str, str]:
    """
    Primera pasada: extrae todos los nombres únicos de las cabeceras
    (el texto exacto que aparece antes del ':' final) y devuelve
    {nombre_completo: inicial}.
    """
    participantes = {}
    for linea in lineas:
        m = PATRON_CABECERA.match(linea.rstrip("\n"))
        if not m:
            continue
        nombre = m.group(2).strip()
        if nombre and nombre not in participantes:
            participantes[nombre] = nombre_a_inicial(nombre)
    return participantes

def construir_subs_cuerpo(participantes: dict[str, str]) -> list[tuple]:
    """
    Construye patrones regex para reemplazar menciones de nombres en el
    CUERPO de los mensajes (no en la cabecera — esa se trata por lookup).

    Para cada participante genera:
      - El nombre base sin prefijo tipo 'CDN' (ej: 'Rebeca').
      - Cada palabra significativa del nombre base (ej: 'Óscar' de 'Óscar S.').
      - La variante sin tilde de cada uno (ej: 'Oscar' además de 'Óscar').

    Orden: más largo primero para evitar sustituciones parciales.
    """
    candidatos: dict[str, str] = {}  # {texto_a_buscar: inicial}

    for nombre, inicial in participantes.items():
        # Quitar prefijo de operador/grupo
        base = nombre
        for prefijo in PREFIJOS_NO_NOMBRE:
            if base.startswith(prefijo):
                base = base[len(prefijo):]
                break

        # Añadir el nombre base completo (ej: 'Óscar S.' o 'Rebeca')
        candidatos[base] = inicial

        # Añadir cada palabra significativa (≥ 2 letras y no solo inicial tipo "S.")
        for palabra in base.split():
            if len(palabra) > 2:
                candidatos[palabra] = inicial

    # Generar variantes con y sin tilde
    pares: list[tuple[str, str]] = []
    vistos: set[str] = set()
    for texto, inicial in candidatos.items():
        for variante in [texto, _sin_tildes(texto)]:
            if variante not in vistos:
                vistos.add(variante)
                pares.append((variante, inicial))

    # Ordenar de más largo a más corto (más específico primero)
    pares.sort(key=lambda x: len(x[0]), reverse=True)

    # Compilar los patrones con límites de palabra
    return [
        (re.compile(rf"\b{re.escape(texto)}\b"), inicial)
        for texto, inicial in pares
    ]

# ---------------------------------------------------------------------------
# NÚCLEO — LIMPIEZA
# ---------------------------------------------------------------------------

def limpiar_linea(
    linea: str,
    participantes: dict[str, str],
    subs_cuerpo: list[tuple],
) -> str | None:
    """
    Aplica todas las transformaciones a una línea.
    Devuelve la línea transformada, o None si debe eliminarse.

    Estrategia de sustitución de nombres:
      - CABECERA: lookup directo en el diccionario (exacto, sin regex).
                  El nombre siempre termina en ':' → sin ambigüedad.
      - CUERPO:   patrones regex para menciones sueltas del nombre.
    """
    m = PATRON_CABECERA.match(linea)

    # ── Líneas de sistema WhatsApp (timestamp sin «Nombre:») ─────────────────
    # Ejemplo: «31/8/25, 20:47 - Los mensajes y las llamadas están cifrados…»
    if not m and PATRON_SISTEMA.match(linea):
        return None

    if m:
        # ── Línea con cabecera WhatsApp ───────────────────────────────────
        prefijo_fecha = m.group(1)   # "DD/MM/YY, HH:MM - "
        nombre        = m.group(2)   # "Óscar S." / "Rebeca" / ...
        cuerpo        = linea[m.end():]

        # Borrar línea si el cuerpo es vacío, multimedia o mensaje borrado
        if cuerpo.strip() in MENSAJES_VACIAR:
            return None

        # Eliminar fragmentos inline del cuerpo
        for fragmento in FRAGMENTOS_BORRAR:
            cuerpo = cuerpo.replace(fragmento, "")

        # Sustituir nombres en el cuerpo (menciones en el texto)
        for patron, reemplazo in subs_cuerpo:
            cuerpo = patron.sub(reemplazo, cuerpo)

        # Sustituir el nombre en la cabecera por lookup directo
        inicial = participantes.get(nombre, nombre)
        linea = f"{prefijo_fecha}{inicial}: {cuerpo}"

    else:
        # ── Línea de continuación (texto multilinea) ──────────────────────
        for fragmento in FRAGMENTOS_BORRAR:
            linea = linea.replace(fragmento, "")
        for patron, reemplazo in subs_cuerpo:
            linea = patron.sub(reemplazo, linea)

    # Eliminar línea si tras limpiar quedó completamente vacía
    if linea.strip() == "":
        return None

    return linea

def limpiar_chat(ruta_entrada: str, ruta_salida: str) -> dict:
    """
    Lee el archivo, aplica todas las transformaciones y escribe el resultado.
    Primera pasada: detecta participantes.
    Segunda pasada: limpia y anonimiza.
    """
    stats = {"total": 0, "eliminadas": 0, "modificadas": 0, "sin_cambios": 0}

    with open(ruta_entrada, "r", encoding="utf-8") as f:
        lineas = f.readlines()

    # ── Primera pasada: detectar participantes ────────────────────────────
    participantes = detectar_participantes(lineas)
    subs_cuerpo   = construir_subs_cuerpo(participantes)

    print(f"\n👥 PARTICIPANTES DETECTADOS ({len(participantes)}):")
    for nombre in sorted(participantes):
        print(f"   {nombre!r:35s}→  {participantes[nombre]}")

    # ── Segunda pasada: limpiar ───────────────────────────────────────────
    lineas_limpias = []
    for linea_orig in lineas:
        stats["total"] += 1
        linea_sin_nl = linea_orig.rstrip("\n")
        resultado = limpiar_linea(linea_sin_nl, participantes, subs_cuerpo)

        if resultado is None:
            stats["eliminadas"] += 1
        else:
            if resultado != linea_sin_nl:
                stats["modificadas"] += 1
            else:
                stats["sin_cambios"] += 1
            lineas_limpias.append(resultado + "\n")

    with open(ruta_salida, "w", encoding="utf-8") as f:
        f.writelines(lineas_limpias)

    return stats

# ---------------------------------------------------------------------------
# MENÚS Y SELECCIÓN DE ARCHIVOS
# ---------------------------------------------------------------------------

def seleccionar_txt() -> str:
    """Pide al usuario la ruta de un .txt o lista los disponibles."""
    print("\n📂 SELECCIÓN DE ARCHIVO")
    ruta_dir = input("   Ruta de la carpeta (Enter = directorio actual): ").strip() or os.getcwd()

    if not os.path.isdir(ruta_dir):
        sys.exit("❌ Ruta no válida o no es un directorio.")

    archivos = sorted(f for f in os.listdir(ruta_dir) if f.lower().endswith(".txt"))

    if not archivos:
        sys.exit("❌ No se encontraron archivos .txt en esa carpeta.")

    print(f"\n   Archivos .txt encontrados en: {ruta_dir}")
    for i, nombre in enumerate(archivos, 1):
        print(f"   {i:2}. {nombre}")

    opcion = input("\n   Elige un número: ").strip()
    try:
        idx = int(opcion) - 1
        if not (0 <= idx < len(archivos)):
            raise ValueError
    except ValueError:
        sys.exit("❌ Opción inválida.")

    return os.path.join(ruta_dir, archivos[idx])

def pedir_ruta_salida(ruta_entrada: str) -> str:
    """Sugiere nombre de salida y permite cambiarlo."""
    base, ext = os.path.splitext(ruta_entrada)
    sugerida = base + "_limpio" + ext
    print(f"\n💾 ARCHIVO DE SALIDA")
    print(f"   Sugerida: {os.path.basename(sugerida)}")
    nueva = input("   Nombre (Enter = usar sugerida): ").strip()
    if nueva:
        carpeta = os.path.dirname(ruta_entrada)
        if not nueva.lower().endswith(".txt"):
            nueva += ".txt"
        return os.path.join(carpeta, nueva)
    return sugerida

def confirmar_sobrescribir(ruta: str) -> bool:
    if not os.path.exists(ruta):
        return True
    resp = input(f"   ⚠️  '{os.path.basename(ruta)}' ya existe. ¿Sobrescribir? (s/N): ").strip().lower()
    return resp == "s"

# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main():
    tee = iniciar_log()
    try:
        print("\n" + "="*65)
        print(f"  CHATwas — Simplificador de chats WhatsApp  |  v{VERSION}")
        print("="*65)
        print("  Simplifica conversaciones de WhatsApp exportadas en .txt:")
        print("  detecta participantes y reduce su nombre a la inicial,")
        print("  y elimina multimedia, mensajes de sistema y borrados.")
        print("="*65)

        # 1. Selección de archivo
        ruta_entrada = seleccionar_txt()
        print(f"\n   ✅ Seleccionado: {os.path.basename(ruta_entrada)}")

        # 2. Ruta de salida
        ruta_salida = pedir_ruta_salida(ruta_entrada)
        if not confirmar_sobrescribir(ruta_salida):
            sys.exit("🛑 Operación cancelada por el usuario.")

        # 3. Procesar
        print(f"\n⚙️  Analizando...")
        stats = limpiar_chat(ruta_entrada, ruta_salida)

        # 4. Resumen
        print(f"\n{'='*65}")
        print(f"  ✅ PROCESO COMPLETADO")
        print(f"{'='*65}")
        print(f"  📄 Líneas leídas       : {stats['total']:>6}")
        print(f"  🗑️  Líneas eliminadas   : {stats['eliminadas']:>6}")
        print(f"  ✏️  Líneas modificadas  : {stats['modificadas']:>6}")
        print(f"  ➡️  Líneas sin cambios  : {stats['sin_cambios']:>6}")
        print(f"{'='*65}")
        print(f"  💾 Guardado en: {ruta_salida}")
        print(f"{'='*65}\n")

    finally:
        tee.close()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Detenido por usuario.")
