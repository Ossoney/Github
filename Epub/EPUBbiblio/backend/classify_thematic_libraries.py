#!/usr/bin/env python3
"""
Clasificador temático de libros para EPUB Biblio.
Analiza los metadatos OPF de los libros de la Biblioteca Principal,
crea las bibliotecas temáticas y vincula los libros (relación muchos a muchos).
"""

import os
import sys
import zipfile
import re
import time
import sqlite3

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from paths import DB_PATH

# 1. Definición de bibliotecas temáticas y sus reglas de coincidencia
THEMATIC_LIBRARIES = [
    {
        "name": "Ciencia Ficción",
        "keywords": [
            "ciencia ficcion", "ciencia ficción", "sci-fi", "science fiction",
            "cyberpunk", "space opera", "distopia", "distopía", "ucronia", "ucronía",
            "postapocaliptico", "postapocalíptico"
        ]
    },
    {
        "name": "Fantasía",
        "keywords": [
            "fantastico", "fantástico", "fantasia", "fantasía", "fantasy",
            "mitologia", "mitología", "magia", "brujeria", "brujería", "brujo", "brujos",
            "bruja", "brujas", "hada", "hadas", "elfo", "elfos", "dragon", "dragones",
            "hechizo", "hechicero", "espada y brujeria"
        ]
    },
    {
        "name": "Terror",
        "keywords": [
            "terror", "gotico", "gótico", "horror", "paranormal", "sobrenatural",
            "vampiro", "vampiros", "zombi", "zombie", "zombies", "hombre lobo", "hombres lobo",
            "gore", "pesadilla", "miedo", "fantasma", "fantasmas", "posesion", "posesión"
        ]
    },
    {
        "name": "Policial y Novela Negra",
        "keywords": [
            "policial", "policiaco", "policíaco", "novela negra", "detective",
            "hardboiled", "crimen", "noir", "det_police", "asesinato"
        ]
    },
    {
        "name": "Intriga, Suspense y Thriller",
        "keywords": [
            "intriga", "suspense", "thriller", "misterio", "espionaje",
            "psicologico", "psicológico", "conspiracion", "conspiración"
        ]
    },
    {
        "name": "Novela Histórica",
        "keywords": [
            "historico", "histórico", "novela historica", "novela histórica",
            "edad media", "antigüedad", "roma", "grecia", "renacimiento",
            "siglo de oro", "guerra civil"
        ]
    },
    {
        "name": "Novela Romántica",
        "keywords": [
            "romantico", "romántico", "romantica", "romántica", "romance",
            "sentimental", "amor", "chick-lit", "pasional"
        ]
    },
    {
        "name": "Erótica y Adultos",
        "keywords": [
            "erotico", "erótico", "erotica", "erótica", "erotismo",
            "sensual", "sumision", "sumisión", "bdsm", "erotic"
        ]
    },
    {
        "name": "Aventuras y Acción",
        "keywords": [
            "aventuras", "aventura", "accion", "acción", "belico", "bélico",
            "piratas", "maritimo", "marítimo", "supervivencia", "western", "oeste"
        ]
    },
    {
        "name": "Autoayuda y Crecimiento Personal",
        "keywords": [
            "autoayuda", "auto-ayuda", "crecimiento personal", "desarrollo personal",
            "superacion", "superación", "motivacion", "motivación", "mindfulness",
            "autoestima", "inteligencia emocional", "coaching", "habitos", "hábitos",
            "liderazgo", "productividad", "espiritualidad", "felicidad", "meditacion",
            "meditación", "bienestar", "resiliencia", "exito", "éxito"
        ]
    },
    {
        "name": "Ensayo, Filosofía y Pensamiento",
        "keywords": [
            "ensayo", "filosofia", "filosofía", "pensamiento", "politica", "política",
            "sociologia", "sociología", "religion", "religión", "espiritualidad",
            "teologia", "teología", "etica", "ética"
        ]
    },
    {
        "name": "Divulgación y Ciencia",
        "keywords": [
            "divulgacion", "divulgación", "ciencias naturales", "ciencias sociales",
            "tecnologia", "tecnología", "fisica", "física", "biologia", "biología",
            "matematicas", "matemáticas", "astronomia", "astronomía", "economia", "economía",
            "medicina", "psicologia", "psicología", "antropologia", "antropología"
        ]
    },
    {
        "name": "Biografías, Memorias y Crónicas",
        "keywords": [
            "biografia", "biografía", "biografias", "biografías", "autobiografia",
            "autobiografía", "memorias", "diarios", "cronica", "crónica",
            "cronicas", "crónicas", "testimonio", "cartas", "epistolar"
        ]
    },
    {
        "name": "Infantil y Juvenil",
        "keywords": [
            "infantil", "juvenil", "young adult", "adolescentes", "cuentos infantiles",
            "faerie", "escolar", "fábulas", "fabulas"
        ]
    },
    {
        "name": "Relatos y Cuentos Cortos",
        "keywords": [
            "relato", "relatos", "cuento", "cuentos", "antologia", "antología",
            "narrativa breve", "microrelato", "microrrelato"
        ]
    },
    {
        "name": "Humor y Sátira",
        "keywords": [
            "humor", "comedia", "satira", "sátira", "parodia", "ironia", "ironía",
            "humoristico", "humorístico"
        ]
    },
    {
        "name": "Poesía",
        "keywords": [
            "poesia", "poesía", "poemas", "verso", "lírica", "lirica", "poemario",
            "soneto", "sonetos", "haiku"
        ]
    },
    {
        "name": "Teatro",
        "keywords": [
            "teatro", "dramaturgia", "tragedia", "drama teatral", "comedia teatral",
            "sainete", "entremes", "entremeses", "monologo", "monólogo"
        ]
    },
    {
        "name": "Economía, Negocios y Finanzas",
        "keywords": [
            "economia", "economía", "finanzas", "negocios", "empresa", "empresas",
            "inversion", "inversión", "inversiones", "bolsa", "dinero", "emprendimiento",
            "emprendedor", "marketing", "gestion empresarial", "gestión empresarial",
            "criptomoneda", "finanzas personales", "finanzas personales", "riqueza", "capitalismo"
        ]
    },
    {
        "name": "Cocina y Gastronomía",
        "keywords": [
            "cocina", "gastronomia", "gastronomía", "recetas", "recetario", "culinario",
            "culinaria", "enologia", "enología", "vinos", "vino", "reposteria", "repostería",
            "chef", "cocinero", "panaderia", "panadería", "cocteleria", "coctelería"
        ]
    },
    {
        "name": "Salud, Nutrición y Bienestar",
        "keywords": [
            "salud", "nutricion", "nutrición", "alimentacion", "alimentación", "dieta",
            "dietas", "ejercicio", "fitness", "entrenamiento", "anatomia", "anatomía",
            "fisiologia", "fisiología", "medicina natural", "longevidad", "sueño",
            "enfermedades", "salud mental", "inmunidad"
        ]
    },
    {
        "name": "Historia Militar y Bélica",
        "keywords": [
            "guerra mundial", "segunda guerra mundial", "primera guerra mundial", "historia militar",
            "batalla", "batallas", "belico", "bélico", "ejercito", "ejército", "armamento",
            "tactica militar", "táctica militar", "estrategia militar", "soldados", "nazismo",
            "holocausto", "guerra civil española", "vietnam", "combate"
        ]
    },
    {
        "name": "Viajes, Expediciones y Rutas",
        "keywords": [
            "viajes", "viaje", "expedicion", "expedición", "expediciones", "guia de viaje",
            "guía de viaje", "turismo", "cuaderno de viaje", "exploracion", "exploración",
            "rutas", "aventuras reales", "cronica de viaje", "crónica de viaje", "geografia", "geografía"
        ]
    },
    {
        "name": "Mitología, Esoterismo y Ocultismo",
        "keywords": [
            "mitologia", "mitología", "mitos griegos", "mitos nordicos", "mitos nórdicos",
            "esoterismo", "ocultismo", "alquimia", "astrologia", "astrología", "tarot",
            "cabala", "cábala", "hermetismo", "chamanismo", "simbologia", "simbología",
            "misticismo", "teosofia", "teosofía", "sociedades secretas", "masoneria", "masonería"
        ]
    },
    {
        "name": "True Crime y Crónica Negra",
        "keywords": [
            "true crime", "cronica negra", "crónica negra", "crimen real", "asesino en serie",
            "asesinos en serie", "criminologia", "criminología", "narcotrafico", "narcotráfico",
            "mafia", "investigacion policial", "investigación policial", "caso real", "forense", "sucesos"
        ]
    },
    {
        "name": "Informática y Tecnología Digital",
        "keywords": [
            "informatica", "informática", "programacion", "programación", "software",
            "hardware", "hacker", "hackers", "inteligencia artificial", "ciberseguridad",
            "computacion", "computación", "algoritmos", "desarrollo web", "codigo", "código",
            "python", "linux", "internet", "redes informaticas", "redes informáticas"
        ]
    },
    {
        "name": "Cómics, Novela Gráfica y Guiones",
        "keywords": [
            "comic", "cómic", "comics", "cómics", "novela grafica", "novela gráfica",
            "manga", "tebeo", "tebeos", "historieta", "historietas", "guion", "guión",
            "guiones", "dramaturgia cinematografica", "storyboard"
        ]
    },
    {
        "name": "Ciencia Ficción Distópica",
        "keywords": [
            "distopia", "distopía", "distopico", "distópico", "postapocaliptico",
            "postapocalíptico", "apocaliptico", "apocalíptico", "cyberpunk", "ucronia",
            "ucronía", "sociedad totalitaria", "futuro distopico", "futuro distópico"
        ]
    },
    {
        "name": "Romance Histórico (Regencia y Época)",
        "keywords": [
            "romance historico", "romance histórico", "romántica histórica", "romantica historica",
            "regencia", "victoriana", "victoriano", "highlander", "highlanders", "escocia",
            "duque", "duques", "lord", "lady", "conde", "nobleza britanica", "salon de baile",
            "corte de inglaterra", "novela romantica historica"
        ]
    },
    {
        "name": "Romance Contemporáneo y Comedia",
        "keywords": [
            "romance contemporaneo", "romance contemporáneo", "comedia romantica", "comedia romántica",
            "chick-lit", "chick lit", "romance urbano", "enemies to lovers", "friends to lovers",
            "amor moderno", "enredos amorosos", "piso compartido", "oficina amor", "comedia de enredo"
        ]
    },
    {
        "name": "Romance Paranormal y Fantástico",
        "keywords": [
            "romantasy", "romance paranormal", "romántica paranormal", "romantica paranormal",
            "romance fantastico", "romance fantástico", "vampiro amor", "hombres lobo romance",
            "reino fae", "fae", "cambiaformas romance", "amor sobrenatural", "inmortales amor"
        ]
    },
    {
        "name": "Sagas Familiares y Generacionales",
        "keywords": [
            "saga familiar", "sagas familiares", "generacional", "generaciones", "clan familiar",
            "arbol genealogico", "árbol genealógico", "herencia familiar", "dinastia", "dinastía",
            "secretos de familia", "saga de época", "saga de epoca", "trilogia familiar"
        ]
    },
    {
        "name": "Narrativa Intimista y Psicológica",
        "keywords": [
            "ficcion psicologica", "ficción psicológica", "novela psicologica", "novela psicológica",
            "intimista", "monologo interior", "monólogo interior", "crisis existencial",
            "relaciones humanas", "duelo", "vacio existencial", "vacío existencial", "soledad",
            "drama intimo", "drama íntimo", "complejidad psicologica", "alma humana"
        ]
    },
    {
        "name": "Novela y Narrativa Contemporánea",
        "keywords": [
            # Se asigna si tiene 'novela', 'drama', 'realista' o ficción general
            # cuando no encaja en categorías especializadas o como base
        ]
    }
]

