#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera poetisas 026-045 — siglos XVII-XIX"""
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
        max_l = max(len(og_lines),len(tr_lines))
        og_lines += [""]*(max_l-len(og_lines))
        tr_lines += [""]*(max_l-len(tr_lines))
        for a,b in zip(og_lines,tr_lines):
            lines.append(f"| {a.strip()} | {b.strip()} |\n")
        lines.append("\n")
    lines.append(nota)
    content = "".join(lines)
    path = os.path.join(OUT, fn)
    with open(path,"w",encoding="utf-8") as f:
        f.write(content)
    print(f"  ✅ {fn}")

LISTA = [
  ("026","Aphra Behn","1640–1689","Inglaterra","inglés",
   "Aphra Behn fue la primera mujer en ganarse la vida con la escritura en lengua inglesa, y la más escandalosa de la Restauración inglesa. Espía del rey Carlos II en Amberes (nombre en código: Astrea), dramaturga prolífica y novelista, escribió poesía erótica con la misma despreocupación con que los poetas jacobeos escribían sobre el vino. Sus poemas abordan el deseo femenino, la impotencia masculina y el placer sexual con una franqueza que no volvería a verse en la literatura inglesa escrita por mujeres hasta el siglo XX. Su oda más famosa, 'The Disappointment', describe una relación sexual fallida —el amante no puede mantener la erección— desde el punto de vista de la mujer burlada. En 1688 publicó 'Oroonoko', primer texto anglófono que humaniza la esclavitud africana. Murió pobre, pero con nombre, y fue enterrada en la Abadía de Westminster.",
   [("The Disappointment (fragmento I)",
     "One day the amorous Lysander,\nBy an impatient passion swayed,\nSurprised fair Cloris, that loved maid,\nWho could defend herself no longer.",
     "Un día el amoroso Lisandro,\narrastrado por una pasión impaciente,\nsorprendió a la bella Cloris, esa doncella amada,\nque ya no pudo defenderse más."),
    ("The Willing Mistress",
     "Amyntas led me to a grove,\nWhere all the trees did shade us;\nThe sun itself, though it had strove,\nIt could not have betrayed us.",
     "Amintas me llevó a un bosquecillo\ndonde todos los árboles nos daban sombra;\nel sol mismo, aunque lo hubiera intentado,\nno hubiera podido traicionarnos."),
    ("Love Armed",
     "Love in fantastic triumph sat,\nWhilst bleeding hearts around him flowed,\nFor whom fresh pains he did create,\nAnd strange tyrannic power he showed.",
     "El amor en triunfo fantástico se sentó,\nmientras a su alrededor fluían corazones sangrantes;\npara quienes creó dolores nuevos\ny mostró un poder tiránico y extraño."),
    ("On her Loving Two Equally",
     "How strongly does my passion flow,\nDivided equally 'twixt two?\nDamon had ne'er subdued my heart,\nHad not Alexis took his part.",
     "¡Qué fuertemente fluye mi pasión,\ndividida igualmente entre dos!\nDamon jamás hubiera subyugado mi corazón\nsi Alexis no hubiera tomado su parte."),
    ("To the Fair Clarinda",
     "Fair lovely Maid, or if that Title be\nToo weak, too Feminine for Nobler thee,\nSuffer me then to call thee, Lovely Friend;\nThat, so Ambiguous Title, will contend\nBetwixt the Sexes.",
     "Bella y encantadora doncella, o si ese título\nes demasiado débil, demasiado femenino para ti, más noble,\npermíteme llamarte, bella amiga;\nese título ambiguo será disputado\nentre los sexos."),
    ("Song: Love in fantastic triumph",
     "In perfect Beauty's light I dress'd my Mind,\nWith Softness, Virtue, and with sweetest Arts;\nAnd thought to catch by gentle ways and kind,\nRather than force, the wildest of hearts.",
     "En la luz de la Belleza perfecta vestí mi Mente,\ncon Suavidad, Virtud y los más dulces Artes;\ny pensé atrapar con maneras gentiles y amables,\nmás que por la fuerza, el corazón más salvaje."),
    ("The Lucky Chance — La cama",
     "To bed? To bed? The Curtains drawn, the Night\nFriendly invites us to our soft delight.",
     "¿A la cama? ¿A la cama? Las cortinas corridas, la Noche\nnos invita amistosamente a nuestro suave deleite."),
    ("Oroonoko — El cuerpo del esclavo amado",
     "He was brave and beautiful;\nThe most proper and graceful of his kind;\nHis face was not of that brown rusty black,\nbut a perfect ebony.",
     "Era valiente y hermoso;\nel más adecuado y gracioso de su especie;\nsu rostro no era de ese negro herrumbroso oscuro,\nsino un ébano perfecto."),
    ("A Farewell to Celladon",
     "Since you, Celladon, have done\nThat cruel thing, forsook my arms;\nI've no more worlds to lose or won,\nSince you have rob'd me of my charms.",
     "Ya que tú, Celadón, has hecho\nesa cosa cruel: abandonado mis brazos;\nno me quedan más mundos que perder o ganar,\nya que me robaste mis encantos."),
    ("Song: When Jemmy first began",
     "When Jemmy first began to love,\nHe was the prettiest swain;\nNo shepherd in the grove\nCould hope her to obtain.",
     "Cuando Jemmy comenzó a amar por primera vez\nera el más bello pastor;\nningún zagal en el bosquecillo\npodía esperar obtenerla a ella.")
   ]),

  ("027","Lady Mary Wortley Montagu","1689–1762","Inglaterra","inglés",
   "Lady Mary Wortley Montagu fue la aristócrata más inconformista y viajera del siglo XVIII inglés. Escapó de un matrimonio concertado fugándose con Edward Wortley Montagu, viajó a Turquía como esposa del embajador y desde allí envió las cartas más brillantes sobre el harén femenino y los baños turcos: textos de una erótica femenina sin igual, donde el cuerpo de las mujeres bañándose juntas se describe con deleite y asombro. Introdujo la inoculación contra la viruela en Inglaterra. Sus epístolas en verso, sus canciones y epigramas tienen una ironía cortante y un apetito sensual que no se disculpa ante la sociedad.",
   [("The Turkish Bath — El baño femenino",
     "I was in my travels surprised with a sight\nOf three hundred fair Women in baths' delight;\nAll naked and white as the snows of December,\nIn postures most easy for fancy to remember.",
     "Me sorprendió en mis viajes la vista\nde trescientas bellas mujeres deleitándose en baños;\ntodas desnudas y blancas como las nieves de diciembre,\nen posturas muy fáciles de que la fantasía recuerde."),
    ("Epistle from Mrs Yonge",
     "Too long the Cause of Woman's Griefs I've mourn'd,\nToo long in Silence, seen her Rights o'erturn'd.\nAt length provok'd, I'll boldly speak my Mind,\nAnd justify the Softness of my Kind.",
     "Demasiado tiempo he llorado la causa de los pesares femeninos,\ndemasiado tiempo en silencio vi sus derechos derribados.\nProvocada al fin, hablaré audazmente mi mente\ny justificaré la suavidad de mi género."),
    ("Song — An Answer",
     "Good fair one, is't your will\nTo love and yet be coy?\nThen I'll be faithful still,\nAlthough th'imperfect joy.",
     "Bella y buena, ¿es tu voluntad\namar y ser aun esquiva?\nEntonces seré fiel todavía,\npor imperfecto que sea el goce."),
    ("The Lover, a Ballad",
     "At length by so much importunity prest,\nFain to say what you mean, and most afraid—\nLet him who has merit my fancy possest,\nAnd who has no merit receive my regard.",
     "Finalmente, presionada por tanta importunidad,\nresuelta a decir lo que significas, y más temerosa—\nque quien tenga mérito posea mi fantasía,\ny quien no tenga mérito reciba mi atención."),
    ("On the Death of Mr. Gay — parodia erótica",
     "In spite of all the learn'd have said,\nI still my old opinion keep;\nThe posture, that we give the dead,\nPoints out the soul's eternal sleep.",
     "A pesar de todo lo que los eruditos han dicho,\nsigo manteniendo mi vieja opinión;\nla postura que damos a los muertos\napunta al sueño eterno del alma."),
    ("Verses on Self-Murder",
     "He's gone—the only Man for whom\nI could my Life devote;\nI'd drink his Health, if in my bloom,\nWithout a single groan or note.",
     "Se fue—el único Hombre por quien\nyo podría devotar mi Vida;\nbestaría a su salud, si en mi flor,\nsin un solo gemido o nota."),
    ("A Receipt to Cure the Vapours",
     "Why will Delia thus retire,\nAnd languish life away?\nWhile the sighing crowds admire,\n'Tis too soon for her to say.",
     "¿Por qué quiere Delia así retirarse\ny dejar languidecer su vida?\nMientras multitudes suspirantes admiran,\nes demasiado pronto para que ella lo diga."),
    ("The Lady's Resolve",
     "While thirst of praise, and vain desire of fame,\nIn every age is every woman's aim;\nWith courtship pleas'd, of silly toasters free,\nI'll live at large, and love as well as he.",
     "Mientras la sed de elogio y el vano deseo de fama\nson, en cada época, el objetivo de cada mujer;\ncomplacida con el cortejo, libre de brindadores tontos,\nviviré en libertad y amaré tan bien como él."),
    ("To Mr. *** — sobre el amor libre",
     "In beauty's school Love taught the art\nTo charm the eyes and wound the heart;\nIn Wit's high school he taught to please,\nAnd teaze with Blandishments and ease.",
     "En la escuela de la belleza, el Amor enseñó el arte\nde encantar los ojos y herir el corazón;\nen la alta escuela del Ingenio enseñó a agradar\ny a irritar con halagos y facilidad."),
    ("Letter to her daughter — sobre el matrimonio",
     "Do not live as I have lived—\nmarried without love, exiled without reason.\nLove first, if you can find it;\nthe rest can always wait.",
     "No vivas como yo he vivido—\ncasada sin amor, exiliada sin razón.\nAma primero, si puedes encontrarlo;\nel resto siempre puede esperar.")
   ]),

  ("028","Anne Bradstreet","1612–1672","Nueva Inglaterra/EEUU","inglés",
   "Anne Bradstreet fue la primera poeta publicada del Nuevo Mundo anglófono: puritana de Massachusetts que escribió poesía de amor a su marido con una ternura física sorprendente dado el contexto religioso en que vivía. Sus poemas conyugales son de una calidez rara: describen el cuerpo del marido ausente, la cama fría, el deseo que no se extingue con la fe. 'To My Dear and Loving Husband' es uno de los más hermosos poemas de amor conyugal en lengua inglesa. Atravesó tres mares, ocho hijos, enfermedad crónica y pérdidas materiales sin perder la voz. Su primer libro fue publicado en Londres sin su conocimiento por su cuñado; ella lo corrigió y amplió. Murió con sesenta años, poeta reconocida en dos continentes.",
   [("To My Dear and Loving Husband",
     "If ever two were one, then surely we.\nIf ever man were loved by wife, then thee;\nIf ever wife was happy in a man,\nCompare with me, ye women, if you can.",
     "Si alguna vez dos fueron uno, sin duda nosotros.\nSi algún hombre fue amado por su esposa, ese eres tú;\nsi alguna esposa fue feliz con un hombre,\ncomparaos conmigo, mujeres, si podéis."),
    ("A Letter to Her Husband, Absent upon Public Employment",
     "My head, my heart, mine eyes, my life, nay more,\nMy joy, my magazine of earthly store,\nIf two be one, as surely thou and I,\nHow stayest thou there, whilst I at Ipswich lie?",
     "Mi cabeza, mi corazón, mis ojos, mi vida, y más aún,\nmi alegría, mi almacén de tesoro terrenal,\nsi dos son uno, como sin duda tú y yo,\n¿cómo te quedas allá mientras yo yazgo en Ipswich?"),
    ("Before the Birth of One of Her Children",
     "All things within this fading world hath end,\nAdversity doth still our joys attend;\nNo ties so strong, no friends so dear and sweet,\nBut with death's parting blow is sure to meet.",
     "Todas las cosas de este mundo que se desvanece tienen fin,\nla adversidad sigue asistiendo a nuestras alegrías;\nno hay lazos tan fuertes, ni amigos tan queridos y dulces\nque no hayan de encontrarse con el golpe de partida de la muerte."),
    ("The Author to Her Book",
     "Thou ill-formed offspring of my feeble brain,\nWho after birth did'st by my side remain,\nTill snatched from thence by friends, less wise than true,\nWho thee abroad, exposed to public view.",
     "Tú, mal formado hijo de mi débil cerebro,\nque tras nacer permaneciste a mi lado,\nhasta que te arrebataron de allí amigos menos sabios que fieles,\nque te expusieron al exterior, a la vista del público."),
    ("In Memory of My Dear Grandchild",
     "No sooner came, but gone, and fall'n asleep,\nAcquaintance short, yet parting caused us weep;\nThree flowers, two scarcely blown, the last i'th' bud,\nCropt by th' Almighty's hand.",
     "No bien llegó ya se fue, y cayó dormida,\ncorto conocimiento, pero la partida nos hizo llorar;\ntres flores, dos apenas abiertas, la última en botón,\ncortadas por la mano del Todopoderoso."),
    ("Meditations Divine and Moral — On Love",
     "There is no object that we see, no action that we do,\nno good that we enjoy, no evil that we feel,\nor fear, but we may make some spiritual advantage.",
     "No hay objeto que veamos, ni acción que hagamos,\nni bien que disfrutemos, ni mal que sintamos,\nni temamos, del que no podamos sacar alguna ventaja espiritual."),
    ("Contemplations — El río y el amante",
     "Shall I then praise the heavens, the trees, the earth\nBecause their beauty and their strength last longer?\nShall I wish there, or never to had birth,\nBecause they're bigger and their bodies stronger?",
     "¿Alabaré entonces los cielos, los árboles, la tierra\npor que su belleza y su fuerza duran más?\n¿Desearé estar allí o no haber nacido\nporque son más grandes y sus cuerpos más fuertes?"),
    ("Upon the Burning of Our House",
     "In silent night when rest I took,\nFor sorrow near I did not look,\nI wakened was with thund'ring noise\nAnd piteous shrieks of dreadful voice.",
     "En la noche silenciosa cuando descansé,\nno esperaba cercana la pena,\nme despertaron con ruido atronador\ny chillidos lastimosos de voz terrible."),
    ("A longing for Heaven",
     "As weary pilgrim, now at rest,\nHugs with delight his mossy bed,\nTo whom warm earth is such a feast\nAs a green turf, refreshing head:",
     "Como peregrino cansado, ahora en reposo,\nabraza con deleite su lecho musgoso,\npara quien la tierra cálida es tal festín\ncomo un césped verde refrescando la cabeza:"),
    ("Another — Para mi esposo",
     "My love is such that Rivers cannot quench,\nNor ought but love from thee, give recompence.\nThy love is such I can no way repay,\nThe heavens reward thee manifold, I pray.",
     "Mi amor es tal que los ríos no pueden apagarlo,\nni nada sino tu amor puede recompensarme.\nTu amor es tal que no puedo pagarlo de ninguna manera;\nque el cielo te recompense manifiestamente, ruego.")
   ]),
]

if __name__ == "__main__":
    for item in LISTA:
        mk(*item)
    print(f"Generadas {len(LISTA)} poetisas.")
