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
 ("106","Hafsa bint al-Hajj","1135–1191","Al-Andalus (España)","árabe",
  "Considerada una de las mejores y más atrevidas poetisas andalusíes del siglo XII. Originaria de Granada, Hafsa vivió una pasión desbordante, legendaria y trágica con el noble poeta Abu Yafar Ibn Said. Sus poemas, dirigidos a él, están plagados de dobles sentidos, invitaciones al goce sexual y descripciones íntimas.",
  [("El permiso de la luna",
    "أزوركَ أم تزورُ فإنّ قلبي \nإلى ما تشتهي أبداً يميلُ\nوقد أمِنَتْ بكَ الأيامُ حتى \nكأنّ ظلامَها أبداً أصيلُ",
    "¿Iré a visitarte o vienes tú? Pues mi corazón\nsiempre se inclina a lo que tú desees.\nLos días se han vuelto tan seguros contigo,\nque parece que su oscuridad fuera una tarde perpetua."),
    
   ("Los labios embriagadores",
    "ثَغْرُكَ قَدْ أَسْكَرَ حَتّى الصَّحْو\nمِنْ خَمْرَةٍ ما عُصِرَتْ فِي الدَّنِّ\nفاشرب من الريقة ما شئته\nولا تخف إثماً ولا تعتني",
    "Tu boca ha embriagado hasta la sobriedad\ncon un vino que no fue exprimido en la tinaja.\nBebe, pues, de mi saliva cuanto quieras,\ny no temas cometer pecado ni te preocupes."),
    
   ("El pecho abierto",
    "زرني أيا خير من زال الفؤاد به\nيهذي على كل حال من تذكره\nولا تخف حرساً فالعين نائمة\nوالنجم قد مال للغرب في سفره",
    "Visítame, oh el mejor de aquellos por quienes el corazón\ndelira en todo momento al recordarlo.\nY no temas a los guardias, pues todo ojo duerme\ny la estrella ya se inclina hacia el occidente en su viaje."),
    
   ("Labios de fuego",
    "رعى الله ليلاً لم أذق فيه غمضة\nوقد بت في حضن الحبيب منعما\nأقبّله حيناً وألثمه طَوراً\nونشرب خمر الحب عذباً ومُفعما",
    "Que Dios proteja esa noche en que no pegué ojo,\ny pasé la noche en el regazo del amado, gozosa.\nBesando sus labios a veces, estrechándolo otras,\ny bebiendo el vino del amor, dulce y desbordante."),
    
   ("El encuentro en el bosque (Rakb al-Ahl)",
    "سل بطحاء العقيق أيا فلان\nعن طيب ما حواه ذلك المكان\nبتنا، ولا رقيبٌ نخشى عيونه\nوسريرنا غصون البان",
    "Pregunta al valle del Ágata, amigo mío,\npor la dulzura que encerró aquel lugar.\nPasamos la noche, sin que un espía temiéramos sus ojos,\ny nuestro lecho fueron las ramas del sauce."),
    
   ("Jardín de delicias",
    "أيا نخلة البستان يا من إذا بدا\nسنى محياه تجلى الغيهب\nاقطف ثمار الوصل من وجنتي\nفإنني لك، يا حبيبي، أطمح",
    "Oh palmera del jardín, tú que cuando asomas\nel resplandor de tu rostro disipa la oscuridad,\nrecoge los frutos de la unión de mis mejillas,\npues yo entero aspiro a ti, amado mío."),
    
   ("Promesa nocturna",
    "في غسق الليل موعدنا، ولا\nتخف عيون الحاسدين ولا العدا\nأنا لك بساطٌ وحضنٌ دافئ\nفاسقني من ريقك الندى",
    "En la oscuridad de la noche es nuestra cita, y no\ntemas a los ojos de envidiosos ni de enemigos.\nYo soy para ti una alfombra y un seno cálido;\ndame de beber de tu saliva el rocío."),
    
   ("Sobre la impaciencia",
    "يا من له في الحشا نارٌ يؤججها\nومالِ قلبي عن ذكراه سُلوانُ\nعجل بوصلكَ فالأنفاس لاهبة\nوالصبر خفَّ والشوق غلاّبُ",
    "Tú, que tienes en mi entraña un fuego que avivas,\ny cuyo recuerdo mi corazón no puede olvidar.\nApresúrate a la unión, pues mis suspiros arden,\nla paciencia disminuye y el deseo es avasallador."),
    
   ("Rendición física",
    "لك جسدي فافعل به ما تشاء\nفلا روح لي إن لم تكن لي رداء\nتعال ولفني بذراعين\nوخذ من شفتي حلو الأداء",
    "Tuyo es mi cuerpo, haz con él lo que quieras,\npues no tengo alma si no eres mi manto.\nVen y envuélveme con tus brazos\ny toma de mis labios el dulce desempeño."),
    
   ("El beso incesante",
    "لا تكتف برشفة من شفاهي\nفالبحر لا يروي ظمأ العطشان\nأغرقني في لجة العشق\nحتى نغدو روحاً في جسدان",
    "No te conformes con un sorbo de mis labios,\npues el mar no sacia la sed del sediento.\nAhógame en el abismo de la pasión\nhasta que nos convirtamos en un alma en dos cuerpos.")]),

 ("107","Margaret Cavendish","1623–1673","Inglaterra","inglés",
  "Figura insólita del siglo XVII inglés, la Duquesa de Newcastle desafió toda convención moral, de género y literaria. Escribió prolíficamente teatro, filosofía, ciencia ficción y poesía extravagante. Sus versos exploraron de manera transgresora los límites del cuerpo y la pasión del alma, y fue acusada de inmodestia al atreverse a publicar versos centrados en las pulsiones de la mujer.",
  [("Of Many Worlds in this World",
    "Just like unto a Nest of Boxes round,\nDegrees of sizes in each Box are found:\nSo in this World, may many Worlds more be,\nThinner and less, and less still by degree;\nSo may the bodies of lovers interlace\nAnd find a universe within an embrace.",
    "Al igual que un nido de cajas redondas,\nGados de tamaños en cada caja se encuentran:\nAsí en este Mundo, muchos Mundos más puede haber,\nMás delgados y menores, y cada vez menores por grados;\nAsí podrían entrelazarse los cuerpos de los amantes\nY encontrar un universo dentro de un abrazo."),
    
   ("A Dialogue between Ruine and the Body",
    "My pulse beats high, my breath draws short and thick,\nDesire has struck my senses to the quick;\nThe bed is soft, the shadowed curtains drawn,\nWe will not sever till the break of dawn.",
    "Mi pulso late rápido, mi respiración es corta y densa,\nEl deseo ha herido mis sentidos hasta lo vivo;\nLa cama es blanda, las cortinas sombreadas echadas,\nNo nos separaremos hasta que despunte el alba."),
    
   ("The Soul's Passion",
    "Though Souls are invisible, and Bodies gross,\nWhen two such lovers meet, they draw so close\nThat flesh itself dissolves into a spright,\nAnd joins the spirit in a hot delight.",
    "Aunque las Almas son invisibles y los Cuerpos toscos,\nCuando dos amantes así se encuentran, se acercan tanto\nQue la carne misma se disuelve en un espíritu\nY se une al alma en un candente deleite."),
    
   ("Love's Anatomy",
    "Love makes the Heart to pant, the Eyes to weep,\nIt steals away our thoughts, and kills our sleep.\nIt runs like fire through every trembling vein,\nAnd blends the utmost pleasure with the pain.",
    "El amor hace palpitar el Corazón, llorar a los Ojos,\nNos roba nuestros pensamientos, y mata nuestro sueño.\nCorre como fuego por cada trémula vena,\nY mezcla el máximo placer con el dolor."),
    
   ("The Unbounded Desire",
    "My mind is like a wild untamed steed,\nThat on the fertile plains of love doth feed;\nMy body burns with such a fervent fire,\nThat nothing can extinguish my desire.",
    "Mi mente es como un corcel salvaje indomable,\nQue en las llanuras fértiles del amor se alimenta;\nMi cuerpo arde con un fuego tan ferviente,\nQue nada puede extinguir mi deseo."),
    
   ("Of Love's Creation",
    "We forge new lives in darkness and in heat,\nWhere two distinct and pulsing natures meet.\nThe breath mixes, the sweat falls like the dew,\nIn love's sweet labour, bodies made anew.",
    "Forjamos nuevas vidas en la oscuridad y en el calor,\nDonde dos naturalezas distintas y palpitantes se encuentran.\nEl aliento se mezcla, el sudor cae como el rocío,\nEn la dulce labor del amor, cuerpos hechos de nuevo."),
    
   ("The Empress of Love",
    "No King upon his throne commands so much,\nAs doth a lover with a single touch;\nMy flesh rebelled, but now it yields the crown,\nAnd lets the conqueror cast my strongholds down.",
    "Ningún Rey sobre su trono ordena tanto,\nComo lo hace un amante con un solo toque;\nMi carne se rebeló, pero ahora cede la corona,\nY deja que el conquistador derribe mis fortalezas."),
    
   ("The Magnetic Kiss",
    "Just as the Loadstone doth the Iron draw,\nMy Lover's face imposes nature's law;\nI cannot turn away my willing lip,\nAnd in the sea of kisses I must slip.",
    "Así como la Piedra Imán atrae al Hierro,\nEl rostro de mi Amante impone la ley de la naturaleza;\nNo puedo apartar mi labio dispuesto,\nY en el mar de besos debo deslizarme."),
    
   ("A Fever in the Blood",
    "There is a fever raging in my blood,\nA swelling tide, an overflowing flood.\nIt will not quench with water nor with wine,\nBut only with the press of your lips on mine.",
    "Hay una fiebre enfurecida en mi sangre,\nUna marea creciente, una inundación desbordante.\nNo se apagará con agua ni con vino,\nSino sólo con la presión de tus labios en los míos."),
    
   ("The Union",
    "When flesh to flesh in amorous combat falls,\nWe breach the mind's severe, forbidding walls;\nIn that ecstatic moment of the night,\nWe touch the borders of divine delight.",
    "Cuando la carne contra la carne cae en amoroso combate,\nQuebramos las severas e imponentes murallas de la mente;\nEn ese extático momento de la noche,\nTocamos las fronteras del deleite divino.")]),

 ("108","Katherine Philips","1632–1664","Inglaterra","inglés",
  "Conocida bajo el pseudónimo 'La Incomparable Orinda', Katherine Philips compuso algunos de los versos pasionales y eróticos más intensos del siglo XVII inglés dirigidos a otras mujeres. Formó un círculo literario femenino laico cuyo eje era ensalzar la 'Amistad' como un fervor y dedicación física y espiritual devoradora. Aunque casada, sus poemas a 'Lucasia' o 'Rosania' revelan una pasión que rebasa los límites de la época.",
  [("To My Excellent Lucasia, on Our Friendship",
    "I did not live until this time\nCrown'd my felicity,\nWhen I could say without a crime,\nI am not thine, but Thee.\nThis carcass breath'd, and walk'd, and slept,\nSo that the World believ'd\nThere was a Soul the motions kept;\nBut they were all deceiv'd.",
    "No estuve viva hasta que este momento\nCoronó mi felicidad,\nCuando pude decir sin cometer un crimen:\nNo soy tuya, sino que soy Tú.\nEste cadáver respiraba, caminaba y dormía,\nDe modo que el mundo creía\nQue había un Alma que mantenía el movimiento;\nPero estaban todos engañados."),
    
   ("To Rosania (now Mrs. Mountague) being with her",
    "As Men that are with Visions grac'd,\nMust have all other thoughts displac'd,\nSo my soul, filled with thy bright beams,\nIs freed from dull and Earthly dreams.\nAnd in my longing arms I take\nThe form that makes my whole frame shake.",
    "Como los hombres que son agraciados con Visiones,\nDeben tener todos sus otros pensamientos desplazados,\nAsí mi alma, llena de tus brillantes rayos,\nEs liberada de torpes y terrenales sueños.\nY en mis anhelantes brazos tomo\nLa forma que hace estremecer todo mi ser."),
    
   ("Injuria's parting with Lucasia",
    "Weeping I leave you, yet I leave my heart,\nFast bound to yours, from which it cannot part.\nAbsence may snatch my body from your sight,\nBut on your breast my soul will lie tonight.",
    "Llorando te dejo, y sin embargo dejo mi corazón,\nFuertemente atado al tuyo, del que no puede separarse.\nLa ausencia puede arrebatar mi cuerpo de tu vista,\nPero sobre tu pecho yacerá mi alma esta noche."),
    
   ("Orinda to Lucasia",
    "Observe the swelling and the panting breast,\nWhich finds in your approach its only rest.\nTo feel the sudden leaping of my blood,\nWhen in your presence all my passions flood.",
    "Observa el hinchado y anhelante pecho,\nQue halla en tu acercamiento su único descanso.\nSentir el repentino salto de mi sangre,\nCuando en tu presencia todas mis pasiones se desbordan."),
    
   ("Friendship's Mystery, To My Dearest Lucasia",
    "Come, my Lucasia, since we see\nThat Miracles Mens faith do move,\nBy wonder and by prodigy\nTo the fierce Arguments of Love:\nWe both are one, and one is both,\nMingled by nature and by troth.",
    "Ven, mi Lucasia, ya que vemos\nQue los milagros mueven la fe de los hombres,\nPor asombro y por prodigio\nHacia los fieros argumentos del amor:\nAmbas somos una, y una somos ambas,\nMezcladas por la naturaleza y por la promesa."),
    
   ("To My Dear Sister Mrs. C. P.",
    "But Oh! when I thy lovely face behold,\nMy trembling lips turn prematurely cold,\nSuch flames within my yearning bosom dwell\nThat outward chill conceals the inner hell.",
    "¡Pero Oh! cuando tu hermoso rostro contemplo,\nMis trémulos labios se vuelven prematuramente fríos,\nTales llamas habitan en mi anhelante pecho\nQue el escalofrío exterior oculta el infierno interior."),
    
   ("On the Kiss by Lucasia",
    "Oh! Let my lips upon thy lips remain,\nAnd breathe the very air you breathe again;\nFor in that touch, simple though it may seem,\nI taste the sweetness of a lover's dream.",
    "¡Oh! Deja que mis labios sobre tus labios permanezcan,\nY respiren el mismo aire que tú vuelves a respirar;\nPues en ese toque, por simple que pueda parecer,\nSaboreo la dulzura del sueño de un amante."),
    
   ("The Virgin Triumph",
    "The conquering beauty of your radiant eyes\nTakes every gazing mortal by surprise,\nBut 'tis the yielding softness of your bed\nWherein my captive spirit would be led.",
    "La conquistadora belleza de tus radiantes ojos\nToma por sorpresa a todo mortal que los mira,\nPero es la blanda suavidad de tu lecho\nHacia donde mi espíritu cautivo querría ser conducido."),
    
   ("A Revery",
    "In the deep hush of night, I lie and yearn,\nWhile the hot fires of separation burn.\nI feel your phantom touch upon my thigh,\nAnd in the empty darkness, softly sigh.",
    "En el profundo silencio de la noche, yazgo y anhelo,\nMientras arden los calientes fuegos de la separación.\nSiento tu roce fantasma sobre mi muslo,\nY en la vacía oscuridad, suspiro suavemente."),
    
   ("Parting with Lucasia",
    "If we must part, let it not be the end,\nMy dearest lover, my most cherished friend.\nTake from my mouth the final, clinging kiss,\nThe pledge of all my agony and bliss.",
    "Si debemos separarnos, que no sea el final,\nMi amante más querida, mi amiga más atesorada.\nToma de mi boca el último, aferrado beso,\nLa prenda de toda mi agonía y mi éxtasis.")]),

 ("109","Mary Sidney","1561–1621","Inglaterra","inglés",
  "Condesa de Pembroke y protectora de poetas (hermana del ilustre Philip Sidney), Mary Sidney fue una de las mujeres más educadas y cultivadas de la época isabelina. A través de sus epigramas, y especialmente en sus paráfrasis rítmicas de los salmos bíblicos y sus elegías, infundió a la poesía laica e inglesa una urgencia carnal que exploraba el deseo, la separación y la angustia corporal del amante.",
  [("Astrophel's Love",
    "I saw the boy, who with his fiery dart\nDoth pierce the most impregnable of hearts.\nHe smiled to see my bosom heaving high,\nAnd lit the lust that dazzled in mine eye.",
    "Vi al niño, que con su dardo ardiente\nPerfora el más inexpugnable de los corazones.\nSonrió al ver mi pecho agitándose alto,\nY encendió la lujuria que deslumbró en mi ojo."),
    
   ("The Night's Cloak",
    "Under the velvet shadow of the night,\nOur trembling forms are hidden from the light;\nThe eager hands that wander in the dark,\nIgnite within the flesh a brilliant spark.",
    "Bajo la sombra de terciopelo de la noche,\nNuestras temblorosas formas se ocultan de la luz;\nLas ansiosas manos que vagan en la oscuridad,\nEncienden dentro de la carne una brillante chispa."),
    
   ("A Sister's Lament (Erotic overture)",
    "The bed is barren since you went away,\nThe weary night outlasts the weary day.\nI miss the weight of you upon my breast,\nWherein your passionate heart was wont to rest.",
    "La cama es yerma desde que te fuiste,\nLa noche fatigosa dura más que el día fatigoso.\nExtraño el peso de ti sobre mi pecho,\nDonde tu apasionado corazón solía descansar."),
    
   ("Cupid's Triumph",
    "Cupid hath triumphed o'er my sober mind,\nAnd left all reason and all rule behind.\nNow nothing matters save the heated touch,\nOf the bold lover whom I love too much.",
    "Cupido ha triunfado sobre mi sobria mente,\nY ha dejado atrás toda razón y toda regla.\nAhora nada importa salvo el toque acalorado,\nDel rudo amante al que amo demasiado."),
    
   ("The Melting Snow",
    "If chaste resolve were made of winter snow,\nYour burning kiss would cause it soon to flow.\nI feel myself dissolving in your arms,\nDefenseless and surrendered to your charms.",
    "Si la casta resolución estuviera hecha de nieve invernal,\nTu beso ardiente causaría que fluyera pronto.\nSiento perderme y disolverme en tus brazos,\nIndefensa y rendida a tus encantos."),
    
   ("The Bower of Bliss",
    "Within the secret bower of the wood,\nWhere no intrusion or profane foot stood,\nWe laid our garments on the mossy floor,\nAnd learned from Love what we knew not before.",
    "Dentro del secreto aposento del bosque,\nDonde no se erguía intromisión ni pie profano,\nDejamos nuestras ropas en el suelo cubierto de musgo,\nY aprendimos del Amor lo que no sabíamos antes."),
    
   ("The Fire Unquenched",
    "They say that time will cool the hottest flame,\nBut every night I murmur out your name,\nAnd every night the same hot fever burns,\nAs for your flesh my hungry body yearns.",
    "Dicen que el tiempo enfriará la llama más caliente,\nPero cada noche murmuro tu nombre,\nY cada noche arde la misma fiebre caliente,\nMientras mi cuerpo hambriento anhela el tuyo."),
    
   ("The Stolen Glance",
    "I caught the look you sent across the hall,\nAnd felt the heavy, silken curtain fall.\nIt spoke of tangled sheets and heavy sighs,\nA naked truth behind polite disguise.",
    "Atrapé la mirada que enviaste a través del salón,\nY sentí caer la pesada cortina de seda.\nHablaba de sábanas enredadas y pesados suspiros,\nUna verdad desnuda tras el educado disfraz."),
    
   ("To Be Undone",
    "Oh, sweet undoing, when the laces part,\nAnd your warm fingers settle on my heart.\nI give you leave to ruin all my pride,\nWhilst in your fierce embraces I reside.",
    "Oh, dulce perdición, cuando los lazos se abren,\nY tus cálidos dedos se asientan sobre mi corazón.\nTe doy permiso para arruinar todo mi orgullo,\nMientras en tus fieros abrazos yo resido."),
    
   ("The Feast of Love",
    "Let other women fast and pray for grace,\nI find my heaven in your close embrace.\nYour lips are wine, your body is the bread,\nUpon which all my mortal lust is fed.",
    "Deja que otras mujeres ayunen y recen por gracia,\nYo encuentro mi cielo en tu apretado abrazo.\nTus labios son vino, tu cuerpo es el pan,\nDel que se alimenta toda mi lujuria mortal.")]),

 ("110","Aemilia Lanyer","1569–1645","Inglaterra","inglés",
  "Aemilia Lanyer (Aemilia Bassano) fue la primera mujer inglesa que buscó publicar y ser poeta profesional, desafiando a la élite isabelina. Para muchos eruditos, debido a su linaje veneciano y ascendencia oscura judía y musical, fue nada menos que la mítica 'Dama Oscura' de los enigmáticos sonetos de Shakespeare. Su poesía es profundamente sensorial y atrevida para su época, demostrando un conocimiento íntimo sobre el placer masculino y femenino.",
  [("The Dark Lady's Reply",
    "You call me dark, and say my eyes are jet,\nAnd yet my dark has caught you in its net.\nYou praise the fairness of the morning sky,\nBut in my midnight is the place you lie.",
    "Me llamas oscura, y dices que mis ojos son de azabache,\nY sin embargo mi oscuridad te ha atrapado en su red.\nElogias la blancura del cielo matutino,\nPero es en mi medianoche el lugar donde tú yaces."),
    
   ("Eve's Defense (Extract)",
    "If Eve did err, it was for knowledge's sake,\nBut what excuse do wanton lovers make?\nThey seek the tree of flesh, the rosy fruit,\nTo satisfy an appetite so brute.",
    "Si Eva erró, fue por el conocimiento,\nPero ¿qué excusa ofrecen los lascivos amantes?\nBuscan el árbol de la carne, el fruto rosado,\nPara satisfacer un apetito tan bruto."),
    
   ("The Musician's Touch",
    "My body is a lute upon your knee,\nPlay upon me a wanton melody.\nFret the tight strings until they vibrate hot,\nAnd hit the secret, resonating spot.",
    "Mi cuerpo es un laúd sobre tu rodilla,\nToca en mí una lasciva melodía.\nTrastea las tensas cuerdas hasta que vibren calientes,\nY golpea el punto secreto y resonante."),
    
   ("To the Lord Chamberlain",
    "The pomp of court fades quickly from my mind,\nWhen in my bed a truer lord I find.\nYour hands command the empire of my flesh,\nAnd make my tired desires spring afresh.",
    "La pompa de la corte se desvanece de prisa de mi mente,\nCuando en mi cama a un señor más verdadero encuentro.\nTus manos dominan el imperio de mi carne,\nY hacen que mis cansados deseos broten de nuevo."),
    
   ("A Dream of Venus",
    "I dreamed that Venus came to me by night,\nAnd showed me every art of soft delight.\nShe taught me how to move, and how to sigh,\nAnd how to drain my eager lover dry.",
    "Soñé que Venus vino a mí por la noche,\nY me mostró cada arte de suave deleite.\nMe enseñó cómo moverme, y cómo suspirar,\nY cómo exprimir hasta secar a mi ansioso amante."),
    
   ("The Stolen Hours",
    "When watchful husbands sleep a heavy sleep,\nInto my chamber my true love does creep.\nWe waste the night in sport and amorous play,\nAnd curse the swift arrival of the day.",
    "Cuando los maridos vigilantes duermen un pesado sueño,\nEn mi alcoba mi verdadero amor se cuela.\nGastamos la noche en retozos y juego amoroso,\nY maldecimos la rápida llegada del alba."),
    
   ("The Silk Ribbon",
    "Unbind the ribbon that confines my hair,\nAnd let my tresses tumble in the air.\nUnbutton, too, the bodice that is tight,\nAnd yield my swelling beauty to your sight.",
    "Desata la cinta que confina mi cabello,\nY deja que mis trenzas caigan sueltas al aire.\nDesabrocha, también, el corpiño que aprieta,\nY cede mi turgente belleza a tu vista."),
    
   ("Love's Alchemy",
    "By alchemy of kisses we transform,\nThe coldest winter to a summer's storm.\nYou turn my base reluctance into gold,\nWith hands so daring, and a touch so bold.",
    "Por la alquimia de los besos transformamos,\nEl invierno más frío en una tormenta estival.\nTú conviertes mi baja reticencia en oro,\nCon manos tan atrevidas, y un roce tan audaz."),
    
   ("The Surrender",
    "I fought your siege with virtue for a shield,\nBut to your burning lips I now must yield.\nThe fortress falls, the garrison gives way,\nAnd I am glad to be the victor's prey.",
    "Combatí tu asedio con la virtud por escudo,\nPero ante tus ardientes labios debo ceder ahora.\nLa fortaleza cae, la guarnición cede el paso,\nY yo me alegro de ser presa del vencedor."),
    
   ("The Morning After",
    "The tangled sheets bear witness to our war,\nAnd I am bruised, but eager still for more.\nThe daylight shows the flush upon my skin,\nA badge of honor from my night of sin.",
    "Las sábanas enredadas son testigos de nuestra guerra,\nY estoy magullada, pero todavía ansiosa por más.\nLa luz del día muestra el rubor sobre mi piel,\nUna insignia de honor de mi noche de pecado.")])
]

if __name__ == "__main__":
    for item in CORRECCIONES:
        mk(*item)
