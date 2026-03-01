print("STARTING RUN")
import os, sys, re, json, time, glob, subprocess

# SDK Setup
try:
    from google import genai as gai
    from google.genai import types as gai_types
except ImportError:
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "google-genai", "--break-system-packages"])
    except:
        pass
    from google import genai as gai
    from google.genai import types as gai_types

API_KEY = os.environ.get("GEMINI_API_KEY", "")
if not API_KEY:
    print("ERROR: falta la variable de entorno GEMINI_API_KEY")
    sys.exit(1)

GENAI_MODEL = "gemini-2.0-flash"

def get_poets_list(client, country, num_poets_target=35):
    """Obtiene una lista extensa de poetas (para poder filtrar dominio publico)"""
    prompt = f"""Eres un experto en literatura asiática.
Necesito una lista de al menos {num_poets_target} de los mejores poetas históricos del amor de **{country}** (considerando el principal idioma histórico y literario de la región).
Dame la lista en formato JSON puro, sin markdown:

[{{
  "name": "Nombre Conocido Occidental",
  "death_year": año_fallecimiento (entero, usar 2026 si sigue vivo, usar negativo para antes de Cristo, 0 si desconocido),
  "native_language": "idioma original principal (ej: persa, urdu, árabe, sánscrito, hindi, turco, coreano, etc.)"
}}]
Importante: La gran mayoría deben haber fallecido ANTES de 1956 (dominio público). Incluye clásicos y modernos tempranos.
"""
    
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=GENAI_MODEL,
                contents=prompt,
                config=gai_types.GenerateContentConfig(temperature=0.4, max_output_tokens=8192)
            )
            text = response.text.strip()
            text = re.sub(r"^```(?:json)?\s*", "", text)
            text = re.sub(r"\s*```\s*$", "", text)
            data = json.loads(text)
            return data
        except Exception as e:
            print(f"Error parseando lista de poetas, intento {attempt+1}: {e}")
            time.sleep(5)
    return []

def build_prompt(poet_name: str, lang: str) -> str:
    return f"""Eres un experto en literatura de {lang}. Necesito los mejores poemas de amor REALES y DOCUMENTADOS del poeta **{poet_name}**.

Responde ÚNICAMENTE con JSON válido. Sin texto antes ni después.

{{
  "bio": "<3-5 oraciones REALES sobre la vida amorosa/sentimental de {poet_name}, con hechos históricos concretos, en español>",
  "poems_found": <número entero: cuántos poemas de amor reales y documentados tiene este poeta>,
  "poems": [
    {{
      "title": "<título real y documentado del poema en {lang}>",
      "original": "<texto completo del poema en escritura original en {lang}, saltos de línea = \\n>",
      "traduccion": "<traducción poética al español, saltos de línea = \\n>"
    }}
  ]
}}

REGLAS ESTRICTAS:
1. Incluye ÚNICAMENTE poemas que sean obras REALES y DOCUMENTADAS de {poet_name}.
2. NO inventes poemas. NO compongas poemas nuevos.
3. El campo "poems_found" debe reflejar honestamente cuántos poemas reales de amor se conocen.
4. Los poemas deben ser DISTINTOS entre sí.
5. Texto original en {lang} con escritura nativa. Si hay menos de 10 poemas documentados, incluye SOLO los que existen realmente."""

def generate_for_poet(client, poet_name: str, lang: str) -> dict | None:
    prompt = build_prompt(poet_name, lang)
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=GENAI_MODEL,
                contents=prompt,
                config=gai_types.GenerateContentConfig(temperature=0.2, max_output_tokens=8192)
            )
            text = response.text.strip()
            text = re.sub(r"^```(?:json)?\s*", "", text)
            text = re.sub(r"\s*```\s*$", "", text)
            data = json.loads(text)
            if "poems" in data:
                valid_poems = []
                seen_titles = set()
                seen_originals = set()
                for p in data["poems"]:
                    title = p.get("title", "").strip()
                    orig = p.get("original", "").strip()
                    trad = p.get("traduccion", "").strip()
                    
                    if not title or not orig or not trad:
                        continue
                    
                    title_lower = title.lower()
                    orig_prefix = orig[:30].lower()
                    
                    if title_lower in seen_titles or orig_prefix in seen_originals:
                        continue
                        
                    seen_titles.add(title_lower)
                    seen_originals.add(orig_prefix)
                    valid_poems.append(p)
                
                data["poems"] = valid_poems
                return data
        except Exception as e:
            print(f"    [API error] intento {attempt+1}: {e}")
            time.sleep(8)
    return None

