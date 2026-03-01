"""Test with a single poet to verify pro model output quality."""
import os, sys, re, json, time
import subprocess

try:
    import google.generativeai as genai
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "google-generativeai"])
    import google.generativeai as genai

API_KEY = os.environ.get("GEMINI_API_KEY", "")
if not API_KEY:
    print("ERROR: falta GEMINI_API_KEY")
    sys.exit(1)

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.0-pro-exp-02-05")

poet_name = "Albert Charton"
lang_original = "francés"

prompt = f"""Eres un experto en literatura amorosa de {lang_original} con conocimiento enciclopédico.
Tu tarea es generar datos reales y completos sobre el poeta **{poet_name}** en formato JSON.

Responde ÚNICAMENTE con JSON válido. Nada antes ni después del JSON.

{{
  "bio": "<3-5 oraciones REALES sobre su vida amorosa/sentimental, en español, basadas en hechos históricos>",
  "poems": [
    {{
      "title": "<título único del poema, diferente para cada uno>",
      "original": "<poema COMPLETO en {lang_original}, mínimo 4 versos, con saltos de línea como \\n>",
      "traduccion": "<traducción COMPLETA al español, poética y bella, con saltos de línea como \\n>"
    }}
  ]
}}

REGLAS ESTRICTAS:
1. El array "poems" debe tener EXACTAMENTE 10 objetos.
2. Los 10 poemas deben ser COMPLETAMENTE DISTINTOS entre sí — títulos, versos y contenido diferentes.
3. PROHIBIDO repetir ningún verso, línea o fragmento entre los 10 poemas.
4. Cada poema debe tener al menos 4 versos.
5. Los poemas deben ser obras REALES de {poet_name} o composiciones originales fieles a su estilo y época.
6. Las traducciones deben ser nobles y poéticas en español.
7. La bio debe mencionar detalles reales de su vida sentimental."""

print(f"Enviando solicitud para: {poet_name}")
response = model.generate_content(prompt)
text = response.text.strip()
text = re.sub(r"```json\s*", "", text)
text = re.sub(r"```\s*", "", text)

try:
    data = json.loads(text)
    poems = data.get("poems", [])
    print(f"\nBio: {data.get('bio', '')[:200]}")
    print(f"\nPoemas generados: {len(poems)}")
    for i, p in enumerate(poems, 1):
        print(f"  {i}. {p.get('title','?')} — {p.get('original','')[:60].replace(chr(10),' ')}...")
    
    titles = [p.get("title","") for p in poems]
    first_lines = [p.get("original","").split("\\n")[0] for p in poems]
    print(f"\nTítulos únicos: {len(set(titles))}/10")
    print(f"Primeras líneas únicas: {len(set(first_lines))}/10")
    print("\n¡TEST OK!" if len(poems) == 10 and len(set(titles)) >= 8 else "\n⚠ Revisar cantidad/variedad")
except json.JSONDecodeError as e:
    print(f"ERROR JSON: {e}")
    print(text[:500])
