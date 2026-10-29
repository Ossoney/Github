
import sys
import os
from pathlib import Path

# Mocking the folder structure for testing
class MockRenamer:
    def __init__(self):
        from epub_modules.renamer import RenamerModule
        self.renamer = RenamerModule()

    def test(self, author, title, original_stem):
        print(f"\nOriginal filename: {original_stem}.epub")
        print(f"Metadata - Author: {author}, Title: {title}")
        new_name = self.renamer._construct_new_name(author, title, original_stem)
        print(f"Resulting filename: {new_name}")

# We need to add the current directory to sys.path to import epub_modules
sys.path.append(os.getcwd())

from epub_modules.renamer import RenamerModule
renamer = RenamerModule()

print("=== TESTING FIXES ===")

# Case 1: Duplicated comments
print("\n--- CASE 1: Duplicated Comments ---")
author = "Frank Herbert"
title = "Hijos de Dune (Edición ilustrada)"
stem = "[Dune 03] Herbert, Frank - Hijos de Dune (Edición ilustrada) (Edicion ilustrada) [83276] (r1.0)"
res = renamer._construct_new_name(author, title, stem)
print(f"Metadata: {author} - {title}")
print(f"Stem: {stem}")
print(f"Result: {res}")

# Case 2: Merged surnames (from hyphen)
print("\n--- CASE 2: Merged Surnames (Hyphen) ---")
author = "Arturo Pérez-Reverte"
title = "Misión en París"
stem = "Pérez-Reverte, Arturo - Misión en París"
res = renamer._construct_new_name(author, title, stem)
print(f"Metadata: {author} - {title}")
print(f"Result: {res}")

# Case 3: Merged surnames (from underscore)
print("\n--- CASE 3: Merged Surnames (Underscore) ---")
author = "Teresa López_Pellisa"
title = "Historia de la ciencia ficción"
stem = "López_Pellisa, Teresa - Historia de la ciencia ficción"
res = renamer._construct_new_name(author, title, stem)
print(f"Metadata: {author} - {title}")
print(f"Result: {res}")

# Case 4: Normal space (already working, but checking for regressions)
print("\n--- CASE 4: Normal Space ---")
author = "Arturo Pérez Reverte"
title = "Misión en París"
stem = "Reverte, Arturo Pérez - Misión en París"
res = renamer._construct_new_name(author, title, stem)
print(f"Metadata: {author} - {title}")
print(f"Result: {res}")
