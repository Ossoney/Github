import os
import sys
import zipfile
import logging
import concurrent.futures
from pathlib import Path
import tempfile

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

try:
    from PIL import Image
    Image.MAX_IMAGE_PIXELS = 200_000_000
except ImportError:
    Image = None

try:
    import lxml
    HTML_PARSER = 'lxml'
    _LXML_AVAILABLE = True
except ImportError:
    HTML_PARSER = 'html.parser'
    _LXML_AVAILABLE = False

DEVICE_PROFILES = {
    'X3': {
        'name': 'Xteink X3',
        'max_width': 480,
        'max_height': 640,
        'suffix': '_X3'
    },
    'X4': {
        'name': 'Xteink X4',
        'max_width': 480,
        'max_height': 800,
        'suffix': '_X4'
    },
    'X4p': {
        'name': 'Xteink X4 Pro',
        'max_width': 480,
        'max_height': 800,
        'suffix': '_X4p'
    },
}

EINK_4GRAY_PALETTE = [0, 0, 0,  85, 85, 85,  170, 170, 170,  255, 255, 255] + [0] * (768 - 12)

def create_4gray_palette_image():
    if not Image:
        return None
    pal_img = Image.new('P', (1, 1))
    pal_img.putpalette(EINK_4GRAY_PALETTE)
    return pal_img

