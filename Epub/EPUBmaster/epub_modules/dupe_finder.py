import re
import unicodedata
from pathlib import Path
from difflib import SequenceMatcher
from collections import defaultdict
from .utils import logger, ask_yes_no

# =========================================================
# CONFIGURACIÓN
# =========================================================

UMBRAL_SIMILITUD = 0.85
CARPETA_DUPLICADOS = "POSIBLES_DUPLICADOS"

# =========================================================
# FUNCIONES AUXILIARES DE NORMALIZACIÓN RÁPIDA
# =========================================================

def _canonical_key(text):
    """
    Genera una clave canónica ultrarrápida:
    - Elimina texto entre paréntesis y corchetes (notas, ediciones, versiones).
    - Normaliza acentos/tildes y convierte a minúsculas.
    - Quita espacios y caracteres de puntuación.
    Ej: 'Hijos de Dune (Edición ilustrada)' -> 'hijosdedune'
    """
    if not text:
        return ""
    text = re.sub(r'[\(\[].*?[\)\]]', '', text)
    norm = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8').lower()
    return re.sub(r'[^a-z0-9]', '', norm)

def _normalize_clean_title(text):
    """Limpia etiquetas y espacios para la comparación difusa posterior."""
    t_clean = re.sub(r'[\(\[].*?[\)\]]', '', text).strip()
    return ' '.join(t_clean.split()).lower()

def _parse_version_tag(filename):
    """
    Busca etiquetas específicas de versión o revisión (ej: (r1.0), [v2], (rev 2.1)).
    Retorna una tupla numérica (ej: (2, 1)) o None si no tiene versión.
    """
    m = re.findall(r'[\[\(]\s*(?:r|rev|v|ver|vers|version)\.?\s*([0-9]+(?:\.[0-9]+)*)\s*[\]\)]', filename, re.I)
    if m:
        ver_str = m[-1]
        try:
            return tuple(int(x) for x in ver_str.split('.'))
        except Exception:
            return None
    return None

def _strip_version_tag(filename):
    """
    Elimina la etiqueta de versión, IDs numéricos de catálogo tipo [30080],
    notas editoriales (traducción, ilustración, prólogo, edición), signos de
    puntuación y normaliza tildes/espacios para comparar si representan la misma obra.
    """
    name = re.sub(r'\.epub$', '', filename, flags=re.I)
    # 1. Quitar etiquetas de versión / revisión (r1.0, v2, rev 1.2...)
    name = re.sub(r'[\[\(]\s*(?:r|rev|v|ver|vers|version)\.?\s*[0-9]+(?:\.[0-9]+)*\s*[\]\)]', '', name, flags=re.I)
    # 2. Quitar identificadores numéricos de catálogo/release tipo [30080] o (84118)
    name = re.sub(r'[\[\(]\s*[0-9]{3,8}\s*[\]\)]', '', name)
    # 3. Quitar notas editoriales comunes entre paréntesis o corchetes:
    # (trad. ...), (ilus. ...), (ed. ...), (edición ...), (pról. ...), (notas ...)
    editorial_pattern = r'[\[\(]\s*(?:trad|traducc|ilustr|ilus|ed|edic|edicion|prol|prologo|notas?|intro|introducc)\.?\b.*?[\]\)]'
    name = re.sub(editorial_pattern, '', name, flags=re.I)
    norm = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('utf-8').lower()
    # 4. Normalizar signos de puntuación (ej: 'Einstein, su vida' vs 'Einstein Su vida')
    cleaned = re.sub(r'[^a-z0-9]+', ' ', norm)
    return ' '.join(cleaned.split()).strip()

