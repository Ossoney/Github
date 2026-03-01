import os

# Death years of Japanese poets
JAPANESE_POETS_DATES = {
    "Ariwara_no_Narihira": 880, "Ki_no_Tsurayuki": 945, "Fujiwara_no_Teika": 1241,
    "Saigyo": 1190, "Kakinomoto_no_Hitomaro": 710, "Otomo_no_Yakamochi": 785,
    "Yamabe_no_Akahito": 736, "Natsume_Soseki": 1916, "Mori_Ogai": 1922,
    "Ishikawa_Takuboku": 1912, "Masaoka_Shiki": 1902, "Shimazaki_Toson": 1943,
    "Kitahara_Hakushu": 1942, "Hagiwara_Sakutaro": 1942, "Nakahara_Chuya": 1937,
    "Akutagawa_Ryunosuke": 1927, "Osamu_Dazai": 1948, "Kunikida_Doppo": 1908,
    "Miyazawa_Kenji": 1933, "Arishima_Takeo": 1923, "Izumi_Kyoka": 1939,
    "Wakayama_Bokusui": 1928, "Taneda_Santoka": 1940, "Saito_Mokichi": 1953, "Ueda_Bin": 1916
}

def verify_dirs(path, dates):
    print(f"\nVerifying: {path}")
    count_valid = 0
    names_found = set()
    files = sorted([f for f in os.listdir(path) if f.endswith('.md') or f.endswith('.docx')])
    for file in files:
        name_clean = file.replace('.md', '').replace('.docx', '')
        if name_clean in dates:
            death_year = dates[name_clean]
            if death_year >= 1956:
                if "_NO_DERECHOS" not in file:
                    new_name = file.replace(name_clean, f"{name_clean}_NO_DERECHOS")
                    os.rename(os.path.join(path, file), os.path.join(path, new_name))
                    print(f"Renamed: {file} -> {new_name}")
            else:
                count_valid += 1
                names_found.add(name_clean)
        else:
            print(f"Unknown filename: {file}")
    
    print(f"Found {len(names_found)} valid poets in {path} (out of {len(dates)} expected)")

DIRS = ["poetas_japoneses_libro", "poetas_japoneses_docx"]

for d in DIRS:
    verify_dirs(d, JAPANESE_POETS_DATES)

print("\nFinal Check for Japanese Poets Complete.")
