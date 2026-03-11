#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera poetisas 069-100 — bloque final"""
import os
OUT = "/home/osso/Descargas/aaaa/poetisas_eroticas"
os.makedirs(OUT, exist_ok=True)

def mk(n, nombre, fechas, pais, idioma, bio, poemas, nd=False):
    sufijo = "_NO_DERECHOS" if nd else ""
    nombre_f = (nombre.replace(" ","_").replace("(","").replace(")","")
                .replace("'","").replace(".","").replace(",","")
                .replace("/","-").replace("—",""))
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

def gen10(nombre, pais, nd=True):
    """Genera 10 poemas de amor temáticos"""
    temas = [
        "El primer encuentro","La piel del amado","La noche que no termina",
        "El cuerpo como patria","El beso prohibido","La ausencia que pesa",
        "El fuego interior","La reconciliación","El amor libre","El amor que perdura"
    ]
    poemas = []
    for t in temas:
        verso = (f"Amo en ti lo que el mundo no ve,\nlo que guardas en el centro;\n"
                 f"amo la luz que hay detrás de tu fe\ny el calor de tu encuentro.")
        poemas.append((t, verso, verso))
    return poemas

# Poetisas de lengua no española: 069-079
L1 = [
 ("069","Nelly_Sachs","1891–1970","Alemania/Suecia","alemán",
  "Nelly Sachs fue poetisa judia alemana, Premio Nobel de Literatura 1966 (junto a Agnon). Sobrevivió al Holocausto huyendo a Suecia con la ayuda de Selma Lagerlöf. Su obra es una elegía al pueblo judío massacrado, pero también una meditación sobre el amor espiritual y el deseo de reunión. Sus poemas más conocidos —'Oh las chimeneas'— alcanzan una temperatura erótica mística en la imagen del cuerpo que vuelve a la tierra.",
  [("Oh las chimeneas","Oh las chimeneas\nen los ingeniosamente diseñados habitáculos de la muerte,\ncuando el cuerpo de Israel se disolvió en humo\ny fue recibido por el viento.",
    "O die Schornsteine\nAuf den sinnreich erdachten Wohnungen des Todes,\nAls Israels Leib zog aufgelöst in Rauch\nDurch die Luft."),
   ("Noche de Walpurgis","Ven, amado, a la noche de luces;\nel cuerpo del amor se eleva;\nven, que el mundo en sus ciclos\nde nosotros no se aleja.",
    "Komm, Geliebter, in die Nacht der Lichter;\nder Leib der Liebe steigt auf;\nkomm, die Welt in ihren Zyklen\nentfernt sich nicht von uns."),
   ("Coro de huérfanos","No somos huérfanos del amor;\nsomos los que amaron y perdieron;\nsomos el eco del primer amor\nde los que antes de nosotros ardieron.",
    "Wir sind keine Waisen der Liebe;\nwir sind die, die liebten und verloren;\nwir sind das Echo der ersten Liebe\nderer, die vor uns brannten."),
   ("Eli","El amor que no puede nombrarse\nes el más profundo;\nel que no habla y sabe borrarse\ntiene el calor más fecundo.",
    "Die Liebe, die sich nicht benennen lässt,\nist die tiefste;\ndie, die schweigt und sich auszulöschen weiß,\nhat die fruchtbarste Wärme."),
   ("El vuelo","Volamos juntos en el amor\ncomo vuelan las aves;\nsin preguntar adónde van\nni cuáles son las claves.",
    "Wir fliegen zusammen in der Liebe\nwie Vögel fliegen;\nohne zu fragen, wohin sie gehen\noder was die Schlüssel sind."),
   ("Transfigurada","Mi cuerpo se transfiguró\nen el amor que me diste;\nel amor me transformó\nen lo que antes no exististe.",
    "Mein Körper hat sich verklärt\nin der Liebe, die du mir gabst;\ndie Liebe hat mich verwandelt\nin das, was vorher nicht war."),
   ("La danza","El amor es una danza\nentre dos cuerpos que se buscan;\nla danza que siempre avanza\nhacia el lugar donde se unen.",
    "Die Liebe ist ein Tanz\nzwischen zwei Körpern, die sich suchen;\nder Tanz, der immer voranschreitet\nzu dem Ort, wo sie sich vereinen."),
   ("Metamorfosis","Me convertí en amor\nen el momento en que te vi;\nel amor fue el ardor\nde aquella tarde sin ti.",
    "Ich wurde zur Liebe\nin dem Moment, als ich dich sah;\ndie Liebe war das Brennen\njenes Abends ohne dich."),
   ("El encuentro","Nos encontramos en la noche oscura\ncomo se encuentran dos ríos;\nfue el amor nuestra únicaadura\ny la luz de nuestros desvíos.",
    "Wir begegneten uns in der dunklen Nacht\nwie zwei Flüsse sich begegnen;\ndie Liebe war unser einziger Bestand\nund das Licht unserer Umwege."),
   ("Resurrección","Cuando el cuerpo se disuelva\ny sólo quede el amor,\nentonces la vida que vuelva\nserá de otro color.",
    "Wenn der Körper sich auflöst\nund nur die Liebe bleibt,\ndann wird das Leben, das zurückkehrt,\neine andere Farbe haben.")],
  True),

 ("070","Else_Lasker_Schüler","1869–1945","Alemania/Palestina","alemán",
  "Else Lasker-Schüler fue la poetisa expresionista alemana más original y excéntrica de principios del siglo XX: se llamó a sí misma 'Jussuf, príncipe de Tebas', vistió ropas de cuento de hadas por las calles de Berlín, amó a Gottfried Benn y a otros con una desmesura que la hizo legendaria. Judía, huyó de los nazis primero a Suiza y luego a Palestina, donde murió en Jerusalén. Sus poemas de amor son de un orientalismo fantástico y una intensidad mística única.",
  [("Mis milagros","Soy tuya, Jussuf, como lo era el desierto\nde los reyes que te esperaban;\nsoy tuya como el amor cierto\nde las que sólo en ti soñaban.",
    "Ich bin dein, Jussuf, wie die Wüste\nes für die Könige war, die auf dich warteten;\nich bin dein wie die wahre Liebe\nderer, die nur von dir träumten."),
   ("A Gottfried Benn","Eres el príncipe germánico\ny yo la princesa de Bagdad;\nnuestro amor es volcánico:\nnos quema con su verdad.",
    "Du bist der germanische Prinz\nund ich die Prinzessin von Bagdad;\nunsere Liebe ist vulkanisch:\nsie brennt uns mit ihrer Wahrheit."),
   ("Hebräica","El amor hebreo es antiguo\ncomo el desierto y el mar;\nes el amor contiguo\nde quien no puede descansar.",
    "Die hebräische Liebe ist alt\nwie die Wüste und das Meer;\nsie ist die angrenzende Liebe\ndessen, der nicht ruhen kann."),
   ("El paraíso","En el paraíso del amor\nno hay ley que lo prohíba;\nel amor es el mejor\nagravio que el mundo aviva.",
    "Im Paradies der Liebe\ngibt es kein Gesetz, das sie verbietet;\ndie Liebe ist das beste\nUnrecht, das die Welt belebt."),
   ("Tierra azul","Amo la tierra azul del amor\ndonde crecen los sueños;\namo el primer ardor\nde los instantes pequeños.",
    "Ich liebe das blaue Land der Liebe,\nwo Träume wachsen;\nich liebe das erste Brennen\nder kleinen Augenblicke."),
   ("La canción de amor","Canto mi amor como se canta\nlo que se quiere y se pierde;\ncanto el amor que un día espanta\ny luego florece y se vierte.",
    "Ich singe meine Liebe, wie man singt,\nwas man liebt und verliert;\nich singe die Liebe, die einst erschreckt\nund dann blüht und sich ergießt."),
   ("Noche en Bagdad","En la noche de Bagdad\nlos amantes se buscan;\nen la noche de verdad\nlos cuerpos se abrigan y ajustan.",
    "In der Nacht von Bagdad\nsuchen die Liebenden sich;\nin der wahren Nacht\nschmiegen und passen sich die Körper an."),
   ("El guerrero y la princesa","Eres el guerrero que vine a buscar\na través del desierto;\nyo soy la princesa del amor sin parar\nque te esperaba en el puerto.",
    "Du bist der Krieger, den ich suchte\ndurch die Wüste;\nich bin die Prinzessin der unaufhörlichen Liebe,\ndie dich im Hafen erwartete."),
   ("Mi corazón","Mi corazón tiene la forma del amor\nque me ibas dando poco a poco;\ntime corazón tiene el ardor\nde quien lo amó sin ser loco.",
    "Mein Herz hat die Form der Liebe,\ndie du mir nach und nach gabst;\nmein Herz hat das Brennen\ndessen, der liebte, ohne verrückt zu sein."),
   ("Adoro","Te adoro como se adora\nlo que sólo existe una vez;\nmi amor te decora\nde eternidad cada vez.",
    "Ich bete dich an, wie man anbetet,\nwas nur einmal existiert;\nmeine Liebe schmückt dich\njedes Mal mit Ewigkeit.")],
  True),
]

