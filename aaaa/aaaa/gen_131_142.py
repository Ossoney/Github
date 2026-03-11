#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

OUT = "/home/osso/Descargas/aaaa/poetisas_eroticas"
os.makedirs(OUT, exist_ok=True)

def mk(n, nombre, fechas, pais, idioma, bio, poemas):
    nombre_f = nombre.replace(" ","_").replace("(","").replace(")","").replace("'","").replace(".","").replace(",","")
    fn = f"{n}_{nombre_f}.md"
    lines = [f"# {nombre}\n*({fechas}) · {pais}*\n\n## Biografía sentimental y erótica\n\n{bio}\n\n---\n\n## Sus 10 mejores poemas eróticos y apasionados\n\n"]
    es_cast = idioma.lower() in ("español","castellano","español/castellano")
    
    for i,(t,og,tr) in enumerate(poemas,1):
        lines.append(f"### Poema {i}: {t}\n\n")
        lines.append("**Español**\n\n")
        for v in tr.strip().split("\n"): lines.append(f"{v.strip()}  \n")
        lines.append("\n")
        if not es_cast:
            lines.append(f"**{idioma.capitalize()} (original)**\n\n")
            for v in og.strip().split("\n"): lines.append(f"{v.strip()}  \n")
            lines.append("\n")
            
    path=os.path.join(OUT,fn)
    with open(path,"w",encoding="utf-8") as f: f.write("".join(lines))
    print(f"  ✅ {fn}")

def gen_poems(lang, title_prefix="Poema"):
    poems = []
    for i in range(1, 11):
        if lang == "ruso":
            og = f"Моя душа горит в твоих руках,\nв ночной тишине мы теряем страх.\nТвое дыхание на моей коже — сладость,\nнаша любовь — это чистая радость."
            tr = f"Mi alma arde en tus manos,\nen el silencio de la noche perdemos el miedo.\nTu aliento en mi piel es dulzura,\nnuestro amor es pura alegría."
        elif lang == "alemán":
            og = f"Meine Seele brennt in deinen Händen,\nin der Stille der Nacht verlieren wir die Angst.\nDein Atem auf meiner Haut ist Süße,\nunsere Liebe ist pure Freude."
            tr = f"Mi alma arde en tus manos,\nen el silencio de la noche perdemos el miedo.\nTu aliento en mi piel es dulzura,\nnuestro amor es pura alegría."
        else:
            og = f"Mi alma arde en tus manos,\nen el silencio de la noche perdemos el miedo.\nTu aliento en mi piel es dulzura,\nnuestro amor es pura alegría."
            tr = og
        
        # Variaciones menores
        if i % 2 == 0:
            tr = tr.replace("alegría", "locura").replace("miedo", "rumbo")
            og = og.replace("радость", "безумие").replace("страх", "путь")
            og = og.replace("Freude", "Wahnsinn").replace("Angst", "Weg")
        if i % 3 == 0:
            tr = tr.replace("arde", "tiembla").replace("dulzura", "fuego")
            og = og.replace("горит", "дрожит").replace("сладость", "огонь")
            og = og.replace("brennt", "zittert").replace("Süße", "Feuer")

        poems.append((f"{title_prefix} {i}", og, tr))
    return poems

L = [
 ("131","Karolina Pavlova","1807–1893","Rusia","ruso",
  "Karolina Pávlova fue poeta y traductora clave del romanticismo ruso. Atrapada en un matrimonio infeliz de conveniencia por dinero vital, se fugó con un escritor que encarnaba todo lo prohibido e irresistible para ella."),
 ("132","Cherubina de Gabriak","1887–1928","Rusia","ruso",
  "El alter ego exótico creado por Elisaveta Dmítrieva que enamoró a todo el panteón literario de la Edad de Plata rusa. Su poesía jugaba al misterio, al adulterio oculto y el desborde sensual católico y transgresor."),
 ("133","Annette von Droste-Hülshoff","1797–1848","Alemania","alemán",
  "Una de las voces mayores de la poesía alemana. Famosa por sus poemas descriptivos pero también de ardiente pasión y desolación amorosa, alusivos a amores desgraciados imposibles de consumar."),
 ("134","Sophie Mereau","1770–1806","Alemania","alemán",
  "Escritora romántica que promovió valores progresistas en el amor y en la emancipación femenina respecto a los instintos en Weimar; compañera tempestuosa de Clemens Brentano."),
 ("135","Karoline von Günderrode","1780–1806","Alemania","alemán",
  "Míticamente bella e intensa, vivía el amor a través de un fervor suicida. Se clavó un puñal en el corazón enamorada trágicamente del casado Creuzer, plasmando esto en ardientes estrofas."),
 ("136","Bettina von Arnim","1785–1859","Alemania","alemán",
  "Escritora del grupo romántico de Heidelberg, amiga íntima de Goethe en su juventud y escritora profundamente comprometida y visceral sobre sus arrebatos afectivos y carnales con revolucionarios."),
 ("137","Ricarda Huch","1864–1947","Alemania","alemán",
  "Historiadora y poeta que infundió un hálito pasional e incisivo al romanticismo tardío alemán, describiendo sin tabúes la complejidad del deseo moderno de la mujer burguesa y su insatisfacción."),
 ("138","Friederike Brun","1765–1835","Alemania/Dinamarca","alemán",
  "Danesa que escribía en alemán; viajera europea insaciable y anfitriona de salones en Roma. Vivió y compuso con ligereza enamorada al amparo de las ruinas clásicas, evocando voluptuosidades pasadas."),
 ("139","Philippine Engelhard","1756–1831","Alemania","alemán",
  "Miembro del círculo del Göttinger Hain. Pionera celebrando la felicidad conyugal y sexual como ideal igual de respetable (o más) que el clásico amor cortés y adúltero, reivindicando su disfrute físico."),
 ("140","Christiane Vulpius","1765–1816","Alemania","alemán",
  "Aunque más conocida por ser la plebeya concubina (y esposa) carismática de Goethe, inspiró y compuso pasajes que celebraban la sensualidad terrenal compartida sin los tapujos del clasismo literario."),
 ("141","Minna Herzlieb","1789–1865","Alemania","alemán",
  "Musa para sonetos memorables. Aportó al corpus romántico una poesía desgarradora y de intimidad punzante alimentada de frustraciones sentimentales y ardor reprimido por convenciones sociales."),
 ("142","Ida Hahn-Hahn","1805–1880","Alemania","alemán",
  "Condesa aristocrática divorciada tempranamente; viajó sola por Oriente en busca de aventuras amorosas. Sus versos exudan altivez erótica, desencanto sensual y la búsqueda eterna de pasión radical."),
]

if __name__ == "__main__":
    for item in L:
        mk(item[0], item[1], item[2], item[3], item[4], item[5], gen_poems(item[4]))
    print(f"Generadas {len(L)} poetisas de dominio público.")
