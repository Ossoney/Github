import os
import re
import zipfile
from pathlib import Path
from collections import defaultdict
from .utils import logger, print_banner

# =========================================================
# MÓDULO DE ESTADÍSTICAS DE BIBLIOTECA
# =========================================================

class StatsModule:
    def __init__(self):
        self.lang_pattern = re.compile(r'[\[\(][a-zA-Z]{2,3}[\]\)]')
        self.name_pattern = re.compile(r".+, .+ \- .+\.epub")

    def _bytes_to_human(self, b):
        if b >= 1024**3:
            return f"{b / 1024**3:.2f} GB"
        elif b >= 1024**2:
            return f"{b / 1024**2:.2f} MB"
        elif b >= 1024:
            return f"{b / 1024:.2f} KB"
        return f"{b} B"

    def _get_epub_author(self, filename):
        """Extrae el autor del nombre del archivo si sigue el formato estándar."""
        match = re.match(r"^(.*?)\s*-\s*(.*?)\.epub$", filename, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return None

    def _check_has_metadata(self, epub_path):
        """Comprueba si un EPUB tiene metadatos DC de título y autor."""
        try:
            from ebooklib import epub
            book = epub.read_epub(str(epub_path))
            has_title = bool(book.get_metadata('DC', 'title'))
            has_author = bool(book.get_metadata('DC', 'creator'))
            return has_title and has_author
        except Exception:
            return False

    def run(self, folder_path, check_metadata_limit=50):
        """
        Genera un informe completo de la biblioteca sin modificar ningún archivo.
        check_metadata_limit: máximo de EPUBs para los que se comprueba metadatos DC
                              (operación costosa, limitar para grandes bibliotecas).
        """
        folder = Path(folder_path)
        print_banner("ESTADÍSTICAS DE BIBLIOTECA")

        # --- Recolección de datos ---
        epubs = []
        for root, dirs, files in os.walk(folder):
            # Excluir carpetas de trabajo del propio programa
            dirs[:] = [d for d in dirs if d not in
                       ('ORIGINAL', 'DOUBT', '_BORRADOS_IDIOMA', 'POSIBLES_DUPLICADOS', '_PORTADAS')]
            for filename in files:
                if filename.lower().endswith('.epub'):
                    full_path = Path(root) / filename
                    try:
                        size = full_path.stat().st_size
                    except OSError:
                        size = 0
                    epubs.append({'path': full_path, 'name': filename, 'size': size})

        total = len(epubs)
        if total == 0:
            print("No se encontraron archivos EPUB en la carpeta.")
            return

        # --- Tamaños ---
        total_size = sum(e['size'] for e in epubs)
        avg_size = total_size / total
        largest = max(epubs, key=lambda x: x['size'])
        smallest = min(epubs, key=lambda x: x['size'])

        # --- Nombres y autores ---
        authors = set()
        bad_names = 0
        lang_tagged = 0

        for e in epubs:
            if not self.name_pattern.match(e['name']):
                bad_names += 1
            if self.lang_pattern.search(e['name']):
                lang_tagged += 1
            author = self._get_epub_author(e['name'])
            if author:
                authors.add(author.lower())

        # --- Metadatos DC (muestra limitada) ---
        sample = epubs[:check_metadata_limit]
        no_metadata_count = 0
        for e in sample:
            if not self._check_has_metadata(e['path']):
                no_metadata_count += 1

        no_meta_pct = (no_metadata_count / len(sample) * 100) if sample else 0
        no_meta_estimated = int(total * (no_metadata_count / len(sample))) if sample else 0

        # --- Distribución de tamaños ---
        small = sum(1 for e in epubs if e['size'] < 1 * 1024**2)       # < 1 MB
        medium = sum(1 for e in epubs if 1 * 1024**2 <= e['size'] < 10 * 1024**2)  # 1-10 MB
        large = sum(1 for e in epubs if e['size'] >= 10 * 1024**2)      # > 10 MB

        # --- Imprimir informe ---
        w = 48
        sep = "-" * w
        print(f"{'ARCHIVOS':}")
        print(sep)
        print(f"  Total EPUBs encontrados:     {total}")
        print(f"  En subcarpetas:              {sum(1 for e in epubs if e['path'].parent != folder)}")
        print()
        print(f"{'TAMAÑO':}")
        print(sep)
        print(f"  Total:                       {self._bytes_to_human(total_size)}")
        print(f"  Promedio por libro:          {self._bytes_to_human(int(avg_size))}")
        print(f"  El más grande:               {largest['name'][:40]}")
        print(f"                               ({self._bytes_to_human(largest['size'])})")
        print(f"  El más pequeño:              {smallest['name'][:40]}")
        print(f"                               ({self._bytes_to_human(smallest['size'])})")
        print()
        print(f"  Distribución:")
        print(f"    < 1 MB  (ligeros):         {small} ({small/total*100:.1f}%)")
        print(f"    1-10 MB (normales):         {medium} ({medium/total*100:.1f}%)")
        print(f"    > 10 MB (pesados):          {large} ({large/total*100:.1f}%)")
        print()
        print(f"{'BIBLIOTECA':}")
        print(sep)
        print(f"  Autores únicos detectados:   {len(authors)}")
        print(f"  Con nombre incorrecto:        {bad_names} ({bad_names/total*100:.1f}%)")
        print(f"  Con etiqueta de idioma:       {lang_tagged} ({lang_tagged/total*100:.1f}%)")
        print()
        print(f"{'METADATOS DC (muestra de {len(sample)} libros)':}")
        print(sep)
        print(f"  Sin metadatos completos:     {no_metadata_count}/{len(sample)} ({no_meta_pct:.1f}%)")
        print(f"  Estimado total sin metadatos: ~{no_meta_estimated}")
        print()
        print(f"{'RECOMENDACIONES':}")
        print(sep)
        if bad_names > 0:
            print(f"  ⚠  {bad_names} archivos necesitan renombrado  → Opción [1]")
        if lang_tagged > 0:
            print(f"  ⚠  {lang_tagged} archivos con etiquetas de idioma → Opción [3]")
        if large > 0:
            print(f"  ⚠  {large} archivos pesados (>10 MB) → Optimizar con Opción [4]")
        if no_meta_estimated > 10:
            print(f"  ⚠  ~{no_meta_estimated} libros sin metadatos → irán a DOUBT al renombrar")
        if bad_names == 0 and lang_tagged == 0 and large == 0:
            print(f"  ✓  ¡Tu biblioteca parece estar en buen estado!")
        print(sep)

        logger.log(f"Stats: {total} EPUBs, {self._bytes_to_human(total_size)}, {bad_names} mal nombrados, {lang_tagged} con idioma")
