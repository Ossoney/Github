import os
import zipfile
import re
import posixpath
import xml.etree.ElementTree as ET
from io import BytesIO
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
from PIL import Image, UnidentifiedImageError
from .utils import logger, ask_yes_no

# =========================================================
# CONFIGURACIÓN
# =========================================================

QUALITY_COMPRESSION = 75
MAX_IMAGE_WIDTH = 1000
IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')
TEXT_EXTENSIONS = ('.xhtml', '.html', '.htm', '.css')

# =========================================================
# FUNCIONES DE PROCESAMIENTO (A NIVEL DE MÓDULO PARA MULTIPROCESSING)
# =========================================================

def _optimize_image_data(image_data):
    original_size = len(image_data)
    try:
        img_input = BytesIO(image_data)
        img = Image.open(img_input)
        
        width, height = img.size
        if width > MAX_IMAGE_WIDTH:
            scale = MAX_IMAGE_WIDTH / width
            new_height = int(height * scale)
            img = img.resize((MAX_IMAGE_WIDTH, new_height), Image.LANCZOS)
        
        output = BytesIO()
        fmt = img.format
        if fmt in ('PNG', 'GIF'):
            if img.mode not in ('RGBA', 'P'):
                img = img.convert('RGB')
                img.save(output, format='JPEG', quality=QUALITY_COMPRESSION, optimize=True)
            else:
                img.save(output, format='PNG', optimize=True)
        else:
            img.save(output, format=fmt or 'JPEG', quality=QUALITY_COMPRESSION, optimize=True)
        
        new_data = output.getvalue()
        if len(new_data) < original_size:
            return new_data, len(new_data)
        return image_data, original_size
    except (UnidentifiedImageError, Exception):
        return image_data, original_size

def _minify_text_data(text_data):
    try:
        text = text_data.decode('utf-8')
        text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
        text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
        text = re.sub(r'\s{2,}', ' ', text)
        new_data = text.strip().encode('utf-8')
        if len(new_data) < len(text_data):
            return new_data, len(new_data)
    except Exception:
        pass
    return text_data, len(text_data)

def _is_solid_color_image(image_data):
    """
    Detecta si una imagen es lisa completamente blanca, negra o transparente.
    Retorna True si es sólida/vacía, False en caso contrario.
    """
    try:
        im = Image.open(BytesIO(image_data))
        if im.mode == 'RGBA':
            extrema = im.getextrema()
            if extrema[3] == (0, 0):  # 100% transparente
                return True
        im_rgb = im.convert('RGB')
        r, g, b = im_rgb.getextrema()
        # Negro absoluto o casi negro por artefactos de compresión
        if r[1] <= 8 and g[1] <= 8 and b[1] <= 8:
            return True
        # Blanco absoluto o casi blanco
        if r[0] >= 248 and g[0] >= 248 and b[0] >= 248:
            return True
        return False
    except Exception:
        return False

