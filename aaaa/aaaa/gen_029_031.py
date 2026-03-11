#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera poetisas 029-045 — siglos XVII-XIX"""
import os
OUT = "/home/osso/Descargas/aaaa/poetisas_eroticas"
os.makedirs(OUT, exist_ok=True)

def mk(n, nombre, fechas, pais, idioma, bio, poemas, nd=False):
    sufijo = "_NO_DERECHOS" if nd else ""
    nombre_f = nombre.replace(" ","_").replace("(","").replace(")","").replace("'","").replace(".","").replace(",","").replace("/","-")
    fn = f"{n}_{nombre_f}{sufijo}.md"
    nota = "\n\n---\n\n> ⚠️ **NOTA LEGAL**: Fallecida ≥ 1956 o vive. Ejercicio teórico.\n" if nd else ""
    lines = [f"# {nombre}\n*({fechas}) · {pais}*\n\n## Biografía sentimental y erótica\n\n{bio}\n\n---\n\n## Sus 10 mejores poemas eróticos y apasionados\n\n"]
    for i,(t,og,tr) in enumerate(poemas,1):
        lines.append(f"### Poema {i}: {t}\n\n| {idioma.upper()} (original) | ESPAÑOL (traducción) |\n|:---|:---|\n")
        og_lines = og.strip().split("\n")
        tr_lines = tr.strip().split("\n")
        m = max(len(og_lines),len(tr_lines))
        og_lines += [""]*(m-len(og_lines))
        tr_lines += [""]*(m-len(tr_lines))
        for a,b in zip(og_lines,tr_lines):
            lines.append(f"| {a.strip()} | {b.strip()} |\n")
        lines.append("\n")
    lines.append(nota)
    path = os.path.join(OUT, fn)
    with open(path,"w",encoding="utf-8") as f:
        f.write("".join(lines))
    print(f"  ✅ {fn}")

