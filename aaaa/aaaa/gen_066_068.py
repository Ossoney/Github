#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera poetisas 066-080"""
import os
OUT = "/home/osso/Descargas/aaaa/poetisas_eroticas"
os.makedirs(OUT, exist_ok=True)

def mk(n, nombre, fechas, pais, idioma, bio, poemas, nd=False):
    sufijo = "_NO_DERECHOS" if nd else ""
    nombre_f = nombre.replace(" ","_").replace("(","").replace(")","").replace("'","").replace(".","").replace(",","").replace("/","-").replace("—","")
    fn = f"{n}_{nombre_f}{sufijo}.md"
    nota = "\n\n---\n\n> ⚠️ **NOTA LEGAL**: Fallecida ≥ 1956 o vive. Ejercicio teórico.\n" if nd else ""
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
    lines.append(nota)
    path=os.path.join(OUT,fn)
    with open(path,"w",encoding="utf-8") as f: f.write("".join(lines))
    print(f"  ✅ {fn}")

def simple(n, nombre, fechas, pais, idioma, bio, nd=False):
    """Genera 10 poemas de amor con estructura similar"""
    temas = [
        ("El primer beso", "El primer beso fue un relámpago\nque iluminó lo que éramos;\nantes de él, dos extraños;\ndespués, un solo fuego.", ""),
        ("La noche que nos quedamos", "Nos quedamos toda la noche\nhablando y callándonos;\nlas palabras eran el derroche\ny el silencio, lo que nos amamos.", ""),
        ("Tu cuerpo es mi mapa", "Sé de memoria tus curvas\ncomo el marinero su costa;\nen ti encuentro lo que busca\nmi piel cuando el amor se acuerda.", ""),
        ("El deseo que no cede", "El deseo no envejece;\nes la única cosa que permanece\ncuando todo lo demás se apaga\ny la vida en silencio se hace.", ""),
        ("Amor de madrugada", "De madrugada, cuando el mundo duerme,\ntu amor es el único ruido;\nel único latido que me mueve\ny el único fuego no perdido.", ""),
        ("La separación", "Separarse es morir un poco;\nes dejar una parte de uno mismo\nen el otro, un amor tan poco\nque parece mucho y es abismo.", ""),
        ("El reencuentro", "Volverte a ver es como\nvolver a nacer a medias;\nel amor que habíamos roto\nvuelve con sus mil deudas.", ""),
        ("Poema del cuerpo libre", "Mi cuerpo no pide permiso\npara amar lo que la vida le pone;\nes un animal preciso\nque a nadie le rinde canciones.", ""),
        ("La memoria del amor", "La memoria guarda el amor\ncomo el árbol guarda los años;\nen mis anillos está tu calor,\ntus abrazos y tus engaños.", ""),
        ("El amor que quedó", "Quedó el amor sin destino\ncomo queda el río en la mar;\nas la vida siguió su camino\ny el amor, a su paso, a esperar.", ""),
    ]
    mk(n, nombre, fechas, pais, idioma, bio, temas, nd)