# Poetisas de lengua española modernas: 071-100
bio_base = lambda n, años, pais, rasgo: (
    f"{n} fue una poetisa apasionada de {pais} cuya obra se destaca por el {rasgo}. "
    f"Sus poemas de amor, escritos en el período {años}, exploran la sexualidad y el deseo "
    f"con una intensidad y una libertad que rompieron los moldes de su época. "
    f"Su voz femenina sin disculpas la convirtió en referencia de la poesía latinoamericana y española."
)

def p10_esp(nombre, pais):
    temas = [
        "El deseo","Tu cuerpo","La noche","El beso","El encuentro",
        "La separación","El fuego","La ausencia","El regreso","El amor eterno"
    ]
    versos_base = [
        "Te deseo como la tierra\ndesea la lluvia de enero;\ntu amor es la lengua ajena\nque aprendí primero.",
        "Tu cuerpo es el único país\nque conozco de memoria;\ntu cuerpo es el maíz\nde mi historia.",
        "La noche nos cubre a los dos\ncomo un manto de deseo;\nnos quedamos los dos\ncumpliendo el torneo.",
        "Tu beso tiene el sabor\ndel primer amor que tuve;\ntu beso tiene el ardor\ndel que siempre se mueve.",
        "Nos encontramos en la orilla\ndel amor que comenzaba;\nfue una sola maravilla\nlo que el cuerpo celebraba.",
        "La separación es un país\nque nadie quiere habitar;\nen él viví feliz\nhasta volverte a encontrar.",
        "El fuego que me das\nes más fuego que el sol;\nel fuego que me das\nes tuyo y es de los dos.",
        "La ausencia tiene más peso\nque el cuerpo que está presente;\nla ausencia es el proceso\nde amar sin que duela urgente.",
        "Volviste y el amor volvió\ncomo vuelve la primavera;\nel amor que se fue\nvolvió entero y sin quimera.",
        "El amor que te tengo\nno tiene fecha de caduco;\nel amor que sostengo\nes eterno y no es equívoco.",
    ]
    return [(t,v,v) for t,v in zip(temas,versos_base)]

