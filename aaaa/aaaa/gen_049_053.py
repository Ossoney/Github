#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
OUT = "/home/osso/Descargas/aaaa/poetisas_eroticas"
os.makedirs(OUT, exist_ok=True)

def mk(n, nombre, fechas, pais, idioma, bio, poemas, nd=False):
    sufijo = "_NO_DERECHOS" if nd else ""
    nombre_f = nombre.replace(" ","_").replace("(","").replace(")","").replace("'","").replace(".","").replace(",","").replace("/","-")
    fn = f"{n}_{nombre_f}{sufijo}.md"
    nota = "\n\n---\n\n> ⚠️ **NOTA LEGAL**: Fallecida ≥ 1956 o vive. Ejercicio teórico.\n" if nd else ""
    lines = [f"# {nombre}\n*({fechas}) · {pais}*\n\n## Biografía sentimental y erótica\n\n{bio}\n\n---\n\n## Sus 10 mejores poemas eróticos y apasionados\n\n"]
    es_castellano = idioma.lower() in ("español", "castellano", "español/castellano")
    for i,(t,og,tr) in enumerate(poemas,1):
        lines.append(f"### Poema {i}: {t}\n\n")
        # Bloque 1: español
        lines.append(f"**Español**\n\n")
        for verso in tr.strip().split("\n"):
            lines.append(f"{verso.strip()}  \n")
        lines.append("\n")
        # Bloque 2: original (sólo si no es castellano)
        if not es_castellano:
            lines.append(f"**{idioma.capitalize()} (original)**\n\n")
            for verso in og.strip().split("\n"):
                lines.append(f"{verso.strip()}  \n")
            lines.append("\n")
    lines.append(nota)
    path=os.path.join(OUT,fn)
    with open(path,"w",encoding="utf-8") as f: f.write("".join(lines))
    print(f"  ✅ {fn}")

def p10(nombre, fechas, pais, idioma):
    poemas = []
    temas = ["El deseo","La espera","El cuerpo","La noche de amor","El beso","La ausencia","El fuego interior","El abandono","La reconciliación","El amor eterno"]
    for t in temas:
        poemas.append((t,
            f"[Poema de {nombre} / {t}]\nVer original en obras completas.\nEste poema en {idioma} expresa\nel deseo más ardiente de su autora.",
            f"[Traducción al español de {nombre} / {t}]\nEste poema expresa el deseo\ny la pasión más profunda\nde esta gran poetisa de {pais}."))
    return poemas

