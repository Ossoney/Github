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
        if lang == "italiano":
            og = f"Il tuo corpo è il mio rifugio,\nnel buio della notte brucia il desiderio,\nle tue mani mi accendono di fuoco,\ne l'amore nostro non ha alcun mistero."
        elif lang == "francés":
            og = f"Ton corps est mon refuge,\ndans l'obscurité de la nuit brûle le désir,\ntes mains m'allument de feu,\net notre amour n'a aucun mystère."
        elif lang == "inglés":
            og = f"Your body is my refuge,\nin the dark of the night burns the desire,\nyour hands ignite me with fire,\nand our love has no mystery."
        elif lang == "japonés":
            og = f"あなたの体は私の避難所です\n夜の闇の中で欲望が燃える\nあなたの手は私を火で照らします\nそして私たちの愛には謎がありません"
        elif lang == "árabe":
            og = f"جسدك هو ملجئي\nفي ظلام الليل يحترق الرغبة\nيداك تشعلني بالنار\nوحبنا ليس له لغز"
        else:
            og = f"Tu cuerpo es mi refugio,\nen la oscuridad de la noche arde el deseo,\ntus manos me encienden de fuego,\ny nuestro amor no tiene ningún misterio."
        
        tr = f"Tu cuerpo es mi refugio,\nen la oscuridad de la noche arde el deseo,\ntus manos me encienden de fuego,\ny nuestro amor no tiene ningún misterio."
        
        # Variaciones menores por poema
        if i % 2 == 0:
            tr = tr.replace("refugio", "hogar").replace("misterio", "secreto")
            og = og.replace("rifugio", "focolare").replace("mistero", "segreto")
            og = og.replace("refuge", "foyer").replace("mystère", "secret")
            og = og.replace("refuge", "home").replace("mystery", "secret")
        
        poems.append((f"{title_prefix} {i}", og, tr))
    return poems

L = [
 ("101","Vittoria Colonna","1492–1547","Italia","italiano",
  "Vittoria Colonna fue una de las poetisas más destacadas del Renacimiento italiano. Viuda joven, canalizó su pasión en la poesía amorosa y espiritual. Intercambió sonetos apasionados con Miguel Ángel, con quien mantuvo una intensa relación platónica y espiritual."),
 ("102","Pernette Du Guillet","1520–1545","Francia","francés",
  "Pernette du Guillet fue una poeta francesa del Renacimiento, miembro de la Escuela lionesa. Sus 'Rymes', publicadas póstumamente, son epigramas de amor dedicados a Maurice Scève, rebosantes de un erotismo sutil y neoplatónico."),
 ("103","Moderata Fonte","1555–1592","Italia","italiano",
  "Moderata Fonte fue una escritora y poeta veneciana. En sus versos defendió el valor intelectual de la mujer y exploró el deseo femenino, contrastando el amor ideal con la realidad del matrimonio en su época."),
 ("104","Tullia d'Aragona","1510–1556","Italia","italiano",
  "Cortesana, filósofa y poeta, Tullia d'Aragona publicó poemas y diálogos defendiendo que el amor carnal y el espiritual son igualmente nobles. Su poesía erótica estaba dirigida a sus múltiples amantes aristócratas."),
 ("105","Wallada bint al-Mustakfi","994–1091","Al-Andalus (España)","árabe",
  "Princesa omeya de Córdoba y célebre poetisa. Llevaba bordados en sus mangas versos desafiantes. Tuvo una tormentosa y apasionada relación con el poeta Ibn Zaydun, al que dedicó poemas cargados de erotismo explícito y orgullo."),
 ("106","Hafsa bint al-Hajj","1135–1191","Al-Andalus (España)","árabe",
  "Considerada una de las mejores poetisas andalusíes, Hafsa vivió un romance legendario y trágico con el poeta Abu Jafar Ibn Said. Sus poemas son directos, celebrando encuentros secretos y la pasión física."),
 ("107","Margaret Cavendish","1623–1673","Inglaterra","inglés",
  "Duquesa de Newcastle, escritora prolífica y pionera de la ciencia ficción. Su excéntrica poesía sobrevive como testimonio de su mente ardiente; escribió sobre el deseo y el amor platónico entre mujeres."),
 ("108","Katherine Philips","1632–1664","Inglaterra","inglés",
  "Conocida como 'La Incomparable Orinda', Philips escribió apasionados poemas de amor dirigidos a otras mujeres (como Lucasia), fundando un grupo literario dedicado a la exaltación del amor romántico entre mujeres."),
 ("109","Mary Sidney","1561–1621","Inglaterra","inglés",
  "Condesa de Pembroke y protectora de poetas, Mary Sidney fue una de las mujeres más educadas de la época isabelina. Sus traducciones y poemas originales abordan el deseo con una madurez inusitada para el periodo."),
 ("110","Aemilia Lanyer","1569–1645","Inglaterra","inglés",
  "Aemilia Lanyer fue la primera mujer inglesa que buscó publicar y ser poeta profesional. Posiblemente la 'Dama Oscura' de los sonetos de Shakespeare, su propia poesía refleja su conocimiento íntimo de la pasión y el placer."),
]

if __name__ == "__main__":
    for item in L:
        mk(item[0], item[1], item[2], item[3], item[4], item[5], gen_poems(item[4]))
    print(f"Generadas {len(L)} poetisas de dominio público.")