class EPUBConverterCore:
    def __init__(self, device_name='X4p', progress_callback=None):
        if device_name not in DEVICE_PROFILES:
            device_name = 'X4p'
        self.device_name = device_name
        profile = DEVICE_PROFILES[device_name]
        self.max_width = profile['max_width']
        self.max_height = profile['max_height']
        self.suffix = profile['suffix']
        self.max_html_size = 300 * 1024
        self.progress_callback = progress_callback or (lambda msg, pct: None)
        self.cover_dimensions = {}

    def _optimize_image(self, file_path, is_cover=False):
        try:
            img = Image.open(file_path)

            if img.width <= 15 or img.height <= 15:
                img.close()
                os.remove(file_path)
                return "deleted"

            # Redimensionar conservando proporción dentro de los límites del lector
            img.thumbnail((self.max_width, self.max_height), Image.Resampling.LANCZOS)
            final_w, final_h = img.size

            # Aplanar canal Alpha sobre blanco
            if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1])
                img = background

            if is_cover:
                # PORTADA: Convertir a escala de grises limpia (modo L) sin dithering destructivo en JPEG
                # para que el bookshelf del e-reader muestre la portada nítida y sin artefactos 8x8.
                img = img.convert('L')
                out_path = Path(file_path).with_suffix('.jpg')
                img.save(out_path, 'JPEG', quality=95, optimize=True)
                self.cover_dimensions[Path(file_path).name] = (final_w, final_h)
            else:
                # RESTO DE IMÁGENES: Floyd-Steinberg cuantizado a 4 grises nativos en BMP 24-bits
                img = img.convert('L')
                pal_img = create_4gray_palette_image()
                img = img.quantize(palette=pal_img, dither=Image.Dither.FLOYDSTEINBERG)
                img = img.convert('RGB')
                out_path = Path(file_path).with_suffix('.bmp')
                img.save(out_path, 'BMP')

            img.close()

            if str(Path(file_path).resolve()) != str(Path(out_path).resolve()):
                os.remove(file_path)

            return "optimized"
        except Exception as e:
            logging.warning("[IMG SKIP] %s: %s", file_path, e)
            return "skipped"

    def _purge_html_soup(self, soup, cover_files=None):
        if cover_files is None:
            cover_files = set()

        for tag in soup(["script", "style", "iframe", "base", "canvas", "video", "audio"]):
            tag.decompose()

        for tag in soup.find_all(True):
            if tag.has_attr('style'):
                del tag['style']
            if tag.has_attr('class'):
                del tag['class']

        _IMG_EXTS = {'.jpg', '.jpeg', '.png', '.webp', '.gif', '.bmp'}

        # Corregir etiquetas <img>
        for tag in soup.find_all('img'):
            src = tag.get('src', '')
            if Path(src).suffix.lower() in _IMG_EXTS:
                if Path(src).name in cover_files:
                    tag['src'] = str(Path(src).with_suffix('.jpg')).replace('\\', '/')
                else:
                    tag['src'] = str(Path(src).with_suffix('.bmp')).replace('\\', '/')

        # Corregir contenedores SVG e <image>
        for tag in soup.find_all('image'):
            for attr in ('src', 'xlink:href', 'href'):
                val = tag.get(attr, '')
                if val and Path(val).suffix.lower() in _IMG_EXTS:
                    base_name = Path(val).name
                    if base_name in cover_files:
                        tag[attr] = str(Path(val).with_suffix('.jpg')).replace('\\', '/')
                        # Si tenemos dimensiones reales de la portada, actualizar ancho/alto y viewBox
                        if base_name in self.cover_dimensions:
                            cw, ch = self.cover_dimensions[base_name]
                            tag['width'] = str(cw)
                            tag['height'] = str(ch)
                            svg_parent = tag.find_parent('svg')
                            if svg_parent:
                                if svg_parent.has_attr('viewbox'):
                                    del svg_parent['viewbox']
                                svg_parent['viewBox'] = f"0 0 {cw} {ch}"
                                svg_parent['width'] = "100%"
                                svg_parent['height'] = "100%"
                    else:
                        tag[attr] = str(Path(val).with_suffix('.bmp')).replace('\\', '/')

        return soup

    def _optimize_and_split_html(self, file_path, opf_modifier_queue, cover_files=None):
        new_files = []
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            soup = BeautifulSoup(content, HTML_PARSER)
            soup = self._purge_html_soup(soup, cover_files)

            purged_html = str(soup).encode('utf-8')
            if len(purged_html) > self.max_html_size and soup.body:
                children = list(soup.body.find_all(recursive=False))

                while len(children) == 1 and children[0].name in ['div', 'section', 'article', 'main']:
                    children[0].unwrap()
                    children = list(soup.body.find_all(recursive=False))

                mid_point = len(children) // 2

                if mid_point > 0:
                    path_obj = Path(file_path)
                    part2_name = f"{path_obj.stem}_part2{path_obj.suffix}"
                    part2_path = path_obj.with_name(part2_name)

                    head_tag = soup.find('head')
                    head_html = str(head_tag) if head_tag else '<head></head>'
                    part2_soup = BeautifulSoup(
                        f'<?xml version="1.0" encoding="utf-8"?>'
                        f'<!DOCTYPE html><html xmlns="http://www.w3.org/1999/xhtml">'
                        f'{head_html}<body></body></html>',
                        HTML_PARSER
                    )

                    for child in children[mid_point:]:
                        extracted = child.extract()
                        part2_soup.body.append(extracted)

                    with open(part2_path, 'w', encoding='utf-8') as f2:
                        f2.write(str(part2_soup))

                    opf_modifier_queue.append((path_obj.name, part2_name))
                    new_files.append(str(part2_path))

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))

        except Exception as e:
            logging.warning("[HTML SKIP] %s: %s", file_path, e)

        return new_files

    def _patch_opf_manifest(self, temp_dir, split_queue):
        if not split_queue:
            return

        for root_dir, _, files in os.walk(temp_dir):
            for file in files:
                if not file.endswith('.opf'):
                    continue

                opf_path = os.path.join(root_dir, file)
                try:
                    if _LXML_AVAILABLE:
                        import lxml.etree as etree
                        tree = etree.parse(opf_path)
                        root_el = tree.getroot()
                        opf_ns = root_el.nsmap.get(None, 'http://www.idpf.org/2007/opf')
                        ns = f'{{{opf_ns}}}' if opf_ns else ''

                        manifest = root_el.find(f'{ns}manifest')
                        spine = root_el.find(f'{ns}spine')

                        if manifest is not None and spine is not None:
                            for orig_filename, part2_filename in split_queue:
                                orig_item = None
                                for item in manifest:
                                    if Path(item.get('href', '')).name == orig_filename:
                                        orig_item = item
                                        break

                                if orig_item is not None:
                                    orig_href = orig_item.get('href', orig_filename)
                                    part2_href = str(Path(orig_href).with_name(part2_filename)).replace('\\', '/')
                                    orig_id = orig_item.get('id', 'item')
                                    part2_id = f'{orig_id}_part2'

                                    new_item = etree.Element(f'{ns}item')
                                    new_item.set('id', part2_id)
                                    new_item.set('href', part2_href)
                                    new_item.set('media-type', orig_item.get('media-type', 'application/xhtml+xml'))
                                    children = list(manifest)
                                    manifest.insert(children.index(orig_item) + 1, new_item)

                                    for itemref in list(spine):
                                        if itemref.get('idref') == orig_id:
                                            new_ref = etree.Element(f'{ns}itemref')
                                            new_ref.set('idref', part2_id)
                                            spine.insert(list(spine).index(itemref) + 1, new_ref)
                                            break

                        tree.write(opf_path, xml_declaration=True, encoding='UTF-8', pretty_print=True)
                    else:
                        with open(opf_path, 'r', encoding='utf-8') as f:
                            soup = BeautifulSoup(f.read(), 'xml')
                        manifest = soup.find('manifest')
                        spine = soup.find('spine')
                        if manifest and spine:
                            for orig_filename, part2_filename in split_queue:
                                orig_item = None
                                for item in manifest.find_all('item'):
                                    if Path(item.get('href', '')).name == orig_filename:
                                        orig_item = item
                                        break
                                if orig_item:
                                    orig_href = orig_item.get('href', orig_filename)
                                    part2_href = str(Path(orig_href).with_name(part2_filename)).replace('\\', '/')
                                    part2_id = f"{orig_item.get('id', 'item')}_part2"
                                    new_el = soup.new_tag(
                                        'item', href=part2_href, id=part2_id,
                                        **{'media-type': orig_item.get('media-type', 'application/xhtml+xml')})
                                    orig_item.insert_after(new_el)
                                    spine_item = spine.find('itemref', idref=orig_item.get('id'))
                                    if spine_item:
                                        spine_item.insert_after(soup.new_tag('itemref', idref=part2_id))
                        with open(opf_path, 'w', encoding='utf-8') as f:
                            f.write(str(soup))
                except Exception as e:
                    logging.warning('[OPF ERROR] %s: %s', opf_path, e)
                return

    def _patch_opf_images(self, temp_dir, cover_files=None):
        if cover_files is None:
            cover_files = set()

        _IMG_EXTS = {'.jpg', '.jpeg', '.png', '.webp', '.gif', '.bmp'}

        for root_dir, _, files in os.walk(temp_dir):
            for file in files:
                if not file.endswith('.opf'):
                    continue
                opf_path = os.path.join(root_dir, file)
                try:
                    if _LXML_AVAILABLE:
                        import lxml.etree as etree
                        tree = etree.parse(opf_path)
                        root_el = tree.getroot()
                        opf_ns = root_el.nsmap.get(None, 'http://www.idpf.org/2007/opf')
                        ns = f'{{{opf_ns}}}' if opf_ns else ''
                        manifest = root_el.find(f'{ns}manifest')
                        if manifest is not None:
                            for item in manifest:
                                href = item.get('href', '')
                                if Path(href).suffix.lower() in _IMG_EXTS:
                                    if Path(href).name in cover_files:
                                        item.set('href', str(Path(href).with_suffix('.jpg')).replace('\\', '/'))
                                        item.set('media-type', 'image/jpeg')
                                    else:
                                        item.set('href', str(Path(href).with_suffix('.bmp')).replace('\\', '/'))
                                        item.set('media-type', 'image/bmp')
                        tree.write(opf_path, xml_declaration=True, encoding='UTF-8', pretty_print=True)
                    else:
                        with open(opf_path, 'r', encoding='utf-8') as f:
                            soup = BeautifulSoup(f.read(), 'xml')
                        for item in soup.find_all('item'):
                            href = item.get('href', '')
                            if Path(href).suffix.lower() in _IMG_EXTS:
                                if Path(href).name in cover_files:
                                    item['href'] = str(Path(href).with_suffix('.jpg')).replace('\\', '/')
                                    item['media-type'] = 'image/jpeg'
                                else:
                                    item['href'] = str(Path(href).with_suffix('.bmp')).replace('\\', '/')
                                    item['media-type'] = 'image/bmp'
                        with open(opf_path, 'w', encoding='utf-8') as f:
                            f.write(str(soup))
                except Exception as e:
                    logging.warning('[OPF ERROR] %s: %s', opf_path, e)
                return

    def _patch_ncx(self, temp_dir, split_queue):
        if not split_queue:
            return

        ncx_path = None
        for root_dir, _, files in os.walk(temp_dir):
            for file in files:
                if file.endswith('.ncx'):
                    ncx_path = os.path.join(root_dir, file)
                    break
            if ncx_path:
                break
        if not ncx_path:
            return

        try:
            if _LXML_AVAILABLE:
                import lxml.etree as etree
                tree = etree.parse(ncx_path)
                root_el = tree.getroot()
                NCX_NS = 'http://www.daisy.org/z3986/2005/ncx/'
                ns = f'{{{NCX_NS}}}'

                for orig_filename, part2_filename in split_queue:
                    for nav_point in root_el.findall(f'.//{ns}navPoint'):
                        content_el = nav_point.find(f'{ns}content')
                        if content_el is None:
                            continue
                        src = content_el.get('src', '')
                        src_path = src.split('#')[0]
                        if Path(src_path).name != orig_filename:
                            continue

                        label_el = nav_point.find(f'{ns}navLabel/{ns}text')
                        orig_label = label_el.text if label_el is not None else orig_filename

                        new_nav = etree.Element(f'{ns}navPoint')
                        new_nav.set('id', f"{nav_point.get('id', 'navPoint')}_part2")
                        lbl = etree.SubElement(new_nav, f'{ns}navLabel')
                        txt = etree.SubElement(lbl, f'{ns}text')
                        txt.text = f'{orig_label} (cont.)'
                        cnt = etree.SubElement(new_nav, f'{ns}content')
                        cnt.set('src', str(Path(src).with_name(part2_filename)).replace('\\', '/'))

                        parent = nav_point.getparent()
                        parent.insert(list(parent).index(nav_point) + 1, new_nav)
                        break

                for i, np in enumerate(root_el.findall(f'.//{ns}navPoint'), start=1):
                    np.set('playOrder', str(i))

                tree.write(ncx_path, xml_declaration=True, encoding='UTF-8', pretty_print=True)
            else:
                with open(ncx_path, 'r', encoding='utf-8') as f:
                    soup = BeautifulSoup(f.read(), 'xml')

                for orig_filename, part2_filename in split_queue:
                    for nav_point in soup.find_all('navPoint'):
                        content_el = nav_point.find('content')
                        if not content_el:
                            continue
                        src = content_el.get('src', '')
                        src_path = src.split('#')[0]
                        if Path(src_path).name != orig_filename:
                            continue

                        label_el = nav_point.find('text')
                        orig_label = label_el.string if label_el else orig_filename

                        new_nav = soup.new_tag('navPoint', id=f"{nav_point.get('id', 'navPoint')}_part2")
                        lbl = soup.new_tag('navLabel')
                        txt = soup.new_tag('text')
                        txt.string = f'{orig_label} (cont.)'
                        lbl.append(txt)
                        new_nav.append(lbl)
                        cnt = soup.new_tag('content', src=str(Path(src).with_name(part2_filename)).replace('\\', '/'))
                        new_nav.append(cnt)
                        nav_point.insert_after(new_nav)
                        break

                for i, np in enumerate(soup.find_all('navPoint'), start=1):
                    np['playOrder'] = str(i)

                with open(ncx_path, 'w', encoding='utf-8') as f:
                    f.write(str(soup))
        except Exception as e:
            logging.warning('[NCX ERROR] %s: %s', ncx_path, e)

    def _patch_nav(self, temp_dir, split_queue):
        if not split_queue:
            return

        nav_candidates = []
        for root_dir, _, files in os.walk(temp_dir):
            for file in files:
                f_lower = file.lower()
                if f_lower in ('nav.xhtml', 'nav.html', 'toc.xhtml', 'toc.html'):
                    nav_candidates.append(os.path.join(root_dir, file))

        if not nav_candidates:
            return

        for nav_path in nav_candidates:
            try:
                with open(nav_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                if '<nav' not in content.lower():
                    continue

                soup = BeautifulSoup(content, HTML_PARSER)
                modified = False

                for orig_filename, part2_filename in split_queue:
                    for a_tag in soup.find_all('a'):
                        href = a_tag.get('href', '')
                        href_path = href.split('#')[0]
                        if Path(href_path).name == orig_filename:
                            parent_li = a_tag.find_parent('li')
                            if parent_li:
                                new_li = BeautifulSoup(str(parent_li), HTML_PARSER).find('li')
                                if new_li and new_li.find('a'):
                                    new_a = new_li.find('a')
                                    new_a['href'] = str(Path(href).with_name(part2_filename)).replace('\\', '/')
                                    new_a.string = f"{a_tag.get_text()} (cont.)"
                                    parent_li.insert_after(new_li)
                                    modified = True
                                    break

                if modified:
                    with open(nav_path, 'w', encoding='utf-8') as f:
                        f.write(str(soup))
            except Exception as e:
                logging.warning('[NAV ERROR] %s: %s', nav_path, e)

    def process_epub_file(self, input_path, output_path):
        input_file = Path(input_path)
        output_file = Path(output_path)
        opf_modifier_queue = []
        self.cover_dimensions = {}

        self.progress_callback("Extrayendo archivo EPUB...", 10)

        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temp_dir:
            with zipfile.ZipFile(input_file, 'r') as zf:
                zf.extractall(temp_dir)

            cover_files = set()
            for root_dir, _, files in os.walk(temp_dir):
                for file in files:
                    if file.endswith('.opf'):
                        with open(os.path.join(root_dir, file), 'r', encoding='utf-8') as f:
                            soup = BeautifulSoup(f.read(), 'xml')
                        meta_cover = soup.find('meta', attrs={'name': 'cover'})
                        if meta_cover:
                            cover_item = soup.find('item', id=meta_cover.get('content'))
                            if cover_item:
                                cover_files.add(Path(cover_item.get('href', '')).name)
                        for item in soup.find_all('item'):
                            if 'cover-image' in item.get('properties', ''):
                                cover_files.add(Path(item.get('href', '')).name)

            image_tasks = []
            html_tasks = []
            fonts_to_delete = []

            for root_dir, _, files in os.walk(temp_dir):
                for file in files:
                    full_path = os.path.join(root_dir, file)
                    ext = file.lower()
                    if ext.endswith(('.html', '.xhtml', '.htm')):
                        html_tasks.append(full_path)
                    elif ext.endswith(('.jpg', '.jpeg', '.png', '.webp', '.bmp', '.gif')):
                        image_tasks.append(full_path)
                    elif ext.endswith(('.ttf', '.otf', '.woff', '.woff2')):
                        fonts_to_delete.append(full_path)

            for font in fonts_to_delete:
                try:
                    os.remove(font)
                except OSError:
                    pass

            self.progress_callback(f"Optimizando {len(image_tasks)} imágenes...", 30)
            workers = min(8, os.cpu_count() or 2)

            def optimize_wrapper(path):
                is_cover = Path(path).name in cover_files
                self._optimize_image(path, is_cover)

            with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
                list(executor.map(optimize_wrapper, image_tasks))

            self._patch_opf_images(temp_dir, cover_files)

            self.progress_callback("Purgando estilos, ajustando cubierta y dividiendo capítulos > 300KB...", 65)
            html_queue = list(html_tasks)
            while html_queue:
                html_path = html_queue.pop(0)
                nuevos = self._optimize_and_split_html(html_path, opf_modifier_queue, cover_files)
                html_queue.extend(nuevos)

            self.progress_callback("Sincronizando manifiestos OPF y tablas TOC...", 85)
            self._patch_opf_manifest(temp_dir, opf_modifier_queue)
            self._patch_ncx(temp_dir, opf_modifier_queue)
            self._patch_nav(temp_dir, opf_modifier_queue)

            self.progress_callback("Reempaquetando EPUB optimizado...", 95)
            with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zf:
                mimetype_path = os.path.join(temp_dir, 'mimetype')
                if os.path.exists(mimetype_path):
                    zf.write(mimetype_path, 'mimetype', compress_type=zipfile.ZIP_STORED)

                for root, _, files in os.walk(temp_dir):
                    for file in files:
                        if file == 'mimetype' and root == temp_dir:
                            continue
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, temp_dir)
                        zf.write(file_path, arcname)

            self.progress_callback("¡Optimización finalizada con éxito!", 100)
            return output_file

    def optimize_wallpaper_file(self, input_path, output_path):
        """Optimiza una imagen individual para wallpaper en formato BMP 24b a 4 grises."""
        img = Image.open(input_path)
        img.thumbnail((self.max_width, self.max_height), Image.Resampling.LANCZOS)

        if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1])
            img = background

        img = img.convert('L')
        pal_img = create_4gray_palette_image()
        img = img.convert('RGB').quantize(palette=pal_img, dither=Image.Dither.FLOYDSTEINBERG)
        out = img.convert('RGB')
        out.save(output_path, 'BMP')
        img.close()
        return output_path