def _detect_empty_or_solid_pages(zin, opf_rel):
    """
    Identifica archivos de página XHTML/HTML vacíos o con solo una imagen sólida (blanca/negra).
    Protege siempre las páginas de portada.
    Retorna un set con los hrefs de manifiesto que deben ser eliminados.
    """
    try:
        opf_data = zin.read(opf_rel)
        root = ET.fromstring(opf_data)
    except Exception:
        return set()

    manifest_items = {}
    cover_ids = set()

    for elem in root.iter():
        if elem.tag.endswith('item') and not elem.tag.endswith('itemref'):
            item_id = elem.attrib.get('id', '')
            href = elem.attrib.get('href', '')
            media_type = elem.attrib.get('media-type', '')
            props = elem.attrib.get('properties', '')
            manifest_items[item_id] = {'href': href, 'media_type': media_type, 'id': item_id}
            if 'cover' in props.lower() or 'cover' in item_id.lower() or 'portada' in href.lower() or 'cover' in href.lower():
                cover_ids.add(item_id)
        elif elem.tag.endswith('meta'):
            if elem.attrib.get('name') == 'cover':
                cover_ids.add(elem.attrib.get('content', ''))

    opf_dir = posixpath.dirname(opf_rel)
    pages_to_remove = set()

    for item_id, item_info in manifest_items.items():
        if item_info['media_type'] not in ('application/xhtml+xml', 'text/html'):
            continue
        if item_id in cover_ids:
            continue

        raw_href = item_info['href']
        zip_path = posixpath.normpath(posixpath.join(opf_dir, raw_href)) if opf_dir else raw_href
        if zip_path not in zin.namelist():
            continue

        # Protección adicional: nombres de archivo que sugieran portada
        base_name = posixpath.basename(zip_path).lower()
        if 'cover' in base_name or 'portada' in base_name:
            continue

        try:
            content = zin.read(zip_path).decode('utf-8', errors='replace')
            body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.DOTALL | re.IGNORECASE)
            body_content = body_match.group(1) if body_match else content

            # Extraer solo texto visible
            text_only = re.sub(r'<[^>]+>', ' ', body_content)
            text_only = re.sub(r'&(?:nbsp|#160|#xa0);', ' ', text_only, flags=re.IGNORECASE)
            text_only = re.sub(r'&\w+;', ' ', text_only).strip()

            # Extraer imágenes referenciadas en el documento
            img_srcs = []
            for m in re.finditer(r'<img\b[^>]*\bsrc=[\'"]([^\'"]+)[\'"]', body_content, re.IGNORECASE):
                img_srcs.append(m.group(1))
            for m in re.finditer(r'<image\b[^>]*\b(?:xlink:href|href)=[\'"]([^\'"]+)[\'"]', body_content, re.IGNORECASE):
                img_srcs.append(m.group(1))

            # Caso 1: Página completamente vacía (sin texto visible ni imágenes)
            if not text_only and not img_srcs:
                pages_to_remove.add(raw_href)
                continue

            # Caso 2: Sin texto visible y con una única imagen que sea totalmente negra, blanca o vacía
            if not text_only and len(img_srcs) == 1:
                img_rel = img_srcs[0]
                page_dir = posixpath.dirname(zip_path)
                img_zip_path = posixpath.normpath(posixpath.join(page_dir, img_rel)) if page_dir else img_rel
                if img_zip_path in zin.namelist():
                    img_data = zin.read(img_zip_path)
                    if _is_solid_color_image(img_data):
                        pages_to_remove.add(raw_href)

        except Exception:
            continue

    return pages_to_remove

