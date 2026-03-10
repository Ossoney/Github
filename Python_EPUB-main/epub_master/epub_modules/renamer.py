import os
import re
import shutil
from pathlib import Path
from ebooklib import epub
from .utils import logger, ask_yes_no, COMMON_TEXTS

# =========================================================
# CONFIGURACIÓN
# =========================================================

CARPETA_DONE = "DONE"
CARPETA_DOUBT = "DOUBT"

# =========================================================
# CLASE RENAMER
# =========================================================

class RenamerModule:
    def __init__(self):
        pass

    def _get_metadata(self, epub_path):
        try:
            # Silence ebooklib warnings if possible or catch them
            book = epub.read_epub(str(epub_path))
            title = ""
            author = ""
            if book.get_metadata('DC', 'title'):
                title = book.get_metadata('DC', 'title')[0][0]
            if book.get_metadata('DC', 'creator'):
                author = book.get_metadata('DC', 'creator')[0][0]
            return title.strip(), author.strip()
        except Exception:
            return None, None

    def _clean_filename(self, nombre):
        return re.sub(r'[\\/:"*?<>|_\-]+', '', nombre)

    def _invert_name(self, name):
        parts = name.split()
        if len(parts) > 1:
            return f"{parts[-1]}, {' '.join(parts[:-1])}"
        return name

    def _construct_new_name(self, author, title, original_stem):
        """Construye el nombre: Apellido, Nombre - Titulo.epub"""
        # Intentar preservar extras (paréntesis/corchetes) del nombre original
        # Lógica simplificada vs original para robustez
        extras_izq = ""
        extras_der = ""
        
        # Simple extraction of brackets
        matches = re.findall(r"(\[.*?\]|\(.*?\))", original_stem)
        if matches:
            # Heurística: si está al principio, es extra izq, si al final, extra der.
            # Por simplicidad, los ponemos al final si no estamos seguros, o intentamos reconstruir.
            # Para esta versión unificada, usaremos una lógica limpia:
            pass 

        if not author or not title:
            return None

        author_clean = self._clean_filename(self._invert_name(author))
        title_clean = self._clean_filename(title)
        
        # Re-check si el original ya tenía extras que queremos conservar
        # El script original tenía lógica compleja regex. La simplificamos para mantenimiento
        # o la copiamos si es crítica. Copiaremos la lógica básica de regex del original.
        base = re.sub(r"[\[\(].*?[\]\)]", "", original_stem).strip()
        base_escaped = re.escape(base)
        
        left_match = re.search(r"^(.*?)" + base_escaped, original_stem)
        if left_match:
            extras_izq = " ".join(re.findall(r"[\[\(].*?[\]\)]", left_match.group(1))).strip()
            
        right_match = re.search(base_escaped + r"(.*?)$", original_stem)
        if right_match:
            extras_der = " ".join(re.findall(r"[\[\(].*?[\]\)]", right_match.group(1))).strip()

        new_name = f"{author_clean} - {title_clean}"
        if extras_izq: new_name = f"{extras_izq} {new_name}"
        if extras_der: new_name = f"{new_name} {extras_der}"
        
        return new_name + ".epub"

    def analyze(self, folder_path, limit=100):
        """
        Analiza la carpeta y cuenta cuántos archivos necesitan renombrado.
        Retorna: dict con estadísticas
        """
        folder = Path(folder_path)
        epubs = list(folder.glob("*.epub"))
        total = len(epubs)
        needs_rename = 0
        
        # Patrón esperado: "Apellido, Nombre - Titulo.epub"
        # Es difícil validar estrictamente sin falsos positivos, pero buscaremos el guión " - "
        pattern = re.compile(r".+, .+ \- .+\.epub")
        
        checked = 0
        for f in epubs:
            if checked >= limit: break
            if not pattern.match(f.name):
                needs_rename += 1
            checked += 1
            
        # Extrapolar si hay más del límite
        if checked < total and checked > 0:
            ratio = needs_rename / checked
            estimated_needs_rename = int(total * ratio)
        else:
            estimated_needs_rename = needs_rename

        return {
            "total_files": total,
            "needs_action": estimated_needs_rename,
            "description": "archivos con nombre incorrecto (estimado)"
        }

    def run(self, folder_path):
        folder = Path(folder_path)
        done_path = folder / CARPETA_DONE
        doubt_path = folder / CARPETA_DOUBT
        
        done_path.mkdir(exist_ok=True)
        doubt_path.mkdir(exist_ok=True)
        
        epubs = list(folder.glob("*.epub"))
        if not epubs:
            logger.log("No EPUBs found.")
            return

        logger.log(f"Iniciando renombrado de {len(epubs)} archivos...")
        print(f"Procesando {len(epubs)} archivos...")

        count_ok = 0
        count_doubt = 0

        for f in epubs:
            try:
                title, author = self._get_metadata(f)
                new_name = self._construct_new_name(author, title, f.stem)
                
                if new_name:
                    dest = done_path / new_name
                    shutil.copy2(f, dest)
                    logger.log(f"Renamed: {f.name} -> {new_name}")
                    count_ok += 1
                else:
                    dest = doubt_path / f.name
                    shutil.copy2(f, dest)
                    logger.log(f"Doubt (No metadata): {f.name}")
                    count_doubt += 1
            except Exception as e:
                logger.log(f"Error processing {f.name}: {e}")
        
        print(f"Finalizado. {count_ok} renombrados, {count_doubt} movidos a DOUBT.")

