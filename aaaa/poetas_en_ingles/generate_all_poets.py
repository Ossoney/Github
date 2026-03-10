#!/usr/bin/env python3
"""Reusable script to generate Markdown files for English-language poets
across multiple countries.

The script defines a generic `mk` function (same as used in the per‑country
batch scripts) and expects a data structure `POETS_BY_COUNTRY` where each
entry is a list of poet dictionaries:
    {
        "filename": "<output markdown filename>",
        "name": "Full Name",
        "years": "birth–death",
        "bio": "Short biography (Spanish).",
        "poems": [
            {"title": "Title (Original / Spanish)", "original": "...", "translation": "..."},
            ... (up to 10 poems)
        ],
        "no_derechos": false  # set True for poets deceased >= 1956
    }

Users can populate `POETS_BY_COUNTRY` manually or load it from external
JSON/CSV files. Running the script will create the appropriate directory
hierarchy under the project root and write one Markdown file per poet.
"""
import os
from pathlib import Path

# Base directory of the project (where this script lives)
BASE_DIR = Path(__file__).resolve().parent


def mk(
    output_dir: Path,
    fn: str,
    name: str,
    years: str,
    bio: str,
    poems,
    no_derechos: bool = False,
):
    """Create a Markdown file for a poet.

    Args:
        output_dir: Directory where the file will be written.
        fn: Filename (including .md).
        name: Poet's full name.
        years: Birth‑death years.
        bio: Spanish biography.
        poems: List of dicts with keys 'title', 'original', 'translation'.
        no_derechos: If True, adds the theoretical‑exercise header.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    header_note = (
        "*(Ejercicio teórico de antología — archivo _NO_DERECHOS)*\n\n"
        if no_derechos
        else ""
    )
    content = f"# {name} ({years})\n\n## Biografía\n{bio}\n\n{header_note}## Selección de 10 poemas de amor\n\n"
    for i, po in enumerate(poems, 1):
        content += f"### {i}. {po['title']}\n\n**Original:**\n{po['original']}\n\n**Traducción:**\n{po['translation']}\n\n"
    file_path = output_dir / fn
    file_path.write_text(content.strip() + "\n", encoding="utf-8")
    print(f"✅ {file_path.relative_to(BASE_DIR)}")


# ---------------------------------------------------------------------------
# Data placeholder – users should replace this with real poet data.
# ---------------------------------------------------------------------------
POETS_BY_COUNTRY = {
    "Escocia": [
        # Example entry – replace with actual data
        {
            "filename": "Robert_Burns.md",
            "name": "Robert Burns",
            "years": "1759–1796",
            "bio": "Poeta escocés, considerado el nacional de Escocia. Sus versos celebran la vida rural y el amor sencillo.",
            "poems": [
                {
                    "title": "A Red, Red Rose / Una Rosa Roja",
                    "original": "O my Luve is like a red, red rose…",
                    "translation": "Oh, mi amor es como una rosa roja…",
                },
                # Add up to 10 poems …
            ],
            "no_derechos": False,
        },
    ],
    "Gales": [
        {
            "filename": "Dylan_Thomas.md",
            "name": "Dylan Thomas",
            "years": "1914–1953",
            "bio": "Poeta galés, famoso por su estilo lírico y sus imágenes sensoriales.",
            "poems": [
                {
                    "title": "Love in the Asylum / Amor en el Asilo",
                    "original": "Love is a temporary madness…",
                    "translation": "El amor es una locura temporal…",
                },
            ],
            "no_derechos": False,
        },
    ],
    "Canadá": [],  # Populate with 25 public‑domain poets + optional _NO_DERECHOS
    "Australia": [],
    "Nueva_Zelanda": [],
    "Sudáfrica": [],
    # Add other English‑speaking territories as needed
}


def main():
    for country, poets in POETS_BY_COUNTRY.items():
        if not poets:
            print(f"[!] No poet data defined for {country}. Skipping…")
            continue
        # Build the output directory: <project>/poetas_en_ingles/<Country>/poetas_<country>
        country_dir_name = country.replace(" ", "_")
        out_dir = (
            BASE_DIR
            / "poetas_en_ingles"
            / country_dir_name
            / f"poetas_{country_dir_name.lower()}"
        )
        for poet in poets:
            mk(
                output_dir=out_dir,
                fn=poet["filename"],
                name=poet["name"],
                years=poet["years"],
                bio=poet["bio"],
                poems=poet["poems"],
                no_derechos=poet.get("no_derechos", False),
            )


if __name__ == "__main__":
    main()
