import re
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
# CLASE DUPE FINDER
# =========================================================

class DupeFinderModule:
    def __init__(self):
        pass

    def _get_info(self, filename):
        # Intentar extraer Autor - Titulo del nombre de archivo
        # Patrón típico: "Apellido, Nombre - Titulo.epub"
        # O "Autor - Titulo.epub"
        match = re.search(r"^(.*?)\s*-\s*(.*?)\.epub$", filename, re.IGNORECASE)
        if match:
            return match.group(1).strip(), match.group(2).strip()
        return "Unknown", filename

    def _compare_titles(self, t1, t2):
        return SequenceMatcher(None, t1.lower(), t2.lower()).ratio() >= UMBRAL_SIMILITUD

    def analyze(self, folder_path, limit=300):
        """
        Busca posibles duplicados. 
        Limitado por defecto porque O(n^2) puede ser lento en grupos grandes.
        """
        folder = Path(folder_path)
        epubs = list(folder.glob("*.epub"))
        
        # Agrupar por autor primero para reducir comparaciones
        by_author = defaultdict(list)
        checked = 0
        
        for f in epubs:
            if checked >= limit: break
            author, title = self._get_info(f.name)
            # Simplificación: Usar primera palabra del autor como clave de agrupación rápida
            key = author.split()[0].lower() if author else "unknown"
            by_author[key].append({'title': title, 'file': f})
            checked += 1
            
        possible_dupes_groups = 0
        
        for key, books in by_author.items():
            if len(books) < 2: continue
            
            # Comparación simplificada para análisis rápido
            # Si hay titulos muy similares en el mismo bucket de autor
            titles = [b['title'] for b in books]
            # Ordenar ayuda a comparaciones adyacentes
            titles.sort()
            for i in range(len(titles) - 1):
                if self._compare_titles(titles[i], titles[i+1]):
                    possible_dupes_groups += 1
                    # Contamos grupos, no archivos individuales, para no inflar
                    # Saltamos al siguiente grupo
                    break
        
        # Extrapolar
        total = len(epubs)
        if checked > 0 and checked < total:
            ratio = possible_dupes_groups / checked
            estimated = int(total * ratio)
        else:
            estimated = possible_dupes_groups

        return {
            "total_files": total,
            "needs_action": estimated,
            "description": "grupos de posibles duplicados (estimado)"
        }

    def run(self, folder_path):
        folder = Path(folder_path)
        print("Analizando biblioteca en busca de duplicados...")
        
        epubs = list(folder.glob("*.epub"))
        by_author = defaultdict(list)
        
        for f in epubs:
            author, title = self._get_info(f.name)
            # Normalizar autor para agrupación: quitar comas, minúsculas
            author_key = re.sub(r'[^\w\s]', '', author).lower()
            by_author[author_key].append({'title': title, 'author_display': author, 'file': f})
            
        dupe_groups = []
        
        for auth_key, books in by_author.items():
            if len(books) < 2: continue
            
            while books:
                current = books.pop(0)
                group = [current]
                
                i = 0
                while i < len(books):
                    candidate = books[i]
                    if self._compare_titles(current['title'], candidate['title']):
                        group.append(candidate)
                        books.pop(i)
                    else:
                        i += 1
                
                if len(group) > 1:
                    dupe_groups.append(group)

        if not dupe_groups:
            print(f"No se encontraron duplicados con similitud > {UMBRAL_SIMILITUD*100}%.")
            return

        print(f"Se encontraron {len(dupe_groups)} grupos de posibles duplicados.")
        dupes_dir = folder / CARPETA_DUPLICADOS
        dupes_dir.mkdir(exist_ok=True)

        for idx, group in enumerate(dupe_groups):
            print(f"\nGrupo {idx+1}. Autor: {group[0]['author_display']}")
            for i, item in enumerate(group):
                print(f"   {chr(65+i)}) {item['file'].name}")
            
            print("   Escribe las letras de los que quieras MOVER a la carpeta de duplicados (ej: AB).")
            sel = input("   Selección (ENTER para ignorar): ").strip().upper()
            
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
                        print(f"   -> Movido: {item['file'].name}")
                    except Exception as e:
                        print(f"   Error moviendo: {e}")