def normalize(text):
    return (text or "").lower().strip()

def extract_subjects_from_epub(file_path):
    """Extrae las etiquetas <dc:subject> del archivo OPF dentro del EPUB."""
    if not os.path.exists(file_path):
        return []
    try:
        with zipfile.ZipFile(file_path, "r") as z:
            opf_path = None
            try:
                container = z.read("META-INF/container.xml").decode("utf-8", errors="ignore")
                m = re.search(r'full-path=["\']([^"\']+)["\']', container)
                if m:
                    opf_path = m.group(1)
            except Exception:
                pass

            if not opf_path:
                opf_candidates = [n for n in z.namelist() if n.endswith(".opf")]
                opf_path = opf_candidates[0] if opf_candidates else None

            if opf_path and opf_path in z.namelist():
                content = z.read(opf_path).decode("utf-8", errors="ignore")
                raw_subjects = re.findall(r'<dc:subject[^>]*>(.*?)</dc:subject>', content, re.IGNORECASE)
                clean_list = []
                for s in raw_subjects:
                    for item in re.split(r'[,;/|]', s):
                        cl = item.strip()
                        if cl and cl not in clean_list:
                            clean_list.append(cl)
                return clean_list
    except Exception:
        pass
    return []

def classify_book(tags_list, title="", desc=""):
    """
    Clasifica un libro en una o más bibliotecas temáticas según sus etiquetas.
    Devuelve lista de nombres de bibliotecas a las que pertenece.
    """
    matched = set()
    norm_tags = [normalize(t) for t in tags_list]
    combined_tags_str = " " + " ".join(norm_tags) + " "

    # Comprobación de categorías especializadas
    desc_norm = normalize(desc)
    title_norm = normalize(title)

    for lib in THEMATIC_LIBRARIES:
        lib_name = lib["name"]
        if lib_name == "Novela y Narrativa Contemporánea":
            continue

        keywords = lib["keywords"]
        for kw in keywords:
            # Comprobación de palabra clave en tags
            if any(kw == t or kw in t for t in norm_tags):
                matched.add(lib_name)
                break
            # O comprobación en título / descripción para géneros concretos no ficción / temáticos
            if lib_name in [
                "Cocina y Gastronomía", "Salud, Nutrición y Bienestar", "Historia Militar y Bélica",
                "Viajes, Expediciones y Rutas", "Mitología, Esoterismo y Ocultismo",
                "Economía, Negocios y Finanzas", "Informática y Tecnología Digital",
                "Cómics, Novela Gráfica y Guiones", "True Crime y Crónica Negra",
                "Ciencia Ficción Distópica",
                "Romance Histórico (Regencia y Época)", "Romance Contemporáneo y Comedia",
                "Romance Paranormal y Fantástico", "Sagas Familiares y Generacionales",
                "Narrativa Intimista y Psicológica"
            ]:
                if len(kw) >= 5 and (f" {kw} " in f" {title_norm} " or f" {kw} " in f" {desc_norm} "):
                    matched.add(lib_name)
                    break

    # Si no cuadró con ninguna específica pero tiene novela/ficción/drama
    has_novel_base = any(t in combined_tags_str for t in ["novela", "narrativa", "ficcion", "ficción", "drama", "realista", "literario", "fiction"])
    if not matched:
        if has_novel_base:
            matched.add("Novela y Narrativa Contemporánea")
        else:
            # Buscar indicios en la descripción
            desc_norm = normalize(desc)
            if any(k in desc_norm for k in ["novela", "historia de amor", "relato", "detective", "asesinato", "personajes"]):
                matched.add("Novela y Narrativa Contemporánea")
            else:
                matched.add("Ensayo, Filosofía y Pensamiento") if any(k in desc_norm for k in ["filosofía", "ensayo", "estudio", "análisis"]) else matched.add("Novela y Narrativa Contemporánea")
    elif "Novela" in [t.capitalize() for t in tags_list] and len(matched) == 0:
        matched.add("Novela y Narrativa Contemporánea")

    return list(matched)

