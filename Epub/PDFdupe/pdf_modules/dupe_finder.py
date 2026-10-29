import re
from pathlib import Path
from difflib import SequenceMatcher
from collections import defaultdict

from .utils import logger, ask_yes_no, format_size
from .pdf_extractor import (
    extract_pdf_data,
    compute_file_hash,
    canonical_key,
    normalize_title,
    strip_version_tag,
    parse_version_tag,
    jaccard_similarity
)

# =========================================================
# CONFIGURACIÓN
# =========================================================

UMBRAL_TITULO_DIFUSO = 0.85
UMBRAL_JACCARD_TEXTO = 0.70  # Requiere al menos 70% de 4-gramas idénticos
CARPETA_DUPLICADOS = "POSIBLES_DUPLICADOS"

class DupeFinderModule:
    def __init__(self):
        pass

    def _get_filename_author_title(self, filename):
        """Intenta separar 'Autor - Titulo.pdf'."""
        name = re.sub(r'\.pdf$', '', filename, flags=re.I)
        match = re.search(r"^(.*?)\s*-\s*(.*?)$", name)
        if match:
            return match.group(1).strip(), match.group(2).strip()
        return "Unknown", name

    def _compare_fuzzy(self, s1, s2, threshold=UMBRAL_TITULO_DIFUSO):
        """Compara títulos con filtro de longitud O(1) y SequenceMatcher."""
        len1 = len(s1)
        len2 = len(s2)
        if len1 == 0 or len2 == 0:
            return False
        max_len = max(len1, len2)
        if abs(len1 - len2) / max_len > (1.0 - threshold):
            return False
        return SequenceMatcher(None, s1, s2).ratio() >= threshold

    def _find_duplicate_groups(self, pdf_files, progress_callback=None):
        """
        Detección en embudo multinivel:
        1. Exactos por SHA-256 (mismo contenido binario)
        2. Mismo ISBN / DOI (mismo libro técnico o científico)
        3. Similitud de texto (SimHash <= MAX_HAMMING_DISTANCE)
        4. Similitud de Nombre/Título (Canónico y Difuso)
        """
        pdf_files = [Path(f) for f in pdf_files]
        total = len(pdf_files)
        data_list = []
        
        from concurrent.futures import ThreadPoolExecutor, as_completed

        # Extracción paralela de alto rendimiento (ThreadPool)
        completed = 0
        def _process_single(f):
            d = extract_pdf_data(f)
            author, title = self._get_filename_author_title(f.name)
            d['filename_author'] = author
            d['filename_title'] = title
            d['canon_filename_title'] = canonical_key(title)
            d['norm_filename_title'] = normalize_title(title)
            d['canon_meta_title'] = canonical_key(d['title'])
            return d

        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = {executor.submit(_process_single, f): f for f in pdf_files}
            for fut in as_completed(futures):
                completed += 1
                f = futures[fut]
                if progress_callback:
                    progress_callback(completed, total, f.name)
                try:
                    data_list.append(fut.result())
                except Exception as e:
                    pass

        matched_files = set()
        dupe_groups = []

        # ---------------------------------------------------------
        # FASE 1: Binario exacto (por tamaño y luego SHA-256)
        # ---------------------------------------------------------
        by_size = defaultdict(list)
        for item in data_list:
            by_size[item['filesize']].append(item)

        for size, items in by_size.items():
            if len(items) > 1 and size > 0:
                by_hash = defaultdict(list)
                for it in items:
                    h = compute_file_hash(it['filepath'])
                    by_hash[h].append(it)
                for h, g in by_hash.items():
                    if len(g) > 1:
                        dupe_groups.append({
                            'type': 'EXACT_HASH',
                            'reason': 'Contenido binario idéntico (SHA-256)',
                            'items': g
                        })
                        for it in g:
                            matched_files.add(it['filepath'])

        remaining = [d for d in data_list if d['filepath'] not in matched_files]

        # ---------------------------------------------------------
        # FASE 2: Mismo ISBN o DOI (identificadores científicos)
        # ---------------------------------------------------------
        by_isbn = defaultdict(list)
        by_doi = defaultdict(list)
        for item in remaining:
            for isbn in item['isbns']:
                by_isbn[isbn].append(item)
            for doi in item['dois']:
                by_doi[doi].append(item)

        for isbn, items in by_isbn.items():
            # Quitar elementos ya emparejados
            valid_items = [it for it in items if it['filepath'] not in matched_files]
            if len(valid_items) > 1:
                dupe_groups.append({
                    'type': 'ISBN_MATCH',
                    'reason': f'Coincidencia exacta de ISBN ({isbn})',
                    'items': valid_items
                })
                for it in valid_items:
                    matched_files.add(it['filepath'])

        remaining = [d for d in data_list if d['filepath'] not in matched_files]

        for doi, items in by_doi.items():
            valid_items = [it for it in items if it['filepath'] not in matched_files]
            if len(valid_items) > 1:
                dupe_groups.append({
                    'type': 'DOI_MATCH',
                    'reason': f'Coincidencia exacta de DOI ({doi})',
                    'items': valid_items
                })
                for it in valid_items:
                    matched_files.add(it['filepath'])

        remaining = [d for d in data_list if d['filepath'] not in matched_files]

        # ---------------------------------------------------------
        # ---------------------------------------------------------
        # FASE 3: Huella de Texto (Jaccard sobre 4-gramas de palabras)
        # ---------------------------------------------------------
        text_books = [it for it in remaining if it.get('shingles') and len(it['shingles']) >= 20]
        used_in_text = set()

        for i in range(len(text_books)):
            b1 = text_books[i]
            if b1['filepath'] in used_in_text:
                continue
            group = [b1]
            for j in range(i + 1, len(text_books)):
                b2 = text_books[j]
                if b2['filepath'] in used_in_text:
                    continue
                sim = jaccard_similarity(b1['shingles'], b2['shingles'])
                if sim >= UMBRAL_JACCARD_TEXTO:
                    group.append(b2)
                    used_in_text.add(b2['filepath'])
            
            if len(group) > 1:
                used_in_text.add(b1['filepath'])
                dupe_groups.append({
                    'type': 'TEXT_SIMILARITY',
                    'reason': f'Contenido textual idéntico o casi idéntico (Jaccard >= {int(UMBRAL_JACCARD_TEXTO * 100)}%)',
                    'items': group
                })
                for it in group:
                    matched_files.add(it['filepath'])

        remaining = [d for d in data_list if d['filepath'] not in matched_files]

        # ---------------------------------------------------------
        # FASE 4: Título Canónico y Difuso por nombre de archivo
        # ---------------------------------------------------------
        # Agrupación por clave canónica del nombre completo del libro
        by_canon_name = defaultdict(list)
        for item in remaining:
            # Clave canónica del nombre de archivo sin extensiones ni tags de version
            clean_base = strip_version_tag(item['filename'])
            k = canonical_key(clean_base)
            if k and len(k) >= 5:
                by_canon_name[k].append(item)

        unmatched_title = []
        for k, items in by_canon_name.items():
            if len(items) > 1:
                dupe_groups.append({
                    'type': 'TITLE_CANONICAL',
                    'reason': 'Mismo título normalizado (distintas versiones o revisiones)',
                    'items': items
                })
                for it in items:
                    matched_files.add(it['filepath'])
            else:
                unmatched_title.extend(items)

        remaining = [d for d in data_list if d['filepath'] not in matched_files]

        # Comparación difusa en los restantes (mismo criterio estricto)
        fuzzy_used = set()
        for i in range(len(remaining)):
            b1 = remaining[i]
            if b1['filepath'] in fuzzy_used:
                continue
            f_group = [b1]
            name1 = normalize_title(strip_version_tag(b1['filename']))
            for j in range(i + 1, len(remaining)):
                b2 = remaining[j]
                if b2['filepath'] in fuzzy_used:
                    continue
                name2 = normalize_title(strip_version_tag(b2['filename']))
                if name1 and name2 and self._compare_fuzzy(name1, name2, threshold=UMBRAL_TITULO_DIFUSO):
                    f_group.append(b2)
                    fuzzy_used.add(b2['filepath'])

            if len(f_group) > 1:
                fuzzy_used.add(b1['filepath'])
                dupe_groups.append({
                    'type': 'TITLE_FUZZY',
                    'reason': f'Nombres de archivo muy similares (>= {int(UMBRAL_TITULO_DIFUSO * 100)}%)',
                    'items': f_group
                })

        return dupe_groups

    def _get_pdf_files(self, folder, recursive=True):
        """Obtiene la lista de PDFs ignorando la carpeta interna POSIBLES_DUPLICADOS."""
        folder = Path(folder)
        pattern = "**/*.pdf" if recursive else "*.pdf"
        try:
            files = []
            for f in folder.glob(pattern):
                # Evitar incluir archivos que ya están en la carpeta de duplicados
                if CARPETA_DUPLICADOS not in f.parts:
                    files.append(f)
            return files
        except Exception:
            return [f for f in folder.glob("*.pdf") if CARPETA_DUPLICADOS not in f.parts]

    def analyze(self, folder_path, recursive=True):
        """Diagnóstico rápido instantáneo para el menú principal."""
        folder = Path(folder_path)
        pdfs = self._get_pdf_files(folder, recursive=recursive)

        total = len(pdfs)
        if not pdfs:
            return {"total_files": 0, "needs_action": 0, "description": "archivos PDF"}

        # Detección instantánea O(1) de candidatos sin abrir los PDFs
        by_canon = defaultdict(list)
        by_size = defaultdict(list)
        for f in pdfs:
            try:
                sz = f.stat().st_size
                by_size[sz].append(f)
            except Exception:
                pass
            c = canonical_key(strip_version_tag(f.name))
            if len(c) >= 4:
                by_canon[c].append(f)

        candidates = set()
        for sz, g in by_size.items():
            if len(g) > 1 and sz > 0:
                for f in g:
                    candidates.add(f)
        for c, g in by_canon.items():
            if len(g) > 1:
                for f in g:
                    candidates.add(f)

        # Si hay candidatos identificados, calculamos grupos estimados
        estimated_groups = max(len([g for g in by_canon.values() if len(g) > 1]),
                               len([g for g in by_size.values() if len(g) > 1]))

        return {
            "total_files": total,
            "needs_action": estimated_groups,
            "description": "grupos de duplicados detectados"
        }

    def _resolve_auto_winner(self, group_items):
        """
        Determina automáticamente si hay un claro ganador:
        1. Versión más alta según el nombre (v2 > v1).
        2. Mayor número de páginas o calidad si el tamaño no es corrupto.
        Retorna (winner, [losers]) o (None, None).
        """
        if len(group_items) < 2:
            return None, None

        base_names = [strip_version_tag(it['filename']) for it in group_items]
        # Si la única diferencia en los nombres es la versión
        if len(set(base_names)) == 1:
            scored = []
            for it in group_items:
                v = parse_version_tag(it['filename'])
                score = v if v is not None else (-1,)
                scored.append((score, it))
            scored.sort(key=lambda x: x[0], reverse=True)
            winner = scored[0][1]
            losers = [it for _, it in scored[1:]]
            return winner, losers

        return None, None

    def run(self, folder_path, dry_run=False, recursive=True):
        folder = Path(folder_path)
        modo_str = "recursivo (incluyendo subcarpetas)" if recursive else "carpeta actual únicamente"
        print(f"Escaneando biblioteca de PDFs en modo {modo_str}...")
        pdfs = self._get_pdf_files(folder, recursive=recursive)
        if not pdfs:
            print("No se encontraron archivos PDF en la carpeta seleccionada.")
            return

        print(f"Indexando y analizando {len(pdfs)} libros técnicos y documentos...")
        
        def show_progress(curr, total, name):
            if curr % 10 == 0 or curr == total:
                short_name = (name[:35] + '...') if len(name) > 38 else name
                print(f"[{curr}/{total}] Procesando: {short_name:<38}", end='\r')

        dupe_groups = self._find_duplicate_groups(pdfs, progress_callback=show_progress)
        print(" " * 75, end='\r') # Limpiar línea de progreso

        if not dupe_groups:
            print("¡Enhorabuena! No se encontraron duplicados en la colección.")
            return

        total_groups = len(dupe_groups)
        total_dupes = sum(len(g['items']) - 1 for g in dupe_groups)
        print(f"\nSe encontraron {total_groups} grupos con un total de ~{total_dupes} posibles duplicados.")

        dupes_dir = folder / CARPETA_DUPLICADOS
        if not dry_run:
            dupes_dir.mkdir(exist_ok=True)

        manual_groups = []
        auto_count = 0

        # Paso 1: Auto-resolución de versiones obvias o idénticos binarios
        for group in dupe_groups:
            items = group['items']
            reason = group['reason']
            
            # Si son idénticos binarios (SHA-256), conservar el primer nombre más limpio
            if group['type'] == 'EXACT_HASH':
                winner = items[0]
                losers = items[1:]
                print(f"\n[AUTO-RESOLUCIÓN] Archivo idéntico (SHA-256):")
                print(f"   Conservar: {winner['filename']}")
                for loser in losers:
                    self._move_duplicate(loser, dupes_dir, dry_run)
                    auto_count += 1
                continue

            winner, losers = self._resolve_auto_winner(items)
            if winner and losers:
                print(f"\n[AUTO-RESOLUCIÓN] Versión más reciente detectada ({reason}):")
                print(f"   Conservar: {winner['filename']}")
                for loser in losers:
                    self._move_duplicate(loser, dupes_dir, dry_run)
                    auto_count += 1
            else:
                manual_groups.append(group)

        # Paso 2: Revisión de grupos restantes
        if manual_groups:
            print(f"\nQuedan {len(manual_groups)} grupos que requieren revisión.")
            if not ask_yes_no("¿Deseas revisar los grupos ahora?", lang='es'):
                print("Operación finalizada. Los grupos no resueltos se han dejado intactos.")
                return

            for idx, g in enumerate(manual_groups, 1):
                items = g['items']
                reason = g['reason']
                print(f"\n" + "=" * 65)
                print(f"GRUPO {idx}/{len(manual_groups)} - Causa: {reason}")
                print("=" * 65)

                for opt_idx, it in enumerate(items, 1):
                    sz = format_size(it['filesize'])
                    pgs = f"{it['pages']} págs" if it['pages'] > 0 else "Sin páginas"
                    isbn_info = f" | ISBN: {list(it['isbns'])[0]}" if it['isbns'] else ""
                    print(f" [{opt_idx}] {it['filename']}")
                    print(f"     -> Tamaño: {sz} | Páginas: {pgs}{isbn_info}")

                print(" [K] Conservar TODOS (No son duplicados / no mover nada)")
                print(" [S] Salir al menú principal")

                choice = input("\nSelecciona el número del archivo que deseas CONSERVAR: ").strip().upper()
                if choice == 'S':
                    print("Saliendo de la revisión...")
                    break
                elif choice == 'K' or not choice:
                    print("Grupo omitido, no se mueve ningún archivo.")
                    continue

                try:
                    chosen_idx = int(choice) - 1
                    if 0 <= chosen_idx < len(items):
                        winner = items[chosen_idx]
                        losers = [it for i, it in enumerate(items) if i != chosen_idx]
                        for loser in losers:
                            self._move_duplicate(loser, dupes_dir, dry_run)
                    else:
                        print("Opción no válida. Grupo omitido.")
                except ValueError:
                    print("Opción no válida. Grupo omitido.")

        print(f"\nProceso completado. Duplicados reubicados en: {CARPETA_DUPLICADOS}/")

    def _move_duplicate(self, item, dupes_dir, dry_run):
        f = item['filepath']
        dest = dupes_dir / f.name
        if dest.exists():
            dest = dupes_dir / f"{f.stem}_dupe{f.suffix}"

        if dry_run:
            print(f"   [SIMULACIÓN] Se movería a '{CARPETA_DUPLICADOS}/': {f.name}")
        else:
            try:
                f.rename(dest)
                logger.log(f"Duplicado movido: {f.name} -> {CARPETA_DUPLICADOS}")
                print(f"   -> Movido a '{CARPETA_DUPLICADOS}/': {f.name}")
            except Exception as e:
                print(f"   Error moviendo {f.name}: {e}")
