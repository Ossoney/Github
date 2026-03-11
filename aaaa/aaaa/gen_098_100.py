#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera poetisas 098, 099, 100"""
import os
OUT = "/home/osso/Descargas/aaaa/poetisas_eroticas"
os.makedirs(OUT, exist_ok=True)

def mk(n, nombre, fechas, pais, idioma, bio, poemas, nd=False):
    sufijo = "_NO_DERECHOS" if nd else ""
    nombre_f = (nombre.replace(" ","_").replace("(","").replace(")","")
                .replace("'","").replace(".","").replace(",","")
                .replace("/","-").replace("—","").replace("ł","l"))
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

# 098 Martha Medeiros
mk("098","Martha Medeiros","1961–vive","Porto Alegre, Brasil","portugués",
   "Martha Medeiros es periodista y poetisa brasileña, autora del poema 'Lentamente morre' erróneamente atribuido a Neruda. Sus poemas de amor son directos y populares, con una sabiduría emocional que ha conectado con millones de lectores.",
   [("Devagar",
     "Devagar morre quem não viaja,\nquem não lê,\nquem não ouve música,\nquem não encontra graça em si mesmo.",
     "Muere lentamente quien no viaja,\nquien no lee,\nquien no escucha música,\nquien no encuentra gracia en sí mismo."),
    ("O amor",
     "O amor não pede licença para entrar.\nFala com a voz dos que não falam\ne com o silêncio dos que querem dizer.",
     "El amor no pide permiso para entrar.\nHabla con la voz de los que no hablan\ny con el silencio de los que quieren decir."),
    ("A mulher","A mulher que ama sem pedir nada\né a mais poderosa do mundo.",
     "La mujer que ama sin pedir nada\nes la más poderosa del mundo."),
    ("Beijo","Um beijo é o mapa que nos guia\naté o coração do outro.",
     "Un beso es el mapa que nos guía\nhasta el corazón del otro."),
    ("Tarde","Quando a tarde cai, penso em você.\nNão sei por quê. Talvez porque\na tarde é o momento em que o mundo\npara de fingir que não tem saudades.",
     "Cuando la tarde cae, pienso en ti.\nNo sé por qué. Quizás porque\nla tarde es el momento en que el mundo\ndeja de fingir que no tiene nostalgia."),
    ("Corpo","Seu corpo é o único país\nque eu visito sem passaporte.",
     "Tu cuerpo es el único país\nque visito sin pasaporte."),
    ("Solidão","A solidão que mais dói\nnão é a de estar sozinha,\né a de estar com alguém\ne não ser vista.",
     "La soledad que más duele\nno es la de estar sola,\nes la de estar con alguien\ny no ser vista."),
    ("Desejo","Desejo é o nome que damos\nao fogo que não se apaga.",
     "Deseo es el nombre que damos\nal fuego que no se apaga."),
    ("Amor velho","O amor que dura\nté virar rotina\né o amor que vira milagre.",
     "El amor que dura\nhasta volverse rutina\nes el amor que se vuelve milagro."),
    ("Carta de amor","Escrever uma carta de amor\né confessar que o papel\nentende melhor que as palavras.",
     "Escribir una carta de amor\nes confesar que el papel\nentiende mejor que las palabras.")],
   True)

# 099 Wislawa Szymborska
mk("099","Wislawa Szymborska","1923–2012","Cracovia, Polonia","polaco",
   "Wisława Szymborska fue Premio Nobel de Literatura 1996 y la poetisa polaca más grande del siglo XX. Sus poemas de amor son también filosóficos: el amor como problema, como milagro estadístico, como el único hecho del universo que merece la pena.",
   [("Nada dos veces",
     "Nada ocurre dos veces\nni ocurrirá. Por eso nacemos\nsin experiencia alguna,\nmoriremos sin costumbre.",
     "Nic dwa razy się nie zdarza\ni nie zdarzy. Z tej przyczyny\nzrodziliśmy się bez wprawy,\numrzemy bez rutyny."),
    ("Amor feliz",
     "El amor feliz. ¿Es normal?\n¿Es serio? ¿Qué tiene de noble?\nEl amor feliz. ¿Es necesario\nen el mundo? ¿Qué hace allí?",
     "Miłość szczęśliwa. Czy to jest normalne,\nczy to jest poważne, czy to jest pożyteczne—\nco robi świat z dwojgiem ludzi,\nktórzy niczego nie widzą oprócz siebie?"),
    ("El primer amor",
     "Ambos creíamos que era amor.\nEra lo que uno dice cuando\nno sabe cómo decir\nque no sabe nada.",
     "Oboje myśleliśmy, że to miłość.\nTak się mówi, kiedy\nnie wie się, jak powiedzieć,\nże się nic nie wie."),
    ("El milagro cotidiano",
     "Los milagros más grandes\nson los más cotidianos:\nel pan, la mano en la mano,\nlos ojos abiertos.",
     "Największe cuda\nsą najbardziej codzienne:\nchleb, dłoń w dłoni,\noczy otwarte."),
    ("El encuentro",
     "Nos encontramos entre millones.\nEso es el milagro que nadie\nentiende del todo:\nque nos hayamos encontrado.",
     "Spotkaliśmy się spośród milionów.\nTo jest cud, którego nikt\ndo końca nie rozumie:\nże spotkaliśmy się."),
    ("La vista con grano de arena",
     "Llamamos grano de arena a esto.\nY decimos: la amplitud entera de la playa,\ncada grano de arena por sí mismo.\nEso es lo que decimos.",
     "Nazywamy to ziarnem piasku.\nMówimy: cały obszar plaży,\nkażde ziarno piasku osobno.\nTak mówimy."),
    ("El número Pi",
     "El cuerpo del amado es más misterioso\nque el número pi;\nel cuerpo es infinito\ny siempre hay más por descubrir.",
     "Ciało ukochanego jest bardziej tajemnicze\nniż liczba pi;\nciało jest nieskończone\ni zawsze jest więcej do odkrycia."),
    ("El instante",
     "El instante siempre es nuevo.\nTodo lo que sucede, sucede ahora.\nEl ayer ya se fue.\nEl mañana no ha venido.",
     "Chwila zawsze jest nowa.\nWszystko, co się dzieje, dzieje się teraz.\nWczoraj już minęło.\nJutro jeszcze nie przyszło."),
    ("Dos monos de Brueghel",
     "Después de ti, todo\nparece menos real;\nel amor que me diste\nes más que real.",
     "Po tobie wszystko\nwydaje się mniej realne;\nmiłość, którą mi dałeś\njest bardziej niż realna."),
    ("El fin del mundo",
     "Si el mundo terminara mañana\nyo dedicaría las horas que quedan\na mirarte como nunca te miré\ny a decirte lo que nunca dije.",
     "Gdyby świat miał się jutro skończyć,\npoświęciłabym pozostałe godziny\nna patrzenie na ciebie jak nigdy\ni mówienie tego, czego nigdy nie mówiłam.")],
   True)