def _clean_empty_pages_references(zin, opf_rel, pages_to_remove):
    """
    Elimina las páginas identificadas del manifest y spine de OPF,
    así como de las entradas navPoint de NCX si existe.
    Retorna un diccionario {zip_filename: updated_bytes} con los archivos OPF y NCX actualizados.
    """
    updated_files = {}
    opf_dir = posixpath.dirname(opf_rel)

    # 1. Actualizar OPF
    try:
        opf_text = zin.read(opf_rel).decode('utf-8', errors='replace')
        root = ET.fromstring(opf_text.encode('utf-8'))

        # Mapear href -> item_id
        href_to_id = {}
        for elem in root.iter():
            if elem.tag.endswith('item') and not elem.tag.endswith('itemref'):
                h = elem.attrib.get('href', '')
                i = elem.attrib.get('id', '')
                if h and i:
                    href_to_id[h] = i

        removed_ids = set()
        for href in pages_to_remove:
            if href in href_to_id:
                removed_ids.add(href_to_id[href])

        # Limpiar manifest y spine en el texto OPF
        for item_id in removed_ids:
            pattern_item = re.compile(
                rf'\s*<[^:>]*:?item\b[^>]*\bid=[\x22\x27]{re.escape(item_id)}[\x22\x27][^>]*>(?:</[^:>]*:?item>)?',
                re.IGNORECASE
            )
            opf_text = pattern_item.sub('', opf_text)

            pattern_itemref = re.compile(
                rf'\s*<[^:>]*:?itemref\b[^>]*\bidref=[\x22\x27]{re.escape(item_id)}[\x22\x27][^>]*>(?:</[^:>]*:?itemref>)?',
                re.IGNORECASE
            )
            opf_text = pattern_itemref.sub('', opf_text)

        updated_files[opf_rel] = opf_text.encode('utf-8')
    except Exception:
        pass

    # 2. Actualizar NCX (Tabla de contenidos)
    ncx_name = None
    for n in zin.namelist():
        if n.lower().endswith('.ncx'):
            ncx_name = n
            break

    if ncx_name:
        try:
            ncx_data = zin.read(ncx_name)
            ncx_root = ET.fromstring(ncx_data)
            ncx_dir = posixpath.dirname(ncx_name)

            # Normalizar los hrefs a remover respecto al directorio del NCX
            target_srcs = set()
            for href in pages_to_remove:
                abs_page = posixpath.normpath(posixpath.join(opf_dir, href)) if opf_dir else href
                rel_to_ncx = posixpath.relpath(abs_page, ncx_dir) if ncx_dir else abs_page
                target_srcs.add(href)
                target_srcs.add(posixpath.basename(href))
                target_srcs.add(rel_to_ncx)

            for parent in list(ncx_root.iter()):
                to_remove = []
                for child in list(parent):
                    if child.tag.endswith('navPoint'):
                        for sub in child:
                            if sub.tag.endswith('content'):
                                src = sub.attrib.get('src', '').split('#')[0]
                                if src in target_srcs:
                                    to_remove.append(child)
                                    break
                for ch in to_remove:
                    sub_nps = [x for x in list(ch) if x.tag.endswith('navPoint')]
                    idx = list(parent).index(ch)
                    parent.remove(ch)
                    for s in reversed(sub_nps):
                        parent.insert(idx, s)

            updated_files[ncx_name] = ET.tostring(ncx_root, encoding='utf-8')
        except Exception:
            pass

    return updated_files

def _optimize_single_epub(epub_path_str):
    """
    Optimiza un archivo EPUB de forma aislada.
    Retorna tupla: (status, filename, original_size, saved_bytes, pct, pages_removed_count, err_msg)
    status: 'ok', 'skip', 'err'
    """
    epub_path = Path(epub_path_str)
    new_epub_path = epub_path.with_suffix(".opt")

    try:
        original_size = epub_path.stat().st_size
        
        with zipfile.ZipFile(epub_path, 'r') as zin:
            # 1. Localizar OPF
            opf_rel = None
            try:
                container_data = zin.read('META-INF/container.xml')
                root = ET.fromstring(container_data)
                for elem in root.iter():
                    if elem.tag.endswith('rootfile'):
                        opf_rel = elem.attrib.get('full-path')
                        if opf_rel:
                            break
            except Exception:
                pass

            if not opf_rel:
                for name in zin.namelist():
                    if name.lower().endswith('.opf'):
                        opf_rel = name
                        break

            # 2. Detectar páginas en blanco o páginas con imagen sólida
            pages_to_remove = set()
            blank_zip_paths = set()
            updated_meta_files = {}

            if opf_rel and opf_rel in zin.namelist():
                pages_to_remove = _detect_empty_or_solid_pages(zin, opf_rel)
                if pages_to_remove:
                    opf_dir = posixpath.dirname(opf_rel)
                    for href in pages_to_remove:
                        z_path = posixpath.normpath(posixpath.join(opf_dir, href)) if opf_dir else href
                        blank_zip_paths.add(z_path)
                    updated_meta_files = _clean_empty_pages_references(zin, opf_rel, pages_to_remove)

            # 3. Escribir nuevo zip optimizado
            with zipfile.ZipFile(new_epub_path, 'w', zipfile.ZIP_DEFLATED) as zout:
                # mimetype siempre primero y sin comprimir (requerimiento EPUB spec)
                if 'mimetype' in zin.namelist():
                    zout.writestr('mimetype', zin.read('mimetype'), compress_type=zipfile.ZIP_STORED)
                
                for item in zin.infolist():
                    if item.filename == 'mimetype':
                        continue
                    
                    # Omitir páginas en blanco detectadas
                    if item.filename in blank_zip_paths:
                        continue
                    
                    # Si el archivo es OPF o NCX modificado, escribir la versión actualizada
                    if item.filename in updated_meta_files:
                        zout.writestr(item.filename, updated_meta_files[item.filename])
                        continue

                    data = zin.read(item)
                    ext = os.path.splitext(item.filename)[1].lower()
                    
                    if ext in IMAGE_EXTENSIONS:
                        data, _ = _optimize_image_data(data)
                    elif ext in TEXT_EXTENSIONS:
                        data, _ = _minify_text_data(data)
                    
                    zout.writestr(item.filename, data)
        
        new_size = new_epub_path.stat().st_size
        removed_count = len(blank_zip_paths)
        if new_size < original_size or removed_count > 0:
            new_epub_path.replace(epub_path)  # Reemplazo atómico
            saved = max(0, original_size - new_size)
            pct = (saved / original_size) * 100 if original_size > 0 else 0
            return ('ok', epub_path.name, original_size, saved, pct, removed_count, None)
        else:
            if new_epub_path.exists():
                new_epub_path.unlink()
            return ('skip', epub_path.name, original_size, 0, 0.0, 0, None)
            
    except zipfile.BadZipFile:
        if new_epub_path.exists():
            try: new_epub_path.unlink()
            except Exception: pass
        return ('err', epub_path.name, 0, 0, 0.0, 0, "archivo ZIP corrupto")
    except Exception as e:
        if new_epub_path.exists():
            try: new_epub_path.unlink()
            except Exception: pass
        return ('err', epub_path.name, 0, 0, 0.0, 0, str(e))

