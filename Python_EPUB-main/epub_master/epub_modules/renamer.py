import os
import re
import shutil
from pathlib import Path
from ebooklib import epub
from .utils import logger, ask_yes_no, COMMON_TEXTS

# =========================================================
# CONFIGURACIÓN
# =========================================================

CARPETA_ORIGINAL = "ORIGINAL"
CARPETA_DOUBT = "DOUBT"

# =========================================================
# CLASE RENAMER
# =========================================================

class RenamerModule:
    def __init__(self):
        pass

    def _get_metadata(self, epub_path):
        try:
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
        """Elimina caracteres inválidos para nombres de archivo y normaliza espacios."""
        # Reemplazar caracteres problemáticos por espacio en lugar de eliminarlos
        # para evitar juntar palabras (ej: Pérez-Reverte -> Pérez Reverte)
        nombre = re.sub(r'[\\/:"*?<>|_\-]+', ' ', nombre)
        # Colapsar múltiples espacios en uno solo y limpiar extremos
        return ' '.join(nombre.split()).strip()

    def _invert_name(self, name):
        """Convierte 'Nombre Apellido' en 'Apellido, Nombre', respetando si ya tiene coma."""
        if not name:
            return name
        if ',' in name:
            return name
        parts = name.split()
        if len(parts) > 1:
            return f"{parts[-1]}, {' '.join(parts[:-1])}"
        return name

    def _deduplicate_extras(self, extras_string, existing_text=""):
        """Deduplica etiquetas y evita las que ya estén en el texto base."""
        if not extras_string:
            return extras_string
            
        import unicodedata
        from difflib import SequenceMatcher
        
        # Normalizar texto existente para comparación
        norm_existing = unicodedata.normalize('NFKD', existing_text.lower()).encode('ASCII', 'ignore').decode('utf-8')
        
        tags = re.findall(r"[\[\(].*?[\]\)]", extras_string)
        unique_tags = []
        seen_normalized = []
        
        for tag in tags:
            norm = unicodedata.normalize('NFKD', tag.lower()).encode('ASCII', 'ignore').decode('utf-8')
            
            # Si la etiqueta ya está contenida en el título/autor base, la saltamos
            if norm in norm_existing or SequenceMatcher(None, norm, norm_existing).ratio() > 0.8:
                continue

            is_dupe = False
            for seen in seen_normalized:
                if norm == seen or SequenceMatcher(None, norm, seen).ratio() > 0.85:
                    is_dupe = True
                    break
            if not is_dupe:
                unique_tags.append(tag)
                seen_normalized.append(norm)
                
        return " ".join(unique_tags)

    def _extract_extras(self, original_stem):
        """
        Extrae las etiquetas extra ([v2], [Calibre], etc.) del nombre original,
        separando las que están a la izquierda y a la derecha del texto base.
        Retorna: (base_text, extras_izq, extras_der)
        """
        base = re.sub(r"[\[\(].*?[\]\)]", "", original_stem).strip()
        base_escaped = re.escape(base)

        extras_izq = ""
        left_match = re.search(r"^(.*?)" + base_escaped, original_stem)
        if left_match:
            extras_izq = " ".join(re.findall(r"[\[\(].*?[\]\)]", left_match.group(1))).strip()

        extras_der = ""
        right_match = re.search(base_escaped + r"(.*?)$", original_stem)
        if right_match:
            extras_der = " ".join(re.findall(r"[\[\(].*?[\]\)]", right_match.group(1))).strip()

        extras_izq = self._deduplicate_extras(extras_izq)
        extras_der = self._deduplicate_extras(extras_der)

        return base, extras_izq, extras_der

    def _construct_new_name(self, author, title, original_stem):
        """Construye el nombre: [extras_izq] Apellido, Nombre - Titulo [extras_der].epub"""
        if not author or not title:
            return None

        base_metadata = f"{author} {title}"
        _, extras_izq, extras_der = self._extract_extras(original_stem)
        
        # Deduplicar extras usando el contenido de los metadatos como base
        extras_izq = self._deduplicate_extras(extras_izq, base_metadata)
        extras_der = self._deduplicate_extras(extras_der, base_metadata)

        author_clean = self._clean_filename(self._invert_name(author))
        title_clean = self._clean_filename(title)

        new_name = f"{author_clean} - {title_clean}"
        if extras_izq:
            new_name = f"{extras_izq} {new_name}"
        if extras_der:
            new_name = f"{new_name} {extras_der}"

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

    def run(self, folder_path, dry_run=False):
        folder = Path(folder_path)
        original_path = folder / CARPETA_ORIGINAL
        doubt_path = folder / CARPETA_DOUBT

        if dry_run:
            print("\n[SIMULACIÓN] Modo Dry-Run activo. No se moverá ningún archivo.\n")
        else:
            original_path.mkdir(exist_ok=True)
            doubt_path.mkdir(exist_ok=True)

        epubs = list(folder.glob("*.epub"))
        if not epubs:
            logger.log("No EPUBs found.")
            print("No se encontraron archivos EPUB en la carpeta.")
            return

        logger.log(f"Iniciando renombrado de {len(epubs)} archivos...")
        print(f"Procesando {len(epubs)} archivos...")

        count_ok = 0
        count_doubt = 0
        count_err = 0

        for f in epubs:
            try:
                title, author = self._get_metadata(f)

                # Fallback: intentar extraer autor y título del propio nombre del archivo
                if not title or not author:
                    base, _, _ = self._extract_extras(f.stem)
                    if " - " in base:
                        parts = base.split(" - ", 1)
                        author = author or parts[0].strip()
                        title = title or parts[1].strip()

                new_name = self._construct_new_name(author, title, f.stem)

                if new_name:
                    if new_name == f.name:
                        # Si el nombre ya es exactamente el que debe ser, no hay que hacer nada.
                        if dry_run:
                            print(f"  [SIMULACIÓN] Ya está correcto: '{f.name}'")
                        logger.log(f"Already correct: {f.name}")
                    else:
                        dest = folder / new_name
                        if dry_run:
                            print(f"  [SIMULACIÓN] Renombrar: '{f.name}' → '{new_name}' (y guardar original en {CARPETA_ORIGINAL}/)")
                        else:
                            # 1. Copiar el original a la carpeta ORIGINAL/
                            backup_dest = original_path / f.name
                            shutil.copy2(str(f), str(backup_dest))
                            # 2. Renombrar el archivo en la carpeta principal
                            f.rename(dest)
                            logger.log(f"Renamed: {f.name} -> {new_name} (Backup in {CARPETA_ORIGINAL}/)")
                        count_ok += 1
                else:
                    dest = doubt_path / f.name
                    if dry_run:
                        print(f"  [SIMULACIÓN] Sin metadatos -> DOUBT: '{f.name}'")
                    else:
                        shutil.move(str(f), str(dest))
                        logger.log(f"Doubt (No metadata): {f.name}")
                    count_doubt += 1

            except Exception as e:
                logger.log(f"Error processing {f.name}: {e}")
                print(f"  [Error] {f.name}: {e}")
                count_err += 1
        
        if dry_run:
            print(f"\n[SIMULACIÓN] Resultado: {count_ok} se renombrarían, {count_doubt} irían a DOUBT, {count_err} errores.")
        else:
            print(f"\nFinalizado. {count_ok} renombrados en la carpeta principal (originales en '{CARPETA_ORIGINAL}/'), {count_doubt} movidos a DOUBT, {count_err} errores.")
