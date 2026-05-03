import os
import re
import shutil
from pathlib import Path
from collections import defaultdict
from .utils import logger, ask_yes_no, COMMON_TEXTS

# =========================================================
# CONFIGURACIÓN
# =========================================================

CARPETA_BORRADOS = "_BORRADOS_IDIOMA"

# =========================================================
# CLASE LANG CLEANER
# =========================================================

class LangCleanerModule:
    def __init__(self):
        # Expresión regular que captura texto de 2-3 letras entre [] o ()
        self.lang_pattern = re.compile(r'[\[\(]([a-zA-Z]{2,3})[\]\)]')
        
        # Lista blanca de códigos de idioma comunes (ISO 639-1 y 639-2)
        # Se excluyen palabras que coinciden con español común (como NO, SIN, SE) 
        # a menos que sea muy probable que sean idiomas.
        self.valid_langs = {
            'EN', 'ENG', 'FR', 'FRA', 'IT', 'ITA', 'PT', 'POR', 'DE', 'GER', 'DEU',
            'RU', 'RUS', 'GL', 'GLG', 'EU', 'EUS', 'CA', 'CAT', 'ZH', 'CHI', 'JA', 'JPN',
            'KO', 'KOR', 'PL', 'POL', 'NL', 'NLD', 'SV', 'SWE', 'DA', 'DAN', 'FI', 'FIN', 
            'TR', 'TUR', 'AR', 'ARA', 'HE', 'HEB', 'EL', 'ELL'
        }
        # Nota: 'NO' (Noruego) se omite por ser demasiado común como palabra en español

    def _is_valid_tag(self, tag_content):
        """Verifica si el contenido de la etiqueta parece un idioma válido."""
        content = tag_content.upper()
        
        # Excluir números romanos comunes (II, III, IV, VI, IX, etc.)
        if re.match(r'^(II|III|IV|VI|VII|VIII|IX|X|XI|XII)$', content):
            return False
            
        return content in self.valid_langs

    def _find_tagged_files(self, folder_path):
        folder = Path(folder_path)
        results = defaultdict(list)
        total_scanned = 0
        
        for root, dirs, files in os.walk(folder):
            dirs[:] = [d for d in dirs if d not in
                       ('DONE', 'DOUBT', '_BORRADOS_IDIOMA', 'POSIBLES_DUPLICADOS', '_PORTADAS')]
            for filename in files:
                if filename.lower().endswith('.epub'):
                    total_scanned += 1
                    matches = self.lang_pattern.finditer(filename)
                    for match in matches:
                        tag_full = match.group(0)
                        tag_content = match.group(1)
                        
                        if self._is_valid_tag(tag_content):
                            full_path = Path(root) / filename
                            results[tag_full.upper()].append(full_path)
        return total_scanned, results

    def analyze(self, folder_path, limit=None):
        """
        Analiza la biblioteca en busca de idiomas no deseados.
        """
        folder = Path(folder_path)
        found_count = 0
        scanned = 0
        
        for root, dirs, files in os.walk(folder):
            # Excluir carpetas de trabajo del propio programa
            dirs[:] = [d for d in dirs if d not in
                       ('DONE', 'DOUBT', '_BORRADOS_IDIOMA', 'POSIBLES_DUPLICADOS', '_PORTADAS')]
            for filename in files:
                if filename.lower().endswith('.epub'):
                    scanned += 1
                    matches = self.lang_pattern.finditer(filename)
                    if any(self._is_valid_tag(m.group(1)) for m in matches):
                        found_count += 1
            if limit and scanned >= limit:
                break
                
        # Extrapolate if limited
        if limit and scanned >= limit and scanned > 0:
            estimated = found_count  # Mostrar valor real revisado, no inflado
            description = f"archivos en otros idiomas (revisados {scanned})"
        else:
            estimated = found_count
            description = "archivos en otros idiomas"

        return {
            "total_files": scanned,
            "needs_action": estimated,
            "description": description
        }

    def run(self, folder_path, dry_run=False):
        folder = Path(folder_path)
        
        if dry_run:
            print("\n[SIMULACIÓN] Modo Dry-Run activo. No se moverá ningún archivo.\n")

        print(f"Escaneando carpeta: {folder} ...")
        total, results = self._find_tagged_files(folder)

        if not results:
            print("No se encontraron archivos con etiquetas de idioma extranjeras.")
            return

        print(f"--- ETIQUETAS ENCONTRADAS ({total} escaneados) ---")
        for tag, files in sorted(results.items()):
            print(f"  {tag} -> {len(files)} archivos")
        
        # Carpeta de seguridad donde se mueven (no se borran)
        borrados_path = folder / CARPETA_BORRADOS

        while True:
            raw_input = input("\nIntroduce la(s) etiqueta(s) a mover (ej: [EN], (GL) o EN, FR) o ENTER para cancelar: ").strip().upper()
            if not raw_input:
                break
            
            # Procesar múltiples etiquetas separadas por comas
            target_tags = [t.strip() for t in raw_input.split(',')]
            
            for tag_input in target_tags:
                if not tag_input: continue

                # Auto-add brackets if missing (ej, si escribe EN o GAL)
                if len(tag_input) in [2, 3] and tag_input.isalpha():
                    tag_input = f"[{tag_input}]"
                
                if tag_input in results:
                    files_to_move = results[tag_input]
                    
                    if dry_run:
                        print(f"\n[SIMULACIÓN] Se moverían {len(files_to_move)} archivos con etiqueta {tag_input}")
                        del results[tag_input]
                    else:
                        print(f"\nVas a mover {len(files_to_move)} archivos con etiqueta {tag_input}")
                        if ask_yes_no(f"¿Confirmar movimiento de {tag_input}?"):
                            borrados_path.mkdir(exist_ok=True)
                            count = 0
                            for f in files_to_move:
                                try:
                                    dest = borrados_path / f.name
                                    shutil.move(str(f), str(dest))
                                    count += 1
                                    logger.log(f"Moved [{tag_input}]: {f.name} -> {CARPETA_BORRADOS}/")
                                except Exception as e:
                                    logger.log(f"Error moving {f.name}: {e}")
                                    print(f"  [Error] {f.name}: {e}")
                            print(f"Movidos {count} archivos de {tag_input} a '{CARPETA_BORRADOS}/'.")
                            del results[tag_input]
                        else:
                            print(f"Operación cancelada para {tag_input}.")
                else:
                    print(f"Etiqueta {tag_input} no encontrada.")

            # Mostrar totalizador de lo que queda
            if results:
                print("\n--- ETIQUETAS RESTANTES ---")
                for tag, files in sorted(results.items()):
                    print(f"  {tag} -> {len(files)} archivos")
            else:
                print("\nNo quedan más etiquetas detectadas.")
                break

        if not dry_run and borrados_path.exists():
            total_moved = len(list(borrados_path.glob("*.epub")))
            print(f"\n[INFO] La carpeta '{CARPETA_BORRADOS}/' contiene {total_moved} archivo(s).")
            print(f"[INFO] Revísalos y bórralos manualmente cuando estés seguro.")