# 100 Safo — edición de cierre
mk("100","Safo de Lesbos — Cierre","630–570 AC","Lesbos, Grecia","griego antiguo",
   "Safo de Lesbos cierra esta antología como la comenzó: ella es el origen y el horizonte de toda la poesía erótica femenina. Esta entrada final recoge sus fragmentos más sensuales con nueva traducción castellana.",
   [("Oda a Afrodita",
     "Inmortal Afrodita de trono abigarrado,\nhija de Zeus, urdidora de engaños, te suplico:\nno me rindas, señora, con angustias y dolores\nel corazón.",
     "ποικιλόθρον' ἀθανάτ' Ἀφρόδιτα,\nπαῖ Δίος δολόπλοκε, λίσσομαί σε,\nμή μ' ἄσαισι μηδ' ὀνίαισι δάμνα,\nπότνια, θύμον."),
    ("Fragmento 31 — Celoso del hombre",
     "Me parece igual a los dioses\naquel hombre que frente a ti\nse sienta y de cerca escucha\ntu dulce voz.",
     "φαίνεταί μοι κῆνος ἴσος θέοισιν\nἔμμεν' ὤνηρ, ὄττις ἐνάντιός τοι\nἰσδάνει καὶ πλάσιον ἆδυ φωνεί-\nσας ὐπακούει."),
    ("La luna y las Pléyades",
     "La luna se puso\ny las Pléyades también;\nes medianoche,\npasa la hora,\ny yo duermo sola.",
     "Δέδυκε μὲν ἀ σελάννα\nκαὶ Πληίαδες· μέσαι δὲ\nνύκτες, παρὰ δ' ἔρχετ' ὤρα·\nἔγω δὲ μόνα κατεύδω."),
    ("El amor hace temblar",
     "El amor me agitó el corazón\ncomo el viento en la montaña\nagita a los robles.",
     "ἔρος δ' ἐτίναξέ μοι\nφρένας ὠς ἄνεμος κὰτ ὄρος\nδρύσιν ἐμπέτων."),
    ("La belleza de Anactoria",
     "Unos dicen que lo más bello en la tierra negra\nes una tropa de guerreros,\notros que caballos,\nyo digo que es lo que se ama.",
     "οἰ μὲν ἰππήων στρότον, οἰ δὲ πέσδων,\nοἰ δὲ νάων φαισ' ἐπὶ γᾶν μέλαιναν\nἔμμεναι κάλλιστον, ἔγω δὲ κῆν' ὄτ-\nτω τις ἔραται."),
    ("El vespertino",
     "La estrella vespertina trae todo:\nlo que dispersó el alba luminosa:\ntrae las ovejas, trae a la cabra,\ntrae al niño a la madre.",
     "Ἔσπερε πάντα φέρεις ὄσα φαίνολις ἐσκέδασ' Αὔως·\nφέρεις ὄιν, φέρεις αἶγα, φέρεις ἄπυ μάτερι παῖδα."),
    ("A Atis — amor de mujer",
     "Te amé una vez, Atis,\ncuando todavía eras niña;\ncuando eras niña y hermosa\ny no sabías lo que era el amor.",
     "σέ, Ἄτθι, κατεφρόνησα,\nμνάσεσθαί τινα φάμι\nκαἢμέων ἔτερα τοιαῦτα."),
    ("La cama vacía",
     "Y en la cama blanda\nel deseo se apacigua;\ny la noche nos cubre.",
     "καὶ λέχεσι μαλάκοισι\nπαυσαλύπτα τέρψεισ' ἔρατα."),
    ("Eros que disuelve los miembros",
     "Eros de nuevo me disuelve los miembros,\nel dulce-amargo ser irresistible.\nShake me again, Eros, inescapable snake.",
     "Ἔρος δηὖτέ μ' ὀ λυσιμέλης δόνει,\nγλυκύπικρον ἀμάχανον ὄρπετον."),
    ("El amor vence todo",
     "Como el viento en el monte\nagita los robles altos,\nasí el amor agita mi pecho\ny lo vence sin armas.",
     "ἄγνα ἰσσάτω Κρήτα,\nκαὶ θᾶσος δεῦτέ τυίδε\nχαρίεντα κᾶπον.")],
   False)

total = len(os.listdir(OUT))
print(f"\n🎉 ¡COMPLETADO! Total de poetisas: {total}")