def main():
    print("=" * 65)
    print("  EPUB BIBLIO - CREACIÓN DE BIBLIOTECAS TEMÁTICAS Y CLASIFICACIÓN")
    print("=" * 65)

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    cur = conn.cursor()

    # 1. Asegurar nombre de Biblioteca 2 como 'Ciencia Ficción (Exclusiva)'
    cur.execute("UPDATE libraries SET name = 'Ciencia Ficción (Exclusiva)' WHERE id = 2 AND name = 'Ciencia Ficción'")
    conn.commit()

    # 2. Crear las bibliotecas temáticas en la tabla libraries
    library_ids = {} # name -> id
    cur.execute("SELECT id, name FROM libraries")
    for lid, lname in cur.fetchall():
        library_ids[lname] = lid

    for lib in THEMATIC_LIBRARIES:
        lname = lib["name"]
        if lname not in library_ids:
            cur.execute("INSERT INTO libraries (name, path) VALUES (?, '')", (lname,))
            conn.commit()
            lib_id = cur.lastrowid
            library_ids[lname] = lib_id
            print(f" [NUEVA BIBLIOTECA CREADA] ID: {lib_id} - {lname}")
        else:
            print(f" [BIBLIOTECA EXISTENTE] ID: {library_ids[lname]} - {lname}")

    # 3. Obtener todos los libros de la Biblioteca Principal (id = 1)
    cur.execute("SELECT id, file_path, title, description, tags FROM books WHERE library_id = 1")
    books = cur.fetchall()
    total = len(books)
    print(f"\nProcesando {total:,} libros de la Biblioteca Principal...")

    book_library_links = []
    book_tags_updates = []
    category_counts = {lib["name"]: 0 for lib in THEMATIC_LIBRARIES}

    t0 = time.time()
    batch_size = 5000

    for idx, (book_id, file_path, title, desc, existing_tags) in enumerate(books, 1):
        # Si ya tiene tags, reusarlos; sino, extraer del EPUB
        if existing_tags:
            tags = [t.strip() for t in existing_tags.split(",") if t.strip()]
        else:
            tags = extract_subjects_from_epub(file_path)

        categories = classify_book(tags, title, desc)
        
        # Guardar tags formateados en books
        if tags and not existing_tags:
            tags_str = ", ".join(tags)
            book_tags_updates.append((tags_str, book_id))

        # Enlazar libro a las categorías correspondientes
        for cat_name in categories:
            cat_id = library_ids.get(cat_name)
            if cat_id:
                book_library_links.append((book_id, cat_id))
                category_counts[cat_name] += 1

        if idx % batch_size == 0 or idx == total:
            # Guardar en base de datos por lotes
            if book_tags_updates:
                cur.executemany("UPDATE books SET tags = ? WHERE id = ?", book_tags_updates)
                book_tags_updates.clear()

            if book_library_links:
                cur.executemany("INSERT OR IGNORE INTO book_libraries (book_id, library_id) VALUES (?, ?)", book_library_links)
                book_library_links.clear()

            conn.commit()
            elapsed = time.time() - t0
            rate = idx / elapsed if elapsed > 0 else 0
            pct = (idx / total) * 100
            print(f"  Progreso: {idx:,}/{total:,} libros ({pct:.1f}%) | Velocidad: {rate:.1f} libros/seg | Tiempo: {elapsed:.1f}s")

    conn.close()

    print("\n" + "=" * 65)
    print("  RESULTADOS DE LAS BIBLIOTECAS TEMÁTICAS CREADAS")
    print("=" * 65)
    for cat_name, cnt in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  • {cat_name}: {cnt:,} libros")

    print(f"\n¡Proceso finalizado en {time.time() - t0:.1f} segundos con éxito!")

if __name__ == "__main__":
    main()