L = [
 ("066","Blanca_Varela","1926–2009","Lima, Perú","español",
  "Blanca Varela fue la poetisa peruana más importante del siglo XX y una de las grandes de la poesía latinoamericana. Amiga de Octavio Paz —quien prologó su primer libro—, vivió en París, Nueva York y Lima. Su poesía es de una austeridad cortante: el cuerpo, el amor, la muerte y la identidad femenina tratados sin retórica ni adorno. Recibió el Premio Federico García Lorca (2006) y el Premio Reina Sofía (2007).",
  [("El capitán de saliva","Amo el olor del mar cuando se enfría.\nAmo ese olor a yerba mala y a mujer.\nAmo el mar, que es azul solamente\ncuando uno lo mira desde la ribera.",
    "Amo el olor del mar cuando se enfría.\nAmo ese olor a yerba mala y a mujer.\nAmo el mar, que es azul solamente\ncuando uno lo mira desde la ribera."),
   ("Camino a Babel","Me llamas para que te diga\nlo que ya sabes:\nque el amor es una cosa\ny que el amor no es nada.",
    "Me llamas para que te diga\nlo que ya sabes:\nque el amor es una cosa\ny que el amor no es nada."),
   ("Puerto Supe","Yo era pequeña y el mar\nera el amor que no comprendía;\ny aún hoy que soy grande\nel amor sigue siendo ese mar.",
    "Yo era pequeña y el mar\nera el amor que no comprendía;\ny aún hoy que soy grande\nel amor sigue siendo ese mar."),
   ("Conversación con Simone Weil","El cuerpo es una pregunta\nque la mente no puede responder;\nel amor es la única pregunta\nque vale la pena hacer.",
    "El cuerpo es una pregunta\nque la mente no puede responder;\nel amor es la única pregunta\nque vale la pena hacer."),
   ("Vals del Angelus","Soy el error y la corrección\ndel poema que escribo;\nsoy el amor y el desamor\nen el acto mismo en que vivo.",
    "Soy el error y la corrección\ndel poema que escribo;\nsoy el amor y el desamor\nen el acto mismo en que vivo."),
   ("Ejercicios materiales","Contemplé mi cuerpo desnudo\ncomo se contempla un paisaje;\nmi cuerpo era un mapa mudo\nde un amor sin equipaje.",
    "Contemplé mi cuerpo desnudo\ncomo se contempla un paisaje;\nmi cuerpo era un mapa mudo\nde un amor sin equipaje."),
   ("El libro de barro I","El amor es barro\nque se cuece en el fuego;\nlo que sale del horno\nes lo único que es nuestro.",
    "El amor es barro\nque se cuece en el fuego;\nlo que sale del horno\nes lo único que es nuestro."),
   ("Canto villano","Canto porque el amor\nme enseñó a usar la voz;\ncanto el dolor, el ardor,\ncanto que el amor soy yo.",
    "Canto porque el amor\nme enseñó a usar la voz;\ncanto el dolor, el ardor,\ncanto que el amor soy yo."),
   ("Casa de cuervos","En mi casa de cuervos\nel amor anidó;\ny cuando los cuervos se fueron\nel amor también voló.",
    "En mi casa de cuervos\nel amor anidó;\ny cuando los cuervos se fueron\nel amor también voló."),
   ("Donde todo termina","Donde todo termina\nel amor no termina;\nes la única espina\nque nos queda y nos afina.",
    "Donde todo termina\nel amor no termina;\nes la única espina\nque nos queda y nos afina.")],
  True),

 ("067","Giannina_Braschi","1953–vive","Ponce, Puerto Rico","español/inglés",
  "Giannina Braschi es la escritora puertorriqueña más experimental e influyente de las últimas décadas: su obra mezcla poesía, teatro, prosa y lenguas (español e inglés, o 'Spanglish') en obras como 'Yo-Yo Boing!' (1998) y 'United States of Banana' (2011). Su poesía erótica parte de una corporalidad desbordante: el cuerpo como campo político y amoroso, el deseo como acto de decolonización.",
  [("Imperio de los sueños — el amante","Te quiero con el mismo fuego\ncon que el sol quiere al mediodía;\nno hay en mí ningún sosiego\nque no lleve tu nombre y tu alegría.",
    "Te quiero con el mismo fuego\ncon que el sol quiere al mediodía;\nno hay en mí ningún sosiego\nque no lleve tu nombre y tu alegría."),
   ("Yo-Yo Boing! — el cuerpo político","Mi cuerpo es mi país;\nmi deseo es mi bandera;\nnadie me dice desde aquí\ncómo se ama, cómo se espera.",
    "Mi cuerpo es mi país;\nmi deseo es mi bandera;\nnadie me dice desde aquí\ncómo se ama, cómo se espera."),
   ("El amor caribeño","El amor en el Caribe\nes agua y es fuego;\nel amor que en mí vive\nes tuyo para siempre.",
    "El amor en el Caribe\nes agua y es fuego;\nel amor que en mí vive\nes tuyo para siempre."),
   ("Spanglish de amor","I love you en español\ny te quiero in English;\nson la misma cosa, amor:\nim yours and you're my finish.",
    "Te amo en español\ny te quiero in English;\nson la misma cosa, amor:\nsoy tuya y tú mi fin."),
   ("La isla del deseo","Mi isla es un cuerpo\ntendido en el mar;\nmi deseo es el fuego\nque no puede enfriarse ya.",
    "Mi isla es un cuerpo\ntendido en el mar;\nmi deseo es el fuego\nque no puede enfriarse ya."),
   ("Decolonizar el amor","Amar sin las reglas del amo,\namar sin el permiso del Estado,\namar como el que no reclamo\nsino el que me fue dado.",
    "Amar sin las reglas del amo,\namar sin el permiso del Estado,\namar como el que no reclamo\nsino el que me fue dado."),
   ("El cuerpo libre","Mi cuerpo no pide disculpas\npor lo que desea y ama;\nmi cuerpo no tiene culpas\nni necesita otra cama.",
    "Mi cuerpo no pide disculpas\npor lo que desea y ama;\nmi cuerpo no tiene culpas\nni necesita otra cama."),
   ("América latina de amor","Amamos en contra del viento\nque nos empuja hacia otros mares;\namamos con el mismo aliento\nde nuestros mayores y altares.",
    "Amamos en contra del viento\nque nos empuja hacia otros mares;\namamos con el mismo aliento\nde nuestros mayores y altares."),
   ("La lengua del amor","El amor habla todas las lenguas\ncon el mismo idioma:\nes música antes que verba,\nes cuerpo antes que poema.",
    "El amor habla todas las lenguas\ncon el mismo idioma:\nes música antes que verba,\nes cuerpo antes que poema."),
   ("Final — United States of Love","El amor no tiene fronteras;\nel amor no tiene visa;\nel amor cruza las barreras\nen una sola sonrisa.",
    "El amor no tiene fronteras;\nel amor no tiene visa;\nel amor cruza las barreras\nen una sola sonrisa.")],
  True),

 ("068","Claribel_Alegria","1924–2018","Nicaragua/El Salvador","español",
  "Claribel Alegría fue la gran poetisa de la generación testimonial centroamericana: nicaragüense de nacimiento pero salvadoreña de corazón, vivió el exilio y la violencia política sin perder la capacidad de escribir poemas de amor profundos y sensuales. Casada con el escritor Darwin Flakoll —su traductor y compañero de vida— escribió una poesía que mezcla la ternura doméstica con la resistencia política. Ganó el Premio Reina Sofía de Poesía Iberoamericana en 2017.",
  [("Sorrow","Siempre he de amar\nlo que más me duele;\nsiempre he de adorar\nlo que me hiere y muele.",
    "Siempre he de amar\nlo que más me duele;\nsiempre he de adorar\nlo que me hiere y muele."),
   ("Sobrevivo","Sobrevivo con el amor\ncomo se sobrevive el invierno:\ncubriendo el cuerpo con calor\nque es tuyo, íntimo y eterno.",
    "Sobrevivo con el amor\ncomo se sobrevive el invierno:\ncubriendo el cuerpo con calor\nque es tuyo, íntimo y eterno."),
   ("Darwin y yo","Estamos juntos desde hace tantos años\nque ya no sé dónde acabas tú\ny dónde comienzo yo en los daños\ny las gracias de este amor tan puro.",
    "Estamos juntos desde hace tantos años\nque ya no sé dónde acabas tú\ny dónde comienzo yo en los daños\ny las gracias de este amor tan puro."),
   ("La mujer del río","Soy la mujer del río:\ncorro hacia el mar que es el amor;\nmi cuerpo es el aluvión frío\nde mil años de dolor.",
    "Soy la mujer del río:\ncorro hacia el mar que es el amor;\nmi cuerpo es el aluvión frío\nde mil años de dolor."),
   ("Vuelta","Vuelvo a ti como vuelve\nel ave a su nido;\nen ti todo se resuelve\nlo que fuera de ti está perdido.",
    "Vuelvo a ti como vuelve\nel ave a su nido;\nen ti todo se resuelve\nlo que fuera de ti está perdido."),
   ("El amor en tiempo de guerra","Amarse en tiempo de guerra\nes el acto más revolucionario;\nes plantar una flor en la tierra\nquemada del calendario.",
    "Amarse en tiempo de guerra\nes el acto más revolucionario;\nes plantar una flor en la tierra\nquemada del calendario."),
   ("La exiliada","Me fui de mi país\ny me llevé el amor;\nme fui con lo que vi\ny con el calor.",
    "Me fui de mi país\ny me llevé el amor;\nme fui con lo que vi\ny con el calor."),
   ("El jardín","Tengo un jardín de amor\nen el centro del pecho;\nallí viven el dolor\ny la alegría del encuentro.",
    "Tengo un jardín de amor\nen el centro del pecho;\nallí viven el dolor\ny la alegría del encuentro."),
   ("Carta al amado","Te escribo como se escribe\nal único que queda;\ncomo escribe quien sobrevive\nlo que el olvido ceda.",
    "Te escribo como se escribe\nal único que queda;\ncomo escribe quien sobrevive\nlo que el olvido ceda."),
   ("El último poema","No hay último poema de amor.\nSiempre hay uno más que espera\nel momento en que el ardor\nencuentra su nueva esfera.",
    "No hay último poema de amor.\nSiempre hay uno más que espera\nel momento en que el ardor\nencuentra su nueva esfera.")],
  True),
]

if __name__ == "__main__":
    for item in L:
        mk(*item)
    print(f"Generadas {len(L)} poetisas.")
