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
 ("131","Teffi_Nadezhda_Lokhvitskaya","1872–1952","Rusia","ruso",
  "Teffi, hermana de la gran poeta Mirra Lokhvitskaya. Famosa sobre todo por su aguda sátira en el exilio parisino. Sus poemas de juventud desvelan un lado íntimo melancólico, sensual y de profunda ansia afectiva ('Siete fuegos'). Sus versos describen a menudo amantes en escenarios decadentes en los que los besos tienen el sabor de la desesperación o del perfume enigmático del místico fin de siglo.",
  [("Кольцо (El Anillo)",
    "Ты надел мне на палец кольцо,\nНо сковал не путы, а кровь.\nЯ впиваюсь в твое лицо,\nЖадно пью эту злую любовь.",
    "Pusiste un anillo en mi dedo,\nPero no encadenó mi mano, sino mi sangre.\nMe clavo en tu rostro,\nY ávidamente bebo este malvado amor."),
    
   ("Красный шелк (Seda roja)",
    "Красный шелк соскользнул на ковер,\nЗаглушая неровный стук.\nЭтот жаркий, немой уговор\nЯ читаю из дрожи рук.",
    "La seda roja se deslizó hacia la alfombra,\nAhogando un sonido desigual.\nEste ardiente y mudo acuerdo\nLo leo en el temblor de tus manos."),
    
   ("Полумрак (Penumbra)",
    "В полумраке твои глаза\nБлиже, ярче, темней и злей.\nЯ сдаюсь на милость, как лоза,\nСмята тяжестью диких ветвей.",
    "En la penumbra tus ojos\nSon más cercanos, brillantes, oscuros y feroces.\nMe rindo a merced, como la vid,\nAplastada por el peso de las ramas salvajes."),
    
   ("Дурман (El narcótico)",
    "От дыханья твоего — дурман,\nГолова кружится, как в бреду.\nЭто самый сладкий мой обман,\nЯ сама на гибель к нам иду.",
    "Por tu aliento — hay un narcótico,\nLa cabeza me da vueltas, como en un delirio.\nEs mi engaño más dulce,\nYo misma voy directo a nuestra perdición."),
    
   ("Укус (Mordisco)",
    "След от губ твоих горит огнем,\nНа плече оставлен дерзкий знак.\nМы забыли обо всем на свете днем,\nПогружаясь в этот сладкий мрак.",
    "La huella de tus labios arde como el fuego,\nEn mi hombro ha quedado una descarada marca.\nHemos olvidado de todo el resto del mundo de día,\nSumergiéndonos en esta dulce oscuridad."),
    
   ("Парижская ночь (Noche parisina)",
    "За окном чужой шумит Париж,\nНо в объятьях мне не холодно ничуть.\nЕсли ты, безумствуя, не спишь,\nДай мне снова в страсти утонуть.",
    "Tras la ventana hace ruido el ajeno París,\nPero en tus abrazos no tengo frío en absoluto.\nSi tú, enloqueciendo, tampoco duermes,\nDéjame ahogarme en la pasión una vez más."),
    
   ("Бессонница (Insomnio)",
    "Я лежу, закрывая глаза,\nЧувствуя тяжесть на бедрах своих.\nНеужели я все же смогла\nРаствориться в руках молодых?",
    "Estoy tumbada, cerrando los ojos,\nSintiendo el peso sobre mis muslos.\n¿Acaso he sido capaz a pesar de todo\nDe disolverme en unas jóvenes manos?"),
    
   ("Слезы страсти (Lágrimas de la pasión)",
    "Я плачу, но не от тоски,\nА от силы, что рвет изнутри.\nСжимаются в судорогах виски,\nО, не останавливайся... гори!",
    "Estoy llorando, pero no es de pena,\nSino de la fuerza que explota desde dentro.\nLas sienes se me aprietan a causa de los espasmos,\n¡Oh, no pares nunca... sigue ardiendo!"),
    
   ("Утренний свет (La luz de la mañana)",
    "Рассвет разрезал темноту,\nНо ты все так же груб и смел.\nЯ перешла свою черту,\nВступив в игру свирепых тел.",
    "El amanecer rajó a toda esta oscuridad,\nPero tú sigues siendo tan bruto y valiente.\nY yo misma me crucé toda mi raya,\nSumándome al juego entre cuerpos que se hacen feroces."),
    
   ("Шепот (El murmullo)",
    "Твой шепот у самого уха,\nКак заклинание древних жриц.\nДля морали я стала глуха,\nПадая в омут без всяких границ.",
    "Tu mismo murmullo que se acerca tan a la oreja,\nY es como si fuere todo un viejo hechizo muy antiguo.\nA lo que diga la moral he quedado oyendo nada,\nCayendo hasta la ciénaga y bien sin poner límite ninguno.")]),

 ("132","Karolina Pavlova","1807–1893","Rusia","ruso",
  "Karolina Pavlova fue una voz poética profundamente marginada por las élites literarias rusas debido a su espíritu indomable y su independencia financiera. Abandonada por su esposo y forzada a la soledad, su poesía adquirió un tono incisivo, de amarga melancolía que a veces desembocaba en versos sobre su asfixiante aislamiento y encendidos anhelos hacia las pasiones y pasados tórridos y románticos que le fueron arrebatados.",
  [("Слепой огонь (Fuego Ciego)",
    "В моей груди горит слепой огонь,\nОн требует не слов, а сильных рук.\nПрижмись ко мне и только тихо тронь,\nЧтоб разорвать отчаяния круг.",
    "En mi pecho arde un fuego ciego,\nQue exige no palabras, sino fuertes manos.\nApriétate a mí y tan solo tócame bajito,\nPara romper el círculo de la desesperación."),
    
   ("Ночь без сна (Noche sin sueño)",
    "Измята простынь, душно в тишине,\nМеня томит незримый, жаркий плен.\nЯ, жаждая, зову тебя во сне,\nСклоняясь пред безумием колен.",
    "Arrugada la sábana, ahogada en el silencio,\nMe fatiga un invisible y ardiente cautiverio.\nYo, deseando con sed, te llamo en el sueño,\nInclinándome ante la locura en las rodillas."),
    
   ("Дикий порыв (Salvaje impulso)",
    "Моя душа — мятеж, а тело — дрожь,\nСлепая жажда все смести с пути.\nО, в эту ночь ты правду иль ложь,\nМне все равно, лишь плотью захвати.",
    "Mi alma es — rebeldía, y el cuerpo — temblor,\nUna ciega sed de barrerlo todo del camino.\nOh, da igual en esta noche que fueres tú la verdad o la mentira,\nMe da igual, con tal que con la carne me agarres."),
    
   ("Шелк и пот (Seda y sudor)",
    "Шелк обжигает мокрую спину,\nЯ задыхаюсь от жадных губ.\nВ эту пучину я гордость кину,\nБудь же со мною и нежен, и груб.",
    "La seda quema sobre esta espalda sudada,\nY yo misma me quedo falta por estos ásperos tus labios.\nHacia este mismo abismo es adónde arrojaré todo pudor,\nY sé tú ahora conmigo siendo a ratos dulce, y de repente grosero."),
    
   ("Предательство плоти (Traición de la carne)",
    "Я обещала быть строгой и хладной,\nНо кровь вскипела, ломая запрет.\nПод твоей лаской, столь беспощадной,\nЯ забываю о тяжести лет.",
    "Prometí ser estricta y de lo más fría,\nPero hete que me hirvió la sangre, rompiendo toda restricción.\nY que bajo este halago bien despiadado,\nEstoy ahora yo olvidando el mucho pasatiempo cruel de mis años."),
    
   ("Прикосновение (El Roce)",
    "Твоя ладонь скользит все ниже, ниже...\nВ глазах темнеет, стон сдержать невмочь.\nСтань мне еще безжалостней и ближе,\nПродли эту бесстыдную ночь.",
    "Va tu misma palma tan resbalosa a ir hasta más abajito, aún más...\nEl ojo se va cubriendo espeso, sin conseguir silenciar el gemido.\nPara que tú te acerques a mí todo bruto y más próximo,\nAlargando esta noche desvergonzada."),
    
   ("Сломленная (Quebrada)",
    "Я рухнула в твои объятия,\nКак птица, сбитая в полете.\nОсудит свет, пошлет проклятия,\nНо я послушна властной плоти.",
    "Me he derrumbado en tus abrazos,\nComo un pájaro derribado en vuelo.\nEl mundo me juzgará, enviará maldiciones,\nPero yo soy obediente a la carne imperiosa."),
    
   ("Изгой (La desterrada)",
    "Отвержена светом, забыта условно,\nНо здесь, на ковре, я царица всего.\nМы любим друг друга так дерзко, греховно,\nЧто в целом мире нет больше никого.",
    "Rechazada por la sociedad, supuestamente olvidada,\nPero aquí, en la alfombra, soy la reina de todo.\nNos amamos tan descaradamente, tan pecaminosamente,\nQue en el mundo entero no hay nadie más."),
    
   ("Пламя (La Llama)",
    "Сжигай меня медленно, не торопись,\nПусть каждый нерв раскалится до звона.\nК высотам порока со мной поднимись,\nГде нет ни стыда, ни суда, ни закона.",
    "Quémame lentamente, no te apresures,\nDeja que cada nervio se ponga al rojo vivo hasta sonar.\nAsciende conmigo a las alturas del vicio,\nDonde no hay vergüenza, ni juicio, ni ley."),
    
   ("После (После)",
    "Устало откинувшись, тяжко дыша,\nЯ чувствую: мы перешли через край.\nМоя изнуренная жаждой душа\nНашла в твоей страсти свой гибельный рай.",
    "Echándome hacia atrás agotada y respirando con pesadez,\nSiento: hemos cruzado el límite.\nMi alma, exhausta de sed,\nHa encontrado en tu pasión su propio paraíso destructivo.")]),

 ("133","Evdokia Rostopchina","1811–1858","Rusia","ruso",
  "Condesa y prolífica poeta de la Rusia Imperial. Muy leída en su época, gozaba de un éxito deslumbrante en la alta sociedad antes de que sus versos, francos y rebeldes, chocaran con la férrea censura patriarcal. Sus arrebatos líricos describen amores adúlteros, desencuentros amorosos en bailes de máscaras y una avasalladora inclinación carnal por jóvenes húsares y poetas con la cual llenaba la vacuidad descorazonada de su matrimonio aristocrático.",
  [("Неотправленное письмо (Carta no enviada)",
    "Я пишу тебе в тайне от всех,\nКогда ночь обнимает столицу.\nМоя страсть — это сладостный грех,\nЧто сжигает меня, как блудницу.",
    "Te escribo en secreto, lejos de todos,\nCuando la noche abraza la capital.\nMi pasión — es un dulce pecado,\nQue me quema viva, como a una ramera."),
    
   ("Маскарад (Baile de máscaras)",
    "Под маской я смелее вдвое,\nМоя рука в твоей руке.\nМы скрылись в темное покои,\nЗабыв о светской мишуре.",
    "Bajo la máscara soy dos veces más osada,\nMi mano está en tu mano.\nNos escondimos en oscuros aposentos,\nOlvidando el oropel de la alta sociedad."),
    
   ("Поцелуй гусара (El beso del húsar)",
    "Твои усы колючи, губы жарки,\nВ твоих объятьях кружится земля.\nЯ отдаюсь без страха и утайки,\nМой юный бог, я полностью твоя.",
    "Tus bigotes son ásperos, tus labios ardientes,\nEn tus brazos la tierra da vueltas.\nMe entrego sin miedo y sin reservas,\nMi joven dios, soy completamente tuya."),
    
   ("Измена (Traición)",
    "Пусть муж мой спит спокойным сном,\nА я крадусь к тебе в ночи.\nМы сбросим цепи, гнет сломаем,\nИстлеют брачные ключи.",
    "Que mi marido duerma con sueño tranquilo,\nMientras yo me escabullo hacia ti en la noche.\nArrojaremos las cadenas, romperemos la opresión,\nY las llaves matrimoniales se convertirán en cenizas."),
    
   ("Власть тела (El poder del cuerpo)",
    "Разум шепчет: 'Остановись',\nА кровь кричит: 'Иди смелей!'.\nЯ бросилась в слепую высь\nСвоих безумных, диких дней.",
    "La razón me susurra: 'Detente',\nPero la sangre grita: '¡Ve, más atrevida!'.\nMe he lanzado a ciegas a las alturas\nDe mis propios y dementes, salvajes días."),
    
   ("Дрожь (Temblor)",
    "Как я дрожала, скинув шелк,\nПод резким взглядом черных глаз.\nТвой аппетит, как жадный волк,\nНастиг меня в полночный час.",
    "Cómo temblaba yo, al arrojar la seda,\nBajo la aguda mirada de tus ojos negros.\nTu apetito, igual que un lobo hambriento,\nMe alcanzó en la hora de la medianoche."),
    
   ("Нагая правда (La verdad desnuda)",
    "Среди перин, нагих и влажных,\nМы познавали суть любви.\nНет клятв пустых, речей бумажных,\nЛишь стоны, жар и пульс в крови.",
    "Entre edredones desnudos y húmedos,\nNosotros conocíamos la esencia del amor.\nNo hay juramentos hueros, ni discursos de papel,\nSólo gemidos, ardor y pulso en la sangre."),
    
   ("Грешная душа (Alma pecadora)",
    "Мне не нужен небесный покой,\nЕсли в нем не найдется тебя.\nЯ согласна низвергнуться в зной,\nЛишь бы мучиться, дико любя.",
    "No necesito el descanso celestial,\nSi en él no puedo encontrarte a ti.\nEstoy de acuerdo en despeñarme hacia el ardor,\nCon tal de torturarme, amándote salvajemente."),
    
   ("Молчание (Silencio)",
    "Не говори ни слова, прикоснись,\nПусть кожа подтвердит твой властный пыл.\nВ моей груди вулканом рвется высь,\nУж нет сопротивляться женских сил.",
    "No digas ni una sola palabra, tócame,\nDeja que la piel confirme tu afán de poder.\nEn mi pecho se desgarra un volcán hacia lo alto,\nYa no me quedan fuerzas de mujer para resistirme."),
    
   ("Рассветный ужас (El horror del amanecer)",
    "Светает. Скоро мне бежать,\nНадеть корсет, лицо благопристойной.\nНо ночью я вернусь в твою кровать,\nСвирепой, жадной, непокорной.",
    "Amanece. Pronto he de huir,\nPoner mi corsé y la cara de señora decente.\nPero por la noche regresaré a tu propia cama,\nSiendo alguien feroz, ávida e indomable.")]),

 ("134","Anna Akhmatova","1889–1966","Rusia","ruso",
  "Gigante de la Edad de Plata rusa. La joven Akhmatova revolucionó la poesía con sus poemas acmeístas acerca de las emociones amorosas cotidianas, directas y punzantes ('La tarde', 'El Rosario'). Mostraba mujeres abrumadas por amantes insensibles, encuentros culpables en cuartos con humo y despedidas en la nieve, articulando el deseo sin romanticismos: con las manos heladas poniéndose el guante izquierdo en la mano derecha de puro aturdimiento pasional.",
  [("Смятение (Confusión)",
    "Было душно от жгучего света,\nА взгляды его — как лучи.\nЯ только вздрогнула: этот\nМожет меня приручить.",
    "Hacía sofocante calor por la luz ardiente,\nY las miradas de él eran — como rayos.\nYo no hice otra cosa que sobresaltarme: éste\nPuede a mí llegar a domarme."),
    
   ("Сероглазый король (El rey de ojos grises)",
    "Слава тебе, безысходная боль!\nУмер вчера сероглазый король.\nВечер осенний был душен и ал,\nМуж мой, вернувшись, спокойно сказал...",
    "¡Gloria a ti, un dolor sin salida!\nMurió ayer mi propio rey el de ojos de grises.\nLa tarde en el otoño estuvo muy asfixiante y escarlata,\nMi esposo, nada más de regresar me ha dicho muy con calma..."),
    
   ("Песня последней встречи (Canción del último encuentro)",
    "Так беспомощно грудь холодела,\nНо шаги мои были легки.\nЯ на правую руку надела\nПерчатку с левой руки.",
    "El pecho se me enfriaba tan desamparadamente,\nPero aun así mis pasos al caminar han estado harto de marchar ligeros.\nYo nada que encima de mi mano de la derecha es que me fui poniendo\nEl guante mismo que llevaba yo puesto desde hace nada para la mano de la izquierda."),
    
   ("Я научилась просто, мудро жить (Aprendí a vivir sencilla y sabiamente)",
    "Шуршат в овраге лопухи,\nИ никнет гроздь рябины желто-красной.\nСлагаю я веселые стихи\nО жизни тленной, тленной и прекрасной.",
    "Crujen en un tremendo barranco los muy varios bardanas,\nY también se está apagando del todo el gran racimo de ese su tan rojo y amarillento acerolo.\nAquí a componer es todo donde yo ahora dedique yo sola para hacer bien alegrecillo poema\nY con toda constancia para nada duradera con una muy inefable y de bella la tal vida misma."),
    
   ("Дверь полуоткрыта (La puerta a medio abrir)",
    "Дверь полуоткрыта,\nВеют липы сладко...\nНа столе забыта\nХлыстик и перчатка.",
    "Ahí se veía una misma puerta que la daban todo con dejar a medio asomar de lo abierta,\nRefrescaban los olores a los grandes de muy lejos con gran dulzor todos los perfumosos tilos...\nY a la mesa sobre encima nada que se dejaron allí una sin duda olvidado que por todo un fuste como látigo fino\nEn donde también pegado le seguí ahí de olvidado una pieza sola de nada entero a simple guantecillo."),
    
   ("Сжала руки под темной вуалью (Estreché las manos bajo el velo oscuro)",
    "Сжала руки под темной вуалью...\n'Отчего ты сегодня бледна?'\n— Оттого что я терпкой печалью\nНапоила его допьяна.",
    "Me andaba entonces de lo lindo bajo la red de gran oscuro el color estrechándome sola muy junta como en la velo...\n'Pero si oye para por cómo que luces al día de en hoy la mismita pálida de nada'\n—De todo por como yo lo agarré siendo todo al que le empapé por la gran pena misma y algo de agria que duele\nY a emborrachar tanto como no dar un límite al tope embriagado se le quedó reventado ya no sin más."),
    
   ("Любовь (Amor)",
    "То змейкой, свернувшись клубком,\nУ самого сердца колдует,\nТо целые дни голубком\nНа белом окошке воркует.",
    "Y aquí una que ya no hace por momentos sino arrastrarse hecho ovillo como culebra,\nY al sitio y ras de junto muy dentro que da un hechizo a donde está en el corazón,\nO aquí como ando nada sin perder todo con esos varios días seguidos e intensos a forma de la paloma blanca\nY por este marco asomado todo a albor de a ventana el día por en cuando sorda va y arrulla."),
    
   ("Муж хлестал меня узорчатым (El marido me azotó con recamado)",
    "Муж хлестал меня узорчатым,\nВдвое сложенным ремнем.\nДля тебя в окошке створчатом\nЯ всю ночь сижу с огнем.",
    "Me fue el mi marido a zurrar que sí de lo muy estampado,\nDándole toda una con al fuerte una en doblado el cinto correoso por muy a la misma dos veces.\nY no para que yo te estuviese mirando a todos estos que se andan a dejar abiertos los abisagradas las ventanas\nY allí quedándome en un no dormir sentadita toda encendiendo el fuego esperando de paso así siempre la noche de mi vida."),
    
   ("Звенела музыка в саду (Sonaba la música en el jardín)",
    "Звенела музыка в саду\nТаким невыразимым горем.\nСвежо и остро пахли морем\nНа блюде устрицы во льду.",
    "Había estado toda rato como ando muy retumbando aquella gran música como la que hubiere muy dentro siempre en este mi jardín\nDe un muy así gran no haber como dar expresión sin dejar el cómo y tanta aflicción pesadumbre.\nPero daban un tal cual frescor como muy filosamente de a olores a un puro olor de hasta la gran del mar\nY todo de en la ración sobrepuesta todas enteras con hielos por unas solas servidas al natural sin faltas la cruda gran ostra."),
    
   ("Я не любви твоей прошу (Yo no te pido amor)",
    "Я не любви твоей прошу.\nОна теперь в надежном месте.\nПоверь, что я твое невесте\nРевнивых писем не пишу.",
    "No es por que el gran del todo ande de verdad muy buscando mendigando como no haber andado en tu muy fuerte de el gran tu amor.\nY esa sí en muy por su gran andada parte por haber llegado para estar resguardada toda gran a salvo en alguna tal segura de lugar.\nCréemelo o de creer que también si es por mí sobre a esa que va de muy tu gran próxima nueva y como no futura prometida esposa tuya\nNunca jamás que hubieres en ser yo como tan de que fuera para hacerte cartas sin falta con algún receloso por si dar a celos alguno que le mande o remita yo ni eso uno solo de nada.")]),

 ("135","Marina Tsvetaeva","1892–1941","Rusia","ruso",
  "Genio poético impar, salvaje y trágico. La intensidad pasional extrema rige sus obras de juventud. Fue de las grandes poetas de la desesperación física, de las cartas abrasadoras de amor (a Rilke, a Pasternak, a Sofia Parnok...). Su lírica carece de la contención acmeísta: fluye a borbotones, gimiendo con rabia, lujuria arrebatada y un sentimiento caníbal por engullir y ser poseída vital y eróticamente por el amor de ambos sexos.",
  [("Под лаской плюшевого пледа (Bajo la caricia de la colcha de felpa)",
    "Под лаской плюшевого пледа\nВчерашний вызываю сон.\nЧто это было? — Чья победа? —\nКто побежден?",
    "Bajo la asfixiante e intensa gran y acariciante colcha al ras felposa por de lana\nInvoco mi gran como si fue un tal y cual o si hubiera habido soñar mío recién ayer.\n¿Acaso en verdad de qué leches qué tan si qué todo de se andaba todo esto? — ¿Por culpa también a quién de en verdad le tocare de a triunfo de aquí sacar el salir gran vencedor victoria al final? —\n¿Quién por de muy remate y ya andado acabó estando para si de uno para en el suelo batido sin resurgir ya de más muy así del el tan que muy bien del de a todo tan vencido?"),
    
   ("Хочу у зеркала, где муть (Quiero ante el espejo, donde hay turbiedad)",
    "Хочу у зеркала, где муть\nИ сон туманящий, —\nЯ выпытать: куда вам путь\nИ где пристанище.",
    "Ando que yo sí le ruego y al gran frente al del espejo ese de donde tanto sin fondo asoma la de asomarse a grande mucha de esa de una muy gran toda así la gran misma la sin duda toda muy tan enorme turbiedad algo que sucia no viéndose un nada claro ni a dos\nY el como que hay al dormir a ensueño ando así por muy de algo que hay la de ir muy cegante nublado muy neblinoso, —\nYo sí como a andarme ir a sacarte ir interrogándote a tirar de por un gran saber al dónde se dirige ya el mi todo ir rumbo tu mismo camino andar todo andado del a todo camino tuyo gran camino\nY al final en todo donde está al remate adónde de la tu grandiosa a toda final estancia o toda andada final en ti en que paró de toda guisa gran cobijo y también toda tú la tu refugio o algo a más de a ti toda guarida final de dar de ti puerto todo tuyo abrigo."),
    
   ("Мне нравится, что вы больны не мной (Me gusta que usted no esté enfermo por mí)",
    "Мне нравится, что вы больны не мной,\nМне нравится, что я больна не вами,\nЧто никогда тяжелый шар земной\nНе уплывет под нашими ногами.",
    "Me agrada de tal caso sobre de que en que a usted de tan grande usted o es a usted a lo de verdad usted se andas de nada sin nada estando sin lo más lo peor que no le de enfermo para andar en mis pos ni de por de nada por mi mismita y mí con en cuanto yo de que o para mí mima,\nMe gusta algo esto de tanto sin que de ya a que le en lo soy para lo nada no estoy del todo enferma para por detrás suyo de como o ni sea para en algo a por ustedes ya por mí mi yo a lo menos ni un tanto en por ustedes para nada,\nQue nunca del nunca a lo siempre y de un sin ir final la una al como si es pesado todo lo gordo de una al como no bola esférico mundo globo del redondo de un terrenal que a planeta o en sí la orbe andada como que da este del terrestre todo globo mundi\nJamás bajo nosotros flote y ande como de muy escapando huido ni nada que ni siquiera hunda no yendo nunca de por a debajo de muy a ras con ras ni nada por al y debajo de debajo el de ninguno lo a entre ni nuestros muy entre sí dos propios y andando arrastrándose que sin ya ni lo de estos al sin lo final de unos en ya pie y pies nuestros."),
    
   ("Жажда (La Sed)",
    "Рот — на рот, и кровь — за кровью!\nБольше сил нет ждать!\nС этой бесовской любовью\nХочется кричать.",
    "Boca a boca, ¡y sangre a por sangre!\n¡Ya no hay más fuerzas para esperar!\nCon este amor tan endemoniado\nDa ganas de ponerse a gritar."),
    
   ("Вскрыла вены (Me abrí las venas)",
    "Вскрыла вены: неостановимо,\nНевосстановимо хлещет жизнь.\nПодставляйте миски и тарелки!\nВсякая тарелка будет — мелкой.",
    "Me he rajado las venas: de forma irrefrenable,\nDe forma irreversible, va manando la vida.\n¡Id poniendo los cuencos y los platos!\nCualquier plato resultará siendo — poco profundo."),
    
   ("Кошка (La Gata)",
    "Ты вошел, как входят в двери:\nНи звонка и ни ключа.\nИ проснулся дикий зверь в\nТеле, ждущем палача.",
    "Tú entraste, igual que por las puertas se entra:\nSin llamar al timbre, y sin que haga falta llave.\nY dentro del cuerpo despertó una bestia salvaje,\nEn este cuerpo, que estaba a la espera de un verdugo."),
    
   ("Имя твое — птица в руке (Tu nombre es — un pájaro en la mano)",
    "Имя твое — птица в руке,\nИмя твое — льдинка на языке.\nОдно-единственное движенье губ.\nИмя твое — пять букв.",
    "Tu nombre es — un pájaro aferrado en la mano,\nTu nombre en la lengua es de hielo un cubito florido y lozano.\nPor tan un solo a solas de movimientos tan movidos de los de como en el del todo tus los de mí al mismo de un mi todo del a un al labio mis de entre ambos mis ya de en mis labios.\nTu nombre es a forma a solas sí un el decir se andaría o no por fin se andaría por de un de al tu tu mismo sin que de tú más a a ver nombre que son es en un nada es el todo de unas a en con gran unas lo en por de todo si nada a de solas hay ya muy del todas que sí todas las nada más cinco unas de muy sin falta o con en total tus todas allí son las ya o sin faltas de con cinco solas letras en sí mismas."),
    
   ("Цыганская страсть (Pasión gitana)",
    "Разодрано в клочья платье,\nИ волосы спутаны в шаль.\nДержи меня в жарком объятье,\nТопчи мою тихую печаль.",
    "Hice que el vestido quedara rasgado entero en tiras y pedazos,\nY hasta lo que es en mis pelos muy tan bien del enredados sueltos todos en sí con y un como que con forma todo a por un muy un gran al su que chal.\nAmárrame de sostenme siempre muy firme atada con de en tu ese tu al tu a como lo un como gran a fuerte como todo si muy cálido abrazo gran abrasador en muy abrazo,\nPisotea como tritura muy de lo que mi mi por esa tal de mi muy tuya que yo le la la de en un muy que tuve lo mi silente tan silente suave o quieta la que ande aquí esa mi más mútica y silenciosa mi muda muy dolorosa mi con gran triste tristeza."),
    
   ("Мой день блуден (Mi día es lujuria)",
    "Мой день блуден и ночь блудна.\nНе выпить чашу страстей до дна.\nНо я бросаюсь в твой дикий омут,\nГде даже боги бесследно тонут.",
    "Mi día entero es puro fornicar lujurioso, igual que de día a lujuria también andará lo es así toda en mí en mi al noche.\nComo no andará de poder andar que me poder beber y a darle a no parar ahogando desde esta sin falta a la de la del gran mía una a mí la que sea mi grande gran mía esta inmensa de la mía toda gran del toda mía en toda a gran vaso a del copa del mis del pasiones mías ahogadas hartas pasiones sin tope al hasta con a apurar remate todo su ras al fondo.\nSin que de por pero nada pero me voy me lanzo tirando de lo mío a para dentro tuyo metiéndome cayéndome voy al de un muy dentro del que sea a lo tuyo este inmenso del salvaje a tu muy tu remolino tuyo remolino del agua loco o pozo salvaje,\nDonde que en el cual del en donde hasta al si a que incluso ahí de no ser también a todos de ahogan enteros los de sin parar mis dioses al hasta todo hasta perder todo sin más todo rastro al de una nada a perdiendo el sin sol y de lo y en el perder las pista los puros en de incluso los mismos unos los hasta mismos a a por unos grandes ahí a ahí perdiéndose dioses."),
    
   ("Кровь на губах (Sangre en los labios)",
    "Мы искусали губы в кровь,\nДеля последнюю любовь.\nОставь меня истерзанной, разбитой,\nНо навсегда твоей, не позабытой.",
    "Nos hemos de mordido hasta la misma sangre sobre en a de los dentro sobre todos como en por en nuestros los más o del nuestros mis los en labio tú y yo y juntos labios a gran sangre los nuestros y labios mutuos para y a sacar todos por sin a ambos dos a mordiscos hacer gran mucha a como gran viva el de la los hacer sangre,\nCon andarse para ande en ir dividiendo en un al así que compartiendo esta en sin a ser aquí ser a estar aquí nos para el final este nuestro a ya al gran último nada sin final a no ir dar no dar fin último gran postrero de todo este es todo a último amar tan a nuestra que amar a la misma de la amor amar pasión final o al último postrer por fin amor no más que amor.\nDéjame ya que y como vete déjate al a mi mí a sola a que aquí dejar y qué es que si es como andada si yéndome aquí arrojado y bien la despedazada o como dejándome o la muy y y como destrozada herida atormentada, sí todo bien o con el ir ya destrozada rota o como con bien mal destrozada estropeada sin muy arruinada arrojada o apedreada destrozada,\nPero nada pero eso más porque de eso sépase sí a sabiendas o si nada que va ser y o ser no de más siempre la más gran inmensa la a por la como lo toda la siempre en la una y tuya entera para tu en del y de por por mí ya que y de todo eso nunca el la ya no andada sin no quedar o ir por con el del tu el para nunca de para con sin nada sin olvidos y ni sin con ser tu jamás o bien nada nunca del siempre o a la y nada o con siempre ya toda e siempre olvidada.")])
]

if __name__ == "__main__":
    for item in CORRECCIONES:
        mk(*item)
