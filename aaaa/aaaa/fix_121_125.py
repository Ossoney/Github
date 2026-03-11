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
    print(f"  ✅ {fn} corregido.")

CORRECCIONES = [
 ("121","Flora Tristan","1803–1844","Francia/Perú","francés",
  "Pionera del feminismo y abuelita de Paul Gauguin. Huyó de un marido abusivo e inició una apasionante y dolorida vida de escritora emancipada ('Viaje de una paria'). Aunque no fue principalmente poetisa, intercala una prosa lírica tan exultantemente corporal, descarnada e íntimamente desesperada reclamando la redención carnal, el goce sensual propio y los deseos libres extramatrimoniales, que hoy son leídos como encendidos monólogos líricos del yo, verdaderos gritos eróticos en favor de lo humano y del cuerpo.",
  [("Le Cri de la Chair (El grito de la carne)",
    "Je refuse le joug du lit obligatoire,\nLes froides nuits d'un triste purgatoire.\nMon corps est mien, il réclame sa part,\nEt s'offre libre au feu de ton regard.",
    "Rechazo el yugo de la cama obligatoria,\nLas noches frías de un triste purgatorio.\nMi cuerpo es mío, reclama su parte,\nY se ofrece libre al fuego de tu mirada."),
    
   ("L'Éveil en Andalousie (El despertar en Andalucía)",
    "Sous le soleil brûlant d'Andalousie,\nJ'ai bu à ta bouche l'eau de la poésie.\nTu m'as prise sans lois, sans autres contrats,\nQue le brûlant étau de tes deux bras.",
    "Bajo el sol ardiente de Andalucía,\nBebí de tu boca el agua de la poesía.\nMe tomaste sin leyes, sin otros contratos,\nQue el ardiente torno de tus dos brazos."),
    
   ("Le Voyageur (El viajero)",
    "La sueur de ta peau sur la route andine,\nA éveillé ma faim, farouche et divine.\nJ'ai déchiré ma robe, aboli ma pudeur,\nPour me perdre enfin dans ton moite chaleur.",
    "El sudor de tu piel en la ruta andina,\nHa despertado mi hambre, feroz y divina.\nHe rasgado mi vestido, abolido mi pudor,\nPara perderme al fin en tu húmedo calor."),
    
   ("L'Amour Paria (El amor Paria)",
    "Moi, la paria, je n'ai de toit ni lit,\nMais le monde entier sous mon ventre frémit.\nPrends-moi dans les fossés ou dans les palais,\nCar l'amoureuse soif n'a jamais de délais.",
    "Yo, la paria, no tengo techo ni cama,\nPero el mundo entero bajo mi vientre se estremece.\nTómame en las cunetas o en los palacios,\nPues la sed amorosa no tiene nunca demoras."),
    
   ("La liberté des Lèvres (La libertad de los labios)",
    "Le mariage est un bagne, un cachot avilissant,\nMais ton baiser volé est un vin frémissant.\nDans l'ombre des wagons, dans les auberges noires,\nJe bâtis sur ton flanc de sensuelles victoires.",
    "El matrimonio es un presidio, un calabozo envilecedor,\nPero tu beso robado es un vino estremecedor.\nEn la sombra de los vagones, en oscuras posadas,\nConstruyo sobre tu costado sensuales victorias."),
    
   ("Nuit de Lima (Noche de Lima)",
    "La lourdeur des orangers, le parfum de jasmin,\nOnt jeté mon amant si fiévreux sur mon sein.\nNous avons bu la nuit, nous avons mordu l'aube,\nLaissant la loi des sots choir avec ma robe.",
    "La pesadez de los naranjos, el perfume de jazmín,\nHan arrojado a mi amante tan febril sobre mi seno.\nHemos bebido la noche, hemos mordido el alba,\nDejando la ley de los necios caer junto con mi vestido."),
    
   ("Le Refus (El rechazo)",
    "Ne me parle plus Dieu, de devoir ou de prêtre,\nC'est la moiteur de l'autre qui m'enseigne à être.\nLe sang pulse, la chair appelle et se soumet,\nAu seul Maître désir, qui triomphe à jamais.",
    "Ya no me hables de Dios, de deber o de sacerdote,\nEs la humedad del otro quien me enseña a ser.\nLa sangre pulsa, la carne llama y se somete,\nAl único Maestro deseo, que triunfa por siempre."),
    
   ("Tempête d'Arequipa (Tempestad de Arequipa)",
    "L'orage secouait les toits bruns de la ville,\nMais sur ta peau haletante, je trouvais un asile.\nDans un gémissement la foudre est retombée,\nEt j'ai connu le ciel dans ta chambre dérobée.",
    "La tormenta sacudía los techos pardos de la ciudad,\nPero sobre tu piel jadeante, yo encontraba un asilo.\nEn un gemido el relámpago ha vuelto a caer,\nY he conocido el cielo en tu alcoba robada."),
    
   ("Vagabonde (Vagabunda)",
    "Mes pieds sont écorchés, mon dos las et meurtri,\nMais à travers ton torse mon cœur s'est nourri.\nTon souffle sur ma gorge efface ma détresse,\nEt transforme ma fièvre en ardente allégresse.",
    "Mis pies están desollados, mi espalda cansada y magullada,\nPero a través de tu torso mi corazón se ha nutrido.\nTu aliento sobre mi garganta borra mi zozobra,\nY transforma mi fiebre en ardiente júbilo."),
    
   ("Épilogue Charnel (Epílogo carnal)",
    "Quand je serai poussière et que mon feu sera mort,\nQu'on retienne de moi le sursaut de mon corps,\nQui chercha jusqu'au bout, bravant le déshonneur,\nL'orgasme triomphant et la sueur du bonheur.",
    "Cuando yo sea polvo y mi fuego esté muerto,\nQue se recuerde de mí el sobresalto de mi cuerpo,\nQue buscó hasta el final, desafiando el deshonor,\nEl orgasmo triunfante y el sudor de la felicidad.")]),

 ("122","Louise Colet","1810–1876","Francia","francés",
  "Provocativa y pasional en su arte, y apodada «la Musa» por la fama de su asombrosa belleza y temperamento de fuego. Amante escandalosa de literatos como Victor Cousin, Alfred de Musset, Alfred de Vigny y, sobre todo, de Gustave Flaubert, a quien dedicó algunas de sus páginas más arrebatadoras y furiosas en cartas y ardientes versos amatorios. Fiel exponente de la amante desesperada y carnal del pleno espíritu romántico.",
  [("L'Orage de la Nuit",
    "La chambre est chaude, et dehors pleut la nuit,\nMais c'est ton corps tendu qui seul me fait du bruit.\nEntre tes mains mon sein frissonne et se pâme,\nEt tu bois sur mes lèvres la fève de mon âme.",
    "El cuarto está cálido, y afuera llueve la noche,\nPero es tu cuerpo tenso el único que me hace ruido.\nEntre tus manos mi seno se estremece y se desmaya,\nY tú bebes sobre mis labios el haba de mi alma."),
    
   ("Le Souffle de l'Amant",
    "J'entends ta respiration courte, brisée, farouche,\nQuand tu viens écraser ton désir sur ma bouche.\nAh ! laisse-moi mourir de cent morts enlacées,\nSur ces draps froissés et ces nuits enfiévrées.",
    "Oigo tu respiración corta, rota, arisca,\nCuando vienes a estrujar tu deseo sobre mi boca.\n¡Ah! déjame morir de cien muertes entrelazadas,\nSobre estas sábanas arrugadas y estas noches afiebradas."),
    
   ("À Gustave",
    "Ours magnifique et lourd, qui m'étouffe et qui m'aime,\nMa chair est un velours où s'écrit ton poème.\nTon étreinte me brise et pourtant je la veux,\nDe la pointe du pied jusqu'aux bords des cheveux.",
    "Oso magnífico y pesado, que me asfixia y que me ama,\nMi carne es un terciopelo donde se escribe tu poema.\nTu abrazo me quiebra y sin embargo lo quiero,\nDe la punta del pie hasta los bordes de los cabellos."),
    
   ("Morsure de Joie",
    "Tu m'as blessé l'épaule et j'adore la trace,\nDe la morsure avide où le plaisir s'enlace.\nTu as su réveiller des abîmes de faim,\nQui réclament le feu sans répit, sans déclin.",
    "Me has herido el hombro y adoro el rastro,\nDe la avidez de la mordedura donde el placer se enlaza.\nHas sabido despertar abismos de hambre,\nQue reclaman el fuego sin respiro, sin decaer."),
    
   ("Heures secrètes",
    "L'horloge a retenti, mais le temps est détruit,\nPar les spasmes brûlants de notre folle nuit.\nNos souffles confondus, nos membres enchaînés,\nFont de la volupté notre sort bien renté.",
    "El reloj ha sonado, pero el tiempo se ha destruido,\nPor los espasmos ardientes de nuestra loca noche.\nNuestros alientos confundidos, nuestros miembros encadenados,\nHacen de la voluptuosidad nuestra muy adinerada suerte."),
    
   ("La Robe défaite",
    "Ma robe a glissé lourde, avec ses nœuds de soie,\nPour te livrer la proie que ta vigueur foudroie.\nNe laisse pas l'aube ternir notre exploit noir,\nAh, pénètre-moi bien pour vaincre le désespoir.",
    "Mi vestido se ha deslizado pesadamente, con sus nudos de seda,\nPara entregarte la presa que tu vigor fulmina.\nNo dejes que el alba deslustre nuestra negra hazaña,\nAh, penétrame bien para vencer la desesperación."),
    
   ("Les amants furieux",
    "C'est un combat de tigres que l'allégresse vraie,\nOù chacun, haletant, succombe sur la plaie.\nC'est la joie animale, insolente, sauvage,\nQui emporte nos corps vers le même naufrage.",
    "Es un combate de tigres la alegría verdadera,\nDonde cada uno, jadeante, sucumbe sobre la herida.\nEs la alegría animal, insolente, salvaje,\nQue arrastra a nuestros cuerpos hacia el mismo naufragio."),
    
   ("Le Calice Épuisé",
    "J'ai bu ton vin, j'ai tout tari ton sang,\nTon flanc bat la mesure auprès de mon flanc blanc.\nS'il est un coin de paradis pour la pécheresse,\nC'est la grande sueur de notre immense ivresse.",
    "He bebido tu vino, he secado toda tu sangre,\nTu costado bate el compás junto a mi tez blanca.\nSi hay un rincón del paraíso para la pecadora,\nEs el grandioso sudor de nuestra inmensa embriaguez."),
    
   ("L'Emprise",
    "Tu es la tempête qui secoue mes frêles os,\nY trouve sous ma peau le suprême repos.\nOuvre donc les tréfonds de ma chair amoureuse,\nEt fais de ta douceur ma plaie la plus heureuse.",
    "Eres la tormenta que sacude mis frágiles huesos,\nY encuentra bajo mi piel el supremo reposo.\nAbre pues las profundidades de mi carne enamorada,\nY haz de tu dulzura mi herida más feliz."),
    
   ("Plainte voluptueuse",
    "Arrête ! Je me meurs de trop de volupté !\nEt dans ta force brute gît ma fragilité.\nMais ne t'éloigne pas, serre-moi jusqu'au bout,\nCar c'est de cet excès que je me fais le joug.",
    "¡Detente! ¡Que me muero de demasiada voluptuosidad!\nY en tu fuerza bruta yace mi fragilidad.\nPero no te alejes, apriétame hasta el final,\nPues es de este exceso que me hago yo el yugo.")]),

 ("123","Marie Krysinska","1857–1908","Francia/Polonia","francés",
  "Figura bohemia de talento inclasificable, habitual cabaretera de París. De raíces polacas, muchos la consideran la verdadera creadora del verso libre en la lírica francesa (aunque el crédito fue a menudo masculino). Sus versos musicales, disonantes y cargados de provocación celebran una carnalidad lánguida y exótica en habitaciones donde flotaban el humo del teatro, el opio y el deseo exacerbado.",
  [("Chanson de chair",
    "La chair s'éveille comme un lourd parfum noir,\nQui rôde lascivement le long des lourds miroirs.\nTes doigts, lents et précis, modèlent ma pudeur,\nEt l'éclatent en feux dans la moite chaleur.",
    "La carne se despierta como un pesado perfume negro,\nQue merodea lascivamente a lo largo de los pesados espejos.\nTus dedos, lentos y precisos, modelan mi pudor,\nY lo hacen estallar en fuegos dentro del húmedo calor."),
    
   ("Les lèvres ivres",
    "Je ne veux pas d'amour tiède et de fade discours,\nJ'exige les sanglots, les spasmes et les jours\nQui sombrent de fatigue entre des draps fiévreux,\nÉcrasés sous le poids de nos corps malheureux.",
    "No quiero amor tibio y discursos insípidos,\nExijo los sollozos, los espasmos y los días\nQue se hunden en fatiga entre sábanas febriles,\nAplastados bajo el peso de nuestros cuerpos desventurados."),
    
   ("Danse du désir",
    "Mon corset s'en est allé, mes dentelles ont fui,\nEt je reste pour toi, prêtresse de la nuit.\nPrends l'offrande qui rougit sous le bout de tes mains,\nEt ne m'accorde pas de repos pour demain.",
    "Mi corsé se ha marchado, mis encajes han huido,\nY me quedo para ti, sacerdotisa de la noche.\nToma la ofrenda que enrojece bajo la yema de tus manos,\nY no me concedas reposo alguno para el mañana."),
    
   ("Baiser d'Orient",
    "Ta bouche a la saveur de la myrrhe et du sang,\nUn délice affamé, douloureux et brûlant.\nChaque baiser mordant est une flèche douce\nQui s'enfonce très loin dans ma chair qui s'émousse.",
    "Tu boca tiene el sabor de la mirra y de la sangre,\nUna delicia hambrienta, dolorosa y ardiente.\nCada beso mordaz es una flecha dulce\nQue se hunde muy profundo en mi carne que se embota."),
    
   ("Chambre close",
    "Toute l'aube est exclue, les rideaux sont fermés,\nTon visage est noyé dans l'ambre parfumé.\nIci il n'y a de Dieu, ni de loi vaine,\nQue le frisson rapide où tu te fais ma reine.",
    "Toda el alba está excluida, las cortinas echadas,\nTu rostro está ahogado en el ámbar perfumado.\nAquí no existe Dios, ni ley vana,\nSalvo el rápido escalofrío con el cual te haces mi reina."),
    
   ("Mélodie Rythmée",
    "Un rythme lancinant court le long de tes reins,\nQui m'appelle, me lie, et m'attire à tes mains.\nNos deux respirations sont un chant libre et nu,\nVersant la mélodie vers un point inconnu.",
    "Un ritmo penetrante corre por tus lomos,\nQue me llama, me ata, y me atrae a tus manos.\nNuestras dos respiraciones son un canto libre y desnudo,\nVertiendo la melodía hacia un punto desconocido."),
    
   ("Soif Inassouvie",
    "Je crève de la soif de crever dans ton lit,\nDe noyer chaque aurore dans un même délit.\nJe veux user mon dos aux lattes de ton bord,\nEt frémir tout entière jusqu'au bord de la mort.",
    "Reviento de la sed de reventar en tu cama,\nDe ahogar cada aurora en un mismo delito.\nQuiero gastar mi espalda en los listones de tu somier,\nY estremecerme por entera hasta el borde de la muerte."),
    
   ("L'Abîme charnel",
    "Ton ombre s'abat sur moi et l'univers se fend,\nJe tombe sans retour en un gouffre ardent.\nAinsi soit aboli l'ennui du genre humain,\nPuisque je tiens ta chair tremblante dans ma main.",
    "Tu sombra se abate sobre mí y el universo se parte en dos,\nCaigo sin retorno en una fosa ardiente.\nQue así sea abolido el tedio del género humano,\nYa que sostengo tu carne temblorosa en mi mano."),
    
   ("Symphonie muette",
    "Dans l'air opaque et chaud de l'alcôve secrète,\nLe sang bat le tympan : la symphonie muette\nC'est ton ventre vibrant collé contre mon flanc,\nQui murmure les notes du plaisir exigeant.",
    "En el aire opaco y cálido del reservado alcázar secretro,\nLa sangre golpea el tímpano: la sinfonía muda\nEs tu vientre vibrante pegado contra mi costado,\nQue murmura las notas del placer exigente."),
    
   ("La Bête Appaisée",
    "La bête haletante est enfin rassasiée,\nTa lourde tête s'est sur ma gorge posée.\nMais je vois dans tes yeux qu'une étincelle encore\nSe prépare à ruer dans la pâleur de l'aurore.",
    "La bestia jadeante está por fin saciada,\nTu pesada cabeza sobre mi garganta se ha posado.\nPero veo en tus ojos que una chispa aún\nSe prepara a arremeter en la palidez de la aurora.")]),

 ("124","Louise Ackermann","1813–1890","Francia","francés",
  "Poeta filosófica y radical, cuya fama quedó sepultada por la misoginia de la época por abordar el pesimismo, el dolor y la carnalidad fiera tras sufrir una temprana viudez en 1846 (de su esposo Paul Ackermann, quien murió tras apenas dos años desposados). Plasmó su rabia y deseo en versos donde maldecía a la divinidad por arrebatarle los placeres de la carne, cantando al goce perdido, a la urgencia ardiente de la juventud y al lamento brutal de una piel privada del ardor.",
  [("Le Cri du Manque (El grito de la carencia)",
    "J'ai connu, pour mon mal, les ardeurs du lit,\nEt maintenant ton ombre est tout ce qui me suit.\nMon corps est affamé de cette folle étreinte,\nOù la raison sombrait pour y noyer la crainte.",
    "Conocí, para mi mal, los ardores del lecho,\nY ahora tu sombra es lo único que me persigue.\nMi cuerpo está hambriento del tonto abrazo,\nDonde la razón se hundía para allí ahogar el temor."),
    
   ("L'Appel de la Jeunesse (La llamada de la juventud)",
    "Mes veines pleines d'ambre réclament ton retour,\nCar la nuit sans tes mains est d'un poids froid et lourd.\nViens déchirer ce voile de veuve trop austère,\nEt rends-moi le péché de ma force première.",
    "Mis venas llenas de ámbar reclaman tu vuelta,\nPues la noche sin tus manos es de un peso frío y pesado.\nVen a desgarrar este velo de viuda demasiado austera,\nY devuélveme el pecado de mi fuerza inicial."),
    
   ("Blasphème charnel (Blasfemia carnal)",
    "Je hais le ciel lointain qui t'arrache à mes bras,\nEt je maudis l'autel si ton corps n'y est pas.\nPlus sacrée que la croix est la chaste moiteur,\nOù nous mêlions salive, râle, et sueur.",
    "Odio el cielo lejano que te arranca de mis brazos,\nY maldigo el altar si tu cuerpo allí ya no está.\nMás sagrada que la cruz era aquella pura humedad,\nDonde mezclábamos saliva, estertor, y sudor."),
    
   ("Mémoire du contact (Memoria del contacto)",
    "Le creux de mon épaule se souvient de ta dent,\nCe fut un jour d'orage, fulgurant et ardent.\nLa trace est effacée, mais sous la peau, je brûle,\nEt mon sein douloureux sous ta morsure ondule.",
    "El hueco de mi hombro se acuerda de tu diente,\nFue un día de tormenta, fulgurante y ardiente.\nEl rastro se ha borrado, pero bajo la piel yo sigo ardiendo,\nY mi seno dolorido bajo tu mordedura ondula."),
    
   ("L'Immortel Désir (El inmortal deseo)",
    "On me dit d'oublier, de me tourner vers Dieu,\nMais seul me manque l'or du vertige amoureux.\nIl n'est d'éternité que dans la fente close,\nOù s'offrait à ton bec le calice d'une rose.",
    "Me dicen que olvide, que me vuelva hacia Dios,\nPero sólo añoro el oro del vértigo amoroso.\nNo hay eternidad sino en la grieta escondida,\nDonde se ofrecía a tu pico el cáliz de una rosa."),
    
   ("Fièvre nocturne (Fiebre nocturna)",
    "Les draps froids de la nuit ravivent l'incendie,\nMon ventre abandonné pleure la tragédie.\nS'il est un froid royaume de mort dans la nature,\nC'est mon flanc qui gémit, attendant ta parure.",
    "Las frías sábanas de la noche reavivan el incendio,\nMi vientre abandonado llora la tragedia.\nSi hay un frío reino de muerte en la naturaleza,\nEs mi flanco que gime, aguardando tu aderezo."),
    
   ("L'Anathème (El anatema)",
    "Maudite soit la loi qui nomme le plaisir\nUn crime, alors qu'il est l'unique vrai désir !\nNos corps entrelacés nient l'obscure tombe,\nEt dans l'ivresse humaine le divin toujours tombe.",
    "¡Maldita sea la ley que nombra al placer\nUn crimen, cuando es él el único verdadero deseo!\nNuestros cuerpos entrelazados niegan la oscura tumba,\nY dentro de la embriaguez la humana divinidad cae siempre."),
    
   ("Rancœur du Lit (Rencor de la Cama)",
    "Oh, chambre au lit béant qui m'offrit le délire,\nTu n'es plus qu'un cachot, un instrument qui m'ire.\nRends-moi ces lentes nuits, ces souffles effrénés,\nOù nous tordions ensemble, aveugles, déchaînés.",
    "Oh, cuarto del lecho vacío que me ofrecisteis el delirio,\nYa no sois más que un calabozo, un instrumento que me irrita.\nDevuélveme esas lentas noches, esos alientos desenfrenados,\nDonde nos apiñábamos juntos, ciegos, desatados."),
    
   ("Abandon sublime (Abandono sublime)",
    "Oui, j'ai tout sacrifié pour ta bouche amoureuse,\nEt dans mon déshonneur je me suis sentie heureuse.\nLa morale des sots s'est fracassée chez moi,\nSous la beauté farouche et tremblante de toi.",
    "Sí, lo he sacrificado todo por tu boca enamorada,\nY en mi deshonor me he sentido incluso feliz.\nLa moral de los tontos se ha hecho trizas en mi casa,\nBajo la belleza feroz y temblorosa de ti."),
    
   ("Le Testament (El testamento)",
    "Ne gravez sur ma tombe aucun pieux verset,\nMais l'évocation crue du lit qui m'apaisait.\nJ'ai vécu pour la flamme et non pour la cendre,\nQu'on retienne de moi cet aveu pur et tendre.",
    "No graben en mi tumba ningún piadoso versículo,\nSino la cruda evocación del lecho que me complacía.\nHe vivido para la llama y no para la ceniza,\nQue se recuerde de mí esta confidencia tierna y carnal.")]),

 ("125","Rosemonde Gerard","1866–1953","Francia","francés",
  "Casada con el famoso dramaturgo Edmond Rostand y celebridad apabullante de la Belle Époque. Se dice que Rosemonde le inspiraba y corregía sus obras más afamadas (como 'Cyrano de Bergerac'). Publicó aclamados poemas de amor (inventó la expresión '...te amo hoy más que ayer y menos que mañana'). Su poesía transita la pasión devoradora, rindiendo constante pleitesía al cuerpo amado en medio de lujosos escenarios victorianos, abrigos de piel, trenes europeos e íntimas sedas que ocultan desenfrenados escándalos románticos.",
  [("L'Éternelle Chanson (La canción eterna)",
    "Car vois-tu, chaque jour je t'aime davantage,\nAujourd'hui plus qu'hier et bien moins que demain.\nLes fèvres de la nuit m'offrent ton frais visage,\nOù viennent s'enivrer ma bouche et puis ma main.",
    "Pues mira tú, que cada día te amo todavía más,\nHoy mucho más que ayer y mucho menos que mañana.\nLas fiebres de la noche me ofrecen tu rostro fresco,\nDonde vienen a embriagarse mi boca y luego mis manos."),
    
   ("Les Fourrures (Los abrigos de pieles)",
    "Le train file dans la nuit d'Europe, et ta chaleur\nS'engouffre dans ma peau malgré les rudes toiles.\nSous mes lourdes fourrures frisonne un grand voleur :\nC'est la bête d'amour sous ce ciel aux étoiles.",
    "El tren se desliza en la noche de Europa, y el calor\nSe hunde en mi piel a pesar de las rudas telas.\nBajo mis pesadas pieles resuena un gran ladrón:\nEs la bestia del amor bajo este cielo cuajado en estrellas."),
    
   ("Fièvre du Soir (Fiebre de Noche)",
    "Tu arraches ma guimpe avec la brutalité\nD'un seigneur impatient qui conquiert sa captive.\nJe cède sous ton poids en pleine volupté,\nEt ma chair pantelante sous ta langue est vive.",
    "Arrancas mi corsé con la brutalidad\nDe un señor impaciente que conquista a su cautiva.\nCedo bajo tu peso en plena voluptuosidad,\nY mi carne jadeante bajo tu lengua es muy viva."),
    
   ("Luxure de Velours (Lujuria de Terciopelo)",
    "Dans les sombres salons étouffés d'ottomanes,\nNous cherchions un retrait loin du regard mondain.\nMon sang réclamait tes mains chaudes et profanes,\nPour fondre dans ton torse hier comme demain.",
    "En los sombríos salones asfixiados de otomanas,\nBuscábamos un retraimiento lejos de toda mirada mundana.\nMi sangre reclamaba tus manos calientes y profanas,\nPara fundirse en tu torso ayer como en un mañana."),
    
   ("Le Ruban (El Lazo)",
    "Le ruban de satin, si lentement défait,\nAnnonce sur ton lit mon ultime défaite.\nC'est une exquise peur qui me brûlant refait,\nTandis que mon amant me dévore muette.",
    "El lazo de satén, tan lentamente deshecho,\nAnuncia sobre tu cama mi última derrota.\nEs un exquisito miedo que ardiéndome rehace,\nMientras mi amante me devora dejándome en silencio."),
    
   ("Absence Insatiable (Ausencia Insaciable)",
    "Dès que le jour reluit, ton ombre m'abandonne,\nEt mon flanc endolori frémit de ta mémoire.\nLa moindre de mes nuits tout entière me donne\nLe feu de tes lèvres, d'une douceur notoire.",
    "Tan pronto como reluce el día, tu sombra me abandona,\nY mi flanco adolorido se estremece con tu memoria.\nLa menor de mis noches a ti toda entera se entrega,\nBajo el fuego en tus labios, de una dulzura notoria."),
    
   ("Le Sanglot (El Gemido)",
    "Ne retiens pas ce cri qui déchire le masque,\nQuand au point des amours notre chute est fatale.\nBrise-moi de bonheur sous le vent de ta bourrasque,\nDans le nid odorant d'une alcôve brutale.",
    "No retengas ese grito que desgarra la máscara de la moral,\nCuando a punto de los amores nuestra caída se hace fatal.\nQuiébrame de alegría bajo el viento de tus ráfagas,\nEn el nido oloroso de una alcoba tan brutal."),
    
   ("Ta Bouche (Tu Boca)",
    "Ce ne sont pas les yeux qui commandent l'amour,\nMais la forme tenace et rouge de ta bouche.\nQui dans la pénombre fait pâlir chaque jour,\nEt rend l'esprit dément quand la peau s'embouche.",
    "No son para nada los ojos los que comandan el amor,\nSino la forma tenaz y roja que dibuja ahí tu boca.\nQue en la penumbra hace que el día se torne descolor,\nY vuelve el espíritu loco cuando la piel con su piel choca."),
    
   ("Secret d'Hiver (Secreto de Invierno)",
    "Au-dehors, la neige étouffe la capitale,\nMais j'ai dans le sang l'Orient enflammé.\nMon corps se cambre sous une rage géniale,\nSous la dent du génie et le poids de l'aimé.",
    "Por fuera, la nieve es la que apaga a la capital,\nPero tengo hirviendo en la sangre al Oriente en llamas.\nMi cuerpo se contonea bajo una enrabietada furia genial,\nBajo el diente vivo del celo genio y el peso tenso que tú me dabas."),
    
   ("Consummation (Consumación)",
    "Si l'éternité n'est qu'un long sommeil noir,\nC'est le sursaut de chair qui justifia la trame.\nTon poids affolant est le plus beau désespoir,\nOù viennent chavirer le corps avec l'âme.",
    "Si es que la eternidad no es más que un largo sueño estancado en un vacío oscuro,\nEs el estremecimiento en la carne el que le da a ella todo su peso al puro tramado.\nTu peso de enloquecer es la causa mayor a este mi bello futuro,\nCon el que viene para mi el ahogarse en tu propio pecho en el cuerpo que habíase entregado.")])
]

if __name__ == "__main__":
    for item in CORRECCIONES:
        mk(*item)
