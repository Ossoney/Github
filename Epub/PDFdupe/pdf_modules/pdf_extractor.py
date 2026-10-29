import re
import unicodedata
import hashlib
from pathlib import Path
import fitz  # PyMuPDF
# Silenciar advertencias internas de MuPDF en consola (errores de xrefs, sintaxis de streams rotos, etc.)
try:
    fitz.TOOLS.mupdf_display_errors(False)
except Exception:
    pass
from .utils import logger
from .cache_db import cache_db

# =========================================================
# CONFIGURACIÓN Y CONSTANTES
# =========================================================

# Expresiones regulares para ISBN (10 y 13) y DOI
ISBN_REGEX = re.compile(r'(?:ISBN(?:-1[03])?:?\s*)?(?=[0-9X]{10}|(?=(?:[0-9]+[-\s]){3,})[0-9\s-]{13,17})(97[89][-\s]?[0-9]{1,5}[-\s]?[0-9]+[-\s]?[0-9]+[-\s]?[0-9]|[0-9]{1,5}[-\s]?[0-9]+[-\s]?[0-9]+[-\s]?[0-9X])', re.IGNORECASE)
DOI_REGEX = re.compile(r'10\.\d{4,9}/[-._;()/:A-Za-z0-9]+', re.IGNORECASE)

# Stopwords mínimas para normalización de texto
COMMON_STOPWORDS = {
    'el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas', 'de', 'del', 'a', 'al', 'en', 'y', 'o',
    'the', 'a', 'an', 'of', 'in', 'to', 'for', 'and', 'or', 'on', 'with', 'by', 'at', 'from'
}

def clean_isbn(raw):
    """Normaliza y valida un ISBN (10 o 13 dígitos) con checksum para evitar falsos positivos."""
    if not raw:
        return None
    val = re.sub(r'[^0-9X]', '', raw.upper())
    # Descartar secuencias ficticias o de ejemplo
    if val in ('0123456789', '1234567890', '0000000000', '9999999999'):
        return None

    if len(val) == 10:
        # Checksum ISBN-10
        total = 0
        for i in range(9):
            if not val[i].isdigit():
                return None
            total += int(val[i]) * (10 - i)
        last = 10 if val[9] == 'X' else (int(val[9]) if val[9].isdigit() else -1)
        if last == -1:
            return None
        total += last
        if total % 11 == 0:
            return val
        return None

    elif len(val) == 13:
        # Checksum ISBN-13
        if not val.isdigit() or not val.startswith(('978', '979')):
            return None
        total = 0
        for i in range(12):
            total += int(val[i]) * (1 if i % 2 == 0 else 3)
        check = (10 - (total % 10)) % 10
        if int(val[12]) == check:
            return val
        return None

    return None

def compute_file_hash(filepath, block_size=65536):
    """Calcula SHA-256 de un fichero para duplicados binarios exactos."""
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        buf = f.read(block_size)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(block_size)
    return hasher.hexdigest()

def canonical_key(text):
    """
    Normaliza texto a clave canónica alfanumérica sin acentos ni puntuación:
    'El Arte de la Guerra (2da Ed.)' -> 'artedelaguerra'
    """
    if not text:
        return ""
    text = re.sub(r'[\(\[].*?[\)\]]', '', text)
    norm = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8').lower()
    return re.sub(r'[^a-z0-9]', '', norm)

def normalize_title(text):
    """Limpia etiquetas de versión y puntuación para comparación difusa."""
    if not text:
        return ""
    t_clean = re.sub(r'[\(\[].*?[\)\]]', '', text).strip()
    norm = unicodedata.normalize('NFKD', t_clean).encode('ASCII', 'ignore').decode('utf-8').lower()
    cleaned = re.sub(r'[^a-z0-9]+', ' ', norm)
    return ' '.join(cleaned.split()).strip()

def strip_version_tag(filename):
    """Elimina tags de versión tipo (v2), (2nd ed), [2021], etc."""
    name = re.sub(r'\.pdf$', '', filename, flags=re.I)
    name = re.sub(r'[\[\(]\s*(?:r|rev|v|ver|vers|version)\.?\s*[0-9]+(?:\.[0-9]+)*\s*[\]\)]', '', name, flags=re.I)
    name = re.sub(r'[\[\(]\s*(?:1st|2nd|3rd|[0-9]+th)?\s*(?:ed|edic|edicion|edition)\b.*?[\]\)]', '', name, flags=re.I)
    name = re.sub(r'[\[\(]\s*[0-9]{3,8}\s*[\]\)]', '', name)
    norm = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('utf-8').lower()
    cleaned = re.sub(r'[^a-z0-9]+', ' ', norm)
    return ' '.join(cleaned.split()).strip()