# =========================================================
# CLASE OPTIMIZER
# =========================================================

class OptimizerModule:
    def __init__(self):
        pass

    def _optimize_image(self, image_data):
        return _optimize_image_data(image_data)

    def _minify_text(self, text_data):
        return _minify_text_data(text_data)

    def analyze(self, folder_path, limit=20):
        """
        Escanea algunos EPUBs para ver si hay imágenes grandes que se podrían optimizar.
        Nota: Costoso (abre ZIPs). Usamos un límite bajo.
        """
        folder = Path(folder_path)
        epubs = list(folder.glob("*.epub"))
        total = len(epubs)
        optimizable_candidates = 0
        
        checked = 0
        for f in epubs:
            if checked >= limit: break
            checked += 1
            try:
                with zipfile.ZipFile(f, 'r') as z:
                    for info in z.infolist():
                        if (info.file_size > 500 * 1024 and
                                os.path.splitext(info.filename)[1].lower() in IMAGE_EXTENSIONS):
                            optimizable_candidates += 1
                            break
            except Exception:
                pass
        
        if checked > 0:
            ratio = optimizable_candidates / checked
            estimated = int(total * ratio)
        else:
            estimated = 0

        return {
            "total_files": total,
            "needs_action": estimated,
            "description": "archivos pesados/optimizables (estimado)"
        }

    def run(self, folder_path, dry_run=False):
        folder = Path(folder_path)
        epubs = list(folder.glob("*.epub"))

        if not epubs:
            print("No se encontraron archivos EPUB en la carpeta.")
            return

        if dry_run:
            print(f"\n[SIMULACIÓN] Modo Dry-Run activo. No se modificará ningún archivo.\n")
            print(f"Se analizarían {len(epubs)} archivos EPUB:")
            total_potential = 0
            for i, epub_path in enumerate(epubs):
                try:
                    with zipfile.ZipFile(epub_path, 'r') as z:
                        large_imgs = [
                            info for info in z.infolist()
                            if os.path.splitext(info.filename)[1].lower() in IMAGE_EXTENSIONS
                            and info.file_size > 100 * 1024
                        ]
                        if large_imgs:
                            potential_kb = sum(i.file_size for i in large_imgs) / 1024
                            total_potential += potential_kb
                            print(f"  [{i+1}/{len(epubs)}] {epub_path.name}: {len(large_imgs)} imagen(s) grande(s) (~{potential_kb:.0f} KB)")
                        else:
                            print(f"  [{i+1}/{len(epubs)}] {epub_path.name}: ya optimizado")
                except Exception as e:
                    print(f"  [{i+1}/{len(epubs)}] {epub_path.name}: error al leer ({e})")
            print(f"\n[SIMULACIÓN] Ahorro potencial estimado: ~{total_potential/1024:.2f} MB")
            return

        workers = max(1, min(8, os.cpu_count() or 4))
        logger.log(f"Iniciando optimización de {len(epubs)} archivos con {workers} procesos en paralelo...")
        print(f"Optimizando {len(epubs)} archivos en paralelo ({workers} hilos de CPU)...")
        
        total_saved = 0
        count_ok = 0
        count_skip = 0
        count_err = 0
        errors_list = []

        total_files = len(epubs)
        completed = 0

        # Usar ProcessPoolExecutor para procesamiento intensivo de CPU (Pillow + compresión)
        try:
            with ProcessPoolExecutor(max_workers=workers) as executor:
                futures = {executor.submit(_optimize_single_epub, str(p)): p for p in epubs}
                for future in as_completed(futures):
                    completed += 1
                    status, filename, original_size, saved, pct, removed_count, err_msg = future.result()
                    
                    pages_info = f", {removed_count} pág. vacía(s) eliminada(s)" if removed_count > 0 else ""
                    if status == 'ok':
                        count_ok += 1
                        total_saved += saved
                        logger.log(f"Optimized {filename}: -{saved/1024:.1f} KB ({pct:.1f}%){pages_info}")
                        print(f"[{completed}/{total_files}] ✓ {filename} (-{saved/1024:.1f} KB, -{pct:.1f}%{pages_info})")
                    elif status == 'skip':
                        count_skip += 1
                        logger.log(f"Skipped {filename}: no compression gain")
                        print(f"[{completed}/{total_files}] — {filename} (ya óptimo)")
                    else:
                        count_err += 1
                        errors_list.append(f"{filename}: {err_msg}")
                        logger.log(f"Error optimizing {filename}: {err_msg}")
                        print(f"[{completed}/{total_files}] ✗ {filename}: {err_msg}")
        except Exception as e:
            # Fallback seguro si ProcessPoolExecutor tuviera restricciones de entorno
            logger.log(f"Aviso multiprocessing: {e}. Procesando secuencialmente...")
            for p in epubs:
                completed += 1
                status, filename, original_size, saved, pct, removed_count, err_msg = _optimize_single_epub(str(p))
                pages_info = f", {removed_count} pág. vacía(s) eliminada(s)" if removed_count > 0 else ""
                if status == 'ok':
                    count_ok += 1
                    total_saved += saved
                    print(f"[{completed}/{total_files}] ✓ {filename} (-{saved/1024:.1f} KB, -{pct:.1f}%{pages_info})")
                elif status == 'skip':
                    count_skip += 1
                    print(f"[{completed}/{total_files}] — {filename} (ya óptimo)")
                else:
                    count_err += 1
                    errors_list.append(f"{filename}: {err_msg}")
                    print(f"[{completed}/{total_files}] ✗ {filename}: {err_msg}")
        
        print(f"\n{'='*50}")
        print(f"Optimizados: {count_ok}  |  Sin cambios: {count_skip}  |  Errores: {count_err}")
        print(f"Ahorro total: {total_saved / 1024 / 1024:.2f} MB")
        
        if errors_list:
            print(f"\n[!] Detalle de archivos con errores:")
            for err in errors_list:
                print(f"  - {err}")
            print(f"Consulta el archivo epubmaster.log para más información técnica.")
        print(f"{'='*50}")
