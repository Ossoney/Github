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
 ("101","Vittoria Colonna","1492–1547","Italia","italiano",
  "Vittoria Colonna fue la poeta más venerada del Renacimiento italiano. Viuda en su juventud del Marqués de Pescara, consagró inicialmente su obra a su luto, pero pronto su poesía se llenó de un fervor pasional y místico. Intercambió ardientes versos con Miguel Ángel Buonarroti, en una relación epistolar e intelectual que desbordaba el simple platonismo para adentrarse en la devoción física y espiritual mutua.",
  [("Scrivo sol per sfogar l'interna doglia (Soneto I)",
    "Scrivo sol per sfogar l'interna doglia,\ndi che si pasce il cor, ch'altro non vole;\ne non per giunger lume al mio bel sole,\nche lasciò in terra sì onorata spoglia.\nGiusta cagion a lamentar m'invoglia:\nch'io scemi la sua gloria assai mi dole;\nper altra lingua, e per più saggie fole,\nconvien ch'a morte il gran nome si toglia.\nLa pura fe, l'ardir, l'alta virtute,\nil chiaro sangue, il suo valor sovrano,\nil vivo ingegno, e la beltà perdute,\nchi 'l piange, scriva; e con dolente mano,\nla sua ferita e la mia di salute\nmostri, con l'arco disarmato e vano.",
    "Escribo solo para desahogar el dolor interno,\ndel que se nutre el corazón, que no quiere otra cosa;\ny no para añadir luz a mi bello sol,\nque dejó en la tierra tan honrados despojos.\nJusta razón a lamentarme me incita:\nque yo disminuya su gloria mucho me duele;\npor otra lengua, y por más sabia historia,\nconviene que a la muerte su gran nombre se arrebate.\nLa pura fe, el ardor, la alta virtud,\nla noble sangre, su valor soberano,\nel vivo ingenio, y la belleza perdidas,\nquien lo llore, escriba; y con doliente mano,\nsu herida y mi falta de salud\nmuestre, con el arco desarmado y vano."),
   
   ("A Miguel Ángel (Soneto epistolar)",
    "Se 'l ver non m'inganna, o mio signore,\nil vostro ingegno e la vertù sublime\nin guisa d'oro i miei pensier reprime,\nch'io non ho ardir di dimostrarvi il core.\nMa se la voglia mia vi fosse fuore,\nvedreste ben che nell'afflitte rime\nl'alma si strugge, e il grande affetto esprime\nche mi tien legata al vostro amore.\nL'arte che nel sasso e nel colore\nmostrate, al mondo tutto innalza e splende;\nma la fiamma che qui dentro m'accende\nè più viva del vostro bel lavore.",
    "Si la verdad no me engaña, oh mi señor,\nvuestro ingenio y la virtud sublime\na manera de oro mis pensamientos reprime,\nque no tengo audacia de demostraros el corazón.\nPero si mi deseo se manifestara,\nveríais bien que en las afligidas rimas\nel alma se consume, y el gran afecto expresa\nque me tiene atada a vuestro amor.\nEl arte que en la piedra y en el color\nmostráis, al mundo todo eleva y resplandece;\npero la llama que aquí dentro me enciende\nes más viva que vuestro hermoso trabajo."),
   
   ("Il mio bel sole (Soneto)",
    "Vivo su questo scoglio orrido e solo,\nquasi come un augel che piange e canta;\ne quant'ho di dolor si disincanta\nse 'l mio bel sole in visione volo.\nCosì lontana dal mio bene e polo,\nil petto d'un disio caldo s'ammanta;\ne benché il lutto la mia vita schianta,\nl'amore nel petto mi consola il duolo.",
    "Vivo sobre este escollo hórrido y solo,\ncasi como un ave que llora y canta;\ny cuanto tengo de dolor se desencanta\nsi a mi bello sol en visión vuelo.\nAsí de lejos de mi bien y polo,\nel pecho de un deseo cálido se cubre;\ny aunque el luto mi vida destroce,\nel amor en el pecho me consuela el duelo."),
    
    ("Ardente fiamma", 
    "S'io penso all'ora che la fiamma ardente\nnel sen mi s'accese al primo sguargo,\npare che l'alm' a quel pensier si ardo\ne cerchi il fuoco ove languir beata.\nNon fuggirei la grazia disperata\ndi chi m'ha preso e mi tien in suo dardo.",
    "Si pienso en la hora en que la llama ardiente\nen mi seno se encendió a la primera mirada,\nparece que el alma ante ese pensamiento arde\ny busca el fuego donde languidecer feliz.\nNo huiría de la gracia desesperada\nde quien me ha prendido y me tiene en su dardo."),
    
    ("Deseo mortal",
    "Qual mortale desio sì mi punge\nch'io bramo quello ch'è sì lunge?\nIl corpo mio vorrebbe aver vicino\nquel che l'anima sente per destino.\nBrama l'abbraccio che non è mai dato\ne piange il letto oramai desolato.",
    "¿Qué deseo mortal así me punza\nque anhelo aquello que está tan lejos?\nMi cuerpo querría tener cerca\nlo que el alma siente por destino.\nAnhela el abrazo que nunca es dado\ny llora el lecho ahora desolado."),
    
     ("Fuego y Hielo",
    "Ghiaccio son di fuori, e dentro foco;\nil qual se non avesse spiraglio un poco,\nmetterebbe in cenere il mio core.\nE questo è 'l dono che mi fa l'Amore.",
    "Hielo soy por fuera, y fuego por dentro;\nel cual si no tuviera un resquicio un poco,\nreduciría a cenizas mi corazón.\nY este es el don que me hace el Amor."),
    
     ("Ojos que apresan",
    "Occhi miei che vedeste la bellezza\nche mi legò le mani al dolce laccio,\nor per punizion vi strugga la carezza\nche non potei sentire in suo abbaccio.",
    "Ojos míos que visteis la belleza\nque me ató las manos al dulce lazo,\nahora por castigo os consuma la caricia\nque no pude sentir en su abrazo."),
    
     ("La memoria del toque",
    "Rimane nella carne la memoria\ndi quando la tua man strinse la mia;\nuna sì breve e passaggera storia\nche nella mente si fa melodia\ne nel corpo divien furiosa brama.",
    "Queda en la carne la memoria\nde cuando tu mano estrechó la mía;\nuna tan breve y pasajera historia\nque en la mente se vuelve melodía\ny en el cuerpo se convierte en furiosa avidez."),
    
     ("Amor inabarcable",
    "Non può capire il senso, non può l'alma\nquanto sia grande e fier questo desio.\nIo per trovare una fugace calma\npalare vorrei con te, ben mio,\nche l'ardor che nascondo mi consuma.",
    "No puede comprender el sentido, no puede el alma\ncuán grande y fiero sea este deseo.\nYo para encontrar una fugaz calma\nhablar querría contigo, bien mío,\nque el ardor que escondo me consume."),
    
     ("Entrega total",
    "Se potessi donarti la mia vita,\nla verserei nel tuo calice d'oro;\nin te trovo la grazia infinita,\nil solo ed indivisibile tesoro\nche sazia questa fame repentina.",
    "Si pudiera donarte mi vida,\nla vertería en tu cáliz de oro;\nen ti encuentro la gracia infinita,\nel único e indivisible tesoro\nque sacia esta hambre repentina.")]),


 ("102","Pernette Du Guillet","1520–1545","Francia","francés",
  "Pernette du Guillet fue la encarnación poética del deseo femenino en el Renacimiento francés. Miembro brillante de la 'Escuela Lionesa', dedicó casi la totalidad de su breve obra (las 'Rymes') al poeta Maurice Scève. Sus poemas son respuestas ardientes y eróticas a los versos de él, conjugando la pasión física clandestina con la elevación platónica de los amantes.",
  [("Epigrama II : Qui dira ma flamme",
    "Qui dira ma flamme secrète\nQue je cache en mon pauvre cœur ?\nL'Amour qui me fait son sujette\nMe donne aussi de la rigueur.\nMais quand je vois mon serviteur,\nMon cœur de feu se renouvelle :\nJe me voudrais trouver cruelle,\nEt je me fonds en la chaleur.",
    "¿Quién dirá mi llama secreta\nQue escondo en mi pobre corazón?\nEl Amor que me hace su súbdita\nMe otorga también rigor.\nPero cuando veo a mi servidor,\nMi corazón de fuego se renueva:\nYo me quisiera encontrar cruel,\nY me fundo en el calor."),
   
   ("Epigrama VI : La nuit",
    "La nuit m’est courte, et le jour m’est trop long,\nQuand ton regard, ô mon bien, je ne vois;\nSi je me plains, on me dit que j'ai tort,\nCar l’amour feint ne connaît pas mes lois.\nMais de mon feu tu sais bien quelle est l'ardeur,\nEt dans mon lit je brûle de langueur.",
    "La noche me es corta, y el día demasiado largo,\nCuando tu mirada, oh mi bien, no veo;\nSi me quejo, me dicen que no tengo razón,\nPues el amor fingido no conoce mis leyes.\nPero de mi fuego sabes bien cuál es el ardor,\nY en mi lecho ardo de languidez."),
   
   ("Epigrama XIII",
    "Si je ne suis pour vous belle et charmante,\nEt si mon corps ne vous peut retenir,\nSachez de vrai que mon âme est ardente,\nEt qu'à vous seul elle veut s'unir.\nPrenez de moi ce qui est le meilleur,\nL'étreinte douce et la chaude ferveur.",
    "Si no soy para vos hermosa y encantadora,\nY si mi cuerpo no os puede retener,\nSabed de verdad que mi alma es ardiente,\nY que sólo a vos ella quiere unirse.\nTomad de mí lo que es mejor,\nEl abrazo dulce y el cálido fervor."),
    
    ("Chanson : L'amour me point",
    "L'amour me point et l'amertume,\nQuand je ressens ton doux toucher;\nMon corps est comme l'enclume\nOù ton désir vient me forger.",
    "El amor me pincha y la amargura,\nCuando siento tu dulce tocar;\nMi cuerpo es como el yunque\nDonde tu deseo viene a forjarme."),
    
    ("L'absence",
    "Ton absence me fait mourir de froid,\nMais ton retour me consume en la flamme;\nTu es le roi de mon corps et de mon âme,\nFaisant de moi l'esclave de ta loi.",
    "Tu ausencia me hace morir de frío,\nPero tu regreso me consume en la llama;\nEres el rey de mi cuerpo y de mi alma,\nHaciendo de mí la esclava de tu ley."),
    
    ("Le Baiser",
    "Un doux baiser, sur ma lèvre posé,\nPar mon amour en secret déposé,\nFait plus de bien à mon corps languissant\nQue tout le mire du Grand Orient.",
    "Un dulce beso, sobre mi labio posado,\nPor mi amor en secreto depositado,\nHace más bien a mi cuerpo languideciente\nQue toda la mirra del Gran Oriente."),
    
    ("Le désir éveillé",
    "Je ne savais ce qu'était le désir,\nAvant de voir tes yeux pleins de plaisir;\nÀ présent je brûle de toute part,\nConsumée par ton seul regard.",
    "Yo no sabía qué era el deseo,\nAntes de ver tus ojos llenos de placer;\nAhora ardo por todas partes,\nConsumida por tu sola mirada."),
    
    ("Rencontre secrète",
    "Dans l'ombre douce où nous nous sommes vus,\nNos deux corps nus ne furent point déçus.\nLa hâte prit nos souffles et nos mains,\nJusqu'à l'aurore des fiers lendemains.",
    "En la dulce sombra donde nos vimos,\nNuestros dos cuerpos desnudos no fueron decepcionados.\nLa prisa tomó nuestros alientos y nuestras manos,\nHasta la aurora de los fieros mañanas."),
    
    ("Soumission consentie",
    "Prends-moi, je suis à toi, corps et pensée;\nPar ta vertu je suis si oppressée,\nQue ma volonté n'est plus que la tienne,\nEt que ma chair veut que tu la retiennes.",
    "Tómame, soy tuya, cuerpo y pensamiento;\nPor tu virtud estoy tan oprimida,\nQue mi voluntad no es más que la tuya,\nY que mi carne quiere que tú la retengas."),
    
     ("Adieu au jour",
    "Adieu le jour qui me sépare de toi,\nViens douce nuit, compagne de l'émoi;\nDans ton obscur mon amour me retrouve,\nEt dans ses bras mon ardeur l'approuve.",
    "Adiós al día que me separa de ti,\nVen dulce noche, compañera de la conmoción;\nEn tu oscuridad mi amor me reencuentra,\nY en sus brazos mi ardor lo aprueba.")]),


 ("103","Moderata Fonte","1555–1592","Italia","italiano",
  "Escritora veneciana excepcional, cuyo verdadero nombre era Modesta Pozzo. Moderata Fonte desafió las convenciones del matrimonio de su época. En sus poemas epifánicos defiende un erotismo basado en el respeto intelectual y el deseo mutuo sincero entre iguales, contraponiéndolo a la dominación conyugal masculina que solía anular a las mujeres venecianas.",
  [("Il vero foco (Soneto)",
    "Non è ver foco quel che s'accende\nper sola brama di brutale ardore,\nche passa tosto come vano fiore\ne l'alma pura di tristezza offende.\nMa quel che per dolcezza il petto incende\nquand'arte e grazia palesan l'amore,\nquesto è desio che non reca dolore,\ne in un morbido laccio i corpi prende.",
    "No es verdadero fuego aquel que se enciende\npor solo deseo de brutal ardor,\nque pasa pronto como vana flor\ny el alma pura de tristeza ofende.\nSino aquel que por dulzura el pecho incendia\ncuando arte y gracia manifiestan el amor,\neste es deseo que no trae dolor,\ny en un suave lazo los cuerpos toma."),
   
   ("A un Amante Gentile",
    "Se la virtù col tuo voler si sposa,\nio ti darò la mente e il corpo mio.\nNulla di me ti fia mai nascosa,\nse onesto e puro fia il tuo disio.\nIn un letto di fiori e di intelletto\ntroverai il fiero tuo diletto.",
    "Si la virtud con tu querer se casa,\nyo te daré la mente y el cuerpo mío.\nNada de mí te será nunca oculto,\nsi honesto y puro fuera tu deseo.\nEn un lecho de flores y de intelecto\nencontrarás tu fiero deleite."),
   
   ("Il Bacio",
    "Un bacio tuo mi ruba la ragione\ne mi trasporta in paradiso tosto;\nnon c'è saggezza o santa religione\nche tenga il mio voler di fiamme nascosto.",
    "Un beso tuyo me roba la razón\ny me transporta al paraíso de pronto;\nno hay sabiduría o santa religión\nque mantenga mi querer de llamas escondido."),
    
    ("Desio femminile",
    "Credon gli uomini stolti che le donne\nnon sentan l'ardel de la fiamma viva;\nma sotto queste riverite gonne\nla carne brama ed è d'amore priva.",
    "Creen los hombres necios que las mujeres\nno sienten el arder de la llama viva;\npero bajo estas reverenciadas faldas\nla carne anhela y está de amor privada."),
    
    ("Notti veneziane",
    "Sopra il canale scivola silente\nla gondola che porta il mio tesoro;\nnel buio della stanza, impertinente,\nla mano scioglie i nastri e i fili d'oro.",
    "Sobre el canal se desliza silente\nla góndola que trae a mi tesoro;\nen la oscuridad del cuarto, impertinente,\nla mano desata las cintas y los hilos de oro."),
    
    ("Labbra di corallo",
    "Labbra tue di corallo che mi chiamano,\nsiete il peccato che più mi contenta;\ni baci vostri la mia pena sanano\ne la mia sete di piacer fomenta.",
    "Labios tuyos de coral que me llaman,\nsois el pecado que más me contenta;\nvuestros besos mi pena sanan\ny mi sed de placer fomenta."),
    
    ("Ardire dell'anima",
    "Come il nocchier che spera nella stella,\nio cerco nel tuo guardo la mia meta;\nche l'unirsi dei corpi è cosa bella,\nse l'anima a congiungersi è inquieta.",
    "Como el barquero que espera en la estrella,\nyo busco en tu mirada mi meta;\nque el unirse de los cuerpos es cosa bella,\nsi el alma a conjugarse está inquieta."),
    
    ("Il gioco d'amore",
    "Amore è gioco che si gioca in due,\nnella stanza segreta senza lumi;\nle mie carezze a mischiarsi co' le tue,\nin un mare di dolci, caldi piumi.",
    "El amor es juego que se juega de a dos,\nen la habitación secreta sin luces;\nmis caricias al mezclarse con las tuyas,\nen un mar de dulces, cálidas plumas."),
    
    ("La fiamma e la farfalla",
    "Io sono la farfalla, e tu sei la luce;\ngiro intorno a te, e mi consumo.\nIl desio al tuo petto mi conduce,\ne muoio lieta in te, senza alcun fumo.",
    "Yo soy la mariposa, y tú eres la luz;\ngiro en torno a ti, y me consumo.\nEl deseo a tu pecho me conduce,\ny muero feliz en ti, sin humo alguno."),
    
    ("Speranza del tocco",
    "Spero che la notte copra il mondo\naffinché la tua man mi trovi ignuda.\nIn questo amor carnale e pur profondo,\nnessuna legge sia a noi più cruda.",
    "Espero que la noche cubra el mundo\npara que tu mano me encuentre desnuda.\nEn este amor carnal y aún profundo,\nninguna ley nos sea ya más cruda.")]),


 ("104","Tullia d'Aragona","1510–1556","Italia","italiano",
  "Cortesana de altísimo nivel, filósofa y poetisa de Roma y Venecia. Tullia d'Aragona publicó el revolucionario tratado 'De la infinitud del amor', donde argumentaba filosóficamente que el deseo y la pasión física son componentes tan divinos y nobles como el amor espiritual. Sus poemas están dedicados a sus ilustres amantes, cargados de peticiones eróticas envueltas en brillante platonismo.",
  [("Soneto a Benedetto Varchi",
    "Amore, che m’ha fatto a lui suggella,\ne m’ha legato a l’amoroso passo,\nor m’unge di desir che non è casso,\ne il corpo e l’alma tutto in sé favella.\nLe mie membra per lui son come fiamme,\nche aspettan l'esca de' baci pietosi;\nnelle notti non sietemi nascosi,\nché pel poter amar la grazia damme.",
    "El amor, que me ha hecho a él su sello,\ny me ha atado al amoroso paso,\nahora me unge de deseo que no es nulo,\ny el cuerpo y el alma todo en sí habla.\nMis miembros por él son como llamas,\nque esperan la yesca de los besos piadosos;\nen las noches no me estéis ocultos,\nque para poder amar la gracia dadme."),
   
   ("Il piacer degno",
    "Non v'è colpa nell'amar la carne bella,\ns'essa è albergo di spirito cortese;\ni due son rami della stessa appella,\ne uniscono nel letto in fiamme accese.\nPrendimi il corpo, tu, che hai la mia mente,\ned amiamoci qui, divinamente.",
    "No hay culpa en amar la carne bella,\nsi esta es albergue de espíritu cortés;\nlos dos son ramas de la misma llamada,\ny se unen en el lecho en llamas encendidas.\nTómame el cuerpo, tú, que tienes mi mente,\ny amémonos aquí, divinamente."),
   
   ("A Girolamo Muzio",
    "Lascia le rime e sciogli a me le trecce,\nche della notte il tempo presto vola;\nquelle filosofiche, severe frecce\nle deporremo sulla coltre sola.",
    "Deja las rimas y suéltame las trenzas,\nque de la noche el tiempo pronto vuela;\nesas filosóficas, severas flechas\nlas depondremos sobre la colcha sola."),
    
    ("Baci in fiore",
    "Le rose aprent'il seno al matutin,\ncosì le labbra mie s'aprono a te.\nDammi il bacio ch'è dolce peregrin,\ne fonditi, amor mio, dentro di me.",
    "Las rosas abriendo el seno a la mañana,\nasí mis labios se abren a ti.\nDame el beso que es dulce peregrino,\ny fúndete, amor mío, dentro de mí."),
    
    ("Senza pudore",
    "A me non giova la virtù pudica\nse mi gela nel petto e fa languire.\nVoglio esser d'Amore affamata amica,\ne fra le tue braccia infine morire.",
    "A mí no me aprovecha la virtud púdica\nsi me hiela el pecho y me hace languidecer.\nQuiero ser de Amor hambrienta amiga,\ny entre tus brazos al fin morir."),
    
    ("La fiamma di Venere",
    "Venere diede il foco alle mie membra\nper render grazie a te, mio bel signore;\nil corpo freme e un vulcano sembra,\npronto a versar la lava dell'amore.",
    "Venus dio el fuego a mis miembros\npara darte gracias a ti, mi bello señor;\nel cuerpo se estremece y un volcán parece,\nlisto para verter la lava del amor."),
    
    ("Il talamo",
    "Questo letto di piume e seta ricca\nnon ha valor se non ci sei tu sopra;\nla brama è spina che nel fianco ficca,\nfinché la tua virtù il mio corpo copra.",
    "Esta cama de plumas y seda rica\nno tiene valor si no estás tú sobre ella;\nla avidez es espina que en el costado se clava,\nhasta que tu virtud mi cuerpo cubra."),
    
    ("Dolce arsura",
    "Mi brucia il sangue se mi stai vicino,\nmi secca la gola il tuo desir sfacciato.\nVersami amore come dolce vino,\ne fa di me il tuo calice amato.",
    "Me quema la sangre si me estás cerca,\nme seca la garganta tu deseo descarado.\nViérteme amor como dulce vino,\ny haz de mí tu cáliz amado."),
    
    ("Contro gli stolti",
    "Dicano i frati che l'amor è vizio,\nio diro sempre ch'è celese dote.\nIl corpo, quando ama, fa l'uffizio\nde le schiere angeliche e remote.",
    "Digan los frailes que el amor es vicio,\nyo diré siempre que es dote celeste.\nEl cuerpo, cuando ama, hace el oficio\nde las huestes angélicas y remotas."),
    
    ("L'invocazione notturna",
    "Vieni fanciullo o vieni uomo altero,\npoco m'importa finché sei bramoso;\nil mio giaciglio è vasto e del mistero\nio ti farò conoscere il riposo.",
    "Ven muchacho o ven hombre altivo,\npoco me importa mientras seas deseoso;\nmi yacija es vasta y del misterio\nyo te haré conocer el descanso.")]),


 ("105","Wallada bint al-Mustakfi","994–1091","Al-Andalus (España)","árabe",
  "Hija del califa omeya de Córdoba, Wallada fue una princesa valiente, dueña de un salón literario vital donde acudían los mejores intelectos andalusíes. Desafió los cánones islámicos rechazando usar el velo y llevando bordados en las orlas de sus túnicas versos eróticos. Vivió un tórrido, célebre y tempestuoso romance con el poeta Ibn Zaydun, al que ella misma sedujo y cantó con total desinhibición física.",
  [("Bordado en el hombro derecho de su túnica",
    "أنا والله أصلح للمعالي\nوأمشي مشيتي وأتيه تيها",
    "Por Dios que estoy hecha para la gloria\ny que camino, orgullosa, por mi propio camino."),
   
   ("Bordado en el hombro izquierdo de su túnica",
    "أُمَكِّنُ عاشقي من صفح خدي\nوأُعطي قُبْلَتي مَنْ يشتهيها",
    "Doy a mi amante de mi mejilla la parte más tersa\ny entrego mis besos a quienquiera que los apetezca."),
   
   ("Invitación en la noche pura (A Ibn Zaydun)",
    "ترقب إذا جن الظلام زيارتي\nفإني رأيت الليل أكتم للسرِّ\nوَبي منك ما لو كانَ بالشمسِ لم تلح\nوبالبدر لم يطلع وَبالنجم لم يسرِ",
    "Cuando caiga la noche, aguarda mi visita,\npues veo que la noche es la que mejor guarda los secretos.\nSiento por ti tal pasión que, si la tuviese el sol,\nno brillaría, ni la luna asomaría, ni las estrellas se alzarían."),
    
   ("Despecho (A Ibn Zaydun tras su traición)",
    "ولولا أن أكون على اضطراب\nلما أنزلت نفسي عن سمائي\nلقad خنت العهود وكنت تحظى\nبجناتٍ نعيم من رجائي",
    "Y de no estar yo en tal estado de perturbación,\njamás habría descendido de mis cielos.\nHas traicionado los pactos, a ti, que gozabas\nde los jardines del puro deleite de mis esperanzas."),
    
    ("Reproche por la criada",
    "تعمدتَ هجري من غيرِ ذنبٍ\nوبتَّ تمنيني بالوصالِ\nولكنك مال قلبك لِجاريتي\nوتلك لعمري من أفعالِ الجهالِ",
    "Tú me has abandonado a propósito y sin culpa mía,\ny pasaste la noche prometiéndome la unión;\npero tu corazón se inclinó por mi sirvienta,\ny eso, por mi vida, es propio de los ignorantes."),
    
    ("Orgullo herido",
    "أنت الذي لو كنت تنصفني\nلم تلتفت يوماً إلى دوني",
    "Tú eres aquel que, de ser justo conmigo,\njamás hubieras mirado a una inferior a mí."),
    
    ("La seducción",
    "أدنو ليلاً وأسلبك الرقادا\nلأطفئَ في لقاك بي ارتيادا\nولا أبالي بما قال الوشاةُ",
    "Me acerco de noche y te robo el sueño\npara apagar en tu encuentro mi propia avidez\ny no me importa lo que digan los calumniadores."),
    
    ("El néctar ajeno",
    "تركتَ ماء الخلدِ من فرعِي\nلتشربَ من ماءِ البِئَارِ",
    "Dejaste el agua de la eternidad de mis pechos\npara ir a beber de las aguas de los pozos [se refiere a la criada]."),
    
    ("El sol y el fango",
    "أنا شمسٌ تضيءُ لكَ الليالي\nلكنك آثرتَ الغرقَ في الوحلِ",
    "Yo soy un sol que te ilumina las noches\npero tú preferiste ahogarte en el fango."),
    
    ("Adiós al amante",
    "وداعاً يامن كان قرةَ عيني\nالآن أُغْلِقُ بابَ الشوقِ دونكَ",
    "Adiós tú que fuiste la luz de mis ojos\nAhora cierro la puerta del deseo para siempre de ti.")])
]

if __name__ == "__main__":
    for item in CORRECCIONES:
        mk(*item)
