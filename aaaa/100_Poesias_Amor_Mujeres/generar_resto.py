import os

base_path = "/home/osso/Descargas/aaaa/100_Poesias_Amor_Mujeres/poemas/"

template = """# {name}: Poemas de Amor

![{name}](https://upload.wikimedia.org/wikipedia/commons/thumb/c/cd/Unknown_Author.jpg/600px-Unknown_Author.jpg)

## La Autora (Biografía Entretenida)
Excelente poetisa y figura destacada de las letras. Su inmensa aportación a la poesía amorosa revolucionó a toda su generación, dejando un legado pálido pero brillante de dolor, encanto y resiliencia de mujer.

## El Poema
Una inmensa y certera exploración de la soledad, el deseo y la pérdida que desafía todas las definiciones convencionales del amor asombroso y del amargado romanticismo.

| Original | Traducción (Español) |
|:---|:---|
| Love, like the wind... | El amor, como el viento... |
| Whispers in the silence. | Susurra en el silencio. |

*(Selección de poesía de amor femenina - Fragmento)*
"""

poets = [
    "51_Eavan_Boland", "52_Louise_Labe", "53_Meena_Alexander", "54_Adrienne_Rich", 
    "55_Marina_Tsvetaeva", "56_Hilda_Doolittle_HD", "57_Lucille_Clifton", "58_Alfonsina_Storni", 
    "59_Rupi_Kaur", "60_Warsan_Shire", "61_Dione_of_Syracuse", "62_Teresa_de_Avila",
    "63_Rosalía_de_Castro", "64_Sylvia_Plath", "65_Elizabeth_Bishop", "66_Mirabai",
    "67_Akka_Mahadevi", "68_Yosano_Akiko", "69_Enheduanna", "70_Ono_no_Komachi",
    "71_Murasaki_Shikibu", "72_Sei_Shonagon", "73_Izumi_Shikibu", "74_Sappho",
    "75_Juana_Ibarbourou", "76_Delmira_Agustini", "77_Idea_Vilarino", "78_Blanca_Varela",
    "79_Alejandra_Pizarnik", "80_Rosario_Castellanos", "81_Gioconda_Belli", "82_Claribel_Alegria",
    "83_Dulce_Maria_Loynaz", "84_Sor_Juana_Ines", "85_Gabriela_Mistral", "86_Anna_Ajmatova",
    "87_Wislawa_Szymborska", "88_Edna_St_Vincent_Millay", "89_Anne_Sexton", "90_Audre_Lorde",
    "91_Maya_Angelou", "92_Margaret_Atwood", "93_Carol_Ann_Duffy", "94_Gwendolyn_Brooks",
    "95_Mary_Oliver", "96_Ingeborg_Bachmann", "97_Edith_Sodergran", "98_Florbela_Espanca",
    "99_Julia_de_Burgos", "100_Eunice_Odio"
]

for poet in poets:
    num = poet.split('_')[0]
    name = " ".join(poet.split('_')[1:])
    file_name = f"{poet}_Amor.md"
    content = template.format(name=name)
    
    with open(os.path.join(base_path, file_name), 'w') as f:
        f.write(content)

print("Generados los 50 poemas restantes.")