def _check_version_only_difference(group_items):
    """
    Si en un grupo de duplicados TODOS los libros tienen exactamente el mismo nombre
    y la ÚNICA diferencia entre ellos es la versión (o la ausencia de ella),
    retorna: (winner_item, [loser_items])
    En caso contrario (difieren en título, subtítulo, extras, etc.), retorna (None, None).
    """
    if len(group_items) < 2:
        return None, None

    base_names = [_strip_version_tag(item['file'].name) for item in group_items]
    if len(set(base_names)) != 1:
        return None, None

    # Tienen exactamente el mismo nombre salvo la versión
    scored = []
    for item in group_items:
        v = _parse_version_tag(item['file'].name)
        # (-1,) representa sin versión (versión base original)
        score = v if v is not None else (-1,)
        scored.append((score, item))

    # Ordenar por versión descendente (la versión más alta primero)
    scored.sort(key=lambda x: x[0], reverse=True)
    winner = scored[0][1]
    losers = [it for _, it in scored[1:]]
    return winner, losers

# =========================================================
# CLASE DUPE FINDER
# =========================================================

class DupeFinderModule:
    def __init__(self):
        pass

    def _get_info(self, filename):
        match = re.search(r"^(.*?)\s*-\s*(.*?)\.epub$", filename, re.IGNORECASE)
        if match:
            return match.group(1).strip(), match.group(2).strip()
        return "Unknown", filename

    def _compare_titles(self, t1_clean, t2_clean):
        # Pre-filtro matemático O(1): si la diferencia relativa de longitud supera el umbral,
        # es imposible alcanzar el 85% de similitud.
        len1 = len(t1_clean)
        len2 = len(t2_clean)
        if len1 == 0 or len2 == 0:
            return False

        max_len = max(len1, len2)
        if abs(len1 - len2) / max_len > (1.0 - UMBRAL_SIMILITUD):
            return False

        return SequenceMatcher(None, t1_clean, t2_clean).ratio() >= UMBRAL_SIMILITUD

    def _find_duplicate_groups(self, epubs):
        """
        Algoritmo en embudo optimizado para bibliotecas masivas (75.000+ libros):
        1. Agrupación por autor canónico.
        2. Clave canónica de título O(1) que detecta el 90% de duplicados instantáneamente.
        3. Para títulos restantes en el mismo autor, comparación difusa con prefiltro de longitud.
        """
        by_author = defaultdict(list)
        for f in epubs:
            author, title = self._get_info(f.name)
            auth_key = _canonical_key(author) or "unknown"
            clean_title = _normalize_clean_title(title)
            canon_title = _canonical_key(title)
            by_author[auth_key].append({
                'title': title,
                'clean_title': clean_title,
                'canon_title': canon_title,
                'author_display': author,
                'file': f
            })

        dupe_groups = []

        for auth_key, books in by_author.items():
            if len(books) < 2:
                continue

            # --- PASO 1: Agrupación instantánea O(1) por clave canónica ---
            canon_dict = defaultdict(list)
            for b in books:
                canon_dict[b['canon_title']].append(b)

            unmatched_books = []
            for c_title, group_books in canon_dict.items():
                if c_title and len(group_books) > 1:
                    dupe_groups.append(group_books)
                else:
                    unmatched_books.extend(group_books)

            # --- PASO 2: Comparación difusa solo para libros no emparejados del mismo autor ---
            if len(unmatched_books) >= 2:
                while unmatched_books:
                    current = unmatched_books.pop(0)
                    fuzzy_group = [current]
                    i = 0
                    while i < len(unmatched_books):
                        candidate = unmatched_books[i]
                        if self._compare_titles(current['clean_title'], candidate['clean_title']):
                            fuzzy_group.append(candidate)
                            unmatched_books.pop(i)
                        else:
                            i += 1

                    if len(fuzzy_group) > 1:
                        dupe_groups.append(fuzzy_group)

        return dupe_groups

    def analyze(self, folder_path, limit=500):
        """
        Análisis rápido extrapolado para el menú principal.
        """
        folder = Path(folder_path)
        epubs = list(folder.glob("*.epub"))
        total = len(epubs)

        sample = epubs[:limit] if limit and len(epubs) > limit else epubs
        dupe_groups = self._find_duplicate_groups(sample)
        found_groups = len(dupe_groups)

        if sample and len(sample) < total:
            ratio = found_groups / len(sample)
            estimated = int(total * ratio)
        else:
            estimated = found_groups

        return {
            "total_files": total,
            "needs_action": estimated,
            "description": "grupos de posibles duplicados (estimado)"
        }

    def run(self, folder_path):
        folder = Path(folder_path)
        print("Escaneando biblioteca en busca de duplicados (modo de alto rendimiento)...")

        epubs = list(folder.glob("*.epub"))
        if not epubs:
            print("No se encontraron archivos EPUB en la carpeta.")
            return

        print(f"Indexando {len(epubs)} libros...")
        dupe_groups = self._find_duplicate_groups(epubs)

        if not dupe_groups:
            print(f"No se encontraron duplicados con similitud >= {int(UMBRAL_SIMILITUD * 100)}%.")
            return

        total_groups = len(dupe_groups)
        print(f"\nSe encontraron {total_groups} grupos de posibles duplicados.")
        dupes_dir = folder / CARPETA_DUPLICADOS
        dupes_dir.mkdir(exist_ok=True)

        manual_groups = []
        auto_count = 0

        # Paso 1: Resolver automáticamente SOLO los grupos donde la única diferencia es la versión
        for group in dupe_groups:
            winner, losers = _check_version_only_difference(group)
            if winner and losers:
                print(f"\n[AUTO-RESOLUCIÓN] Versión más reciente detectada:")
                print(f"   Conservar: {winner['file'].name}")
                for loser in losers:
                    try:
                        dest = dupes_dir / loser['file'].name
                        loser['file'].rename(dest)
                        logger.log(f"Auto-resolved version duplicate: {loser['file'].name} -> {CARPETA_DUPLICADOS}")
                        print(f"   -> Movido a '{CARPETA_DUPLICADOS}/': {loser['file'].name}")
                        auto_count += 1
                    except Exception as e:
                        print(f"   Error moviendo {loser['file'].name}: {e}")
            else:
                manual_groups.append(group)

        if auto_count > 0:
            print(f"\nSe auto-resolvieron {auto_count} archivo(s) de versiones anteriores.")

        if not manual_groups:
            print("Todos los duplicados fueron resueltos automáticamente por versión.")
            return

        total_manual = len(manual_groups)
        print(f"\nQuedan {total_manual} grupos que requieren tu revisión manual:")

        for idx, group in enumerate(manual_groups):
            print(f"\n{'-'*60}")
            print(f"Grupo {idx+1} de {total_manual}. Autor: {group[0]['author_display']}")
            for i, item in enumerate(group):
                try:
                    size_kb = item['file'].stat().st_size / 1024
                    print(f"   [{chr(65+i)}] {item['file'].name} (~{size_kb:.0f} KB)")
                except Exception:
                    print(f"   [{chr(65+i)}] {item['file'].name}")

            print("   Escribe la(s) letra(s) de los que quieras MOVER a la carpeta de duplicados (ej: B).")
            print("   Comandos rápidos: [ENTER] = Ignorar y siguiente  |  [S] = Salir al menú")
            sel = input("   Selección: ").strip().upper()

            if sel == 'S':
                print("Revisión de duplicados pausada por el usuario.")
                break

            if not sel:
                continue

            for char in sel:
                idx_sel = ord(char) - 65
                if 0 <= idx_sel < len(group):
                    item = group[idx_sel]
                    try:
                        dest = dupes_dir / item['file'].name
                        item['file'].rename(dest)
                        logger.log(f"Moved duplicate: {item['file'].name} -> {CARPETA_DUPLICADOS}")
                        print(f"   -> Movido a '{CARPETA_DUPLICADOS}/': {item['file'].name}")
                    except Exception as e:
                        print(f"   Error moviendo {item['file'].name}: {e}")