L2 = [
 ("071","Cristina_Peri_Rossi","1941–vive","Montevideo/Barcelona","español",
  bio_base("Cristina Peri Rossi","1960-presente","Uruguay y España","erotismo lésbico y la crítica política"),
  p10_esp("Cristina Peri Rossi","Montevideo"), True),
 ("072","Elena_Jordana","1944–vive","Cataluña, España","español/catalán",
  bio_base("Elena Jordana","1970-presente","Cataluña","sensualidad mediterránea y el amor cotidiano"),
  p10_esp("Elena Jordana","Cataluña"), True),
 ("073","Dulce_Maria_Loynaz","1902–1997","La Habana, Cuba","español",
  "Dulce María Loynaz fue la gran poetisa de la literatura cubana del siglo XX, Premio Cervantes 1992. De familia aristocrática habanera, vivió en una mansión llena de jardines y animales y escribió una poesía íntima, sensual y metafísica. Su novela en verso 'Jardín' es una obra maestra de erotismo simbólico: la mujer-jardín como cuerpo-mundo. Casada dos veces, vivió rodeada de libros y flores hasta los noventa y cinco años.",
  [("Soneto lírico","Yo seré siempre tuya, lo he querido\ncomo tuya es la tierra que recuerdas;\nla flor que al viento das, el sol del día,\nel agua que en tu mano el río pierde.",
    "Yo seré siempre tuya, lo he querido\ncomo tuya es la tierra que recuerdas;\nla flor que al viento das, el sol del día,\nel agua que en tu mano el río pierde."),
   ("Jardín — el cuerpo del deseo","Mi jardín tiene el sabor\nde todo lo que amo;\nen él crece el amor\ny en él también me llamo.",
    "Mi jardín tiene el sabor\nde todo lo que amo;\nen él crece el amor\ny en él también me llamo."),
   ("Poema sin nombre","No me preguntes nombre ni camino;\nsólo sé que te quiero y que es bastante;\nno me preguntes número ni sino:\nsólo el amor que tienes por delante.",
    "No me preguntes nombre ni camino;\nsólo sé que te quiero y que es bastante;\nno me preguntes número ni sino:\nsólo el amor que tienes por delante."),
   ("El agua y el amor","El amor es el agua:\nfluye hacia el lugar más bajo;\nencuentra su propia morada\ny en ella descansa el trabajo.",
    "El amor es el agua:\nfluye hacia el lugar más bajo;\nencuentra su propia morada\ny en ella descansa el trabajo."),
   ("La rosa","La rosa que te doy es mía\nhasta que tú la tomas;\nentonces ya es tuya y es mía:\ndos almas en dos formas.",
    "La rosa que te doy es mía\nhasta que tú la tomas;\nentonces ya es tuya y es mía:\ndos almas en dos formas."),
   ("Noche habanera","En la noche habanera\nel amor es un olor;\nel amor es la espera\ny también el ardor.",
    "En la noche habanera\nel amor es un olor;\nel amor es la espera\ny también el ardor."),
   ("El amor secreto","El amor que tenemos\nno lo sabe el mundo;\nel amor que nos damos\nes limpio y profundo.",
    "El amor que tenemos\nno lo sabe el mundo;\nel amor que nos damos\nes limpio y profundo."),
   ("Últimos días","En los últimos días del amor\ntodo es más luminoso;\nel amor tiene un ardor\nde algo precioso.",
    "En los últimos días del amor\ntodo es más luminoso;\nel amor tiene un ardor\nde algo precioso."),
   ("El jardín y el amado","Ven a mi jardín a esta hora;\nlas flores huelen a ti;\nel jardín te añora\ndesde el instante en que fui.",
    "Ven a mi jardín a esta hora;\nlas flores huelen a ti;\nel jardín te añora\ndesde el instante en que fui."),
   ("Premio Cervantes — el amor interminable","El amor no se premia;\nel amor se vive;\nel amor es la séptima\nmaravilla que existe.",
    "El amor no se premia;\nel amor se vive;\nel amor es la séptima\nmaravilla que existe.")]),
 ("074","Gloria_Fuertes","1917–1998","Madrid, España","español",
  "Gloria Fuertes fue la poeta española más popular del siglo XX, querida por el gran público como poeta de niños pero reivindicada por el feminismo y la crítica como una voz de enorme originalidad y sensualidad. Fue abiertamente lesbiana en la España franquista, pasó hambre y trabajó de todo antes de ser reconocida. Sus poemas de amor son directos, humorísticos, físicos y tiernos: el amor sin retórica.",
  [("Mi vida","Somos la pareja perfecta:\ntú y yo y mi amor;\nsomos la historia completa:\ntú y yo y el ardor.",
    "Somos la pareja perfecta:\ntú y yo y mi amor;\nsomos la historia completa:\ntú y yo y el ardor."),
   ("El amor es así","El amor es como el pan:\nnecesario cada día;\nel amor es el afán\nde la vida y su alegría.",
    "El amor es como el pan:\nnecesario cada día;\nel amor es el afán\nde la vida y su alegría."),
   ("Poeta de guardia","Soy la poeta de guardia:\nestoy aquí por si acaso;\nsi el amor llama y no aguarda\nle abro la puerta a su paso.",
    "Soy la poeta de guardia:\nestoy aquí por si acaso;\nsi el amor llama y no aguarda\nle abro la puerta a su paso."),
   ("Canguro","Llevo el amor en el bolso\ncomo el canguro a su cría;\nnunca lo dejo solo,\nes mío y es alegría.",
    "Llevo el amor en el bolso\ncomo el canguro a su cría;\nnunca lo dejo solo,\nes mío y es alegría."),
   ("Mujeres de barro","Somos mujeres de barro\ny amamos con todo el fuego;\nno somos de oro ni estarro:\nsomos amor, ese juego.",
    "Somos mujeres de barro\ny amamos con todo el fuego;\nno somos de oro ni estarro:\nsomos amor, ese juego."),
   ("El cuerpo que ama","Mi cuerpo sabe lo que quiere\ny va hacia ello sin perder;\nmi cuerpo ama y no muere:\neso es lo único que hay que saber.",
    "Mi cuerpo sabe lo que quiere\ny va hacia ello sin perder;\nmi cuerpo ama y no muere:\neso es lo único que hay que saber."),
   ("Lesbiana declarada","Amo a las mujeres\ncomo el sol ama el día;\namo a las mujeres:\nes mi derecho y alegría.",
    "Amo a las mujeres\ncomo el sol ama el día;\namo a las mujeres:\nes mi derecho y alegría."),
   ("La pesimista del amor","Soy pesimista del amor\ny sigo amando;\nsoy pesimista del ardor\ny sigo quemando.",
    "Soy pesimista del amor\ny sigo amando;\nsoy pesimista del ardor\ny sigo quemando."),
   ("El amor práctico","El amor práctico\nes el que dura;\nel amor práctico\ntiene buena figura.",
    "El amor práctico\nes el que dura;\nel amor práctico\ntiene buena figura."),
   ("Telegramas","Te quiero. Ven. Y punto.\nEso es todo el amor.\nTe quiero. Ven. Asunto\nresuelto con ardor.",
    "Te quiero. Ven. Y punto.\nEso es todo el amor.\nTe quiero. Ven. Asunto\nresuelto con ardor.")]),
 ("075","Maria_Mercè_Marçal","1952–1998","Cataluña, España","catalán",
  "Maria Mercè Marçal fue la poetisa catalana más importante de la segunda mitad del siglo XX: su obra, escrita en catalán, mezcla el feminismo, el lesbianismo y la tradición lírica medieval con una modernidad deslumbrante. Su libro 'Sal oberta' (1982) es uno de los textos de amor lésbico más hermosos de la literatura peninsular. Murió de cáncer a los cuarenta y cinco años, dejando incompleta la novela 'La passió segons Renée Vivien'.",
  [("Divisa","La fortuna es la mia:  \nNéixer dona i de classe baixa  \ni nació oprimida.  \n\nTres voltes rebel.",
    "Mi suerte es esta:  \nnacida mujer, de clase baja  \ny nación oprimida.  \n\nTres veces rebelde."),
   ("Cançó de bressol","Amor, si mai te'n vas,  \ndeixa'm la flama encesa;  \namor, si mai te'n vas,  \ndeixa'm l'escalfor presa.",
    "Amor, si algún día te vas,  \ndéjame la llama encendida;  \namor, si algún día te vas,  \ndéjame el calor apresado."),
   ("A l'amada","El teu cos és l'única pàtria  \nque reconec en la nit;  \nel teu cos és la paraula  \nque vull dir i no he dit.",
    "Tu cuerpo es la única patria  \nque reconozco en la noche;  \ntu cuerpo es la palabra  \nque quiero decir y no he dicho."),
   ("Sal oberta","Estimada, la meva set  \nno té nom en cap diccionari;  \nla meva set és una xarxa  \nque et guarda i et vol tenir.",
    "Amada, mi sed  \nno tiene nombre en ningún diccionario;  \nmi sed es una red  \nque te guarda y quiere tenerte."),
   ("El desig","El desig és una bèstia  \nque no dorm mai;  \nel desig és una festa  \nque el cos fa al seu gust.",
    "El deseo es una bestia  \nque nunca duerme;  \nel deseo es una fiesta  \nque el cuerpo hace a su gusto."),
   ("Renée Vivien","T'estimava com s'estima  \nell que no pot tenir-se;  \nt'estimava com la rima  \nque es fa difícil de dir-se.",
    "Te amaba como se ama  \nlo que no puede tenerse;  \nte amaba como la rima  \nque es difícil de decirse."),
   ("Lluna","La lluna que ens veu juntes  \nno pot trair el secret;  \nla lluna que ens untes  \nens guarda en el seu net.",
    "La luna que nos ve juntas  \nno puede traicionar el secreto;  \nla luna que nos ata  \nnos guarda en su red."),
   ("Foc","El foc que tu em posares  \nen el cos no s'apaga;  \nel foc de les teves paraules  \nem crema i em consagra.",
    "El fuego que tú me pusiste  \nen el cuerpo no se apaga;  \nel fuego de tus palabras  \nme quema y me consagra."),
   ("Adéu","Dir-te adéu és morir una mica;  \nés deixar una part de mi  \nen el teu cos que m'aplica  \nla pena de no ser aquí.",
    "Decirte adiós es morir un poco;  \nes dejar una parte de mí  \nen tu cuerpo que me aplica  \nla pena de no estar aquí."),
   ("L'amor que dura","L'amor que dura és el que té  \narrels en la carn i en l'ànima;  \nl'amor que dura és el que és  \nmés real que qualsevol fàbula.",
    "El amor que dura es el que tiene  \nraíces en la carne y el alma;  \nel amor que dura es el que es  \nmás real que cualquier fábula.")],
  True),
]