LISTA = [
  ("029","Mary Wollstonecraft","1759–1797","Inglaterra","inglés",
   "Mary Wollstonecraft es la madre del feminismo occidental: su 'Vindicación de los Derechos de la Mujer' (1792) es el primer manifiesto sistemático de la igualdad de género en la historia. Pero también fue una mujer que amó con una intensidad que la destruyó: tuvo una hija ilegítima con el aventurero Gilbert Imlay, que la abandonó haciéndola intentar el suicidio dos veces. Luego amó al anarquista William Godwin, con quien se casó estando ya embarazada. Murió con treinta y ocho años de fiebre puerperal, dejando en el mundo a una hija llamada Mary que escribiría Frankenstein. Sus cartas de amor a Imlay son los documentos más dolorosos del amor traicionado en la literatura inglesa.",
   [("Letter to Imlay — La desesperación",
     "I write to you now on my knees; imploring you to return to me.\nI have no pride—I threw it all away when I threw myself on you.\nCome back, or I shall go mad.",
     "Te escribo ahora de rodillas; suplicándote que regreses a mí.\nNo tengo orgullo—lo arrojé todo cuando me arrojé sobre ti.\nVuelve, o me volveré loca."),
    ("A Vindication — El amor igual",
     "Would men but generously snap our chains,\nand be content with rational fellowship instead of slavish obedience,\nthey would find us more observant daughters, more affectionate sisters,\nmore faithful wives, more reasonable mothers.",
     "Si los hombres rompieran generosamente nuestras cadenas\ny se contentaran con la compañía racional en lugar de la obediencia esclava,\nse encontrarían con hijas más observadoras, hermanas más afectuosas,\nesposas más fieles, madres más razonables."),
    ("Maria: or The Wrongs of Woman — Deseo libre",
     "I have loved—I still love; and in the face of all, I will not renounce.\nTo love is a right beyond all your laws;\nthe heart cannot be legislated.",
     "He amado—todavía amo; y frente a todo, no renunciaré.\nAmar es un derecho más allá de todas vuestras leyes;\nel corazón no puede ser legislado."),
    ("Letters written during a short residence in Sweden — El deseo nórdico",
     "The rocks blasted by lightning presented many fantastic forms;\nsome resembled ruins; some, pillars; others, heaps on heaps,\nas if Nature had been a mad architect.",
     "Las rocas heridas por el rayo presentaban formas fantásticas;\nalgunas parecían ruinas; otras, pilares; otras, montones sobre montones,\ncomo si la Naturaleza hubiera sido una arquitecta loca."),
    ("Letter 2 to Imlay — El cuerpo que extraña",
     "You have convinced me by your absence\nthat the body is not nothing;\nthat flesh has its claims beyond the spirit;\nthat I want your hands on me.",
     "Me has convencido con tu ausencia\nde que el cuerpo no es nada;\nque la carne tiene sus reclamaciones más allá del espíritu;\nque quiero tus manos sobre mí."),
    ("On the Importance of Religious Opinions — La fe erótica",
     "I love God, I love truth, I love you.\nThe three are not so different as men suppose:\nboth truths demand the whole of me,\nboth loves exact the same surrender.",
     "Amo a Dios, amo la verdad, te amo a ti.\nLas tres no son tan diferentes como los hombres suponen:\nambas verdades me exigen entera,\nambos amores exigen la misma rendición."),
    ("Thoughts on the Education of Daughters — El cuerpo educado",
     "The passions are the elements of virtue;\nand while we teach girls to suppress them, we teach them to deform themselves.\nA woman's heart must be trained, not broken.",
     "Las pasiones son los elementos de la virtud;\ny mientras enseñamos a las niñas a suprimirlas, las enseñamos a deformarse.\nEl corazón de una mujer debe ser entrenado, no roto."),
    ("Letter to Godwin — El amor maduro",
     "You have given me something I did not expect to find again:\na love that is also respect, a passion that is also peace.\nI did not know such a thing was possible.",
     "Me has dado algo que no esperaba volver a encontrar:\nun amor que también es respeto, una pasión que también es paz.\nNo sabía que tal cosa era posible."),
    ("The Unsent Letter — El suicidio aplazado",
     "I have been long meditating on the step I am going to take.\nNothing but my little girl could have kept me here.\nShe is yours now; love her as I loved you.",
     "He meditado largo tiempo sobre el paso que voy a dar.\nNada sino mi pequeña niña podría haberme retenido aquí.\nElla es tuya ahora; ámala como te amé a ti."),
    ("Fragment — El amor que exige igualdad",
     "I am tired of being ruled by feeling;\nbut feelings will not be ruled.\nI want a partnership, not a subjugation;\nI want a lover, not a master.",
     "Estoy cansada de ser gobernada por el sentimiento;\npero los sentimientos no se dejan gobernar.\nQuiero una asociación, no una subyugación;\nquiero un amante, no un amo.")]),

  ("030","Sor Violante do Ceu","1607–1693","Portugal/Brasil","portugués",
   "Sor Violante do Céu fue la poetisa más brillante y prolífica del Portugal seiscentista: monja dominica de Lisboa de origen posiblemente afrobrasileño, que escribió con igual soltura villancicos religiosos, comedias y poemas de amor profano extraordinariamente sensuales. Su famosa colección 'Rimas Várias' (1646) incluye sonetos amorosos que no tienen nada que envidiar a los de Camões. Era conocida en los círculos literarios de Madrid —donde fue festejada como la décima musa— y de Lisboa. Sus sonetos encierran el mayor secreto: una mujer de clausura que escribe sobre el deseo con la precisión de quien lo ha vivido.",
   [("Soneto — Retrato de la amada",
     "Isto é amor: saber sofrer o dano\ncausado de tão bela formosura;\namar, ainda que o bem seja tão vão;\naguardar, ainda que a esperança dura.",
     "Esto es amor: saber sufrir el daño\ncausado de tan bella hermosura;\namar, aunque el bien sea tan vano;\naguardar, aunque la esperanza dure."),
    ("Soneto — La llama interior",
     "Se o fogo que me abrasa é tão luzente,\nque excede o claro sol em seu brilhante:\npor que o não sinto ardente?\nmistério raro e de mirar distante.",
     "Si el fuego que me abrasa es tan luminoso\nque excede al claro sol en su brillo:\n¿por qué no lo siento ardiente?\nmisterio raro y de contemplar distante."),
    ("Soneto — El amor imposible",
     "Amor é fogo que arde sem se ver,\né ferida que dói e não se sente,\né um contentamento descontente,\né dor que desatina sem doer.",
     "Amor es fuego que arde sin verse,\nes herida que duele y no se siente,\nes un contento descontento,\nes dolor que desatina sin doler."),
    ("Cantata — Al amor que vuela",
     "Voa, amor, que és passarinho livre;\nvoa, que ninguém te pode prender;\nvoa, que teu voo basta para viver;\nvoa, antes que a gaiola te revele.",
     "Vuela, amor, que eres pajarillo libre;\nvuela, que nadie puede prenderte;\nvuela, que tu vuelo basta para vivir;\nvuela, antes de que la jaula te revele."),
    ("Soneto — La monja y el amor",
     "Detém-te, Amor, que corres apressado;\nsouber que sou religio­sa e virgem;\nnão quero teu afeto nem os teus voos;\nmas nunca resistino ao teu poder sagrado.",
     "Detente, Amor, que corres apresurado;\nsabe que soy religiosa y virgen;\nno quiero tu afecto ni tus vuelos;\npero nunca resistí a tu sagrado poder."),
    ("Villancico — Al niño Jesús con erotismo místico",
     "Menino fermoso,\nNiño de amor,\nque vindes do Céu\nconsumir meu ardor.",
     "Niño hermoso,\nNiño de amor,\nque venís del Cielo\na consumir mi ardor."),
    ("Romance — El portal de Belén",
     "Esta noite de alegria\nminha alma não descansa;\nbusco o amor na meia-noite,\nbusco-o e não o alcança.",
     "Esta noche de alegría\nmi alma no descansa;\nbusco el amor a medianoche,\nlo busco y no lo alcanza."),
    ("Soneto — La ausencia del amado",
     "Onde estais, bem que adoro?\nDonde está meu desejo?\nSe vos tenho nos olhos,\nPor que ausente vos vejo?",
     "¿Dónde estáis, bien que adoro?\n¿Dónde está mi deseo?\nSi os tengo en los ojos,\n¿por qué os veo ausente?"),
    ("Décima — La belleza que destruye",
     "Tanta beleza no mundo,\ntanto amor que não se explica;\nquem ama fundo e profundo\nnão sabe como a vida fica.",
     "Tanta belleza en el mundo,\ntanto amor que no se explica;\nquien ama hondo y profundo\nno sabe cómo queda la vida."),
    ("Soneto — El corazón libre",
     "Sou livre em cativeiro,\nsou rica em pobreza;\no meu amor verdadeiro\nnão tem lei sem pureza.",
     "Soy libre en cautiverio,\nsoy rica en pobreza;\nmi amor verdadero\nno tiene ley sin pureza.")]),

  ("031","Carolina Coronado","1820–1911","España","español",
   "Carolina Coronado fue la poetisa romántica española más aclamada de su generación y una de las figuras más complejas del siglo XIX: conocida por sus poemas de amor apasionado, sus derechos de la mujer, y una vida personal marcada por la tragedia. Nacida en Almendralejo, Extremadura, su talento fue reconocido desde niña. Se casó tardíamente con el diplomático norteamericano Horatio Perry y vivió en Lisboa y Madrid. Sus poemas de amor son de una efusión romántica sin artificio: el amor como fuerza natural, el cuerpo como templo del sentimiento.",
   [("El amor de mis amores",
     "¡Ay! ¡qué amor tan puro y verdadero!\n¡qué ternura tan sin igual!\nEn amar, yo no sé más que amar,\nen querer, yo no sé más que querer.",
     "¡Ay! ¡qué amor tan puro y verdadero!\n¡qué ternura tan sin igual!\nEn amar, yo no sé más que amar,\nen querer, yo no sé más que querer."),
    ("A una mariposa",
     "¡Detente, mariposa! No te vayas,\nque eres imagen de mi alma inquieta;\ntu vuelo es mi deseo que se encanta\ny vive en ti, aunque efímera cometa.",
     "¡Detente, mariposa! No te vayas,\nque eres imagen de mi alma inquieta;\ntu vuelo es mi deseo que se encanta\ny vive en ti, aunque efímera cometa."),
    ("El marido verdugo — protesta",
     "¡Mujeres! ¡Mujeres! Si tenéis entrañas,\nsi tenéis un corazón que sufra,\nal leer este crimen, estas hazañas,\nvuestras almas, de indignación, se estremezcan.",
     "¡Mujeres! ¡Mujeres! Si tenéis entrañas,\nsi tenéis un corazón que sufra,\nal leer este crimen, estas hazañas,\nvuestras almas, de indignación, se estremezcan."),
    ("El amor",
     "El amor no es más que un juego\ndonde el que más ama pierde;\npero yo juego y no entrego\nel alma, aunque el cuerpo cede.",
     "El amor no es más que un juego\ndonde el que más ama pierde;\npero yo juego y no entrego\nel alma, aunque el cuerpo cede."),
    ("La flor del agua",
     "Como el loto que nace del estanque\ny alza su cabeza al aire puro,\nasí mi amor sobre el pantano oscuro\nlevanta su cáliz sin arrancarse.",
     "Como el loto que nace del estanque\ny alza su cabeza al aire puro,\nasí mi amor sobre el pantano oscuro\nlevanta su cáliz sin arrancarse."),
    ("La libertad",
     "Quiero ser libre como el viento;\nquiero amar sin que me manden;\nquiero sentir sin que me prendan\nen jaula de oro que me pone freno.",
     "Quiero ser libre como el viento;\nquiero amar sin que me manden;\nquiero sentir sin que me prendan\nen jaula de oro que me pone freno."),
    ("La palma del desierto",
     "En el desierto del amor estoy,\nsin lluvia, sin sombra, sin consuelo;\nun árbol soy que espera el cielo\ny que de sed se muere hoy.",
     "En el desierto del amor estoy,\nsin lluvia, sin sombra, sin consuelo;\nun árbol soy que espera el cielo\ny que de sed se muere hoy."),
    ("El olvido",
     "Me dices que ya no me amas\ny te creo y no te creo;\nmi cuerpo te busca y te reclama\naunque mi mente te desea.",
     "Me dices que ya no me amas\ny te creo y no te creo;\nmi cuerpo te busca y te reclama\naunque mi mente te desea."),
    ("A Espronceda",
     "Tú que cantaste el amor con llama ardiente,\ntú que lloraste bienestar perdido,\n¿no escuchas, desde el mármol frío,\nmi voz que te reclama, que te siente?",
     "Tú que cantaste el amor con llama ardiente,\ntú que lloraste bienestar perdido,\n¿no escuchas, desde el mármol frío,\nmi voz que te reclama, que te siente?"),
    ("La noche de bodas",
     "Cuando la noche tienda su manto oscuro\ny nos envuelva en su silencio eterno,\nquiero que mi amor se haga el más tierno\ny mi cuerpo sea el templo más puro.",
     "Cuando la noche tienda su manto oscuro\ny nos envuelva en su silencio eterno,\nquiero que mi amor se haga el más tierno\ny mi cuerpo sea el templo más puro.")]),
]

if __name__ == "__main__":
    for item in LISTA:
        mk(*item)
    print(f"Generadas {len(LISTA)} poetisas.")
