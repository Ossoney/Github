import os
from pathlib import Path
from collections import defaultdict
from .utils import logger, ask_yes_no, COMMON_TEXTS

# =========================================================
# CONFIGURACIÓN
# =========================================================

LANGUAGE_TAGS = {"[CA]", "[EO]", "[EN]", "[GAL]", "[FR]", "[IT]", "[DE]"}

# =========================================================
# CLASE LANG CLEANER
# =========================================================

class LangCleanerModule:
    def __init__(self):
        pass

    def _find_tagged_files(self, folder_path):
        folder = Path(folder_path)
        results = defaultdict(list)
        total_scanned = 0
        
        # Recorrer recursivamente
        for root, _, files in os.walk(folder):
            for filename in files:
                if filename.lower().endswith('.epub'):
                    total_scanned += 1
                    for tag in LANGUAGE_TAGS:
                        if tag in filename:
                            full_path = Path(root) / filename
                            results[tag].append(full_path)
                            break
        return total_scanned, results

    def analyze(self, folder_path, limit=None):
        """
        Analiza la biblioteca en busca de idiomas no deseados.
        """
        # scan_limit no aplica bien aquí porque necesitamos ver si EXISTEN, 
        # pero para "dashboard" podríamos hacer un os.walk parcial o limitado.
        # Dado que os.walk es rápido en metadatos, lo haremos completo pero sin leer contenido.
        
        folder = Path(folder_path)
        found_count = 0
        scanned = 0
        
        # Simple limit implementation for performance on massive libraries
        for root, _, files in os.walk(folder):
            for filename in files:
                if filename.lower().endswith('.epub'):
                    scanned += 1
                    for tag in LANGUAGE_TAGS:
                        if tag in filename:
                            found_count += 1
                            break
            if limit and scanned >= limit:
                break
                
        # Extrapolate if limited
        if limit and scanned >= limit and scanned > 0:
            ratio = found_count / scanned
            # Just report "detected X in first N files" conceptually, or extrapolate
            # For dashboard simplicity, let's just return what we found or a projection
            estimated = int((found_count / scanned) * scanned * (10 if scanned < 1000 else 1)) # Rough heuristic
            description = f"archivos en otros idiomas (revisados {scanned})"
        else:
            estimated = found_count
            description = "archivos en otros idiomas"

        return {
            "total_files": scanned,
            "needs_action": estimated,
            "description": description
        }

    def run(self, folder_path):
        folder = Path(folder_path)
        print(f"Escaneando carpeta: {folder} ...")
        total, results = self._find_tagged_files(folder)

        if not results:
            print("No se encontraron archivos con etiquetas de idioma extranjeras.")
            return

        print(f"--- ETIQUETAS ENCONTRADAS ({total} escaneados) ---")
        for tag, files in sorted(results.items()):
            print(f"[{tag}] -> {len(files)} archivos")
        
        while True:
            tag_input = input("\nIntroduce la etiqueta a borrar (ej: [EN]) o ENTER para cancelar: ").strip().upper()
            if not tag_input:
                break
            
            # Auto-add brackets if missing
            if not tag_input.startswith("["): tag_input = "[" + tag_input
            if not tag_input.endswith("]"): tag_input = tag_input + "]"
            
            if tag_input in results:
                files_to_delete = results[tag_input]
                print(f"Vas a borrar {len(files_to_delete)} archivos con etiqueta {tag_input}.")
                if ask_yes_no("¿Estás seguro?"):
                    count = 0
                    for f in files_to_delete:
                        try:
                            f.unlink()
                            count += 1
                            logger.log(f"Deleted: {f.name}")
                        except Exception as e:
                            logger.log(f"Error deleting {f.name}: {e}")
                    print(f"Eliminados {count} archivos.")
                    # Remove from results to prevent double deletion attempt
                    del results[tag_input]
                else:
                    print("Operación cancelada para esta etiqueta.")
            else:
                print("Etiqueta no encontrada en los resultados.")
            
            if not results:
                print("No quedan más etiquetas detectadas.")
                break