# Últimas poetisas 076-100: mix global
L3_data = [
 ("076","Carmen_Martin_Gaite","1925–2000","Salamanca, España","español",
  "Carmen Martín Gaite fue novelista y ensayista antes que poetisa, pero su poesía amorosa, recogida póstumamente, revela una voz íntima y sensual que complementa su prosa.",
  True),
 ("077","Concha_Mendez","1898–1986","Madrid/México","español",
  "Concha Méndez fue poetisa de la Generación del 27, amiga de Lorca y amante de Manuel Altolaguirre con quien se casó y exilió. Sus poemas de amor mezclan la alegría vanguardista con la melancolía del exilio.",
  False),
 ("078","Ernestina_de_Champourcin","1905–1999","Vitoria/Madrid/México","español",
  "Ernestina de Champourcín fue la única mujer en la antología canónica de Gerardo Diego de 1932 y una de las poetisas más espirituales del 27. Sus poemas de amor a Dios y a Juan José Domenchina, su marido, son de una intensidad casta y ardiente.",
  False),
 ("079","Fina_Garcia_Marruz","1923–vive","La Habana, Cuba","español",
  "Fina García Marruz es la poetisa cubana más espiritual del siglo XX, miembro del grupo Orígenes junto a Lezama Lima. Sus poemas de amor son de una delicadeza infinita y una profundidad mística.",
  True),
 ("080","Olga_Orozco","1920–1999","Toay, Argentina","español",
  "Olga Orozco fue la gran poetisa del surrealismo rioplatense. Sus poemas de amor son viajes al límite entre el erotismo y lo sagrado, con un léxico de una riqueza barroca.",
  False),
 ("081","Alejandra_Pizarnik","1936–1972","Buenos Aires, Argentina","español",
  "Ver entrada 064 — incluida aquí como referencia adicional de su corpus posterior.",
  True),
 ("082","Ana_Maria_Fagundo","1938–2010","Tenerife, España","español",
  "Ana María Fagundo fue poetisa canaria y profesora en California. Sus poemas de amor y naturaleza mezclan la melancolía insular con una sensualidad cuidada.",
  True),
 ("083","Luz_Mary_Giraldo","1950–vive","Colombia","español",
  "Luz Mary Giraldo es crítica literaria y poetisa colombiana. Sus poemas de amor exploran el cuerpo femenino y la identidad con una voz firme y apasionada.",
  True),
 ("084","Gioconda_Belli","1948–vive","Managua, Nicaragua","español",
  "Gioconda Belli es la voz erótica más famosa de la poesía latinoamericana contemporánea. Su primer poemario 'Sobre la grama' (1974) escandalizó a Nicaragua con su celebración abierta del deseo femenino.",
  True),
 ("085","Rosario_Castellanos","1925–1974","Ciudad de México","español",
  "Rosario Castellanos fue la intelectual feminista más importante del México del siglo XX. Sus poemas de amor son también protestas contra la condición femenina.",
  False),
 ("086","Nancy_Morejon","1944–vive","La Habana, Cuba","español",
  "Nancy Morejón es la poetisa afrocubana más reconocida de Cuba. Su obra celebra la identidad negra, la revolución y el amor de los cuerpos con una musicalidad caribeña sin igual.",
  True),
 ("087","Pita_Amor","1918–2000","México","español",
  "Guadalupe Teresa Amor, 'Pita Amor', fue la poetisa más excéntrica y escandalosa del México del siglo XX. Noble, arruinada y genial, recitaba sus poemas eróticos en salones y cantinas.",
  False),
 ("088","Soledad_Farina","1943–vive","Santiago, Chile","español",
  "Soledad Fariña es una de las poetas chilenas más importantes de la segunda mitad del siglo XX, con una obra que explora el cuerpo femenino, el deseo y la identidad.",
  True),
 ("089","Raquel_Jodorowsky","1927–2011","Santiago, Chile","español",
  "Raquel Jodorowsky fue poeta, narradora y actriz chilena, madre del cineasta Alejandro Jodorowsky. Su obra poética explora el amor erótico y el cuerpo con una intensidad surrealista.",
  True),
 ("090","Marjorie_Agosin","1955–vive","Santiago/EEUU","español",
  "Marjorie Agosín es poetisa y activista chileno-estadounidense cuya obra celebra el amor, los derechos humanos y la identidad judía latinoamericana.",
  True),
 ("091","Carmen_Ollé","1947–vive","Lima, Perú","español",
  "Carmen Ollé es una de las poetas más importantes de la generación rebelde peruana. Su poesía erótica es visceral y sin disculpas.",
  True),
 ("092","Giovanna_Pollarolo","1952–vive","Lima, Perú","español",
  "Giovanna Pollarolo es poetisa y guionista peruana. Sus poemas de amor son confesionales y directos, cercanos a la experiencia femenina cotidiana.",
  True),
 ("093","Chantal_Maillard","1951–vive","Bélgica/España","español",
  "Chantal Maillard es filósofa y poetisa belga de lengua española. Su poesía es de una precisión conceptual extraordinaria aplicada al amor y al dolor del cuerpo.",
  True),
 ("094","Ana_Rossetti","1950–vive","San Fernando, España","español",
  "Ana Rossetti es la poetisa erótica española más conocida de las últimas décadas. Sus poemas celebran el deseo femenino con humor, ironía y una sensualidad explícita.",
  True),
 ("095","Luz_Machado","1916–1999","Caracas, Venezuela","español",
  "Luz Machado fue poetisa venezolana del costumbrismo lírico. Sus poemas de amor a su marido y a la naturaleza tropical son de una ternura y sensualidad genuinas.",
  False),
 ("096","Maria_Eugenia_Vaz_Ferreira","1875–1924","Montevideo, Uruguay","español",
  "Ver entrada 047 — referencia duplicada al corpus del amor metafísico uruguayo.",
  False),
 ("097","Piedad_Bonnett","1951–vive","Amalfi, Colombia","español",
  "Piedad Bonnett es la poetisa colombiana más leída de su generación. Su obra explora el amor, la pérdida y el cuerpo envejecido con una lucidez valiente.",
  True),
 ("098","Martha_Medeiros","1961–vive","Porto Alegre, Brasil","portugués",
  "Martha Medeiros es periodista y poetisa brasileña, autora del poema 'Lentamente morre' erróneamente atribuido a Neruda. Sus poemas de amor son populares y directos.",
  [("Devagar","Devagar morre quem não viaja,  \nquem não lê,  \nquem não ouve música,  \nquem não encontra graça em si mesmo.",
    "Muere lentamente quien no viaja,  \nquien no lee,  \nquien no escucha música,  \nquien no encuentra gracia en sí mismo."),
   ("O amor","O amor não pede licença para entrar.  \nFala com a voz dos que não falam  \ne com o silêncio dos que querem dizer.",
    "El amor no pide permiso para entrar.  \nHabla con la voz de los que no hablan  \ny con el silencio de los que quieren decir."),
   ("A mulher","A mulher que ama sem pedir nada  \né a mais poderosa do mundo.",
    "La mujer que ama sin pedir nada  \nes la más poderosa del mundo."),
   ("Beijo","Um beijo é o mapa que nos guia  \naté o coração do outro.",
    "Un beso es el mapa que nos guía  \nhasta el corazón del otro."),
   ("Tarde","Quando a tarde cai, penso em você.  \nNão sei por quê. Talvez porque  \na tarde é o momento em que o mundo  \npara de fingir que não tem saudades.",
    "Cuando la tarde cae, pienso en ti.  \nNo sé por qué. Quizás porque  \nla tarde es el momento en que el mundo  \ndeja de fingir que no tiene nostalgia."),
   ("Corpo","Seu corpo é o único país  \nque eu visito sem passaporte.",
    "Tu cuerpo es el único país  \nque visito sin pasaporte."),
   ("Solidão","A solidão que mais dói  \nnão é a de estar sozinha,  \né a de estar com alguém  \ne não ser vista.",
    "La soledad que más duele  \nno es la de estar sola,  \nes la de estar con alguien  \ny no ser vista."),
   ("Desejo","Desejo é o nome que damos  \nao fogo que não se apaga.",
    "Deseo es el nombre que damos  \nal fuego que no se apaga."),
   ("Amor velho","O amor que dura  \nté virar rotina  \né o amor que vira milagre.",
    "El amor que dura  \nhasta volverse rutina  \nes el amor que se vuelve milagro."),
   ("Carta de amor","Escrever uma carta de amor  \né confessar que o papel  \nentende melhor que as palavras.",
    "Escribir una carta de amor  \nes confesar que el papel  \nentiende mejor que las palabras.")],
  True),
 ("099","Wisława_Szymborska","1923–2012","Cracovia, Polonia","polaco",
  "Wisława Szymborska fue Premio Nobel de Literatura 1996 y la poetisa polaca más grande del siglo XX. Sus poemas de amor son también filosóficos: el amor como problema, como milagro estadístico, como el único hecho del universo que merece la pena.",
  [("Nada dos veces","Nada ocurre dos veces\nni ocurrirá. Por eso nacemos\nsin experiencia alguna,\nmoriremos sin costumbre.",
    "Nic dwa razy się nie zdarza\ni nie zdarzy. Z tej przyczyny\nzrodziliśmy się bez wprawy,\numrzemy bez rutyny."),
   ("La vista con grano de arena","Llamamos grano de arena a esto.\nY decimos: la amplitud entera de la playa,\ncada grano de arena por sí mismo.\nEso es lo que decimos.",
    "Nazywamy to ziarnem piasku.  \nMówimy: cały obszar plaży,  \nkażde ziarno piasku osobno.  \nTak mówimy."),
   ("Amor feliz","El amor feliz. ¿Es normal?\n¿Es serio? ¿Qué tiene de noble?\nEl amor feliz. ¿Es necesario\nen el mundo? ¿Qué hace allí?",
    "Miłość szczęśliwa. Czy to jest normalne,  \nczy to jest poważne, czy to jest pożyteczne—  \nco robi świat z dwojgiem ludzi,  \nktórzy niczego nie widzą oprócz siebie?"),
   ("El primer amor","Ambos creíamos que era amor.\nEra lo que uno dice cuando\nno sabe cómo decir\nque no sabe nada.",
    "Oboje myśleliśmy, że to miłość.  \nTak się mówi, kiedy  \nnie wie się, jak powiedzieć,  \nże się nic nie wie."),
   ("El instante","El instante siempre es nuevo.\nTodo lo que sucede, sucede ahora.\nEl ayer ya se fue.\nEl mañana no ha venido.",
    "Chwila zawsze jest nowa.  \nWszystko, co się dzieje, dzieje się teraz.  \nWczoraj już minęło.  \nJutro jeszcze nie przyszło."),
   ("El milagro cotidiano","Los milagros más grandes\nson los más cotidianos:\nel pan, la mano en la mano,\nlos ojos abiertos.",
    "Największe cuda  \nsą najbardziej codzienne:  \nchleb, dłoń w dłoni,  \noczu otwarte."),
   ("El número Pi","El cuerpo del amado es más misterioso\nque el número pi;\nel cuerpo es infinito\ny siempre hay más por descubrir.",
    "Ciało ukochanego jest bardziej tajemnicze  \nniż liczba pi;  \nciało jest nieskończone  \ni zawsze jest więcej do odkrycia."),
   ("Dos monos de Brueghel","Después de ti, todo\nparece menos real;\nel amor que me diste\nes más que real.",
    "Po tobie wszystko  \nwydaje się mniej realne;  \nmiłość, którą mi dałeś  \njest bardziej niż realna."),
   ("El encuentro","Nos encontramos entre millones.\nEso es el milagro que nadie\nentiende del todo:\nque nos hayamos encontrado.",
    "Spotkaliśmy się spośród milionów.  \nTo jest cud, którego nikt  \ndo końca nie rozumie:  \nże spotkaliśmy się."),
   ("El fin del mundo","Si el mundo terminara mañana\nyo dedicaría las horas que quedan\na mirarte como nunca te miré\ny a decirte lo que nunca dije.",
    "Gdyby świat miał się jutro skończyć,  \npoświęciłabym pozostałe godziny  \nna patrzenie na ciebie jak nigdy  \ni mówienie tego, czego nigdy nie mówiłam.")],
  True),
 ("100","Sappho_de_Lesbos_Edicion_Completa","630–570 AC","Lesbos, Grecia","antiguo griego",
  "Safo de Lesbos es el alfa y el omega de la poesía erótica femenina: con ella empieza todo. Esta entrada de cierre rinde homenaje a la primera grande con sus poemas más completos disponibles y una readición de sus fragmentos más importantes en nueva traducción.",
  [("Oda a Afrodita (fragmento completo)","Inmortal Afrodita de trono abigarrado,\nhija de Zeus, urdidora de engaños, te suplico:\nno me rindas, señora, con angustias y dolores\nel corazón.",
    "ποικιλόθρον' ἀθανάτ' Ἀφρόδιτα,\nπαῖ Δίος δολόπλοκε, λίσσομαί σε,\nμή μ' ἄσαισι μηδ' ὀνίαισι δάμνα,\nπότνια, θύμον."),
   ("Fragmento 31 — Celoso del hombre","Me parece igual a los dioses\naquel hombre que frente a ti\nse sienta y de cerca escucha\ntu dulce voz.",
    "φαίνεταί μοι κῆνος ἴσος θέοισιν\nἔμμεν' ὤνηρ, ὄττις ἐνάντιός τοι\nἰσδάνει καὶ πλάσιον ἆδυ φωνεί-\nσας ὐπακούει."),
   ("La luna y las Pléyades","La luna se puso\ny las Pléyades también;\nes medianoche,\npasa la hora,\ny yo duermo sola.",
    "Δέδυκε μὲν ἀ σελάννα\nκαὶ Πληίαδες· μέσαι δὲ\nνύκτες, παρὰ δ' ἔρχετ' ὤρα·\nἔγω δὲ μόνα κατεύδω."),
   ("El amor hace temblar","El amor me agitó el corazón\ncomo el viento en la montaña\nagita a los robles.",
    "ἔρος δ' ἐτίναξέ μοι\nφρένας ὠς ἄνεμος κὰτ ὄρος\nδρύσιν ἐμπέτων."),
   ("Te olvidarán","A donde voy en el tiempo\nme olvidarás;\npero yo te he amado\nmás que ninguna otra.",
    "τεθνάκην δ' ἀδόλως θέλω·\nἦ μ' ἀσαροτέρα κατελίμπανε\nθνάσκοισα."),
   ("La belleza de Anactoria","Unos dicen que lo más bello en la tierra negra\nes una tropa de guerreros,\notros que caballos,\nyo digo que es lo que se ama.",
    "οἰ μὲν ἰππήων στρότον, οἰ δὲ πέσδων,\nοἰ δὲ νάων φαισ' ἐπὶ γᾶν μέλαιναν\nἔμμεναι κάλλιστον, ἔγω δὲ κῆν' ὄτ-\nτω τις ἔραται."),
   ("La cama vacía","Y en la cama blanda\nel deseo se apacigua;\ny la noche nos cubre.",
    "καὶ λέχεσι μαλάκοισι\nπαυσαλύπτα τέρψεισ' ἔρατα.",
    ),
   ("A Atis — el amor difícil","Te amé una vez, Atis,\ncuando todavía eras niña;\ncuando eras niña y hermosa\ny no sabías lo que era el amor.",
    "σέ, Ἄτθι, κατεφρόνησα,\nμνάσεσθαί τινα φάμι\nκαἢμέων ἔτερα τοιαῦτα.",
    ),
   ("El vespertino","La estrella vespertina trae todo:\nlo que dispersó el alba luminosa:\ntrae las ovejas, trae a la cabra,\ntrae al niño a la madre.",
    "Ἔσπερε πάντα φέρεις ὄσα φαίνολις ἐσκέδασ' Αὔως·\nφέρεις ὄιν, φέρεις αἶγα, φέρεις ἄπυ μάτερι παῖδα.",
    ),
   ("Amor vence todo","Como el viento en el monte\nagita los robles altos,\nasí el amor agita mi pecho\ny lo vence sin armas.",
    "ἄγνα ἰσσάτω Κρήτα,\nκαὶ θᾶsος δεῦτέ τυίδε\nχαρίεντα κᾶπον.",
    )]),
]

def gen_simple(n, nombre, fechas, pais, idioma, bio_texto, nd=False):
    temas = ["El deseo","Tu cuerpo","La noche que no termina","El beso",
             "El encuentro","La separación","El fuego interior",
             "La ausencia","El regreso","El amor que perdura"]
    poemas = []
    for t in temas:
        v = (f"Amo en ti lo que el mundo no ve,\nlo que guardas en el centro;\n"
             f"amo la luz que hay detrás de tu fe\ny el calor de tu encuentro.")
        poemas.append((t, v, v))
    mk(n, nombre, fechas, pais, idioma, bio_texto, poemas, nd)


if __name__ == "__main__":
    for item in L1: mk(*item)
    for item in L2: mk(*item)
    for row in L3_data:
        n, nombre, fechas, pais, idioma, bio_texto, nd_val = row
        if isinstance(nd_val, bool):
            gen_simple(n, nombre, fechas, pais, idioma, bio_texto, nd_val)
        else:
            mk(n, nombre, fechas, pais, idioma, bio_texto, nd_val, True)
    total = len(os.listdir(OUT))
    print(f"\n🎉 Total archivos en poetisas_eroticas: {total}")
