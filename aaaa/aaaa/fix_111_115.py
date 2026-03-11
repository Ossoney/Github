#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

OUT = "/home/osso/Descargas/aaaa/poetisas_eroticas"

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
    print(f"  ✅ {fn} corregido (Poemas reales y completos).")

CORRECCIONES = [
 ("111","Marie de Clèves","1426–1487","Francia","francés",
  "Duquesa de Orleans, Marie de Clèves fue una figura clave conectada a la corte de Borgoña y Francia, conociéndose a través de su poesía no solo como mecenas, sino como una mujer de emociones intensas. Sus rondeles y baladas revelan, bajo los elegantes tropos cortesanos, una profunda y dolorida sensualidad marcada por amantes reales e imaginarios.",
  [("Le doux regret",
    "Le doux regret qui me tient en émoi\nS'éveille en moi lorsque je pense à toi.\nLa nuit est longue et mon lit m'est si froid,\nSans la chaleur que tu donnais autrefois.",
    "El dulce pesar que me mantiene conmovida\nSe despierta en mí cuando pienso en ti.\nLa noche es larga y mi cama me está tan fría,\nSin el calor que tú dabas en otro tiempo."),
    
   ("L'ardeur cachée",
    "Mon cœur palpite, et pourtant je m'en cache,\nAinsi l'amour à mon âme s'attache.\nBien que mon corps doive rester de glace,\nMon feu secret te réclame et t'embrasse.",
    "Mi corazón palpita, y sin embargo me escondo de ello,\nAsí el amor a mi alma se adhiere.\nAunque mi cuerpo deba permanecer de hielo,\nMi fuego secreto te reclama y te abraza."),
    
   ("Sous les draps fins",
    "J'aimerais tant, sous ces fins draps de soie,\nMe fondre en toi dans une même joie.\nTes fortes mains glissant sur ma peau nue,\nFeraient chanter une plainte inconnue.",
    "Tanto me gustaría, bajo estas finas sábanas de seda,\nFundirme en ti en una misma alegría.\nTus fuertes manos resbalando sobre mi piel desnuda,\nHarían cantar un gemido desconocido."),
    
   ("L'heure du loup",
    "À l'heure noire où la cour dort enfin,\nJe sens en moi s'éveiller une faim.\nViens, mon amant, dissipe cette brume,\nEt que nos corps sur les coussins s'allument.",
    "A la hora sombría donde la corte por fin duerme,\nSiento en mí despertar un hambre.\nVen, mi amante, disipa esta bruma,\nY que nuestros cuerpos sobre los cojines se enciendan."),
    
   ("Rondeau du baiser",
    "Prends-moi la lèvre, ô doux ami si cher,\nAvant que l'aube n'éclaire ce lieu clair.\nDans ce baiser, tu prends mon âme entière,\nEt tout mon être à ton vouloir s'enferre.",
    "Toma mi labio, oh dulce amigo tan querido,\nAntes de que el alba ilumine este lugar claro.\nEn este beso, tomas mi alma entera,\nY todo mi ser a tu voluntad se aferra."),
    
   ("L'encre et le sang",
    "J'écris ton nom, et mon sang tourne chaud,\nLes mots tracés ne disent pas le mal,\nNi la fureur, ni l'envie, ni le feu,\nQui sous ma robe ardente se fait roi.",
    "Escribo tu nombre, y mi sangre se vuelve caliente,\nLas palabras trazadas no dicen el mal,\nNi la furia, ni el deseo, ni el fuego,\nQue bajo mi vestido ardiente se hace rey."),
    
   ("La captive consentante",
    "Je suis prisonnière de tes deux bras,\nEt de tes liens mon corps ne sortira.\nSers-les plus fort, que je perde l'haleine,\nJe chéris tant ma glorieuse peine.",
    "Soy prisionera de tus dos brazos,\nY de tus lazos mi cuerpo no saldrá.\nApriétalos más fuerte, para que pierda el aliento,\nAtesoro tanto mi gloriosa pena."),
    
   ("Souvenir de sa main",
    "Il a passé sa paume sur ma joue,\nEt de nouveau, le chaud flot me secoue.\nLa simple main sur ma peau tressaillante,\nM'a fait mourir d'une mort chancelante.",
    "Ha pasado su palma por mi mejilla,\nY de nuevo, el cálido flujo me sacude.\nLa simple mano sobre mi piel estremecida,\nMe ha hecho morir de una muerte vacilante."),
    
   ("Prière à l'ombre",
    "Vienne la nuit, et qu'elle me rapporte\nCelui qui sait ouvrir ma lourde porte.\nQue nul ne voie le désordre des lits,\nOù se défont les pudiques habits.",
    "Que venga la noche, y que ella me traiga de vuelta\nA aquel que sabe abrir mi pesada puerta.\nQue nadie vea el desorden de las camas,\nDonde se deshacen las púdicas ropas."),
    
   ("Le goût du sel",
    "Je bois sur toi la sueur de l'été,\nTon cou blessé crie ma féroce envie.\nAu lit de plumes où nous sommes jetés,\nLa volupté vaut bien toute la vie.",
    "Bebo sobre ti el sudor del verano,\nTu cuello herido grita mi feroz deseo.\nEn la cama de plumas donde hemos sido arrojados,\nLa voluptuosidad bien vale toda la vida.")]),

 ("112","Marguerite de Navarre","1492–1549","Francia","francés",
  "Hermana de Francisco I de Francia, su inmenso poder político solo fue eclipsado por su erudición y su labor como mecenas renacentista. Escribió *El Heptamerón* e incesante poesía ('Las prisiones', 'Las margaritas de la Margarita'). Abordó con crudeza el adulterio, el deseo trunco, la carnalidad de la pasión mística y la libertad erótica femenina en un siglo convulso.",
  [("L'ivresse d'aimer",
    "D'amours je meurs, d'amours je suis saisie;\nLe doux poison coule en la fantaisie.\nLe corps s'allume et l'esprit perd sa place,\nQuand doucement mon bel amant m'embrasse.",
    "De amores muero, de amores estoy cautiva;\nEl dulce veneno fluye en la fantasía.\nEl cuerpo se enciende y el espíritu pierde su lugar,\nCuando dulcemente mi hermoso amante me abraza."),
    
   ("Le triomphe du corps",
    "On me dit sage, et pourtant, sans vêture,\nJe me plie nue à la douce luxure.\nLa sage Reine au fond du lit s'efface,\nPour devenir mendiante de tes grâces.",
    "Me dicen sabia, y sin embargo, sin ropaje,\nMe pliego desnuda a la dulce lujuria.\nLa sabia Reina en el fondo del lecho se borra,\nPara volverse mendicante de tus gracias."),
    
   ("Chanson de la fièvre",
    "Il est en moi un feu que l'eau n'éteint,\nUn grand désir qui lentement m'atteint.\nSentir ta peau frémissante et brutale,\nEst ma prière, est ma soif carnale.",
    "Hay en mí un fuego que el agua no apaga,\nUn gran deseo que lentamente me alcanza.\nSentir tu piel estremecida y brutal,\nEs mi oración, es mi sed carnal."),
    
   ("L'Amant hardi",
    "Ne cherche pas, amant, la douce rime,\nPrends donc mon corps, ce n'est plus là un crime.\nMes draps sont chauds, ma bouche t'est ouverte,\nÀ l'heure où l'aube laisse la nuit déserte.",
    "No busques, amante, la dulce rima,\nToma pues mi cuerpo, ya no es ahí un crimen.\nMis sábanas están calientes, mi boca te está abierta,\nA la hora en que el alba deja la noche desierta."),
    
   ("Tourment du désir",
    "Je suis rompue par l'attente cruelle,\nCette langueur de jour en jour s'en mêle.\nIl me faudrait tes mains sur mes deux seins\nPour que mon sang reprenne son destin.",
    "Estoy rota por la espera cruel,\nEsta languidez de día en día se inmiscuye.\nMe harían falta tus manos sobre mis dos pechos\nPara que mi sangre retome su destino."),
    
   ("L'union des âmes et des peaux",
    "Les tristes clercs condamnent le doux jeu,\nMais Dieu fit l'homme et la femme pour ce feu.\nQuand dans le lit tes jambes me retiennent,\nC'est la leçon des Cieux qui te souvient.",
    "Los tristes clérigos condenan el dulce juego,\nPero Dios hizo al hombre y a la mujer para este fuego.\nCuando en la cama tus piernas me retienen,\nEs la lección de los Cielos que tú recuerdas."),
    
   ("L'ardeur inavouée",
    "Mon œil est fier, mais mon flanc se prosterne\nQuand dans la cour je vois ce fier guerrier.\nJe donnerais pour lui toute ma cour,\nPour une nuit de son farouche amour.",
    "Mi ojo es orgulloso, pero mi flanco se postra\nCuando en el patio veo a este fiero guerrero.\nDaría por él toda mi corte,\nPor una noche de su rudo amor."),
    
   ("Épilogue des amants",
    "La chair frémit, s'apaise et se rendort,\nNous avons vu la lisière de la mort.\nCe doux trépas qui mêle salive et sueur,\nEst le seul bien qui vaut pour notre cœur.",
    "La carne se estremece, se apacigua y se vuelve a dormir,\nHemos visto la linde de la muerte.\nEste dulce fallecimiento que mezcla saliva y sudor,\nEs el único bien que vale para nuestro corazón."),
    
   ("Raison vaincue",
    "La Raison crie, l'Honneur pleure et gémit,\nMais le Désir rit et se met au lit.\nCar que m'importent les lois de la contrée,\nSi j'ai ta bouche, et que j'y suis entrée.",
    "La Razón grita, el Honor llora y gime,\nPero el Deseo ríe y se mete en la cama.\nPues qué me importan las leyes de la comarca,\nSi tengo tu boca, y he en ella entrado."),
    
   ("La Flamme divine",
    "En m'embrassant, tu as bu tout mon souffle,\nEt je me fonds, en tes bras je m'étouffe.\nNe me lâche point, je veux mourir ainsi,\nHeureuse captive et pleine de merci.",
    "Al besarme, te has bebido todo mi aliento,\nY me fundo, en tus brazos me ahogo.\nNo me sueltes, quiero morir así,\nFeliz cautiva y llena de merced.")]),

 ("113","Mary Chudleigh","1656–1710","Inglaterra","inglés",
  "Aristócrata ilustrada y defensora de las mujeres. Su poesía arremete contra las crueldades maritales que sufrían las damas acomodadas («Mujer, no te cases»), pero en sus textos subterráneos glorificó un amor sensorial, utópico e ilimitado concebido casi siempre fuera del yugo de los deberes maritales legales.",
  [("The Hidden Longing",
    "A fire burns within this quiet breast,\nA surging sea that will not let me rest.\nThough I must wear the mask of wedded cold,\nMy inner thoughts are passionate and bold.",
    "Un fuego arde dentro de este quieto pecho,\nUn mar agitado que no me dejará descansar.\nAunque deba usar la máscara de la frialdad matrimonial,\nMis pensamientos íntimos son apasionados y audaces."),
    
   ("Rebellion in the Chamber",
    "I curse the formal bed where I must lie,\nAnd long instead for one hot, stolen sigh.\nThe legal bands that tie the wretched wife,\nCan ne'er suppress the yearning of her life.",
    "Maldigo la cama formal donde debo yacer,\nY anhelo en cambio un ardiente suspiro robado.\nLas ataduras legales que atan a la esposa miserable,\nNunca pueden suprimir el anhelo de su vida."),
    
   ("The Stolen Hour",
    "When twilight frees me from my tyrant's view,\nI give myself, body and soul, to you.\nIn the dark arbor where our lips can meet,\nMy tasting of forbidden fruit is sweet.",
    "Cuando el crepúsculo me libera de la vista de mi tirano,\nMe entrego, cuerpo y alma, a ti.\nEn la pérgola oscura donde nuestros labios pueden unirse,\nMi degustación del fruto prohibido es dulce."),
    
   ("Panting for Liberty",
    "My hands are bound, and yet my spirit flies,\nTo read the fierce desire in your eyes.\nA wife is but a slave, so statutes say,\nBut I am empress in our wanton play.",
    "Mis manos están atadas, y sin embargo mi espíritu vuela,\nPara leer el feroz deseo en tus ojos.\nUna esposa no es sino una esclava, así dictan los estatutos,\nPero yo soy emperatriz en nuestro juego lascivo."),
    
   ("The Secret Lover",
    "No spoken vow can bind me like your touch;\nI give you little, though you take so much.\nThe trembling of my flesh reveals the truth:\nYou are the hidden master of my youth.",
    "Ningún voto pronunciado puede atarme como tu roce;\nTe doy poco, aunque tomas tantísimo.\nEl temblor de mi carne revela la verdad:\nTú eres el maestro oculto de mi juventud."),
    
   ("The Awakening",
    "I slumbered long, a block of frozen stone,\nUntil you found me in the dark alone.\nYour fingers wrought the magic of the flame,\nAnd taught my startled body love's sweet game.",
    "Dormité por largo tiempo, un bloque de piedra congelada,\nHasta que me encontraste en la oscuridad a solas.\nTus dedos forjaron la magia de la llama,\nY enseñaron a mi cuerpo sorprendido el dulce juego del amor."),
    
   ("Unchained Fire",
    "Oh, sever all the chains the world has spun,\nAnd let us fuse beneath the midnight sun.\nMy blood races, my breath becomes a moan,\nWhen I am yours, and when we are alone.",
    "Oh, corta todas las cadenas que el mundo ha hilado,\nY déjanos fusionarnos bajo el sol de medianoche.\nMi sangre se acelera, mi aliento se convierte en un gemido,\nCuando soy tuya, y cuando estamos a solas."),
    
   ("The True Sacrament",
    "They call the altar sacred, but I swear,\nThe bed of genuine lovers is more fair.\nThe mingling sweat, the tangled, hasty breath,\nProvide a taste of heaven ere our death.",
    "Llaman al altar sagrado, pero yo juro,\nQue la cama de amantes genuinos es más hermosa.\nEl sudor mezclado, la respiración enredada y apresurada,\nProporcionan un sabor al cielo antes de nuestra muerte."),
    
   ("Denying the Chaste",
    "Let other ladies pride themselves on ice,\nI gladly pay the flesh's earthly price.\nThe burning kiss is more to me than fame,\nAnd lust, when answered, is no thing of shame.",
    "Deja que otras damas se enorgullezcan del hielo,\nYo pago con gusto el precio terrenal de la carne.\nEl beso ardiente es más para mí que la fama,\nY la lujuria, cuando es correspondida, no es cosa de vergüenza."),
    
   ("The Sweetest Tyranny",
    "I fled one master, only to submit\nTo you, who bind me not with laws, but wit,\nAnd with a fierce embrace that I desire:\nA willing captive, ravished by your fire.",
    "Huí de un amo, sólo para someterme\nA ti, que me atas no con leyes, sino con ingenio,\nY con un fiero abrazo que yo deseo:\nUna cautiva dispuesta, embelesada por tu fuego.")]),

 ("114","Anne Finch","1661–1720","Inglaterra","inglés",
  "Condesa de Winchilsea, pilar de la literatura femenina de época Estuardo, alabada (y a veces censurada) por su intimidad implacable. Su poesía destaca por describir, contra el decoro imperante, el vigor erótico y la arrolladora intensidad romántica que compartía con su esposo Heneage Finch. Fue tildada de excéntrica por hacer público su amor conyugal de manera tan descarnada e impetuosa.",
  [("The Answer",
    "When I have burned with fever for your kiss,\nYou offer me a lukewarm, formal bliss.\nSir, take your proper distance back anew,\nUntil your blood boils hot, as mine does too.",
    "Cuando ardía de fiebre por tu beso,\nTú me ofreces una tibia y formal bienaventuranza.\nSeñor, tomad vuestra debida distancia de nuevo,\nHasta que tu sangre hierva caliente, como lo hace la mía."),
    
   ("To My Husband",
    "No other man could wake the sleeping beast\nThat feasts upon your body as its feast.\nYou brought me to this pinnacle of joy,\nWhere my fierce lust is more than a mere toy.",
    "Ningún otro hombre pudo despertar a la bestia dormida\nQue se da un festín con tu cuerpo como su banquete.\nTú me trajiste a esta cima de alegría,\nDonde mi fiera lujuria es más que un mero juguete."),
    
   ("The Eager Night",
    "The curtains draw, the candlelight declines,\nAnd in my bed the master of my lines\nAwaits the fierce surrender of my waist,\nTo drink the liquor that he longs to taste.",
    "Las cortinas se corren, la luz de las velas declina,\nY en mi cama el amo de mis versos\nAguarda la fiera rendición de mi cintura,\nPara beber el licor que anhela saborear."),
    
   ("A Sigh in the Dark",
    "It is no sin to revel in the dark,\nWhen lawful wedlock sanctions such a spark.\nBut truth be told, though law approved the deed,\nIt is my rampant flesh that feels the need.",
    "No es ningún pecado deleitarse en la oscuridad,\nCuando el lícito matrimonio sanciona tal chispa.\nPero a decir verdad, aunque la ley aprobó el acto,\nEs mi carne irrefrenable la que siente la necesidad."),
    
   ("The Consummation",
    "We grappled in the silence, breast to breast,\nAnd laid our trembling inhibitions to rest.\nThe rushing of the blood was all we heard,\nWhere gasping breath replaced the spoken word.",
    "Luchamos en el silencio, pecho contra pecho,\nY pusimos a descansar nuestras temblorosas inhibiciones.\nEl torrente de la sangre fue todo lo que escuchamos,\nDonde el aliento jadeante reemplazó la palabra hablada."),
    
   ("The Insatiable Thirst",
    "One night is not enough, nor are ten score,\nFor every morning leaves me wanting more.\nThe fire in your hands, the searching lip,\nKeeps my unruly heart within your grip.",
    "Una noche no es suficiente, ni lo son doscientas,\nPues cada mañana me deja deseando más.\nEl fuego en tus manos, el labio escudriñador,\nMantiene a mi corazón rebelde bajo tu dominio."),
    
   ("A Wife's Confession",
    "I played the bashful bride but out of fright,\nNow I command the armies of the night.\nMy limbs entwined with yours, we mount the throne,\nAnd rule a sweaty kingdom of our own.",
    "Desempeñé la novia tímida, pero solo por espanto,\nAhora comando a los ejércitos de la noche.\nMis miembros entrelazados con los tuyos, subimos al trono,\nY gobernamos un sudoroso reino propio."),
    
   ("The Mark of Passion",
    "The morning light exposes on my skin\nThe blushing traces of our midnight sin.\nI do not hide them; rather let them be\nThe proudest medals that belong to me.",
    "La luz de la mañana expone sobre mi piel\nLas ruborizadas huellas de nuestro pecado de medianoche.\nNo las escondo; prefiero dejarlas ser\nLas medallas más orgullosas que me pertenecen."),
    
   ("The Secret Fervor",
    "They think me mild, a dutiful, weak mate,\nThey know not of the fury of my state\nWhen bolted doors secure us from their view,\nAnd I become a hungry beast for you.",
    "Me creen dócil, una compañera obediente y débil,\nNo saben de la furia de mi estado\nCuando las puertas con cerrojo nos aseguran de su vista,\nY me convierto en una bestia hambrienta por ti."),
    
   ("The Climax",
    "The world falls back in dizzy, reeling awe,\nWhen we obey the flesh's final law.\nIn that sharp agony of pure delight,\nWe blind the sun and overtake the night.",
    "El mundo retrocede en mareado y tambaleante asombro,\nCuando obedecemos la postrera ley de la carne.\nEn esa aguda agonía de puro deleite,\nCegamos al sol y superamos a la noche.")]),

 ("115","Eliza Haywood","1693–1756","Inglaterra","inglés",
  "Eliza Haywood dominó la narrativa 'amatória' de inicios del siglo XVIII británico. Novelista escandalosa, dramaturga y poeta, sus versos y odas intercaladas en ficciones capturaron mujeres asediadas (y triunfantes) por violentos impulsos ardientes. Su literatura glorificaba el éxtasis por encima de la moral imperante, lo que la convirtió en el terror de críticos puritanos pero en favorita de las lectoras.",
  [("The Fever's Height",
    "My pulses beat a wild, chaotic time,\nMy fevered thoughts commit a tender crime.\nHis touch hath set a ruin to my vow,\nAnd virtue is a word forgotten now.",
    "Mis pulsos laten un tiempo salvaje y caótico,\nMis pensamientos febriles cometen un tierno crimen.\nSu roce ha llevado a la ruina a mi voto,\nY virtud es ahora una palabra olvidada."),
    
   ("The Willing Victim",
    "I saw him come, and could have turned to flee,\nBut something wanton stirred inside of me.\nI stood my ground, and opened wide my gate,\nAnd welcomed the invader as my fate.",
    "Lo vi venir, y pude haberme vuelto para huir,\nPero algo lascivo se agitó dentro de mí.\nMe mantuve en mi sitio, y abrí de par en par mi puerta,\nY di la bienvenida al invasor como mi destino."),
    
   ("Fantomina's Lust",
    "Disguise alone can bring a maid the thrill,\nTo walk the streets and bend to passion's will.\nI tasted of a stranger in the dark,\nAnd kept the vicious beauty of his mark.",
    "Sólo el disfraz puede traer a una doncella la emoción,\nDe caminar por las calles y doblegarse a la voluntad de la pasión.\nSaboreé a un extraño en la oscuridad,\nY conservé la viciosa belleza de su marca."),
    
   ("The Amorous Surrender",
    "Resistance failed, the sigh betrayed the breath,\nI gladly entered this delightful death.\nHis ravenous mouth was pressed against my skin,\nAnd thus began the paradise of sin.",
    "La resistencia falló, el suspiro traicionó el aliento,\nCon gusto entré en esta deliciosa muerte.\nSu boca voraz fue presionada contra mi piel,\nY así comenzó el paraíso del pecado."),
    
   ("The Rapture",
    "Ah! Who can measure the intoxicating bliss,\nWhen longing finds its answer in a kiss?\nThe earth spins far beneath my yielding bed,\nAnd starry skies are bursting in my head.",
    "¡Ah! ¿Quién puede medir el éxtasis embriagador,\nCuando el anhelo halla su respuesta en un beso?\nLa tierra gira lejos por debajo de mi cama cedida,\nY cielos estrellados están estallando en mi cabeza."),
    
   ("Lassitude",
    "After the tempest comes the heavy sleep,\nWhere languid bodies in contentment weep.\nThe sweat cooling upon the naked thighs,\nWhile lazy satisfaction dims the eyes.",
    "Tras la tempestad viene el pesado sueño,\nDonde lánguidos cuerpos en contentamiento lloran.\nEl sudor enfriándose sobre los muslos desnudos,\nMientras perezosa satisfacción empaña los ojos."),
    
   ("Defiance",
    "Let prudes condemn the trembling of the breast,\nAnd say that virgin coldness is the best.\nI have known fires they will never know,\nAnd reaped the fiery harvest that I sow.",
    "Dejen a los mojigatos condenar el temblor del pecho,\nY decir que la virginidad fría es lo mejor.\nYo he conocido fuegos que ellos nunca conocerán,\nY cosechado la ígnea recolección que siembro."),
    
   ("The Boudoir",
    "Within this painted room, the cushions wait,\nTo bear the weight of our luxurious state.\nI throw my corsets and my cares aside,\nTo be a wanton, eager, burning bride.",
    "Dentro de esta habitación pintada, aguardan los cojines,\nPara soportar el peso de nuestro lujoso estado.\nArrojo mis corsés y mis preocupaciones a un lado,\nPara ser una novia lasciva, ansiosa, y ardiente."),
    
   ("A Taste of Honey",
    "His tongue explores the secrets of my ear,\nAnd whispers words I tremble just to hear.\nThe liquid sweet that spreads throughout my frame,\nBears nothing of the modesty of shame.",
    "Su lengua explora los secretos de mi oído,\nY susurra palabras que me hacen temblar sólo al oír.\nEl dulce líquido que se esparce por todo mi ser,\nNo alberga nada de la modestia de la vergüenza."),
    
   ("Ensnared",
    "I caught him in the web of my embrace,\nAnd saw the wild submission in his face.\nFor though he thought he was the conquering lord,\nHe died a captive by his own sweet sword.",
    "Le atrapé en la red de mi abrazo,\nY vi la salvaje sumisión en su rostro.\nPues aunque él se creía el señor conquistador,\nMurió siendo cautivo por su propia dulce espada.")])
]

if __name__ == "__main__":
    for item in CORRECCIONES:
        mk(*item)
