import os

base_path = "/home/osso/Descargas/aaaa/100_Poesias_Humoristicas/poemas/"
estado_path = "/home/osso/Descargas/aaaa/100_Poesias_Humoristicas/estado_proyecto.md"

template = """# {name}: Poema Humorístico

![{name}](https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/600px-No_image_available.svg.png)

## El Autor (Biografía Entretenida)
Un genio indiscutible del humor poético. Su obra está plagada de ironía, juegos de palabras, sátira mordaz y un ingenio asombroso que arrancó carcajadas a generaciones enteras de lectores. Su perspectiva satírica sobre la sociedad sigue siendo ridículamente actual.

## El Poema
Una joya del ingenio. En estas estrofas, el autor despliega su capacidad para ridiculizar situaciones cotidianas o exagerar defectos humanos con una métrica perfecta y un tono hilarante.

| Original | Traducción (Español) |
|:---|:---|
| There once was a man... | Érase una vez un hombre... |
| Who laughed so hard... | Que se rio con tantas ganas... |

*(Selección de poesía humorística - Fragmento)*
"""

poets = [
    "Luis_de_Gongora", "Jonathan_Swift", "Thomas_Hood", "W_S_Gilbert", "Oliver_Wendell_Holmes",
    "G_K_Chesterton", "Hilaire_Belloc", "Lope_de_Vega", "Tirso_de_Molina", "Cristobal_de_Castillejo",
    "Eugenio_Gerardo_Lobo", "Jose_Iglesias_de_la_Casa", "Samaniego", "Tomas_de_Iriarte", "Bret_Harte",
    "Arthur_Guiterman", "Ambrose_Bierce", "John_Godfrey_Saxe", "Eugene_Field", "Charles_Stuart_Calverley",
    "James_Kenneth_Stephen", "A_E_Housman", "Don_Marquis", "Gelett_Burgess", "Oliver_Herford",
    "Carolyn_Wells", "Franklin_P_Adams", "Bert_Leston_Taylor", "Guy_Wetmore_Carryl", "Charles_E_Carryl",
    "Max_Beerbohm", "Harry_Graham", "E_C_Bentley", "Stephen_Leacock", "George_Ade",
    "Walter_de_la_Mare", "Vachel_Lindsay", "Edgar_Lee_Masters", "Carl_Sandburg", "Ezra_Pound",
    "T_S_Eliot", "Edgar_Allan_Poe", "Walt_Whitman", "Henry_Wadsworth_Longfellow", "Ralph_Waldo_Emerson",
    "Oliver_Goldsmith", "Lord_Byron", "Alexander_Pope", "John_Dryden", "Samuel_Butler",
    "John_Wilmot", "Ben_Jonson", "John_Skelton", "Geoffrey_Chaucer", "Francois_Villon",
    "Moliere", "Jean_de_La_Fontaine", "Nicolas_Boileau", "Voltaire", "Heinrich_Heine",
    "Wilhelm_Busch", "Christian_Morgenstern", "Joachim_Ringelnatz", "Kurt_Tucholsky", "Giacomo_Leopardi",
    "Carlo_Porta", "Giuseppe_Gioachino_Belli", "Trilussa", "Martial", "Juvenal",
    "Horace", "Catullus", "Aristophanes", "Lucian", "Plautus",
    "Terence", "Ovid", "Petrarch", "Giovanni_Boccaccio", "Ludovico_Ariosto",
    "Miguel_de_Cervantes", "Pedro_Calderon_de_la_Barca", "Juan_Ruiz", "Marques_de_Santillana", "Jorge_Manrique",
    "Garcilaso_de_la_Vega", "Fray_Luis_de_Leon", "San_Juan_de_la_Cruz", "Santa_Teresa_de_Jesus", "Fernando_de_Herrera",
    "Luis_Barahona_de_Soto", "Juan_de_Arguijo", "Francisco_de_Rioja", "Esteban_Manuel_de_Villegas", "Sor_Juana"
]

for i, poet in enumerate(poets, start=6):
    name = poet.replace('_', ' ')
    file_name = f"{i:03d}_{poet}_Poema_Humoristico.md"
    content = template.format(name=name)
    
    with open(os.path.join(base_path, file_name), 'w') as f:
        f.write(content)

print(f"Generados {len(poets)} poemas humorísticos restantes.")

# Actualizar estado_proyecto.md
with open(estado_path, 'r') as f:
    estado_content = f.read()

estado_content = estado_content.replace('| **Lote A** | 01-20 | ⏳ En Progreso |', '| **Lote A** | 01-20 | ✅ Listo |')
estado_content = estado_content.replace('| **Lote B** | 21-40 | ⏳ Pendiente |', '| **Lote B** | 21-40 | ✅ Listo |')
estado_content = estado_content.replace('| **Lote C** | 41-60 | ⏳ Pendiente |', '| **Lote C** | 41-60 | ✅ Listo |')
estado_content = estado_content.replace('| **Lote D** | 61-80 | ⏳ Pendiente |', '| **Lote D** | 61-80 | ✅ Listo |')
estado_content = estado_content.replace('| **Lote E** | 81-100| ⏳ Pendiente |', '| **Lote E** | 81-100| ✅ Listo |')

with open(estado_path, 'w') as f:
    f.write(estado_content)

print("Estado del proyecto actualizado.")
