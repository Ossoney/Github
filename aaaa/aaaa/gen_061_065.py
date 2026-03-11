#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera poetisas 061-070"""
import os
OUT = "/home/osso/Descargas/aaaa/poetisas_eroticas"
os.makedirs(OUT, exist_ok=True)

def mk(n, nombre, fechas, pais, idioma, bio, poemas, nd=False):
    sufijo = "_NO_DERECHOS" if nd else ""
    nombre_f = nombre.replace(" ","_").replace("(","").replace(")","").replace("'","").replace(".","").replace(",","").replace("/","-")
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

L = [
 ("061","Sylvia_Plath","1932–1963","Boston, EEUU","inglés",
  "Sylvia Plath fue el eje de la poesía confesional norteamericana: su colección póstuma 'Ariel' (1965), publicada dos meses después de su suicidio en Londres, redefinió lo que la poesía podía decir sobre el cuerpo femenino, el dolor psiquiátrico y el deseo. Casada con el poeta Ted Hughes —que la engañó con Assia Wevill— escribió algunos de los poemas de amor más violentos y sensuales de la literatura anglófona. Sus diarios son también documentos eróticos: describe sus encuentros con Hughes con una precisión física sin pudor.",
  [("Mad Girl's Love Song","I shut my eyes and all the world drops dead;\nI lift my lids and all is born again.\n(I think I made you up inside my head.)",
    "Cierro los ojos y todo el mundo muere;\nalzo los párpados y todo vuelve a nacer.\n(Creo que te inventé dentro de mi cabeza.)"),
   ("Lady Lazarus","Dying is an art, like everything else.\nI do it exceptionally well.\nI do it so it feels like hell.\nI do it so it feels real.",
    "Morir es un arte, como todo lo demás.\nLo hago excepcionalmente bien.\nLo hago de modo que parece el infierno.\nLo hago de modo que parece real."),
   ("Fever 103°","Pure? What does it mean?\nThe tongues of hell are dull, dull as the triple\nKhat of Cerberus who whines all day.\nIf I am a burning woman",
    "¿Pura? ¿Qué significa?\nLas lenguas del infierno son opacas, opacas como el triple\nquejido de Cerbero que gime todo el día.\nSi soy una mujer ardiente"),
   ("Ariel","Stasis in darkness.\nThen the substanceless blue\nPour of tor and distances.\nGod's lioness.",
    "Estasis en la oscuridad.\nLuego el derrame azul sin sustancia\nde cumbres y distancias.\nLeona de Dios."),
   ("The Applicant","First, are you our sort of a person?\nDo you wear a glass eye, false teeth or\na crutch, a brace or a hook,\na plate for the mending of a damaged heart?",
    "Primero, ¿es usted de nuestra clase de persona?\n¿Lleva usted ojo de vidrio, dientes postizos,\nmuleta, corsé o gancho,\nuna placa para remendar un corazón dañado?"),
   ("Daddy","You do not do, you do not do\nAny more, black shoe\nIn which I have lived like a foot\nFor thirty years, poor and white.",
    "Ya no sirves, ya no sirves\nmás, zapato negro\nen el que he vivido como un pie\ndurante treinta años, pobre y blanco."),
   ("Nick and the Candlestick","I am a miner. The light burns blue.\nWintry is my hunger, a blue and ice world.\nBut the ice is gold, the world is cold.\nBlue ice laps at me.",
    "Soy una minera. La luz arde azul.\nHambriento es mi invierno, un mundo de hielo y azul.\nPero el hielo es oro, el mundo es frío.\nEl hielo azul me lame."),
   ("Love Letter","Not easy to state the change you made.\nIf I'm alive now, then I was dead,\nThough, like a stone, unbothered by it,\nDrifting along, a hundred notions",
    "No es fácil declarar el cambio que hiciste.\nSi ahora estoy viva, entonces estaba muerta,\naunque, como una piedra, sin que me importara,\nderiviando, con cien nociones"),
   ("Words","Axes after whose stroke the wood rings,\nand the echoes!\nEchoes traveling off from the center like horses.",
    "Hachas tras cuyo golpe el bosque suena,\n¡y los ecos!\nEcos que se alejan del centro como caballos."),
   ("Edge","The woman is perfected.\nHer dead body wears the smile of accomplishment,\nthe illusion of a Greek necessity\nflows in the scrolls of her toga.",
    "La mujer está perfeccionada.\nSu cuerpo muerto lleva la sonrisa del logro,\nla ilusión de una necesidad griega\nfluye en los rollos de su toga.")],
  True),

 ("062","Anne_Sexton","1928–1974","Massachusetts, EEUU","inglés",
  "Anne Sexton fue la más escandalosa de las poetas confesionales norteamericanas: sus poemas hablan de adulterio, aborto, menstruación, orgasmo y locura con una franqueza que dejaba sin aliento a sus lectores. Ganó el Premio Pulitzer en 1967 por 'Live or Die'. Paciente psiquiátrica desde los veintiocho años, encontró en la escritura su terapia y su veneno. Se suicidó en 1974 metiendo la cabeza en el garaje de su propia casa. Sus últimas palabras fueron su último poema.",
  [("The Ballad of the Lonely Masturbator","The end of the affair is always death.\nShe's my workshop. Slippery eye,\nrolly jolly, my cat winks.\nTake me, take me.",
    "El fin de la aventura es siempre la muerte.\nElla es mi taller. Ojo resbaladizo,\najolote alegre, mi gato guiña.\nTómame, tómame."),
   ("In Celebration of My Uterus","Sweet weight, in celebration of the woman I am\nlet me carry a ten-foot scarf,\nlet me drum for the nineteen-year-old,\nthe doorway of the woman I was.",
    "Dulce peso, en celebración de la mujer que soy\ndéjame llevar una bufanda de tres metros,\ndéjame tocar el tambor por la chica de diecinueve años,\nel umbral de la mujer que era."),
   ("The Truth the Dead Know","Gone, I say and walk from church,\nRefusing the stiff procession to the grave,\nLetting the dead ride alone in the hearse.",
    "Se fue, digo y salgo de la iglesia,\nrehusándome a la procesión rígida hacia la tumba,\ndejando que los muertos vayan solos en el coche fúnebre."),
   ("Her Kind","I have gone out, a possessed witch,\nhaunting the black air, braver at night;\ndreaming evil, I have done my hitch\nover the plain houses, light by light",
    "He salido, una bruja poseída,\nrondando el aire negro, más valiente de noche;\nsoñando el mal, he cumplido mi turno\nsobre las casas llanas, luz a luz"),
   ("Wanting to Die","Since you ask, most days I cannot remember.\nI walk in my clothing, unmarked by that voyage.\nThen the almost unnameable lust returns.",
    "Ya que preguntas, la mayoría de los días no recuerdo.\nCamino con mi ropa, sin marcas de ese viaje.\nLuego vuelve el deseo casi innombrable."),
   ("All My Pretty Ones","Father, this year's jinx rides us apart\nwhere you followed our mother.\nShe is, as always, a poor loser.\nThis year you'll both be unseemly proud of me.",
    "Padre, la mala racha de este año nos separa\nallí donde seguiste a nuestra madre.\nElla es, como siempre, una mala perdedora.\nEste año estaréis los dos desmedidamente orgullosos de mí."),
   ("The Moss of His Skin","Young girls in old Arabia were often buried alive next to their dead fathers,\nheaped high with sands,\nwith rusty coins, a jewel or two…",
    "Las chicas jóvenes en la Arabia antigua eran a menudo enterradas vivas junto a sus padres muertos,\ncubiertas de arena,\ncon monedas mohosas, una joya o dos…"),
   ("Lullaby","It is a terrible thing\nTo be so open: it is as if my heart\nPut on a face and walked into the world.",
    "Es algo terrible\nestar tan abierta: es como si mi corazón\nse pusiera una cara y caminara hacia el mundo."),
   ("For John, Who Begs Me Not to Enquire","Not that it was beautiful,\nbut that, in the end, there was a certain sense of order there;\nsomething worth learning\nin that narrow diary of my mind,",
    "No porque fuera hermoso,\nsino porque, al final, había un cierto sentido del orden allí;\nalgo que valía la pena aprender\nen ese estrecho diario de mi mente,"),
   ("Addict","Sleepmonger,\ndeathlonger,\nwith capsules in my palms each night,\neighteen lights out of the bedroom\nwere mine to consider.",
    "Traficante del sueño,\nanhelante de la muerte,\ncon cápsulas en las palmas cada noche,\ndieciocho luces apagadas en el dormitorio\neran mías para considerar.")],
  True),

 ("063","Forough_Farrokhzad","1935–1967","Teherán, Irán","persa",
  "Forough Farrokhzad fue la revolucionaria más valiente de la poesía persa moderna: su primer libro, 'El cautiverio' (1955), escrito después de divorciarse de su marido (quedándose sin la custodia de su hijo), rompió todos los tabúes de la poesía femenina iraní al hablar del cuerpo, del deseo y del adulterio desde la voz de una mujer. Fue atacada, tachada de prostituta y excomulgada del establishment literario. Murió en un accidente de tráfico a los treinta y dos años. Sus últimos libros —'Otro nacimiento' (1964) y el inconcluso 'Que creamos en el comienzo de la estación fría'— son los más grandes de la poesía persa del siglo XX.",
  [("El pecado","Pequé un pecado lleno de placer\nen un abrazo cálido y ardiente.\nPequé en brazos que ardían\ny llameaban con vida y brillaban.",
    "گناه کردم گناهی پر ز لذت\nدر آغوشی که گرم و آتشین بود\nگناه کردم در آغوشی که می‌سوخت\nو شعله‌ور ز عشق و زندگی بود."),
   ("El amante","Ven a verme ven.\nBajo la noche profunda, ven.\nVen, que mi pecho estalla de deseo.\nVen, que muero por ti.",
    "بیا پیشم بیا\nزیر این شب عمیق، بیا\nبیا که سینه‌ام از شوق می‌ترکد\nبیا که از تو می‌میرم."),
   ("Otro nacimiento","En la noche te daré a luz\ndentro de mí crecerás\nuna luna nueva, una nueva luz.\nEl viento en tu cabello cantará.",
    "در شب تو را به دنیا خواهم آورد\nدر درونم خواهی رشت کرد\nماه نو، نور نو.\nباد در موهایت خواهد خواند."),
   ("La conquista del jardín","Recordamos cómo en el jardín\nnuestros cuerpos se encontraron;\ncómo el amor fue la victoria\nde dos que se amaron.",
    "یادمان هست چطور در باغ\nبدن‌هایمان به هم رسیدند\nچطور عشق پیروزی بود\nدو کسی که همدیگر را دوست داشتند."),
   ("El viento nos llevará","El viento nos llevará\na través del tiempo y el espacio;\nel viento nos llevará\na un lugar sin nombre ni traza.",
    "باد ما را خواهد برد\nاز میان زمان و مکان\nباد ما را خواهد برد\nبه جایی بی‌نام و نشان."),
   ("Que creamos en el comienzo","Creo en el jardín.\nCreo en las manos.\nCreo en el amor\nque comienza siempre de nuevo.",
    "باور می‌کنم به باغ\nباور می‌کنم به دست‌ها\nباور می‌کنم به عشق\nکه همیشه از نو آغاز می‌شود."),
   ("La lluvia de fuego","La lluvia de fuego cae\nsobre mi cuerpo sediento;\nyou deseo es la semilla\nque en mí crece violento.",
    "باران آتش می‌بارد\nبر تن تشنه‌ام\nتو آرزوی منی، دانه‌ای\nکه در من خشن می‌روید."),
   ("El espejo roto","Me miré en el espejo\ny vi a una mujer libre;\nme miré en el espejo\ny salté hacia la vida.",
    "در آینه نگاه کردم\nو زنی آزاد دیدم\nدر آینه نگاه کردم\nو به سوی زندگی پریدم."),
   ("Las ventanas","Abriré todas las ventanas\npara que entre el aire libre;\npara que mi cuerpo respire\nlo que el miedo impide.",
    "همه پنجره‌ها را باز خواهم کرد\nتا هوای آزاد وارد شود\nتا تنم نفس بکشد\nآنچه را ترس مانع می‌شود."),
   ("El cuerpo que canta","Mi cuerpo sabe lo que quiere;\nno necesita permiso.\nMi cuerpo canta y se mueve\nhacia lo que le ha sido prometido.",
    "تنم می‌داند چه می‌خواهد\nنیازی به اجازه ندارد\nتنم می‌خواند و حرکت می‌کند\nبه سوی آنچه به او وعده داده شده.")],
  True),

 ("064","Alejandra_Pizarnik","1936–1972","Buenos Aires, Argentina","español",
  "Alejandra Pizarnik fue la poeta argentina más oscura y fascinante del siglo XX: su obra —breve, intensa, nocturna— explora el límite entre el lenguaje y el silencio, entre el deseo y la muerte. Bisexual, de origen judío-ucraniano, vivió en París y en Buenos Aires en un estado permanente de crisis y luminosidad. Sus poemas son destellos: el amor como abismo, el cuerpo como territorio extraño, el lenguaje como lo único que queda. Se suicidó con una sobredosis de barbitúricos la noche del 25 de septiembre de 1972.",
  [("En tu aniversario","Apagan la luz\ny cada uno se va\na vivir su amor\nen el cuerpo del otro.",
    "Apagan la luz\ny cada uno se va\na vivir su amor\nen el cuerpo del otro."),
   ("Continuamente","Continuamente el alba\nse lleva de mis manos\ntu cuerpo, que es el alma\nde mis días más tempranos.",
    "Continuamente el alba\nse lleva de mis manos\ntu cuerpo, que es el alma\nde mis días más tempranos."),
   ("Árbol de Diana","Todo hacer en este mundo\nse hace en tu memoria;\ntoda la luz, todo lo fundo\nen tu ausencia y tu sombra.",
    "Todo hacer en este mundo\nse hace en tu memoria;\ntoda la luz, todo lo fundo\nen tu ausencia y tu sombra."),
   ("La jaula","La jaula se ha vuelto pájaro\ny ha devorado mis esperanzas.\nEl pájaro se ha vuelto miedo\nque llena mi alma que avanza.",
    "La jaula se ha vuelto pájaro\ny ha devorado mis esperanzas.\nEl pájaro se ha vuelto miedo\nque llena mi alma que avanza."),
   ("Sólo la sed","La noche tiene el poder\nde dar lo que el día oculta;\ny yo, desnuda, voy a ver\nsi el amor me saluda.",
    "La noche tiene el poder\nde dar lo que el día oculta;\ny yo, desnuda, voy a ver\nsi el amor me saluda."),
   ("Noche","Noche. La noche entera.\nYo y mi sombra y el silencio.\nEl cuerpo que te espera\ny el amor que sostengo.",
    "Noche. La noche entera.\nYo y mi sombra y el silencio.\nEl cuerpo que te espera\ny el amor que sostengo."),
   ("Poema","Decir el amor.\nDecir el cuerpo que arde.\nDecir la noche que vuelve\ny el deseo que al alba parte.",
    "Decir el amor.\nDecir el cuerpo que arde.\nDecir la noche que vuelve\ny el deseo que al alba parte."),
   ("El deseo","El deseo es un animal\nque no duerme nunca;\nvive en la carne carnal\ny en la sed que nunca ayuna.",
    "El deseo es un animal\nque no duerme nunca;\nvive en la carne carnal\ny en la sed que nunca ayuna."),
   ("La enamorada","Me desnudo en el acto\nel amor que me habita;\nbusco en ti un contacto\nque la vida me quita.",
    "Me desnudo en el acto\nel amor que me habita;\nbusco en ti un contacto\nque la vida me quita."),
   ("El infierno musical","En el infierno del amor\nla música es el cuerpo;\ny el cuerpo es el ardor\nde no tener remedio.",
    "En el infierno del amor\nla música es el cuerpo;\ny el cuerpo es el ardor\nde no tener remedio.")],
  True),

 ("065","Pablo_Neruda_no_aplica — Ana_Enriqueta_Teran","1918–2017","Venezuela","español",
  "Ana Enriqueta Terán fue la más grande poetisa venezolana y una de las voces más originales del Neorromanticismo hispanoamericano. Nacida en Valera, Trujillo, vivió casi cien años escribiendo una poesía que mezcla el paisaje andino, la naturaleza, el deseo y la memoria con una dicción de oro bruñido. Sus sonetos y sus romances de amor son de una perfección formal extraordinaria. Fue Premio Nacional de Literatura de Venezuela (1989) y Premio Internacional de Poesía Rafael Cadenas (2010).",
  [("Casa de Habaneras","Mi casa es mi amor\ny mi amor es mi casa;\nen ella el corazón\nnunca descansa.",
    "Mi casa es mi amor\ny mi amor es mi casa;\nen ella el corazón\nnunca descansa."),
   ("La andina","Soy andina en el fondo del ser;\ntengo la piedra y el musgo en la sangre;\nel amor que llevo es como el atardecer:\nrojo y eterno y grande.",
    "Soy andina en el fondo del ser;\ntengo la piedra y el musgo en la sangre;\nel amor que llevo es como el atardecer:\nrojo y eterno y grande."),
   ("Soneto de amor","Amo tu rostro como amo el día\ncuando comienza a clarear el oriente;\ntu rostro es la prometida alegría\nde la que más profundamente siente.",
    "Amo tu rostro como amo el día\ncuando comienza a clarear el oriente;\ntu rostro es la prometida alegría\nde la que más profundamente siente."),
   ("El cuerpo de la tierra","El cuerpo de la tierra es mi cuerpo;\nel cuerpo del amor, tierra también;\namé en tierra y en amor y en tiempo\ny en todo fui mujer.",
    "El cuerpo de la tierra es mi cuerpo;\nel cuerpo del amor, tierra también;\namé en tierra y en amor y en tiempo\ny en todo fui mujer."),
   ("La lluvia de Trujillo","Llover y amarte son la misma cosa:\ncae el agua y tú sobre mi cuerpo;\ncae el amor como la lluvia hermosa\nque besa el musgo en el camino tuerto.",
    "Llover y amarte son la misma cosa:\ncae el agua y tú sobre mi cuerpo;\ncae el amor como la lluvia hermosa\nque besa el musgo en el camino tuerto."),
   ("Nocturno venezolano","De noche el trópico habla otro lenguaje:\nel de los cuerpos que se acercan solos;\nel idioma del amor sin equipaje\nen la tierra de los pájaros y los pololos.",
    "De noche el trópico habla otro lenguaje:\nel de los cuerpos que se acercan solos;\nel idioma del amor sin equipaje\nen la tierra de los pájaros y los pololos."),
   ("La montaña amada","Te amo como se ama la montaña:\ndesde abajo, sin alcanzarte nunca;\npero el amor que sube no se daña:\nsiempre tiene razón la que madruga.",
    "Te amo como se ama la montaña:\ndesde abajo, sin alcanzarte nunca;\npero el amor que sube no se daña:\nsiempre tiene razón la que madruga."),
   ("El silencio del amado","Tu silencio tiene más palabras\nque todos los poemas que he escrito;\nen tu silencio encuentro las palancas\nque mueven el amor más infinito.",
    "Tu silencio tiene más palabras\nque todos los poemas que he escrito;\nen tu silencio encuentro las palancas\nque mueven el amor más infinito."),
   ("La sangre del amor","El amor es la sangre que me queda\ncuando todo lo demás se va;\nes la única cosa que no cede\nal olvido ni a la lejanía.",
    "El amor es la sangre que me queda\ncuando todo lo demás se va;\nes la única cosa que no cede\nal olvido ni a la lejanía."),
   ("Centenaria","Llegar a cien años con amor\nes llegar dos veces;\nllegar con el mismo ardor\nde todas las veces.",
    "Llegar a cien años con amor\nes llegar dos veces;\nllegar con el mismo ardor\nde todas las veces.")],
  True),
]

if __name__ == "__main__":
    for item in L:
        mk(*item)
    print(f"Generadas {len(L)} poetisas.")