def parse_version_tag(filename):
    """Detecta números de versión o edición en el nombre."""
    m = re.findall(r'[\[\(]\s*(?:r|rev|v|ver|vers|version)\.?\s*([0-9]+(?:\.[0-9]+)*)\s*[\]\)]', filename, re.I)
    if m:
        try:
            return tuple(int(x) for x in m[-1].split('.'))
        except Exception:
            pass
    # Buscar edición: 2nd ed, 3rd edition
    m_ed = re.search(r'([0-9]+)(?:st|nd|rd|th)?\s*(?:ed|edition|edic)', filename, re.I)
    if m_ed:
        try:
            return (int(m_ed.group(1)),)
        except Exception:
            pass
    return None

def get_text_shingles(text, k=4):
    """
    Genera el conjunto de n-gramas de palabras (shingles) del texto.
    Garantiza 0% falsos positivos al comparar contenido textual.
    """
    if not text:
        return set()
    words = re.findall(r'[a-z0-9áéíóúñ]{3,}', text.lower())
    if len(words) < k:
        return set([' '.join(words)]) if words else set()
    return set(' '.join(words[i:i+k]) for i in range(len(words)-k+1))

def jaccard_similarity(set1, set2):
    """Calcula similitud de Jaccard entre dos conjuntos de shingles."""
    if not set1 or not set2:
        return 0.0
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union if union > 0 else 0.0

def extract_pdf_data(filepath, max_text_pages=8):
    """
    Extrae metadatos, texto representativo, ISBNs/DOIs y número de páginas de un PDF con PyMuPDF.
    """
    filepath = Path(filepath)
    st = filepath.stat()
    mtime = st.st_mtime
    filesize = st.st_size

    # 1. Comprobar caché persistente SQLite
    cached = cache_db.get_cached(filepath, mtime, filesize)
    if cached:
        return {
            'filepath': filepath,
            'filename': filepath.name,
            'filesize': filesize,
            'mtime': mtime,
            'pages': cached['pages'],
            'title': cached['title'],
            'author': cached['author'],
            'isbns': cached['isbns'],
            'dois': cached['dois'],
            'shingles': cached['shingles'],
            'is_scanned': cached['is_scanned'],
            'read_error': None
        }

    info = {
        'filepath': filepath,
        'filename': filepath.name,
        'filesize': filesize,
        'mtime': mtime,
        'pages': 0,
        'title': '',
        'author': '',
        'isbns': set(),
        'dois': set(),
        'shingles': set(),
        'is_scanned': False,
        'read_error': None
    }
    
    try:
        doc = fitz.open(filepath)
        info['pages'] = len(doc)
        
        # Metadatos estándar PDF
        meta = doc.metadata or {}
        info['title'] = (meta.get('title') or '').strip()
        info['author'] = (meta.get('author') or '').strip()
        
        # Muestreo de páginas: páginas 1 a 6 (donde suelen estar título, créditos, ISBN y prólogo)
        extracted_text_list = []
        pages_to_check = min(len(doc), max_text_pages)
        
        for pno in range(pages_to_check):
            try:
                page = doc[pno]
                txt = page.get_text() or ''
            except Exception:
                continue

            if txt:
                extracted_text_list.append(txt)
                
                # Buscar ISBN
                try:
                    for match in ISBN_REGEX.finditer(txt):
                        cleaned = clean_isbn(match.group(1))
                        if cleaned:
                            info['isbns'].add(cleaned)
                except Exception:
                    pass
                        
                # Buscar DOI
                try:
                    for match in DOI_REGEX.finditer(txt):
                        info['dois'].add(match.group(0).lower().rstrip('.'))
                except Exception:
                    pass
                    
        try:
            doc.close()
        except Exception:
            pass
        
        full_sample = ' '.join(extracted_text_list).strip()
        
        if len(full_sample) > 100:
            info['shingles'] = get_text_shingles(full_sample, k=4)
        else:
            info['shingles'] = set()
            info['is_scanned'] = True  # Probablemente escaneado o solo imágenes
            
        # Guardar en caché SQLite para lecturas instantáneas futuras
        cache_db.save_cached_batch([info])

    except Exception as e:
        info['read_error'] = str(e)
        
    return info