def build_md(poet_name: str, bio: str, poems: list, poems_found: int, lang_original: str) -> str:
    lines = [f"# {poet_name}", "", "## Biografía Sentimental", "", bio, "", "## Poemas de Amor", ""]
    
    for i, p in enumerate(poems, 1):
        orig = p.get("original", "").replace("\\n", "\n")
        trad = p.get("traduccion", "").replace("\\n", "\n")
        lines += [
            f"### {i}. {p.get('title', f'Poema {i}')}",
            "",
            f"| Original ({lang_original}) | Traducción (Español) |",
            "|---|---|",
            f"| {orig.replace(chr(10), '<br>')} | {trad.replace(chr(10), '<br>')} |",
            "",
        ]

    if len(poems) < 10:
        lines += [
            f"---",
            "",
            f"*(No se han encontrado 10 poemas de amor documentados para este autor. Solo existen {len(poems)} registrados en la literatura conocida.)*",
            f"*(Poemas de amor reales documentados: {poems_found if poems_found else len(poems)} en total)*",
            "",
        ]
    return "\n".join(lines)

def process_country(client, country_name):
    # Crear nombre de carpeta estandarizado
    safe_country = country_name.replace(" / ", "_").replace(" ", "_").replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u").replace("Á", "A")
    folder_name = f"poetas_de_{safe_country.lower()}"
    
    print(f"\n{'='*65}")
    print(f"INICIANDO {country_name.upper()}")
    
    base_dir = os.path.join(os.getcwd(), "poetas_asiaticos", safe_country, folder_name)
    os.makedirs(base_dir, exist_ok=True)
    
    valid_count = 0
    no_rights_count = 0
    
    # Check already existing files
    existing = glob.glob(os.path.join(base_dir, "*.md"))
    valid_count = len([f for f in existing if "NO_DERECHOS" not in f])
    
    if valid_count >= 25:
        print(f"✓ La colección {country_name} ya está completa con {valid_count} poetas válidos.")
        return
        
    print(f"1. Obteniendo lista de poetas de {country_name}...")
    poets_list = get_poets_list(client, country_name, 40)
    
    print(f" - Archivos válidos existentes: {valid_count}/25")
    
    for p in poets_list:
        if valid_count >= 25:
            break
            
        poet_name = p.get("name", "Desconocido")
        death_year = p.get("death_year", 2026)
        native_lang = p.get("native_language", "Idioma local")
        
        filename_base = poet_name.replace(" ", "_").replace("/", "-")
        has_rights = (death_year < 1956)
        
        prefix = f"{(valid_count + 1):02d}" if has_rights else "XX"
        
        out_name = f"{prefix}_{filename_base}.md"
        if not has_rights:
            out_name = f"{filename_base}_NO_DERECHOS.md"
            
        out_path = os.path.join(base_dir, out_name)
        if os.path.exists(out_path):
            continue
            
        print(f"  ▶ Generando: {poet_name} (f. {death_year}, {native_lang}) - Dominio Público: {'SI' if has_rights else 'NO'}")
        
        data = generate_for_poet(client, poet_name, native_lang)
        if not data:
            print(f"  ✗ FALLO al generar a {poet_name}")
            continue
            
        bio = data.get("bio", "")
        poems = data.get("poems", [])
        poems_found = data.get("poems_found", len(poems))
        
        md_content = build_md(poet_name, bio, poems, poems_found, native_lang)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(md_content)
            
        print(f"    ✓ Creado: {out_name} con {len(poems)} poemas.")
        
        if has_rights:
            valid_count += 1
        else:
            no_rights_count += 1
            
        time.sleep(3)
        
    print(f"\nCompletado {country_name}: {valid_count} válidos, {no_rights_count} sin derechos marcados.")

def main():
    client = gai.Client(api_key=API_KEY)
    
    # LISTA COMPLETA DE ASIA (Excluyendo China y Japón que ya están hechos en las otras carpetas)
    targets = [
        "Afganistán", "Arabia Saudita", "Armenia", "Azerbaiyán", "Bangladés", "Baréin", "Birmania", 
        "Brunéi", "Bután", "Camboya", "Catar", "Corea del Norte", "Corea del Sur", "Emiratos Árabes Unidos", 
        "Filipinas", "Georgia", "India", "Indonesia", "Irak", "Irán", "Israel", "Jordania", "Kazajistán", 
        "Kirguistán", "Kuwait", "Laos", "Líbano", "Malasia", "Maldivas", "Mongolia", "Nepal", "Omán", 
        "Pakistán", "Palestina", "Singapur", "Siria", "Sri Lanka", "Tailandia", "Tayikistán", "Timor Oriental", 
        "Turkmenistán", "Turquía", "Uzbekistán", "Vietnam", "Yemen"
    ]
    
    for country in targets:
        process_country(client, country)

if __name__ == "__main__":
    main()
print("REACHED END")
