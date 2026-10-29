
import re
import unicodedata
from difflib import SequenceMatcher

def clean_filename(nombre):
    # current logic
    # return re.sub(r'[\\/:"*?<>|_\-]+', '', nombre).strip()
    
    # proposed logic: replace with space
    res = re.sub(r'[\\/:"*?<>|_\-]+', ' ', nombre)
    return ' '.join(res.split()).strip()

def invert_name(name):
    parts = name.split()
    if len(parts) > 1:
        # Check if there's already a comma
        if ',' in name:
            return name
        return f"{parts[-1]}, {' '.join(parts[:-1])}"
    return name

def deduplicate_extras(extras_string):
    if not extras_string:
        return extras_string
        
    tags = re.findall(r"[\[\(].*?[\]\)]", extras_string)
    unique_tags = []
    seen_normalized = []
    
    for tag in tags:
        norm = unicodedata.normalize('NFKD', tag.lower()).encode('ASCII', 'ignore').decode('utf-8')
        is_dupe = False
        for seen in seen_normalized:
            if norm == seen or SequenceMatcher(None, norm, seen).ratio() > 0.85:
                is_dupe = True
                break
        if not is_dupe:
            unique_tags.append(tag)
            seen_normalized.append(norm)
            
    return " ".join(unique_tags)

# Test cases for merging
print("--- Merging Tests ---")
print(f"'Pérez-Reverte' -> '{clean_filename('Pérez-Reverte')}'")
print(f"'López_Pellisa' -> '{clean_filename('López_Pellisa')}'")

# Test cases for duplication
print("\n--- Duplication Tests ---")
title = "Hijos de Dune (Edición ilustrada)"
original_stem = "[Dune 03] Herbert, Frank - Hijos de Dune (Edición ilustrada) (Edicion ilustrada) [83276] (r1.0)"

# Simulate _extract_extras
base = re.sub(r"[\[\(].*?[\]\)]", "", original_stem).strip()
base_escaped = re.escape(base)
extras_der = ""
right_match = re.search(base_escaped + r"(.*?)$", original_stem)
if right_match:
    extras_der = " ".join(re.findall(r"[\[\(].*?[\]\)]", right_match.group(1))).strip()

print(f"Title: {title}")
print(f"Extras extracted: {extras_der}")

# The problem is that title already has (Edición ilustrada)
# and extras_der also has it.
full_name = f"{title} {extras_der}"
print(f"Combined before dedup: {full_name}")

# If we apply deduplicate_extras to the WHOLE thing?
# No, deduplicate_extras only looks for [tag] or (tag).
# Title has (Edición ilustrada).
print(f"Combined after dedup: {deduplicate_extras(full_name)}")
# Wait, deduplicate_extras ONLY returns the tags. It would lose "Hijos de Dune".

