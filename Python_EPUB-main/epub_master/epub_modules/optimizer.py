import os
import zipfile
import re
from io import BytesIO
from pathlib import Path
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
# CLASE OPTIMIZER
# =========================================================

class OptimizerModule:
    def __init__(self):
        pass

    def _optimize_image(self, image_data):
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

    def _minify_text(self, text_data):
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
                            break  # Con encontrar una imagen grande basta para marcarlo
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

        logger.log(f"Iniciando optimización de {len(epubs)} archivos...")
        
        total_saved = 0
        count_ok = 0
        count_skip = 0
        count_err = 0
        errors_list = []

        for i, epub_path in enumerate(epubs):
            print(f"[{i+1}/{len(epubs)}] {epub_path.name}...", end='\r')
            new_epub_path = None
            try:
                original_size = epub_path.stat().st_size
                new_epub_path = epub_path.with_suffix(".opt")
                
                with zipfile.ZipFile(epub_path, 'r') as zin, \
                     zipfile.ZipFile(new_epub_path, 'w', zipfile.ZIP_DEFLATED) as zout:
                    
                    # mimetype siempre primero y sin comprimir (requerimiento EPUB spec)
                    if 'mimetype' in zin.namelist():
                        zout.writestr('mimetype', zin.read('mimetype'), compress_type=zipfile.ZIP_STORED)
                    
                    for item in zin.infolist():
                        if item.filename == 'mimetype':
                            continue
                        
                        data = zin.read(item)
                        ext = os.path.splitext(item.filename)[1].lower()
                        
                        if ext in IMAGE_EXTENSIONS:
                            data, _ = self._optimize_image(data)
                        elif ext in TEXT_EXTENSIONS:
                            data, _ = self._minify_text(data)
                        
                        zout.writestr(item.filename, data)
                
                new_size = new_epub_path.stat().st_size
                if new_size < original_size:
                    new_epub_path.replace(epub_path)  # Atomic replace
                    saved = original_size - new_size
                    total_saved += saved
                    pct = saved / original_size * 100
                    logger.log(f"Optimized {epub_path.name}: -{saved/1024:.1f} KB ({pct:.1f}%)")
                    print(f"[{i+1}/{len(epubs)}] ✓ {epub_path.name} (-{saved/1024:.1f} KB, -{pct:.1f}%)")
                    count_ok += 1
                else:
                    new_epub_path.unlink()
                    logger.log(f"Skipped {epub_path.name}: no compression gain")
                    print(f"[{i+1}/{len(epubs)}] — {epub_path.name} (ya óptimo)")
                    count_skip += 1
                    
            except zipfile.BadZipFile:
                if new_epub_path and new_epub_path.exists():
                    try:
                        new_epub_path.unlink()
                    except Exception:
                        pass
                err_msg = f"{epub_path.name} (ZIP corrupto)"
                logger.log(f"Error {epub_path.name}: archivo ZIP corrupto")
                print(f"[{i+1}/{len(epubs)}] ✗ {err_msg}")
                count_err += 1
                errors_list.append(err_msg)
            except Exception as e:
                if new_epub_path and new_epub_path.exists():
                    try:
                        new_epub_path.unlink()
                    except Exception:
                        pass
                err_msg = f"{epub_path.name}: {e}"
                logger.log(f"Error optimizing {err_msg}")
                print(f"[{i+1}/{len(epubs)}] ✗ {err_msg}")
                count_err += 1
                errors_list.append(err_msg)
        
        print(f"\n{'='*50}")
        print(f"Optimizados: {count_ok}  |  Sin cambios: {count_skip}  |  Errores: {count_err}")
        print(f"Ahorro total: {total_saved / 1024 / 1024:.2f} MB")
        
        if errors_list:
            print(f"\n[!] Detalle de archivos con errores:")
            for err in errors_list:
                print(f"  - {err}")
            print(f"Consulta el archivo epubmaster.log para más información técnica.")
        print(f"{'='*50}")
