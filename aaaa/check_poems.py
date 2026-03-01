import os
import glob
import sys

# Rutas base según plataforma
if sys.platform == "win32":
    BASE = r"c:\Users\OscarSson\Videos\GitHub\aaaa"
else:
    BASE = "/home/osso/Descargas/GitHub_Debian/aaaa"

def p(*parts):
    return os.path.join(BASE, *parts)

directories = {
    "poetas-en-frances (all regions)": p("poetas-en-frances", "**", "*_libro", "*.md"),
    "poetisas_chinas_libro":           p("poetisas_chinas_libro", "*.md"),
    "poetas_chinos_libro":             p("poetas_chinos_libro", "*.md"),
    "poetas_japoneses_libro":          p("poetas_japoneses_libro", "*.md"),
    "poetisas_japonesas_libro":        p("poetisas_japonesas_libro", "*.md"),
    "poetisas_italianas_libro":        p("poetisas_italianas_libro", "*.md"),
}

PLACEHOLDER_TEXTS = [
    "Te voilà revenu",
    "Sin sombras te amo",
    "love you without shadows",
]

def check_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return f"READ ERROR: {e}"
    
    for ph in PLACEHOLDER_TEXTS:
        if ph in content:
            return "placeholder"
    
    table_count = content.count("|---|") + content.count("|:---|")
    if table_count < 10:
        return f"only {table_count} poem tables"
    
    return "OK"

total_bad = 0
for label, pattern in directories.items():
    files = glob.glob(pattern, recursive=True)
    valid_files = [f for f in files if "NO_DERECHOS" not in f]
    bad = []
    for f in valid_files:
        status = check_file(f)
        if status != "OK":
            bad.append((os.path.basename(f), status))
    
    print(f"\n[{label}]: {len(valid_files)} valid files, {len(bad)} incomplete")
    for name, status in bad[:10]:
        print(f"  - {name}: {status}")
    if len(bad) > 10:
        print(f"  ... and {len(bad)-10} more")
    total_bad += len(bad)

print(f"\n=== TOTAL INCOMPLETE FILES: {total_bad} ===")
