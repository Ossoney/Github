import os
import zipfile
import fitz
from pathlib import Path

# Create test directory
test_dir = Path("test_files")
test_dir.mkdir(exist_ok=True)

# Create dummy CBZ
cbz_path = test_dir / "test.cbz"
with zipfile.ZipFile(cbz_path, 'w') as zf:
    # We just need a tiny valid image. This is a 1x1 black JPEG
    tiny_jpg = bytes.fromhex("ffd8ffe000104a46494600010101004800480000ffdb004300080606070605080707070909080a0c140d0c0b0b0c1912130f141d1a1f1e1d1a1c1c20242e2720222c231c1c2837292c30313434341f27393d38323c2e333432ffdb0043010909090c0b0c180d0d1832211c213232323232323232323232323232323232323232323232323232323232323232323232323232323232323232323232323232ffc00011080001000103012200021101031101ffc4001f0000010501010101010100000000000000000102030405060708090a0bffc400b5100002010303020403050504040000017d01020300041105122131410613516107227114328191a1082342b1c11552d1f02433627282090a161718191a25262728292a3435363738393a434445464748494a535455565758595a636465666768696a737475767778797a838485868788898a92939495969798999aa2a3a4a5a6a7a8a9aab2b3b4b5b6b7b8b9bac2c3c4c5c6c7c8c9cad2d3d4d5d6d7d8d9dae1e2e3e4e5e6e7e8e9eaf1f2f3f4f5f6f7f8f9faffc4001f0100030101010101010101010000000000000102030405060708090a0bffc400b51100020102040403040705040400010277000102031104052131061241510761711322328108144291a1b1c109233352f0156272d10a162434e125f11718191a262728292a35363738393a434445464748494a535455565758595a636465666768696a737475767778797a82838485868788898a92939495969798999aa2a3a4a5a6a7a8a9aab2b3b4b5b6b7b8b9bac2c3c4c5c6c7c8c9cad2d3d4d5d6d7d8d9dae2e3e4e5e6e7e8e9eaf2f3f4f5f6f7f8f9faffda000c03010002110311003f00f928a28afcff00d9")
    zf.writestr("page_01.jpg", tiny_jpg)

# Create dummy PDF
pdf_path = test_dir / "test.pdf"
doc = fitz.open()
page = doc.new_page()
page.insert_text((50, 50), "Capitulo 1\nEsto es un test de conversión a EPUB.", fontsize=14)
doc.save(str(pdf_path))
doc.close()

from CBZtoEPUB import convert_cbz_to_epub, TEXTS as T_CBZ
from PDFtoEPUB import convert_pdf_text_to_epub, TEXTS as T_PDF

print("--- Testing CBZtoEPUB ---")
convert_cbz_to_epub(cbz_path, cbz_path.with_suffix('.epub'), T_CBZ['es'])

print("\n--- Testing PDFtoEPUB ---")
convert_pdf_text_to_epub(pdf_path, pdf_path.with_suffix('.epub'), T_PDF['es'])

if cbz_path.with_suffix('.epub').exists():
    print("✅ CBZ convertido exitosamente!")
if pdf_path.with_suffix('.epub').exists():
    print("✅ PDF convertido exitosamente!")

print("Limpiando...")
cbz_path.unlink()
pdf_path.unlink()
if cbz_path.with_suffix('.epub').exists(): cbz_path.with_suffix('.epub').unlink()
if pdf_path.with_suffix('.epub').exists(): pdf_path.with_suffix('.epub').unlink()
test_dir.rmdir()
