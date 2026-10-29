import os
import re
import shutil
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from .utils import logger, ask_yes_no, COMMON_TEXTS, get_epub_metadata_fast, update_epub_author_metadata

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
        # 1. Extracción ultrarrápida (ZIP + OPF directo)
        title, author = get_epub_metadata_fast(epub_path)
        if title or author:
            return (title or "").strip(), (author or "").strip()

        # 2. Fallback a ebooklib si el parser directo no extrajo nada
        try:
            from ebooklib import epub
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

    def _is_various_authors(self, name):
        """Detecta si el autor representa una obra colectiva / varios autores."""
        if not name:
            return False
        import unicodedata
        norm = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('utf-8').lower()
        norm = re.sub(r'[^a-z0-9]', '', norm)
        patterns = {
            'vvaa', 'varios', 'variosautores', 'autoresvarios',
            'variosautoresas', 'autoresasvarios', 'various', 'variousauthors',
            'colectivo', 'autorcolectivo', 'grupo', 'antologia'
        }
        return norm in patterns

    def _invert_name(self, name):
        """Convierte 'Nombre Apellido' en 'Apellido, Nombre', respetando si ya tiene coma o si es VV.AA."""
        if not name:
            return name
        if self._is_various_authors(name):
            return "VV.AA."
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

        # Función auxiliar para resolver metadatos y nuevo nombre de cada archivo
        def _process_one(f):
            try:
                title, author = self._get_metadata(f)

                # Fallback: intentar extraer autor y título del propio nombre del archivo
                name_author = ""
                name_title = ""
                base, _, _ = self._extract_extras(f.stem)
                if " - " in base:
                    parts = base.split(" - ", 1)
                    name_author = parts[0].strip()
                    name_title = parts[1].strip()

                if not title or not author:
                    author = author or name_author
                    title = title or name_title

                is_various = (
                    self._is_various_authors(author) or
                    self._is_various_authors(name_author) or
                    self._is_various_authors(f.stem)
                )

                if is_various:
                    author = "VV.AA."
                    if not title:
                        title = name_title or base

                new_name = self._construct_new_name(author, title, f.stem)
                return (f, new_name, is_various, None)
            except Exception as e:
                return (f, None, False, e)

        # Paralelizar extracción de metadatos con ThreadPoolExecutor
        workers = min(16, (os.cpu_count() or 4) * 2)
        with ThreadPoolExecutor(max_workers=workers) as executor:
            items = list(executor.map(_process_one, epubs))

        count_ok = 0
        count_doubt = 0
        count_err = 0
        count_vvaa_meta = 0

        for f, new_name, is_various, err in items:
            if err:
                logger.log(f"Error processing {f.name}: {err}")
                print(f"  [Error] {f.name}: {err}")
                count_err += 1
                continue

            try:
                if new_name:
                    dest = folder / new_name
                    target_file = f

                    if new_name == f.name:
                        if is_various:
                            if dry_run:
                                print(f"  [SIMULACIÓN] Nombre ya correcto ('{f.name}'). Se actualizarían metadatos OPF a 'VV.AA.'")
                            else:
                                if update_epub_author_metadata(f, "VV.AA."):
                                    count_vvaa_meta += 1
                                    logger.log(f"[VV.AA.] Metadatos OPF actualizados a 'VV.AA.' en {f.name}")
                        else:
                            if dry_run:
                                print(f"  [SIMULACIÓN] Ya está correcto: '{f.name}'")
                            logger.log(f"Already correct: {f.name}")
                    else:
                        if dry_run:
                            vvaa_note = " y actualizar metadatos OPF a 'VV.AA.'" if is_various else ""
                            print(f"  [SIMULACIÓN] Renombrar: '{f.name}' → '{new_name}' (y guardar original en {CARPETA_ORIGINAL}/){vvaa_note}")
                        else:
                            # 1. Copiar el original a la carpeta ORIGINAL/
                            backup_dest = original_path / f.name
                            shutil.copy2(str(f), str(backup_dest))
                            # 2. Renombrar el archivo en la carpeta principal
                            f.rename(dest)
                            target_file = dest
                            logger.log(f"Renamed: {f.name} -> {new_name} (Backup in {CARPETA_ORIGINAL}/)")

                            # 3. Si es de varios autores, actualizar también su OPF interno
                            if is_various:
                                if update_epub_author_metadata(target_file, "VV.AA."):
                                    count_vvaa_meta += 1
                                    logger.log(f"[VV.AA.] Metadatos OPF actualizados a 'VV.AA.' en {target_file.name}")
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
        
        vvaa_msg = f", {count_vvaa_meta} libros actualizados con metadatos 'VV.AA.'" if count_vvaa_meta > 0 else ""
        if dry_run:
            print(f"\n[SIMULACIÓN] Resultado: {count_ok} se renombrarían, {count_doubt} irían a DOUBT, {count_err} errores.")
        else:
            print(f"\nFinalizado. {count_ok} renombrados en la carpeta principal (originales en '{CARPETA_ORIGINAL}/'){vvaa_msg}, {count_doubt} movidos a DOUBT, {count_err} errores.")

    def run_various_authors(self, folder_path, dry_run=False):
        """
        Opción específica para detectar libros de varios autores (en nombre o metadatos),
        estandarizar su nombre a 'VV.AA. - Título.epub' y actualizar sus metadatos internos (content.opf) a 'VV.AA.'.
        """
        folder = Path(folder_path)
        original_path = folder / CARPETA_ORIGINAL

        if dry_run:
            print("\n[SIMULACIÓN] Modo Dry-Run activo. No se modificará ningún archivo.\n")
        else:
            original_path.mkdir(exist_ok=True)

        epubs = list(folder.glob("*.epub"))
        if not epubs:
            logger.log("No EPUBs found.")
            print("No se encontraron archivos EPUB en la carpeta.")
            return

        print(f"Escaneando {len(epubs)} archivos buscando libros de varios autores...")

        def _check_various(f):
            try:
                title, author = self._get_metadata(f)

                # Fallback desde nombre de archivo
                name_author = ""
                name_title = ""
                base, _, _ = self._extract_extras(f.stem)
                if " - " in base:
                    parts = base.split(" - ", 1)
                    name_author = parts[0].strip()
                    name_title = parts[1].strip()

                is_various = (
                    self._is_various_authors(author) or
                    self._is_various_authors(name_author) or
                    self._is_various_authors(f.stem)
                )

                if not is_various:
                    return None

                # Resolver título
                final_title = title or name_title or base
                # Construir nuevo nombre garantizando autor 'VV.AA.'
                new_name = self._construct_new_name("VV.AA.", final_title, f.stem)
                return (f, new_name, author)
            except Exception as e:
                return (f, None, e)

        workers = min(16, (os.cpu_count() or 4) * 2)
        with ThreadPoolExecutor(max_workers=workers) as executor:
            results = list(executor.map(_check_various, epubs))

        candidates = [r for r in results if r is not None]

        if not candidates:
            print("No se encontraron libros de varios autores que requieran procesamiento.")
            return

        print(f"\nDetectados {len(candidates)} libros de autoría colectiva / varios autores.")
        count_renamed = 0
        count_meta_updated = 0
        count_already_ok = 0
        count_err = 0

        for item in candidates:
            f, new_name, current_author = item
            if isinstance(current_author, Exception):
                logger.log(f"Error analizando {f.name}: {current_author}")
                count_err += 1
                continue

            try:
                dest = folder / new_name if new_name else f
                target_file = f

                if dry_run:
                    if new_name and new_name != f.name:
                        print(f"  [SIMULACIÓN] Renombrar: '{f.name}' → '{new_name}' y actualizar metadatos OPF a 'VV.AA.'")
                        count_renamed += 1
                    else:
                        print(f"  [SIMULACIÓN] Nombre ya correcto ('{f.name}'). Se actualizarían metadatos OPF a 'VV.AA.'")
                        count_already_ok += 1
                    continue

                # 1. Copia de respaldo si el nombre va a cambiar o si se van a tocar metadatos
                backup_dest = original_path / f.name
                if not backup_dest.exists():
                    shutil.copy2(str(f), str(backup_dest))

                # 2. Renombrar archivo si es necesario
                if new_name and new_name != f.name:
                    f.rename(dest)
                    target_file = dest
                    count_renamed += 1
                    logger.log(f"[VV.AA.] Renombrado: {f.name} -> {new_name}")
                else:
                    count_already_ok += 1

                # 3. Actualizar metadatos internos del EPUB a 'VV.AA.'
                meta_ok = update_epub_author_metadata(target_file, "VV.AA.")
                if meta_ok:
                    count_meta_updated += 1
                    logger.log(f"[VV.AA.] Metadatos OPF actualizados a 'VV.AA.' en {target_file.name}")
                else:
                    logger.log(f"[VV.AA.] Aviso: no se pudieron actualizar metadatos OPF en {target_file.name}")

            except Exception as e:
                logger.log(f"Error procesando {f.name}: {e}")
                print(f"  [Error] {f.name}: {e}")
                count_err += 1

        if dry_run:
            print(f"\n[SIMULACIÓN] Resultado: {count_renamed} se renombrarían, {count_already_ok} ya tenían nombre correcto, {count_err} errores.")
        else:
            print(f"\nFinalizado: {count_renamed} renombrados a 'VV.AA.', {count_meta_updated} libros actualizados internamente en su OPF.")
            if count_err > 0:
                print(f"Errores encontrados: {count_err}.")