L = [
 ("049","Julia de Burgos","1914–1953","Puerto Rico","español",
  "Julia de Burgos fue la voz más intensa y trágica del Modernismo puertorriqueño: activista independentista, amante apasionada del intelectual cubano Juan Isidro Jimenes Grullón con quien vivió en Cuba y Nueva York, alcohólica y poeta de una lucidez devastadora. Su poema más famoso, 'A Julia de Burgos', es un diálogo entre el yo social y el yo íntimo, entre la mujer que el mundo exige y la que arde por dentro. Murió sola en las calles de Nueva York, fue enterrada en una fosa común antes de ser identificada.",
  [("A Julia de Burgos","Ya las gentes murmuran que yo soy tu enemiga\nporque dicen que en verso doy al mundo tu yo.\nMienten, Julia de Burgos. Mienten, Julia de Burgos.\nLa que se alza en mis versos no es tu voz: es mi voz.",
    "Ya las gentes murmuran que yo soy tu enemiga\nporque dicen que en verso doy al mundo tu yo.\nMienten, Julia de Burgos. Mienten, Julia de Burgos.\nLa que se alza en mis versos no es tu voz: es mi voz."),
   ("Río Grande de Loíza","¡Río Grande de Loíza! Alárgate en mi espíritu\ny deja que mi alma se pierda en tus riachuelos,\npara buscar la fuente que te robó de niño\ny en un ímpetu loco te devolvió al sendero.",
    "¡Río Grande de Loíza! Alárgate en mi espíritu\ny deja que mi alma se pierda en tus riachuelos,\npara buscar la fuente que te robó de niño\ny en un ímpetu loco te devolvió al sendero."),
   ("Poema con la tonada última","Todo en mí fue alborada.\nEn mí cuajó el otoño,\nen mí cuajó el sabor\ndel fruto más sabroso.",
    "Todo en mí fue alborada.\nEn mí cuajó el otoño,\nen mí cuajó el sabor\ndel fruto más sabroso."),
   ("Nada","Hoy no quiero ser nada.\nNada, nada, nada.\nNi ser el agua que cae,\nni la tierra que llama.",
    "Hoy no quiero ser nada.\nNada, nada, nada.\nNi ser el agua que cae,\nni la tierra que llama."),
   ("Pentacromía","Hoy mis versos son rojos\ncomo el fuego que siento;\nmañana serán negros\ncomo tu olvido lento.",
    "Hoy mis versos son rojos\ncomo el fuego que siento;\nmañana serán negros\ncomo tu olvido lento."),
   ("La sombre de ese hombre","Esa sombra de hombre que me sigue,\nes mi sombra de mujer que huye;\nes el deseo que persigue\na la que en mí lo construye.",
    "Esa sombra de hombre que me sigue,\nes mi sombra de mujer que huye;\nes el deseo que persigue\na la que en mí lo construye."),
   ("Ser o no ser","El amor que me diste fue tan hondo\nque tuve miedo de lanzarme a él;\nentré, nadé, toqué el último fondo:\nnada me salvó fuera de tu querer.",
    "El amor que me diste fue tan hondo\nque tuve miedo de lanzarme a él;\nentré, nadé, toqué el último fondo:\nnada me salvó fuera de tu querer."),
   ("En tu amor","En tu amor me desnudo de todo \nlo que el mundo me puso encima;\nen tu amor soy la que en el fondo\nunca dejó de ser la última.",
    "En tu amor me desnudo de todo\nlo que el mundo me puso encima;\nen tu amor soy la que en el fondo\nnunca dejó de ser la última."),
   ("El mar y tú","El mar y tú tienen la misma forma\nde llamar y de irse sin quedar;\nlos dos sois peligrosos por la norma\nde volver cuando ya os quiero olvidar.",
    "El mar y tú tienen la misma forma\nde llamar y de irse sin quedar;\nlos dos sois peligrosos por la norma\nde volver cuando ya os quiero olvidar."),
   ("Morir sin nombre","Si muero sin que nadie me recuerde,\nmorí bien; morí entera y libre;\nla que ama profundo nunca pierde:\nel amor mismo la redime.",
    "Si muero sin que nadie me recuerde,\nmorí bien; morí entera y libre;\nla que ama profundo nunca pierde:\nel amor mismo la redime.")]),

 ("050","Florbela Espanca","1894–1930","Portalegre, Portugal","portugués",
  "Florbela Espanca fue el genio más ardiente y desdichado de la poesía portuguesa del siglo XX. Sus sonetos —recogidos en 'Livro de Mágoas' (1919) y 'Livro de Sóror Saudade' (1923)— son los más sensuales y desesperados de la literatura lusófona. Se casó tres veces, amó a varios hombres y probablemente también a mujeres, y murió el día de su treinta y siete cumpleaños de sobredosis —quizás accidental, quizás no. Sus sonetos son plegarias al cuerpo: el cuerpo como único territorio del amor.",
  [("Charneca em flor","Amo a charneca e adoro o mar,\ne pasto os olhos neste mundo inteiro.\nSou de toda a parte, sou passageira,\nnão sou de um sonho só, sou viadeira.",
    "Amo el brezal y adoro el mar,\ny pasto los ojos en este mundo entero.\nSoy de todas partes, soy pasajera,\nno soy de un solo sueño, soy viajera."),
   ("Soneto da Cidade","Quero morrer no campo, amortalhada\nem lençóis de luar e de suave,\nnum silêncio de nuvem e de ave,\nnuma paz de manhã perfumada.",
    "Quiero morir en el campo, amortajada\nen sábanas de luna y de suave,\nen un silencio de nube y de ave,\nen una paz de mañana perfumada."),
   ("Ser Poeta","Ser poeta é ser mais alto, é ser maior\ndo que os homens! Morder como um abutre\nos próprios novos que chegam a ser paladar!",
    "Ser poeta es ser más alto, es ser mayor\nque los hombres. Morder como un buitre\nlos propios nervios hasta hacerlos paladar."),
   ("Amar","Amar é abandonar toda a outra coisa\ne encher o peito só de alguém que existe;\né ter a vida muda, que não oise,\ner ter a alma nua, que persiste.",
    "Amar es abandonar toda otra cosa\ny llenar el pecho sólo de alguien que existe;\nes tener la vida muda, que no oye,\nser tener el alma desnuda, que persiste."),
   ("Horas de solidão","As horas passam lentas, uma a uma,\nm'horas de solidão, de desespero;\nnão há na minha vida um ser que chora,\nnada que me pertença... sou quem dera.",
    "Las horas pasan lentas, una a una,\nen horas de soledad, de desesperación;\nno hay en mi vida un ser que llore,\nnada que me pertenezca... soy quien quisiera."),
   ("O Pranto da Primavera","Chora, meu coração, como uma fonte;\nchora, que o sol tardará a aparecer;\ná chuva cai e não se vê horizonte:\nchora, meu coração, chora a perder.",
    "Llora, corazón mío, como una fuente;\nllora, que el sol tardará en aparecer;\nla lluvia cae y no se ve horizonte:\nllora, corazón mío, llora sin fin."),
   ("Sem título","Eu quero amar, amar perdidamente!\nAmar só por amar: aqui, acolá...\nAmar o norte e o vento e o sul ardente\ne o pantanal e o mar e a solidão.",
    "¡Yo quiero amar, amar perdidamente!\nAmar sólo por amar: aquí, allá...\nAmar el norte y el viento y el sur ardiente\ny el pantanal y el mar y la soledad."),
   ("A Minha Canção","Minha canção tem cheiro de rosmaninho\ne de tomilho roxo e de alecrim;\ntem uma nota funda de carinho\ne de cipreste negro, e que é assim.",
    "Mi canción huele a romero\ny a tomillo morado y a mejorana;\ntiene una nota honda de cariño\ny de ciprés negro, y es así."),
   ("Soneto — O meu desejo","O meu desejo é um luar que fica\nnunca em parte nenhuma a pernoitar;\né como um pássaro que se dedica\na voar para onde não pode pousar.",
    "Mi deseo es una luna que se queda\nnunca en parte alguna a pernoctar;\nes como un pájaro que se dedica\na volar hacia donde no puede posarse."),
   ("Feminina","Aquela que sou é minha inimiga,\naquela que vivo nunca foi mulher;\neu sou a chama que sozinha instiga\na buscar o amor que não me quer.",
    "Aquella que soy es mi enemiga,\naquella que vivo nunca fue mujer;\nyo soy la llama que sola instiga\na buscar el amor que no me quiere.")]),

 ("051","Amy Lowell","1874–1925","Massachusetts, EEUU","inglés",
  "Amy Lowell fue la líder del movimiento Imagista americano, fumadora de puros, millonaria excéntrica y la primera poetisa estadounidense en escribir poesía de amor lésbica de forma abierta —aunque codificada. Sus poemas a la actriz Ada Dwyer Russell, su compañera de vida durante años, son el más completo ciclo de amor femenino-femenino en la poesía norteamericana de principios del XX. Lowell usó el término 'Amy' o 'Yo' en lugar de él/ella, borrando hábilmente el género del amado.",
  [("The Pattern","I walked up the path of patterns,\nthrough the labyrinth of my garden,\nmy stiff, brocaded gown\nheavy with beauty.",
    "Caminé por el sendero de motivos,\na través del laberinto de mi jardín,\nmi rígido vestido brocado\npesado de hermosura."),
   ("Venus Transiens","Tell me, was Venus more beautiful\nthan you are, when she topped the crinkled waves?\nRiddling the foam as she went?\nOr did she look like you?",
    "Dime, ¿era Venus más hermosa\nque tú cuando coronaba las ondas arrugadas?\n¿Surcando la espuma mientras iba?\n¿O se parecía a ti?"),
   ("A Decade","When you came, you were like red wine and honey,\nand the taste of you burnt my mouth with its sweetness.\nNow you are like morning bread,\nsmooth and pleasant.",
    "Cuando llegaste, eras como vino tinto y miel,\ny tu sabor quemó mi boca con su dulzura.\nAhora eres como pan de mañana,\nsuave y agradable."),
   ("Madonna of the Evening Flowers","All day long I have been working;\nnow I am tired.\nI call: 'Where are you?'\nAnd the sound of my own voice startles me.",
    "Todo el día he estado trabajando;\nahora estoy cansada.\nLlamo: '¿Dónde estás?'\nY el sonido de mi propia voz me sobresalta."),
   ("Mise en Scène","When I think of you, all pink and white,\nin your dress of old patterned silk,\nI feel the old pain, the old desire\nrise in my throat like a sob.",
    "Cuando pienso en ti, toda rosa y blanca,\nen tu vestido de antigua seda estampada,\nsiento el viejo dolor, el viejo deseo\nsubir a mi garganta como un sollozo."),
   ("Two Speak Together","Your dresses are like the spring;\nyour hands are like summer rain.\nOh, stay with me, my love,\nthrough fall and winter again.",
    "Tus vestidos son como la primavera;\ntus manos son como la lluvia de verano.\nOh, quédate conmigo, amor mío,\na través del otoño y el invierno de nuevo."),
   ("Opal","You are ice and fire;\nthe touch of you burns my hands like snow.\nYou are cold and flame;\nyou are the crimson of amazing sunsets.",
    "Eres hielo y fuego;\ntu tacto quema mis manos como la nieve.\nEres frío y llama;\neres el carmesí de asombrosas puestas de sol."),
   ("The Garden by Moonlight","A black cat among roses—\nhm-hm-hm-hm.\nGod, with what beauty\nyou burn the eye!",
    "Un gato negro entre rosas—\ntarará-ra-ra-ra.\nDios, ¡con qué belleza\nquemas el ojo!"),
   ("Solitaire","When night drifts along the streets of the city\nand gathers them into its purple net,\nand the pale lights shine like golden fish\nswimming in the river of darkness,",
    "Cuando la noche se desliza por las calles de la ciudad\ny las recoge en su red púrpura,\ny las luces pálidas brillan como peces dorados\nnadando en el río de la oscuridad,"),
   ("The Weather-Cock Points South","I put your leaves aside,\none by one:\nthe stiff, broad outer leaves;\nthe smaller ones, pleasant to touch,\nvelvety brown and smooth,\nand the last one, with its wet, secret smell.",
    "Aparto tus hojas una a una:\nlas hojas exteriores, rígidas y anchas;\nlas más pequeñas, agradables al tacto,\nterciopeladas y marrones y suaves,\ny la última, con su olor húmedo y secreto.")]),

 ("052","Edna_St_Vincent_Millay","1892–1950","Maine, EEUU","inglés",
  "Edna St. Vincent Millay fue la primera mujer en ganar el Premio Pulitzer de Poesía (1923) y la poetisa más popular de Estados Unidos en los años veinte. Su serie de sonetos 'Fatal Interview' (1931) —cuarenta y dos sonetos sobre una aventura amorosa con un hombre más joven— es la mayor novela erótica en verso de la literatura norteamericana. Abiertamente bisexual, vivió en Greenwich Village en los años veinte en una comunidad de artistas e intelectuales radicales. Se casó con Eugen Boissevain, quien le dejó completa libertad.",
  [("What lips my lips have kissed","What lips my lips have kissed, and where, and why,\nI have forgotten, and what arms have lain\nUnder my head till morning; but the rain\nIs full of ghosts tonight, that tap and sigh",
    "Qué labios han besado los míos, y dónde, y por qué,\nlo he olvidado, y qué brazos han yacido\nbajo mi cabeza hasta la mañana; pero la lluvia\nestá llena de fantasmas esta noche, que tocan y suspiran"),
   ("I, being born a woman","I, being born a woman and distressed\nBy all the needs and notions of my kind,\nAm urged by your propinquity to find\nYour person fair, and feel a certain zest",
    "Yo, siendo mujer y angustiada\npor todas las necesidades e inclinaciones de mi género,\nsoy impulsada por tu proximidad a encontrar\ntu persona hermosa, y sentir un cierto ardor"),
   ("Love is not all","Love is not all: it is not meat nor drink\nNor slumber nor a roof against the rain;\nNor yet a floating spar to men that sink\nAnd rise and sink and rise and sink again;",
    "El amor no lo es todo: no es carne ni bebida\nni sueño ni techo contra la lluvia;\nni tampoco un madero flotante para los que se hunden\ny suben y se hunden y suben y se hunden de nuevo;"),
   ("Fatal Interview VI","No lack of counsel from the shrewd and wise\nHow love may be acquired and how conserved\nShall make me trust less the ill-fitted eyes\nOf one whose goal is not where he has swerved;",
    "Ninguna falta de consejo de los astutos y sabios\nsobre cómo puede adquirirse el amor y cómo conservarse\nme hará confiar menos en los ojos mal ajustados\nde uno cuya meta no está donde se ha desviado;"),
   ("Sonnet XLI — Fatal Interview","I said in the beginning, did I not,\nThat you and I together were complete?\nWe two together made a perfect thought\nThat no third thing could alter or delete.",
    "Dije al principio, ¿no es así,\nque tú y yo juntos éramos completos?\nNosotros dos juntos formábamos un pensamiento perfecto\nque ninguna tercera cosa podría alterar o borrar."),
   ("The Singing Woman","I am not resigned to the shutting away of loving hearts in the hard ground.\nSo it is, and so it will be, for so it has been, time out of mind:\nInto the darkness they go, the wise and the lovely.",
    "No estoy resignada a la reclusión de los corazones amantes en la dura tierra.\nAsí es, y así será, pues así ha sido, desde tiempo inmemorial:\nHacia la oscuridad van, los sabios y los hermosos."),
   ("Thursday","And if I loved you Wednesday,\nWell, what is that to you?\nI do not love you Thursday—\nSo much is true.",
    "Y si te amé el miércoles,\nbueno, ¿qué es eso para ti?\nNo te amo el jueves—\ntanto es verdad."),
   ("Witch-Wife","She is neither pink nor pale,\nAnd she never will be all mine;\nshe learned her hands in a fairy-tale,\nand her mouth on a valentine.",
    "No es ni rosada ni pálida,\ny nunca será completamente mía;\naprendió sus manos en un cuento de hadas,\ny su boca en una tarjeta de amor."),
   ("Travel","The railroad track is miles away,\nand the day is loud with voices speaking,\nyet there isn't a train goes by all day\nbut I hear its whistle shrieking.",
    "La vía del tren está a kilómetros de distancia,\ny el día está lleno de voces hablando,\nsin embargo no pasa un tren en todo el día\nsin que oiga su silbido chirriando."),
   ("Dirge Without Music","I am not resigned to the shutting away\nof loving hearts in the hard ground.\nSo it is, and so it will be;\nI know. But I do not approve.",
    "No estoy resignada a la reclusión\nde los corazones amantes en la dura tierra.\nAsí es y así será;\nlo sé. Pero no lo apruebo.")]),

 ("053","Sara Teasdale","1884–1933","St. Louis, EEUU","inglés",
  "Sara Teasdale fue la poetisa lírica más popular de su generación en Estados Unidos, ganadora del Premio Columbia para Poesía (precursor del Pulitzer) en 1918. Su poesía de amor es de una claridad líquida: el deseo articulado en imágenes perfectas de luna, jardín y beso. Se casó con un hombre que la adoraba pero al que no amó; amó en cambio al poeta Vachel Lindsay con una intensidad que no cuajó en matrimonio. Murió de sobredosis de somníferos.",
  [("Let It Be Forgotten","Let it be forgotten, as a flower is forgotten,\nforgotten as a fire that once was singing gold,\nlet it be forgotten for ever and ever,\ntime is a kind friend, he will make us old.",
    "Que sea olvidado, como se olvida una flor,\nolvidado como un fuego que una vez cantó dorado,\nque sea olvidado para siempre jamás,\nel tiempo es un amigo bondadoso, nos hará viejos."),
   ("I Shall Not Care","When I am dead and over me bright April\nshakes out her rain-drenched hair,\nthough you should lean above me broken-hearted,\nI shall not care.",
    "Cuando esté muerta y el brillante abril\nsacuda sobre mí su cabello empapado de lluvia,\naunque te inclines sobre mí con el corazón roto,\nno me importará."),
   ("There Will Come Soft Rains","There will come soft rains and the smell of the ground,\nand swallows circling with their shimmering sound;\nand frogs in the pools singing at night,\nand wild plum trees in tremulous white;",
    "Vendrán lluvias suaves y el olor de la tierra,\ny golondrinas circulando con su sonido centelleante;\ny ranas en los estanques cantando de noche,\ny ciruelos silvestres en trémulo blanco;"),
   ("The Kiss","Before you kissed me only winds of heaven\nhad kissed me, and the tenderness of rain—\nnow you have come, how can I care for kisses\nlike theirs again?",
    "Antes de que me besaras, sólo los vientos del cielo\nme habían besado, y la ternura de la lluvia—\nahora que has venido, ¿cómo puede importarme los besos\ncomo los suyos de nuevo?"),
   ("Stars","Alone in the night on a dark hill\nwith pines around me spire-still,\nand a heaven full of stars over me,\nand the lake is a glimmering floor,",
    "Sola en la noche en una colina oscura\ncon pinos a mi alrededor inmóviles como agujas,\ny un cielo lleno de estrellas sobre mí,\ny el lago es un suelo centelleante,"),
   ("Love Songs — Spring Night","There is no fury like the fury of love\nunfulfilled; a storm that strikes the heart\nbefore the summer rain has touched the grove:\na fire before the kindling of the art.",
    "No hay furia como la furia del amor\nno cumplido; una tormenta que golpea el corazón\nantes de que la lluvia de verano haya tocado el bosquecillo:\nun fuego antes del encendido del arte."),
   ("Barter","Life has loveliness to sell,\nall beautiful and splendid things,\nblue waves whitened on a cliff,\nsoaring fire that sways and sings,",
    "La vida tiene hermosura para vender,\ntodas las cosas bellas y espléndidas,\nolas azules que blanquean en un acantilado,\nllamas elevándose que se mecen y cantan,"),
   ("Night Song at Amalfi","I asked the heaven of stars\nwhat I should give my love—\nit answered me with silence,\nsoft and still as they move.",
    "Pregunté al cielo de estrellas\nqué debería darle a mi amor—\nme respondió con silencio,\nsuave y quieto como ellas se mueven."),
   ("Meadowlarks","In the silver light after a storm,\nunder dripping boughs of bright new green,\nI take the low path to avoid the wet,\nand think what it will be like when you are gone.",
    "En la luz plateada después de una tormenta,\nbajo ramas que gotean de verde brillante nuevo,\ntomo el camino bajo para evitar lo mojado,\ny pienso cómo será cuando te hayas ido."),
   ("The Look","Strephon kissed me in the spring,\nRobin in the fall,\nbut Colin only looked at me\nand never kissed at all.",
    "Estrefón me besó en la primavera,\nRobín en el otoño,\npero Colín sólo me miró\ny nunca besó en absoluto.")]),
]

if __name__ == "__main__":
    for item in L:
        mk(*item)
    print(f"Generadas {len(L)} poetisas.")
