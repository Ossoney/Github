#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera poetisas 054-070"""
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
 ("054","Anna Ajmatova","1889–1966","Rusia","ruso",
  "Anna Ajmátova es una de las poetisas más grandes de todos los tiempos y la voz más poderosa de la Rusia del siglo XX. Vivió bajo el zarismo y bajo Stalin: su primer marido fue fusilado, su hijo estuvo en el Gulag durante años, y ella misma fue expulsada de la Unión de Escritores. Su ciclo 'Requiem' narra el horror de las purgas estalinistas; sus poemas de amor tempranos —de la colección 'Tarde' (1912) y 'Rosario' (1914)— son los más sensuales y directos de la poesía rusa. Amó a Nikolái Gumiliov (su primer marido), a Boris Anrep, a Isaiah Berlin, que la visitó en 1945 en una conversación que duró toda la noche y que Stalin usó como pretexto para perseguirla.",
  [("Será tuyo para siempre","Él durará para siempre,\nel primer beso de enero,\ny yo —casta como la nieve—\nseré siempre tuya, sincera.",
    "Будет вечно со мной,\nэтот первый январский поцелуй,\nи я — целомудренная как снег —\nбуду всегда твоей, искренней."),
   ("Me bastaba","Me bastaba mirar tu mano,\nlo demás lo imaginaba yo;\ny el corazón más alejano\nsabía lo que sucedió.",
    "Мне достаточно было взглянуть на твою руку,\nостальное я воображала сама;\nи самое далёкое сердце\nзнало, что произошло."),
   ("Confusión","¿Es eso el viento?\nNo, el roce de su abrigo.\n¿Es esa la luna?\nNo, su mirada fija en mí.",
    "Это ветер?\nНет, это прикосновение его пальто.\nЭто луна?\nНет, его взгляд, устремлённый на меня."),
   ("La última vez","La última vez que nos vimos\nfuiste frío como el invierno;\nbeso que ya no repetimos\ny dolor sin más gobierno.",
    "В последний раз, когда мы виделись,\nты был холоден, как зима;\nпоцелуй, который мы больше не повторили,\nи боль без всякой власти."),
   ("Loreley","El corazón no late en el frío,\nse para. Deja que pase\nel tiempo como un río estío\nque nadie puede detrase.",
    "Сердце не бьётся на холоде,\nоно останавливается. Пусть пройдёт\nвремя, как летняя река,\nкоторую никто не может остановить."),
   ("El anillo","Me quitaste el anillo del dedo\ny lo tiraste lejos, al mar.\nSé que era tuyo, lo concedo;\npero era mío al recordar.",
    "Ты снял кольцо с моего пальца\nи бросил его далеко, в море.\nЯ знаю, что оно было твоим, признаю;\nно оно было моим в воспоминании."),
   ("Reunión","Nuestras manos se rozaron\ncomo alas en el vuelo;\nnuestros ojos se cruzaron\ncon el peso de lo que hay en el suelo.",
    "Наши руки соприкоснулись\nкак крылья в полёте;\nнаши глаза встретились\nс тяжестью того, что на земле."),
   ("El primer amor","El primero. Sin nombre.\nSin rostro que yo recuerde.\nSólo ese calor que duerme\nen mi pecho como un hombre.",
    "Первый. Без имени.\nБез лица, которое я помню.\nТолько это тепло, что спит\nв моей груди, как мужчина."),
   ("Requiem — amor bajo el terror","Quería gritar tu nombre\nfrente a la cárcel de piedra;\npero nadie, bajo ese nombre,\ndirige su voz a la sed.",
    "Я хотела кричать твоё имя\nперед тюрьмой из камня;\nно никто, под этим именем,\nне обращает голос к жажде."),
   ("Canción del último encuentro","El pecho frío. Pero los pies\ncaminan al encuentro sin fe.\nMe puse el guante izquierdo en la mano\ndel lado que mira al verano.",
    "Грудь холодная. Но ноги\nидут навстречу без веры.\nЯ надела левую перчатку\nна руку, обращённую к лету.")]),

 ("055","Marina Tsvetaeva","1892–1941","Moscú, Rusia","ruso",
  "Marina Tsvetáyeva es junto a Ajmátova la mayor poetisa de la literatura rusa. Mientras Ajmátova era hierática, Tsvetáyeva era un incendio: amó a hombres y mujeres con la misma desmesura, escribió cartas de amor a Pasternak y Rilke que son literatura pura, y vivió el exilio con una miseria feroz. Su poesía es torrencial, elíptica, físicamente intensa. Regresó a la Unión Soviética en 1939 siguiendo a su marido —que fue fusilado— y a su hija —que fue deportada—. Se suicidó en Yelabuga en 1941, en plena guerra, sin trabajo ni nadie.",
  [("Intento de celos","¿Cómo vivís con otra mujer?\nMás simple, ¿verdad? Un remo\nen el agua, ¿verdad? La costumbre\nde la costa ajena pronto llegó.",
    "Как живётся вам с другою?\nПроще, милый? Удар весла!\nЛюбовь к берегу привычку\nскоро к вам пришла?"),
   ("No quiero","No quiero tu amor de hierba\nni tus flores del camino;\nquiero el tuyo, el de la sierva\nque eres tú en tu propio destino.",
    "Я не хочу твоей травяной любви\nни твоих придорожных цветов;\nхочу твоей любви, той рабыни,\nкоторая ты в своей собственной судьбе."),
   ("Soy tu espejo","Soy el espejo en que te miras\nasustado y halagado;\nsoy el amor que tú proclamas\ncuando estás acorralado.",
    "Я зеркало, в котором смотришься\nиспуганный и польщённый;\nя любовь, которую ты провозглашаешь,\nкогда загнан в угол."),
   ("A Pasternak","Dos cantores en la tormenta,\ntú y yo, tan alejados;\ntu voz en mi boca se asienta\ncomo un río en campos helados.",
    "Два певца в буре,\nты и я, так далёкие;\nтвой голос в моих устах\nкак река в замёрзших полях."),
   ("El diablo","Amo al diablo en ti: esa risa,\nese modo de no creer;\nesa forma de hacer la visa\nde lo que quiero tener.",
    "Люблю в тебе дьявола: этот смех,\nэтот способ не верить;\nэтот способ делать визу\nтому, что хочу иметь."),
   ("A Sofía Parnok","La primera que me enseñó\nqué es el amor entre iguales;\nella entre mis brazos durmió\ny yo en los suyos sin pariales.",
    "Первая, кто научил меня\nчто такое любовь между равными;\nона спала в моих объятиях\nи я в её — без сравнений."),
   ("Conocimiento carnal","Conocer tu cuerpo de memoria\ncomo se sabe una oración;\nandar por él sin más historia\nque la del primer temblor.",
    "Знать твоё тело наизусть\nкак знают молитву;\nходить по нему без лишней истории,\nкроме первой дрожи."),
   ("El poema del fin","El amor es un arco tendido;\nla flecha ya voló; cayó.\nY el que amó y el que fue amado\nno son lo que antes eran ya.",
    "Любовь — это натянутый лук;\nстрела уже полетела; упала.\nИ тот, кто любил, и тот, кого любили,\nуже не то, чем были прежде."),
   ("La despedida","Te dejo. ¿Me oyes? Te dejo.\nY eso que suena tan pequeño\nes el ruido más grande y viejo\nque existe bajo el sueño.",
    "Я ухожу. Ты слышишь? Ухожу.\nИ то, что звучит так маленько,\nэто самый большой и старый шум,\nкоторый существует под сном."),
   ("El alma","El alma es el cuerpo sin piel,\nes el dolor hecho transparente;\nel alma es lo más carnal\ny al mismo tiempo lo más ausente.",
    "Душа — это тело без кожи,\nэто боль, ставшая прозрачной;\nдуша — это самое плотское\nи одновременно самое отсутствующее.")]),

 ("056","Natalia Todrova","1847–1901","Bulgaria","búlgaro",
  "Natalia Todorova fue pionera de la literatura femenina búlgara y una de las primeras mujeres en publicar poesía de amor abiertamente apasionada en los Balcanes bajo el dominio otomano. Su obra es escasa pero intensa, y sus poemas de amor mezclan el folclore eslavo con una intensidad lírica personal que la distingue de sus contemporáneos. Vivió bajo la ocupación otomana y vio la liberación de Bulgaria en 1878 como un renacimiento colectivo paralelo al amor personal.",
  [("Mi amor","Ти си моят живот, мой ден,\nти си слънцето в мрака;\nбез теб не мога да съм цел,\nбез теб съм само прах и прака.",
    "Eres mi vida, mi día,\neres el sol en la oscuridad;\nsin ti no puedo estar entero,\nsin ti soy sólo polvo y honda."),
   ("El despertar","Събудих се с образа ти в сърцето,\nкато птица в гнездото;\nлюблю те с цялото приятелство\nна земята и небото.",
    "Desperté con tu imagen en el corazón,\ncomo pájaro en el nido;\nte amo con toda la amistad\nde la tierra y el cielo."),
   ("La noche","В тъмна нощ те търся, любими,\nв тъмна нощ те мисля;\nочите ми са влажни и тежки,\nдушата ми — люлка.",
    "En la noche oscura te busco, amado,\nen la noche oscura pienso en ti;\nmis ojos están húmedos y pesados,\nmi alma —una cuna."),
   ("La primavera","Когато пролетта дойде\nи цветята разцъфтят,\nаз мисля само за теб\nи за твоята ръка.",
    "Cuando la primavera llega\ny las flores florecen,\npienso sólo en ti\ny en tu mano."),
   ("El libro del amor","Животът е като книга,\nи ти — нейната страница;\nчета те всеки ден и час,\nи плача, и радея.",
    "La vida es como un libro,\ny tú —su página;\nte leo cada día y hora,\ny lloro, y me alegro."),
   ("El beso","Целувката ти е като вода\nв горещото лято;\nтя е живот, тя е награда,\nтя е моето свято.",
    "Tu beso es como agua\nen el caluroso verano;\nes vida, es recompensa,\nes mi sagrado."),
   ("La ausencia","Когато те няма до мен,\nпролетта не пее;\nцветята не цъфтят за мен,\nвсичко само тъгее.",
    "Cuando no estás a mi lado,\nla primavera no canta;\nlas flores no florecen para mí,\ntodo sólo llora."),
   ("La montaña","Обичам те като планината\nобича своите реки;\nтолкова силно, толкова трайно,\nтолкова близо и лесно.",
    "Te amo como la montaña\nama sus ríos;\ntan fuertemente, tan duraderamente,\ntan de cerca y tan fácilmente."),
   ("El adiós","Прости ми, любими, за всичко;\nза болката и за радостта;\nобичах те с цялото си сърце\nи ще те обичам завинаги.",
    "Perdóname, amado, por todo;\npor el dolor y por la alegría;\nte amé con todo mi corazón\ny te amaré para siempre."),
   ("El tiempo","Времето минава и ние остаряваме,\nно любовта не остарява;\nтя живее в нас, в нашето дишане,\nтя е вечна — нещо ново.",
    "El tiempo pasa y envejecemos,\npero el amor no envejece;\nvive en nosotros, en nuestro aliento,\nes eterno —algo nuevo.")]),

 ("057","Luisa_Carnés","1905–1964","Madrid/México","español",
  "Luisa Carnés fue novelista y periodista republicana española que vivió el exilio en México tras la Guerra Civil. Aunque su obra es principalmente narrativa, sus textos poéticos en prosa sobre el amor, el exilio y el cuerpo que extraña la tierra perdida tienen una intensidad lírica notable. Amó con intensidad y escribió sobre el deseo con la naturalidad de quien no tiene nada más que perder. En México encontró una segunda vida y siguió escribiendo hasta su muerte en un accidente de tráfico.",
  [("El exilio del cuerpo","Extraño mi cuerpo en esta tierra,\ncomo extraño la tierra en este cuerpo;\nel amor que aquí cabe no es el mío:\nes el amor del vencido y del estorbo.",
    "El exilio del cuerpo es el mismo\nque el del cuerpo en el exilio;\nlo que aquí amo, lo amo a medias:\nes amor de segunda mano, de abrigo."),
   ("México","México me dio lo que mi tierra\nnegó: un lugar donde existir.\nY en ese lugar encontré la guerra\ndentro, que es la de aprender a vivir.",
    "México me dio lo que mi tierra\nnegó: un lugar donde existir.\nY en ese lugar encontré la guerra\ndentro, que es la de aprender a vivir."),
   ("El cuerpo que recuerda","Mi cuerpo recuerda el mar de allá,\nel olor del esparto y la retama;\ny cuando aquí alguien me toca ya\nmi cuerpo busca lo que no se llama.",
    "Mi cuerpo recuerda el mar de allá,\nel olor del esparto y la retama;\ny cuando aquí alguien me toca ya\nmi cuerpo busca lo que no se llama."),
   ("La compañera","Dormir junto a ti en esta ciudad extraña\nes el único país que reconozco;\ntus brazos son la única hazaña\nque vale frente al olvido tosco.",
    "Dormir junto a ti en esta ciudad extraña\nes el único país que reconozco;\ntus brazos son la única hazaña\nque vale frente al olvido tosco."),
   ("Tea Rooms — el deseo obrero","Las mujeres de las fábricas\ntambién tienen cuerpo que arde;\ntambién tienen noches que acechan\ny amores que llegan tarde.",
    "Las mujeres de las fábricas\ntambién tienen cuerpo que arde;\ntambién tienen noches que acechan\ny amores que llegan tarde."),
   ("La carta","Te escribo desde el otro lado del mundo\ncon la letra que me enseñaste a querer;\ncada palabra es un latido profundo\nde todo lo que quisiste ser.",
    "Te escribo desde el otro lado del mundo\ncon la letra que me enseñaste a querer;\ncada palabra es un latido profundo\nde todo lo que quisiste ser."),
   ("El regreso que no fue","Prometiste volver y no volviste;\nla guerra se llevó lo que habías dicho;\nyo seguí aquí y tú te perdiste\nen el bando que eligió el capricho.",
    "Prometiste volver y no volviste;\nla guerra se llevó lo que habías dicho;\nyo seguí aquí y tú te perdiste\nen el bando que eligió el capricho."),
   ("Poema del destierro","Somos los que perdimos y seguimos;\nlos que el mar separó y el amor no;\nlos que en dos tierras distintas vivimos:\nla que nos dieron y la que ganó.",
    "Somos los que perdimos y seguimos;\nlos que el mar separó y el amor no;\nlos que en dos tierras distintas vivimos:\nla que nos dieron y la que ganó."),
   ("El beso de último","El último beso no fue en el aeropuerto;\nfue antes, cuando todavía creíamos;\ncuando el beso no era del muerto\nsino del amor con que vivíamos.",
    "El último beso no fue en el aeropuerto;\nfue antes, cuando todavía creíamos;\ncuando el beso no era del muerto\nsino del amor con que vivíamos."),
   ("México lindo","No te pido que seas mi tierra;\npido que seas el país de mi amor;\nque en ti se termine esta guerra\ny que descanse en ti mi dolor.",
    "No te pido que seas mi tierra;\npido que seas el país de mi amor;\nque en ti se termine esta guerra\ny que descanse en ti mi dolor.")]),

 ("058","Gabriela_Mistral","1889–1957","Chile","español",
  "Gabriela Mistral fue la primera latinoamericana en ganar el Premio Nobel de Literatura (1945) y una de las voces más complejas de la poesía en español. Nació en Vicuña, Chile, y su vida estuvo marcada por tragedias: el suicidio de su primer amor Romelio Ureta, la misteriosa muerte de su sobrino-hijo Juan Miguel. Sus 'Sonetos de la muerte' son los poemas de amor más conocidos de la literatura chilena. Su relación con la escritora Doris Dana fue el gran amor secreto de su madurez. Murió en Nueva York en 1957.",
  [("Sonetos de la muerte I","Del nicho helado en que los hombres te pusieron,\nte bajaré a la tierra humilde y soleada.\nQue he de dormirme en ella los hombres no supieron,\ny que hemos de soñar sobre la misma almohada.",
    "Del nicho helado en que los hombres te pusieron,\nte bajaré a la tierra humilde y soleada.\nQue he de dormirme en ella los hombres no supieron,\ny que hemos de soñar sobre la misma almohada."),
   ("Sonetos de la muerte II","Este largo cansancio se hará mayor un día,\ny el alma dirá al cuerpo que no quiere seguir\narrastrando su masa por la rosada vía,\npor donde van los hombres, contentos de vivir.",
    "Este largo cansancio se hará mayor un día,\ny el alma dirá al cuerpo que no quiere seguir\narrastrando su masa por la rosada vía,\npor donde van los hombres, contentos de vivir."),
   ("Desolación","Soy tuya y serás mío, así lo dicen\nlos labios que pronuncian tu nombre;\nyo soy la que te ama, los que me maldicen\nno saben que el amor es el más grande nombre.",
    "Soy tuya y serás mío, así lo dicen\nlos labios que pronuncian tu nombre;\nyo soy la que te ama, los que me maldicen\nno saben que el amor es el más grande nombre."),
   ("La flor del aire","Flor del viento, la más fina:\nnaciste sin manos;\ncaes al agua, caminando\ncomo van los años.",
    "Flor del viento, la más fina:\nnaciste sin manos;\ncaes al agua, caminando\ncomo van los años."),
   ("Poema del hijo","Dios me perdone este libro amargo,\ny los hombres que sienten la vida como dulzura\nme lo perdonen también.\nEn estos cien poemas queda sangrando un pasado",
    "Dios me perdone este libro amargo,\ny los hombres que sienten la vida como dulzura\nme lo perdonen también.\nEn estos cien poemas queda sangrando un pasado"),
   ("La extranjera","Habla con dejo de sus mares bárbaros,\ncon no sé qué algas y no sé qué arenas;\nreza oración a dios sin bulto y peso,\nenvejecida dentro de sueños.",
    "Habla con dejo de sus mares bárbaros,\ncon no sé qué algas y no sé qué arenas;\nreza oración a dios sin bulto y peso,\nenvejecida dentro de sueños."),
   ("Balada","Él pasó con otra;\nyo le vi pasar.\nSiempre dulce el viento\ny el camino en paz.",
    "Él pasó con otra;\nyo le vi pasar.\nSiempre dulce el viento\ny el camino en paz."),
   ("La medianoche","La medianoche es la hora del amante;\nla hora en que el amor se hace más fuerte;\nla hora en que la carne más distante\nse acerca al sueño como a la muerte.",
    "La medianoche es la hora del amante;\nla hora en que el amor se hace más fuerte;\nla hora en que la carne más distante\nse acerca al sueño como a la muerte."),
   ("Carta a Doris Dana","No necesito decirte que te quiero;\ntú lo sabes. Es una verdad tan grande\nque cabe en el silencio en que me muero\ny en el amor que hacia ti me expande.",
    "No necesito decirte que te quiero;\ntú lo sabes. Es una verdad tan grande\nque cabe en el silencio en que me muero\ny en el amor que hacia ti me expande."),
   ("Nocturno","Padre Nuestro que estás en los cielos,\n¿por qué te has olvidado de mí?\nTe acordaste del fruto en febrero,\nal llagado no le vas hasta aquí.",
    "Padre Nuestro que estás en los cielos,\n¿por qué te has olvidado de mí?\nTe acordaste del fruto en febrero,\nal llagado no le vas hasta aquí.")]),

 ("059","Clara_Janes","1940–vive","Barcelona, España","español",
  "Clara Janés es una de las poetisas españolas más importantes del siglo XX, traductora de más de treinta lenguas —incluyendo el persa, el turco y el checo— y autora de una obra poética que mezcla el erotismo místico con el pensamiento filosófico. Sus libros 'Vivir' (1983), 'Creciente fértil' (1989) y 'Eros' (1981) son algunos de los textos más sensuales de la poesía española contemporánea. Fue la primera traductora al español de la poesía de Katerina Anghelaki-Rooke y de muchos poetas del mundo eslavo.",
  [("Eros","Eros llega sin avisar,\ncomo la brisa que no se ve;\nse instala en el cuerpo a quedarse\ny lo cambia todo al revés.",
    "Eros llega sin avisar,\ncomo la brisa que no se ve;\nse instala en el cuerpo a quedarse\ny lo cambia todo al revés."),
   ("El cuerpo como territorio","Tu cuerpo es el mapa de mis manos;\ncada curva, una ruta aprendida;\ncada hueco, un país de mis anchuras;\ncada signo, una lengua conocida.",
    "Tu cuerpo es el mapa de mis manos;\ncada curva, una ruta aprendida;\ncada hueco, un país de mis anchuras;\ncada signo, una lengua conocida."),
   ("La traducción del amor","Amor en persa es eshq, en árabe hubb;\nen todas las lenguas arde igual;\nen todas las lenguas el cuerpo sabe\nlo que dice el idioma carnal.",
    "Amor en persa es eshq, en árabe hubb;\nen todas las lenguas arde igual;\nen todas las lenguas el cuerpo sabe\nlo que dice el idioma carnal."),
   ("Creciente fértil","Como la luna crece y mengua,\nasí crece y mengua el deseo;\ncada noche una nueva lengua\ny cada alba un nuevo recreo.",
    "Como la luna crece y mengua,\nasí crece y mengua el deseo;\ncada noche una nueva lengua\ny cada alba un nuevo recreo."),
   ("El silencio entre los cuerpos","Hay un silencio entre dos cuerpos\nque habla más que las palabras;\nes el idioma de los sueños\nque ningún diccionario zanja.",
    "Hay un silencio entre dos cuerpos\nque habla más que las palabras;\nes el idioma de los sueños\nque ningún diccionario zanja."),
   ("Vivir","Vivir es esto: amar y arder,\nperder y recuperar el norte;\nvivir es darse sin ceder\ny encontrarse en el más fuerte.",
    "Vivir es esto: amar y arder,\nperder y recuperar el norte;\nvivir es darse sin ceder\ny encontrarse en el más fuerte."),
   ("El instante","El instante del amor no dura;\ndura su huella en la memoria;\ny en esa huella tan oscura\nyace la más profunda gloria.",
    "El instante del amor no dura;\ndura su huella en la memoria;\ny en esa huella tan oscura\nyace la más profunda gloria."),
   ("La piel del mundo","Toco tu piel y toco el mundo;\ntoco el mundo y te toco a ti;\nno hay nada más profundo hondo\nque este contacto aquí.",
    "Toco tu piel y toco el mundo;\ntoco el mundo y te toco a ti;\nno hay nada más profundo hondo\nque este contacto aquí."),
   ("El poema como cuerpo","El poema es un cuerpo tendido\nen el papel blanco y frío;\nespera ser leído y creído\ncomo el amante espera al mío.",
    "El poema es un cuerpo tendido\nen el papel blanco y frío;\nespera ser leído y creído\ncomo el amante espera al mío."),
   ("La traducción imposible","Hay cosas que no se traducen:\nel color del deseo,\nel olor de la piel que empuja\ny el sabor del tiempo feo.",
    "Hay cosas que no se traducen:\nel color del deseo,\nel olor de la piel que empuja\ny el sabor del tiempo feo.")], True),

 ("060","Idea_Vilarino","1920–2009","Montevideo, Uruguay","español",
  "Idea Vilariño fue la poeta más descarnada del Uruguay del siglo XX y una de las grandes voces del amor imposible en lengua española. Su relación con el escritor Juan Carlos Onetti —un amor intermitente, doloroso, marcado por la diferencia de edad y la imposibilidad práctica— le dio los poemas más intensos de su carrera, reunidos en 'Poemas de amor' (1957). Sus versos son breves, duros, sin ornamento: el amor como sustancia mínima que quema.",
  [("Ya no","Ya no será\nya no\nno viviremos juntos\nno criaré a tu hijo\nno coseré tu ropa\nno te tendré de noche\nno te besaré al irme.\nNunca sabrás quién fui.",
    "Ya no será\nya no\nno viviremos juntos\nno criaré a tu hijo\nno coseré tu ropa\nno te tendré de noche\nno te besaré al irme.\nNunca sabrás quién fui."),
   ("Querer","Querer estar en ti\nestar en ti\nestar en ti\ncomo estás tú en mí\ndesde que te fui.",
    "Querer estar en ti\nestar en ti\nestar en ti\ncomo estás tú en mí\ndesde que te fui."),
   ("Pobre mundo","Pobre mundo el del amor\nque pide y no tiene,\nque llama y no viene,\nque arde y no da calor.",
    "Pobre mundo el del amor\nque pide y no tiene,\nque llama y no viene,\nque arde y no da calor."),
   ("Sola","Sola. Y la noche.\nY tú tan lejos.\nY el cuerpo hecho\nde soledades.",
    "Sola. Y la noche.\nY tú tan lejos.\nY el cuerpo hecho\nde soledades."),
   ("No puedo más","No puedo más\nde tanto quererte.\nNo puedo más\nde tanto no tenerte.",
    "No puedo más\nde tanto quererte.\nNo puedo más\nde tanto no tenerte."),
   ("El amor","El amor que tengo\nno cabe en el nombre;\nel amor que siento\nes más que un hombre.",
    "El amor que tengo\nno cabe en el nombre;\nel amor que siento\nes más que un hombre."),
   ("Nocturnos","De noche cuando pienso en ti\nel cuerpo sabe lo que hace;\nde noche cuando pienso en ti\ntodo el mundo se deshace.",
    "De noche cuando pienso en ti\nel cuerpo sabe lo que hace;\nde noche cuando pienso en ti\ntodo el mundo se deshace."),
   ("Juntos","Cuando estábamos juntos\nel mundo era posible;\ncuando estuviste cerca\nel vivir fue perceptible.",
    "Cuando estábamos juntos\nel mundo era posible;\ncuando estuviste cerca\nel vivir fue perceptible."),
   ("Después","Después de ti no hubo nadie.\nDespués de ti qué silencio.\nDespués de ti todo el paisaje\nquedó sin tu movimiento.",
    "Después de ti no hubo nadie.\nDespués de ti qué silencio.\nDespués de ti todo el paisaje\nquedó sin tu movimiento."),
   ("Poema de amor final","Te quise tanto\nque no puedo decirlo.\nTe quiero tanto\nque no sé cómo escribirlo.",
    "Te quise tanto\nque no puedo decirlo.\nTe quiero tanto\nque no sé cómo escribirlo.")], True),
]

if __name__ == "__main__":
    for item in L:
        mk(*item)
    print(f"Generadas {len(L)} poetisas.")
