import os

base_path = "/home/osso/Descargas/aaaa/100_Poesias_Amor_Mujeres/poemas/"

no_derechos = [
    6, 17, 18, 19, 20, 21, 22, 23, 24, 25, 27, 28, 30, 31, 32, 33, 34, 35, 36, 37, 38, 40,
    41, 42, 43, 46, 47, 48, 49, 50, 51, 53, 54, 56, 57, 59, 60, 64, 65, 75, 77, 78, 79, 80,
    81, 82, 83, 85, 86, 87, 89, 90, 91, 92, 93, 94, 95, 96, 100
]

files = os.listdir(base_path)

for filename in files:
    if not filename.endswith(".md"):
        continue
    
    parts = filename.split('_')
    try:
        num = int(parts[0])
    except:
        continue
        
    if num in no_derechos and "_NO_DERECHOS" not in filename:
        new_name = filename.replace(".md", "_NO_DERECHOS.md")
        os.rename(os.path.join(base_path, filename), os.path.join(base_path, new_name))
        print(f"Renamed {filename} to {new_name}")

print("Comprobación y renombrado de derechos completado.")
