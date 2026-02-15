import os
import shutil
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
        except:
            return image_data, original_size

    def _minify_text(self, text_data):
        try:
            text = text_data.decode('utf-8')
            # Basic cleaning
            text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
            text = re.sub(r'\s{2,}', ' ', text)
            new_data = text.encode('utf-8')
            if len(new_data) < len(text_data):
                return new_data, len(new_data)
        except:
            pass
        return text_data, len(text_data)

    def analyze(self, folder_path, limit=20):
        """
        Escanea algunos EPUBs para ver si hay imágenes grandes que se podrían optimizar.
        Nota: Esto es costoso (abrir ZIPs). Usamos un límite bajo.
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
                        if info.file_size > 500 * 1024 and os.path.splitext(info.filename)[1].lower() in IMAGE_EXTENSIONS:
                            optimizable_candidates += 1
                            break # Con encontrar una imagen grande basta para marcarlo
            except:
                pass
        
        # Extrapolar
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

    def run(self, folder_path):
        folder = Path(folder_path)
        epubs = list(folder.glob("*.epub"))
        logger.log(f"Iniciando optimización de {len(epubs)} archivos...")
        
        temp_dir = folder / ".epub_temp"
        if temp_dir.exists(): shutil.rmtree(temp_dir)
        temp_dir.mkdir()

        total_saved = 0
        
        for i, epub_path in enumerate(epubs):
            print(f"[{i+1}/{len(epubs)}] Optimizando {epub_path.name}...", end='\r')
            try:
                original_size = epub_path.stat().st_size
                new_epub_path = epub_path.with_suffix(".opt")
                
                with zipfile.ZipFile(epub_path, 'r') as zin, zipfile.ZipFile(new_epub_path, 'w', zipfile.ZIP_DEFLATED) as zout:
                    # Copiar mimetype primero sin comprimir
                    if 'mimetype' in zin.namelist():
                        zout.writestr('mimetype', zin.read('mimetype'), compress_type=zipfile.ZIP_STORED)
                    
                    for item in zin.infolist():
                        if item.filename == 'mimetype': continue
                        
                        data = zin.read(item)
                        ext = os.path.splitext(item.filename)[1].lower()
                        
                        if ext in IMAGE_EXTENSIONS:
                            data, _ = self._optimize_image(data)
                        elif ext in TEXT_EXTENSIONS:
                            data, _ = self._minify_text(data)
                        
                        zout.writestr(item.filename, data)
                
                new_size = new_epub_path.stat().st_size
                if new_size < original_size:
                    shutil.move(str(new_epub_path), str(epub_path))
                    saved = original_size - new_size
                    total_saved += saved
                    logger.log(f"Optimized {epub_path.name}: Saved {saved/1024:.2f} KB")
                else:
                    new_epub_path.unlink() # Borrar si no mejora
                    logger.log(f"Skipped {epub_path.name}: No compression gain")
                    
            except Exception as e:
                logger.log(f"Error optimizing {epub_path.name}: {e}")
        
        if temp_dir.exists(): shutil.rmtree(temp_dir)
        print(f"\nFinalizado. Ahorro total: {total_saved / 1024 / 1024:.2f} MB")
