import os
import zipfile
import fitz
from pathlib import Path
from PIL import Image

def run_all_tests():
    test_dir = Path("test_files")
    test_dir.mkdir(exist_ok=True)

    # 1. Crear imagen individual, doble página, página blanca y página negra
    tiny_img = Image.new("RGB", (200, 300), color=(100, 150, 200))
    double_img = Image.new("RGB", (600, 300), color=(200, 100, 50)) # Ratio 2:1 -> doble página
    white_img = Image.new("RGB", (200, 300), color=(255, 255, 255)) # En blanco
    black_img = Image.new("RGB", (200, 300), color=(0, 0, 0)) # En negro

    tiny_path = test_dir / "p1.jpg"
    double_path = test_dir / "p2_double.jpg"
    white_path = test_dir / "p3_white.jpg"
    black_path = test_dir / "p4_black.jpg"
    tiny_img.save(tiny_path, "JPEG")
    double_img.save(double_path, "JPEG")
    white_img.save(white_path, "JPEG")
    black_img.save(black_path, "JPEG")

    # 2. Crear cómic CBZ de prueba
    cbz_path = test_dir / "test_comic.cbz"
    with zipfile.ZipFile(cbz_path, 'w') as zf:
        zf.write(tiny_path, "page_01.jpg")
        zf.write(double_path, "page_02_double.jpg")
        zf.write(white_path, "page_03_white.jpg")
        zf.write(black_path, "page_04_black.jpg")

    # 3. Crear PDF de prueba (texto)
    pdf_text_path = test_dir / "test_text.pdf"
    doc_text = fitz.open()
    p1 = doc_text.new_page()
    p1.insert_text((50, 50), "Capítulo 1: El comienzo\nEste es un texto de prueba para Reflowable EPUB.", fontsize=14)
    doc_text.save(str(pdf_text_path))
    doc_text.close()

    # 4. Crear PDF de prueba (cómic / imagen con páginas blancas/negras)
    pdf_comic_path = test_dir / "test_comic_src.pdf"
    doc_comic = fitz.open()
    p_img1 = doc_comic.new_page(width=200, height=300)
    p_img1.insert_image(fitz.Rect(0, 0, 200, 300), filename=str(tiny_path))
    p_img2 = doc_comic.new_page(width=600, height=300)
    p_img2.insert_image(fitz.Rect(0, 0, 600, 300), filename=str(double_path))
    p_img3 = doc_comic.new_page(width=200, height=300)
    p_img3.insert_image(fitz.Rect(0, 0, 200, 300), filename=str(white_path))
    p_img4 = doc_comic.new_page(width=200, height=300)
    p_img4.insert_image(fitz.Rect(0, 0, 200, 300), filename=str(black_path))
    doc_comic.save(str(pdf_comic_path))
    doc_comic.close()

    from CBZtoEPUB import convert_comic_to_epub, TEXTS as T_CBZ
    from PDFtoCBZ import convertir_pdf_kcc
    from PDFtoEPUB import convert_pdf_text_to_epub, convert_pdf_image_to_epub, TEXTS as T_PDF

    print("\n--- 1. Testing CBZtoEPUB (con split de dobles y perfil Kindle Oasis) ---")
    cbz_epub = test_dir / "test_comic.epub"
    convert_comic_to_epub(
        cbz_path, cbz_epub, T_CBZ['es'],
        profile_key='kindle_oasis', split_double=True, reading_direction='rtl'
    )
    if cbz_epub.exists():
        print("✅ CBZ/CBR -> EPUB Fixed-Layout generado con éxito!")

    print("\n--- 2. Testing PDFtoCBZ (con split de dobles y perfil Kobo) ---")
    cbz_res, variacion = convertir_pdf_kcc(
        pdf_comic_path, profile_key='kobo_forma', split_double=True, reading_dir='rtl'
    )
    if cbz_res and cbz_res.exists():
        print(f"✅ PDF -> CBZ generado con éxito! Variación: {variacion:.1f}%")

    print("\n--- 3. Testing PDFtoEPUB (Texto -> Reflowable) ---")
    epub_text = test_dir / "test_text.epub"
    convert_pdf_text_to_epub(pdf_text_path, epub_text, T_PDF['es'])
    if epub_text.exists():
        print("✅ PDF Texto -> EPUB Reflowable generado con éxito!")

    print("\n--- 4. Testing PDFtoEPUB (Imágenes / Cómics -> Fixed-Layout con dobles divididas) ---")
    epub_img = test_dir / "test_comic_pdf.epub"
    convert_pdf_image_to_epub(
        pdf_comic_path, epub_img, T_PDF['es'],
        profile_key='kindle_oasis', split_double=True, reading_direction='rtl'
    )
    if epub_img.exists():
        print("✅ PDF Cómic -> EPUB Fixed-Layout generado con éxito!")

    # Limpieza
    print("\nLimpiando archivos temporales...")
    for f in test_dir.glob("*.*"):
        try: f.unlink()
        except Exception: pass
    test_dir.rmdir()
    print("Todo completado limpiamente.")

if __name__ == '__main__':
    run_all_tests()
