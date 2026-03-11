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
 ("126","Ada Negri","1870–1945","Italia","italiano",
  "Nacida en la Italia proletaria, Ada Negri irrumpió en la escena poética rompiendo los moldes burgueses con una poesía palpitante, ruda y natural. Cantó al amor plebeyo, violento y directo. Sus versos sobre pasiones amorosas exudan el esfuerzo físico, la inmediatez de la sangre y la carnalidad de quienes no tienen tiempo de fingir pudor, ensalzando la belleza del placer arrollador sobre fardos de heno o en cuartos ahogados por el sol estival.",
  [("Il Canto del Sangue (El canto de la sangre)",
    "Non vedi come freme la mia vena ?\nÈ un fiume rosso che domanda il mare.\nStringimi forte, sciogli ogni catena,\nIn questo gorgo mi voglio annegare.",
    "¿No ves cómo se estremece mi vena?\nEs un río rojo que exige el mar.\nApriétame fuerte, desata toda cadena,\nEn este remolino quiero ahogarme."),
    
   ("Maternità (Maternidad Carnal)",
    "Dal tuo respiro roco, un fuoco sento\nChe fino alle midolla mi pervade.\nSul corpo tuo m'abbandono nel vento,\nSfiorando l'ebbrezza di chi in fiamme cade.",
    "De tu respiración ronca, siento un fuego\nQue me invade hasta la misma médula.\nSobre tu cuerpo me abandono en el viento,\nRozando la embriaguez de quien cae en llamas."),
    
   ("Senza Leggi (Sin Leyes)",
    "Che importa il mondo e la vana morale,\nSe la tua bocca impone il suo dominio ?\nIo cedo lieta all'assalto fatale,\nNuda nel buio del nostro sterminio.",
    "¿Qué importa el mundo y la vana moral,\nSi tu boca impone su dominio?\nCedo gozosa al asalto fatal,\nDesnuda en la oscuridad de nuestro exterminio."),
    
   ("Estiva Invasione (Invasión Estival)",
    "Il caldo mozza il fiato e le parole,\nE resta solo l'urto dei due petti.\nTu mi consumi come fa il bel sole,\nStrappando l'ombra a tutti i miei diletti.",
    "El calor corta el aliento y las palabras,\nY sólo queda el choque de los dos pechos.\nTú me consumes como hace el bello sol,\nArrancando la sombra a todos mis deleites."),
    
   ("Popolana Amante (La amante plebeya)",
    "Non ho lenzuola lisce o di gran seta,\nMa la mia carne è fresca e trepidante.\nPrendimi qui, selvaggia, irrequieta,\nFino a stremarti nell'urto ansimante.",
    "No tengo sábanas lisas ni de gran seda,\nPero mi carne es fresca y trepidante.\nTómame aquí, salvaje, inquieta,\nHasta extenuarte en el choque anhelante."),
    
   ("L'Abbraccio Cieco (El abrazo ciego)",
    "Chiudo i miei occhi al raggio del mattino,\nPerché il tuo tocco riempia i miei confini.\nVoglio sentire tutto il tuo destino,\nE rimescolarmi coi tuoi caldi crini.",
    "Cierro mis ojos al rayo de la mañana,\nPara que tu roce llene mis confines.\nQuiero sentir todo tu destino,\nY revolverme con tus cálidas crines."),
    
   ("Sete (Sed)",
    "Dammi da bere l'acqua del tuo bacio,\nSono riarsa da quest'arsa attesa.\nSento che sotto il tuo vigor mi sfaccio,\nDolcemente abbattuta ed arresa.",
    "Dame de beber el agua de tu beso,\nEstoy reseca por esta ardida espera.\nSiento que bajo tu vigor me deshago,\nDulce y totalmente abatida y rendida."),
    
   ("Vittoria (Victoria)",
    "Hai vinto tu, col muscolo e lo sguardo,\nIo che ridevo d'ogni fiera voglia.\nAdesso al tuo cospetto piango ed ardo,\nSpogliata del mio io come di spoglia.",
    "Has vencido tú, con el músculo y la mirada,\nYo que me reía de cualquier fiero deseo.\nAhora ante ti lloro y ardo,\nDespojada de mi propio ser como un despojo."),
    
   ("Passione Selvaggia (Pasión Salvaje)",
    "Mordimi il collo finché non ho male,\nFinché il piacere sbaragli il dolore.\nIl nostro istinto è antico, animale,\nE fa tremare di furia il mio core.",
    "Muérdeme el cuello hasta que me duela,\nHasta que el placer desbarate al dolor.\nNuestro instinto es antiguo, animal,\nY hace temblar de furia a mi corazón."),
    
   ("Ultima Brama (Última Avidez)",
    "Vorrei morire mentre sei in me fuso,\nPer rimanere eterna in quell'ardore.\nLontana dal dolor d'un mondo chiuso,\nPadrona solo di questo mio fiore.",
    "Quisiera morir mientras estás en mí fundido,\nPara permanecer eterna en aquel ardor.\nLejos del dolor de un mundo cerrado,\nDueña únicamente de ésta mi flor.")]),

 ("127","Grazia Deledda","1871–1936","Italia","italiano",
  "Premio Nobel de Literatura. Aunque célebre por su prosa profundamente telúrica sobre su Cerdeña natal (donde retrató amores prohibidos contra un entorno asfixiante e implacable), en su lírica inicial (y en los poemas intercalados de sus héroes), saca a la luz pasiones oscuras, celos viscerales, adulterios carnales y un deseo volcánico que ruge como la naturaleza sarda bajo el dominio represor, evidenciando instintos sensuales muy por delante de la puritana Italia de su época.",
  [("Il Fuoco Nascosto (El fuego oculto)",
    "Brucia la macchia e l'aria sa di fumo,\nMa più del bosco brucia il mio respiro.\nQuando t'accosti, le mie forze spiumo,\nE nei tuoi occhi scuri mi ritiro.",
    "Arde la maleza y el aire huele a humo,\nPero más que el bosque arde mi aliento.\nCuando te acercas, mis fuerzas se despluman,\nY en tus ojos oscuros me retiro."),
    
   ("Amore Bandito (Amor Bandolero)",
    "Nascosti nella grotta pastorale,\nLa legge degli uomini qua non vige.\nCi unisce solo l'impeto carnale,\nChe ogni regola ed ansia sconfigge.",
    "Escondidos en la cueva pastoril,\nLa ley de los hombres aquí no rige.\nNos une solo el ímpetu carnal,\nQue toda regla y ansiedad derrota."),
    
   ("La Sete della Murgia (La sed de la Meseta)",
    "Secca è la terra, secche son le vene,\nTu sei la pioggia che rinnova il prato.\nPrendi le mie pudiche e false catene,\nE fammi tua con urto disperato.",
    "Seca es la tierra, secas son mis venas,\nTú eres la lluvia que renueva el pasto.\nToma mis púdicas y falsas cadenas,\nY hazme tuya con choque desesperado."),
    
   ("Notte Sarda (Noche Sarda)",
    "Nessuno vedrà il segno dei tuoi denti,\nCelato tra i fieri ricami del corpetto.\nSiamo nel buio, soli, veementi,\nE il peccato fiorisce nel mio petto.",
    "Nadie verá la marca de tus dientes,\nOculta entre los fieros bordados del corpiño.\nEstamos en la oscuridad, solos, vehementes,\nY el pecado florece dentro de mi pecho."),
    
   ("Il Respiro nel Vento (El respiro en el viento)",
    "Sento venirti prima di vederti,\nL'istinto mi ha svegliato in mezzo al letto.\nHo preparato i miei domini incerti,\nPer darti nuda e calda asilo e tetto.",
    "Siento tu venida antes de verte,\nEl instinto me ha despertado en medio del lecho.\nHe preparado mis dominios inciertos,\nPara darte, desnuda y cálida, asilo y techo."),
    
   ("Vendicante Passione (Pasión Vengadora)",
    "Io ti vorrei veder morir d'amore,\nSudare le mie stesse smanie grevi.\nDivorerei il tuo aspro e maschio cuore,\nFinché la sete estrema tu non bevi.",
    "Yo quisiera verte morir de amor,\nSudar mis mismas y graves ansiedades.\nDevoraría tu áspero y varonil corazón,\nHasta que la sed extrema no te bebas."),
    
   ("Sotto il Nuraghe (Bajo el Nuraga)",
    "Al riparo di pietre millenarie,\nCi scambiamo promesse ardenti e ladre.\nL'oblio scende su le menti varie,\nEd è solo la carne a farsi madre.",
    "Al amparo de piedras milenarias,\nNos intercambiamos ardientes y ladronas promesas.\nEl olvido desciende sobre las mentes varias,\nY es sólo la carne la que se hace madre."),
    
   ("Miele Amaro (Miel Amarga)",
    "Come il corbezzolo, sei dolce ed agro,\nUn veleno squisito che m'inghiotte.\nNel tuo selvaggio abbraccio mi consacro,\nLanciando gridi nella folta notte.",
    "Como el madroño, eres dulce y agrio,\nUn veneno exquisito que a mí me engulle.\nEn tu salvaje abrazo me consagro,\nLanzando gritos en la espesa noche."),
    
   ("Fatica Dolce (Dulce Fatiga)",
    "Rotte ho le ossa per la tua tempesta,\nIeri sull'erba folta del ciglione.\nMa nell'anima mia oggi c'è festa,\nDomata e paga di ribellione.",
    "Rotas tengo las osamentas por tu tormenta,\nAyer sobre la espesa hierba del cerrojo.\nPero en mi alma hoy hay mucha fiesta,\nDomada y paga tras la rebelión."),
    
   ("L'Isola Carnale (La isla carnal)",
    "Siamo circondati dal vasto mare,\nNessuna fuga e nessun pentimento.\nNon ci resta che piangere ed urlare,\nCullati dal violento nostro accento.",
    "Estamos rodeados por el mar extenso,\nSin haber ya huida ni arrepentimiento.\nNo nos queda que asir el cuerpo tenso,\nY abrazarnos bajo el salvaje viento.")]),

 ("128","Antonia Pozzi","1912–1938","Italia","italiano",
  "Poesía sensual e intensa marcada ferozmente por amores trágicos, en particular el romance reprimido con su maduro profesor de griego. Toda su obra quedó rigurosamente inédita en su vida (mantenida en libretas ocultas). Tras suicidarse muy joven a causa de la represión moral y la frustración, salieron a la luz versos estremecedores, cargados de intimidad febril, visiones desnudas y una desgarradora voluptuosidad ansiosa de fusión total.",
  [("Desiderio",
    "Sentivo il tuo respiro sui capelli,\nE mi scendeva il sangue fino al cuore.\nIo chiudevo gli occhi come fanno quelli\nChe bevono assetati il loro amore.",
    "Sentía tu respiración sobre mi cabello,\Y me bajaba la sangre hasta el corazón.\nYo cerraba los ojos como hacen aquellos\nQue beben sedientos su propio amor."),
    
   ("Spasimo (Espasmo)",
    "La mano tua premeva le mie spalle,\nIo mi sentivo sciogliere nell'onda.\nNon ho mai visto stelle così gialle,\nCadere nella notte sitibonda.",
    "Tu mano presionaba sobre mis hombros,\nYo me sentía desatarme en la ola.\nNunca he visto estrellas tan amarillas,\nCaer dentro de esa noche sedienta."),
    
   ("Vuoto Rovente (Vacío candente)",
    "Mi hai lasciata bruciante nel silenzio,\nMa il tuo odore è rimasto sul tappeto.\nVoglio strappare questo cupo assenzio,\nE urlare al mondo il nostro buio segreto.",
    "Me has dejado ardiendo en el silencio,\nPero tu olor se ha quedado en la alfombra.\nQuiero arrancar este oscuro ajenjo,\nY gritar al mundo nuestro escondido secreto."),
    
   ("La Cella (La celda)",
    "Questo letto è una cella e io son presa,\nDalle catene immaginarie tue.\nE sto qui, rotta, dalla febbre accesa,\nAd aspettare che torniamo due.",
    "Esta cama es una celda y estoy presa,\nPor las tuyas imaginarias cadenas.\nY me quedo aquí rota, de fiebre encendida,\nA esperar hasta que de nuevo volvamos a ser dos."),
    
   ("Canto d'Attesa (Canto de Espera)",
    "Fioriscono i ciliegi giù nel prato,\nMa nella stanza mia domina il nero.\nGemo se penso al tuo colpo assestato,\nAl tuo corpo violento e lusinghiero.",
    "Florecen los cerezos allá en el prado,\nPero en el cuarto mío domina lo negro.\nGimo si pienso en tu golpe asentado,\nAl cuerpo tuyo y a su fiero choque."),
    
   ("Notturno Privato (Nocturno Privado)",
    "La penombra accarezza la fessura,\nDa cui mi spio il fremito del seno.\nTu l'hai svegliato da questa paura,\nIn un delirio, ansante, senza freno.",
    "La penumbra acaricia mi ranura,\nPor la que me espío el temblor de mi pecho.\nTú lo has despertado de esa pavura,\nEn un delirio ansioso, al fin deshecho."),
    
   ("Innocenza Perduta (Inocencia Perdida)",
    "Dicevano ch'io fossi un giglio bianco,\nOra sono una rosa tutta rossa.\nMi hai stretto tanto forte, mi hai fatto manco,\nE l'anima in ginocchio n'è scossa.",
    "Decían que yo era un lirio todo blanco,\nAhora soy una rosa color rojo fuerte.\nMe has apretado tanto que ya he quedado un banco,\nY el alma de rodillas ahora de aquí no se mueve."),
    
   ("La Gola Arida (Garganta Árida)",
    "Ho sete della tua bava leggera,\nDi quella spinta muta ed infernale.\nQuesta non è più una vita veritiera,\nSenza il rito del nostro carnale.",
    "Tengo sed tuya de la baba ligera,\nDe toda esa empujada que tú llevabas muda e infernal.\nÉsta ya no sigue siendo una vida siquiera,\nSi no hay de ella de nuevo el rito de lo carnal."),
    
   ("Risveglio Brado (Despertar Salvaje)",
    "Stamane ho visto il segno sul mio collo,\nE ho sorriso con volto inumano.\nAppartengo a te, mio aspro satollo,\nAnche se il mondo ti crede lontano.",
    "Esta mañana vi la seña sobre mi gran cuello,\nY entonces sonreí con un rostro inhumano.\nTe pertenezco a ti, fiero y oscuro destello,\nAunque todo el mundo crea que ya estás lejano."),
    
   ("Epitafio per il Desiderio (Para el deseo)",
    "Se morirò schiantata da me stessa,\nSappi che il tuo sudore mi ha uccisa.\nLa fiamma fu troppo accesa e confessa,\nEd ora l'ombra a te mi ha divisa.",
    "Si muriera partida desde mí hasta lo profundo,\nQue sepas que ese tu sudor fue aquí a mí quien me ha matado.\nLa llama era demasiado subida e intensa,\nY la sombra a ti hoy mismo me ha arrebatado.")]),

 ("129","Zinaida Gippius","1869–1945","Rusia","ruso",
  "La gran musa escandalosa e instigadora del simbolismo ruso. Gippius vestía ropa masculina, exploraba la androginia y poseía una sexualidad que intrigaba y horrorizaba a la alta sociedad de San Petersburgo. Sus versos no cantan al amor maternal tradicional, sino a la excitación demoníaca, a los placeres prohibidos del alma y del cuerpo andrógino, tejiendo un erotismo místico oscuro a menudo dirigido tanto a hombres como mujeres.",
  [("Любовь — одна (El amor es uno)",
    "Единый раз вскипает пеной\nИ рассыпается волна.\nНе может сердце жить изменой,\nИзмены нет: любовь — одна.",
    "Una sola vez hierve como espuma\nY se deshace la ola.\nEl corazón no puede vivir de la traición,\nNo hay traición: el amor es uno solo."),
    
   ("Поцелуй (El beso)",
    "О, этот первый, влажный, жгучий!\nОн словно пламя на губах.\nИ каждый член, ослаб, измучен,\nТеряет разум свой и страх.",
    "¡Oh, ese primero, húmedo, ardiente!\nEs como una llama sobre los labios.\nY cada miembro, debilitado y extenuado,\nPierde su razón y todo su miedo."),
    
   ("Андрогин (El andrógino)",
    "Я не мужчина и не дева,\nПлоти сплелися в дикий жгут.\nТы не познаешь слез и гнева,\nКогда губами нас сожгут.",
    "No soy hombre ni soy doncella,\nLas carnes se han trenzado en un salvaje hilo.\nTú no conocerás lágrimas ni cóleras,\nCuando por labios nuestro ardor sea consumido."),
    
   ("Страсть (Pasión)",
    "Как душно в комнате от зноя,\nОт наших сбивчивых речей!\nОтдай мне тело молодое\nВ чаду бессонных этих дней.",
    "¡Qué sofocante es el calor en la alcoba,\nProveniente de nuestros atropellados discursos!\nEntrégame a mí todo tu cuerpo joven\nEn el delirio de estos desvelados días."),
    
   ("Темный грех (El pecado oscuro)",
    "Нам сладок грех, что скрыт от света,\nВ тени бархатных портьер.\nДуша покорна, недопета,\nИ мы вступаем за барьер.",
    "Nos es dulce el pecado, oculto a la luz,\nEn la sombra de los telones de terciopelo.\nEl alma dócil, aún sin terminar de cantarse,\nY cruzamos, así, todas las barreras."),
    
   ("Огни (Fuegos)",
    "В твоих зрачках — костры и угли,\nИ руки тянутся в ночи.\nМы напряглись и разом стухли,\nКак обгоревшие мечи.",
    "En tus pupilas — hay ascuas y tizones,\nY las manos se extienden en la noche profunda.\nNos tensamos y al unísono nos exhalamos,\nExactamente igual que si fuéramos espadas quemadas."),
    
   ("Жажда (Sed)",
    "Твоих волос густая бездна,\nТвоя пылающая грудь...\nИ эта ночь для нас полезна,\nЧтоб в наслажденьи утонуть.",
    "En la abisal y espesa negrura de tus trenzas,\nY tu siempre ardiente palpitante pecho...\nLa noche hoy para nosotros ha sido de lo más provechosa,\nPara que en el placer nos hayamos ahogado enteros."),
    
   ("Тайна ложа (El secreto del lecho)",
    "Смята постель в испуге страстном,\nВздохи застыли на губах.\nВ этом безумии опасном\nСгинул безвинный прежний страх.",
    "Está arrugada y revuelta nuestra cama por miedo pasional,\nLos suspiros que teníamos se congelaron sobre la boca.\nEn esta nuestra locura inminente y peliaguda\nHa naufragado al fin nuestro miedo original."),
    
   ("Змея (La Serpiente)",
    "Скольжу, не зная, где граница\nТвоих изогнутых колен.\nЯ — древняя жрица-блудница,\nБерущая мужчину в плен.",
    "Me deslizo, sin saber, donde acaba justo toda linde\nDe tus retorcidas muslos en las rodillas.\nYo soy — una de verdad arcana ramera curandera,\nQue se cobra enteros con ella a sus grandes hombres."),
    
   ("Смерть в любви (Muerte en el amo)",
    "Задуши меня нежностью жесткой,\nРаствори мою волю до дна.\nЯ покроюсь кровавой полоской,\nВедь безумной любви предана.",
    "Ahógame un poco con rudezas oscuras blandas,\nDisuélveme mi control con gran constancia.\nYo me voy cubriendo de heridas rojizas muy intensas,\nPues a toda esta locura amorosa estoy entregada.")]),

 ("130","Mirra Lokhvitskaya","1869–1905","Rusia","ruso",
  "Conocida comúnmente como 'la Safo rusa', Mirra desafió a la conservadora aristocracia zarista dedicando por primera vez poemarios completos y exitosos de mujeres al placer y exaltación embriagadora del deseo carnal humano. Sus libros están repletos de besos y ardientes espasmos que anticipaban a un torrencial feminismo poético extático.",
  [("Песнь любви (Canto de amor)",
    "Я хочу быть с тобой, я хочу твоих поцелуев!\nДай мне припасть к твоей жаркой груди.\nВ этом мире мы словно в бурю танцуем,\nНичего не страшась впереди.",
    "¡Yo quiero estar aquí junto a ti, ansío mucho tus picos!\nDéjame siempre arrojarme hacia el fiero fervor de tu calor.\nCasi que estamos en este inmenso mundo danzando en tormentos,\nInconscientes de que lo peor ya viene todo en el exterior."),
    
   ("Огонь и ночь (Fuego y noche)",
    "Узоры теней на нашей постели\nТанцуют безумный и радостный танец.\nМы в этой ночи до конца догорели,\nРазвеяв по ветру стыдливый румянец.",
    "Los perfiles sobre la penumbra en todo el sitio de la posada\nDanzan como un demente de gran manera con la alborada.\nAquí con nosotros dentro de la madrugada se han ido desatando grandes fuegos,\nLlevándose bien lejos toda nuestra timidez hacia mil juegos."),
    
   ("Властные губы (Labios imperiosos)",
    "Твои губы горят и тревожат,\nЯ сдаюсь под их натиском смелым.\nНичего мне на свете дороже,\nЧем сливаться с твоим смуглым телом.",
    "Tus labios que arden siempre e inquietan un poco mi cabeza,\nYo misma cedo totalmente bajo ese empuje que se avecina.\nOye pues sí que no tengo en vida mejor ninguna extraña simpleza,\nQue tener que desvanecer en tu propia silueta purpurina."),
    
   ("В объятиях (En brazos)",
    "Задохнувшись от близости душной,\nЯ теряю контроль над собой.\nЯ была неприступной, послушной,\nА теперь я лишь раб пред тобой.",
    "Ahogándome bien un ratito al verte venir sintiendo ahogo,\nMe empiezo a desmayar todo el centro si bien que te miro.\nAntes yo no tenía ninguna entrada y que era recatada,\nY tú mira cómo me sacaste como me ha devorado un vampiro."),
    
   ("Цветы желания (Flores del deseo)",
    "Расцвели орхидеи порока\nНа моих раскаленных устах.\nЯ люблю тебя страстно, жестоко,\nЗабывая и гордость, и страх.",
    "Empezaron ya a brotar orquídeas con desmesuras,\nSobre estas bocas de lo más tórridas sin cura.\nOh Dios cómo se nota lo que encierran las más fieras locuras,\nAl ver que yo supe cómo arroje para atrás todas las viejas amarguras."),
    
   ("Кровь кипит (La sangre hierve)",
    "О, как бьется вена на шее,\nКогда ты прижимаешь меня...\nС каждой лаской я только смелее,\nИ безумней от жажды огня.",
    "Toma ya fíjate de notar qué rápido se salta una arteria por mi cuello,\nCuando tú siempre tiendes a llevarme junto al abrazo destello...\nA partir de un nuevo roce me suelto cada día con lo arrojado en atrevidas,\nY más ida que nada esperando tener las hambres que siempre van unidas."),
    
   ("Твой след (Tu rastro)",
    "Ты ушел, но следы от укусов\nУкрашают, как звёзды, плечо.\nЯ презрела законы для трусов,\nМне с тобою всегда горячо.",
    "Te piraste ya y mira en qué me dejaste los cortes a lo largo de un pecho,\nQue adornaban como lo que parecen unos tajazos los cuales que has hecho.\nHe arremetido las más viejas moralinas con tal de un gran derecho,\nPorque yo contigo ardí muy quemantemente hasta casi subir el techo."),
    
   ("Вопли восторга (Gritos de asombro)",
    "Пусть соседи стучат в наши стены,\nЯ не в силах сдержать громкий стон.\nО, какие блаженные плены!\nПотрясает меня этот сон.",
    "Y que piquen los pesados desde la pared de en frente,\nNo soy yo una capaz a estar conteniendo toda mi bulla en la boca silente.\n¡Toma con mi éxtasis y todas estas las pesadumbres que llevo latentes!\nEs la locura misma que tengo yo hasta estar con esta pesadilla reincidente."),
    
   ("Жгучий плен (Prisión ardiente)",
    "Мы связали друг друга руками,\nКак узлом непокорных страстей.\nВ этот миг ты мне стал небесами,\nПовелителем жизни моей.",
    "Ya nos habíamos trabado mutuamente sin casi darnos la cuenta de las garras,\nComo apretones que a mí todo este impulso se me vino a dar al cinto en amarras.\nDentro de todos tus desvarios he sabido tener la gloria de tus altas barras,\nAmo absoluto te me has hecho y la propia vida sí que se desgarra."),
    
   ("Пенный вал (Ola de espuma)",
    "Будто бросилась в море сверкая,\nОбдала меня пеной волна.\nУмираю, тебя обнимая,\nУтонув в поцелуях до дна.",
    "Es como un ahogo donde lo que tuve parecía dar con mi chapuzón muy lejos,\nDe espuma rebotada desde mis entrañas hasta en los destellos y hasta lo oscuro.\nEchar de cabeza hacia atrás apretándote si por todo esto yo a ti te apuro,\nAhogándome desde lo gordo por besuqueos siempre ya desde un principio en el apuro.")])
]

if __name__ == "__main__":
    for item in CORRECCIONES:
        mk(*item)
