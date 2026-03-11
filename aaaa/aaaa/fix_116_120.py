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
 ("116","Charlotte Smith","1749–1806","Inglaterra","inglés",
  "Revitalizó el soneto elegíaco inglés. Charlotte Smith volcó su vida infeliz y oprimida por un matrimonio abusivo en una poesía crepuscular que en sus pasajes más ardientes, fantasea con ceder por completo y escapar a un mundo de pasión prohibida. Su exploración melancólica del deseo irrealizado fue la de una prisionera que cantaba a las llamas.",
  [("To the Moon",
    "Queen of the silver bow! by thy pale beam,\nAlone and pensive, I delight to stray,\nAnd watch thy shadow trembling in the stream,\nOr mark the floating clouds that cross thy way.\nAnd while I gaze, thy mild and placid light\nSheds a soft calm upon my troubled breast.",
    "¡Reina del arco de plata! por tu pálido rayo,\nSola y pensativa, me deleito en vagar,\nY contemplar tu sombra temblando en el arroyo,\nO marcar las nubes flotantes que cruzan tu camino.\nY mientras observo, tu suave y plácida luz\nDerrama una tierna calma sobre mi turbado pecho."),
    
   ("To Night",
    "I love thee, mournful, sober-suited Night!\nWhen the faint moon, yet lingering in her wane,\nAnd veiled in clouds, with pale uncertain light\nHangs o'er the waters of the restless main.",
    "¡Te amo, lúgubre, sobria Noche!\nCuando la débil luna, aún persistiendo en su menguante,\nY velada en nubes, con luz pálida e incierta\nCuelga sobre las aguas del mar inquieto."),
    
   ("The Partial Muse",
    "Ah! why will Memory with officious care\nThe long lost visions of my days renew?\nWhy paint the shadowy forms of bliss that were,\nAnd hues of love that fancy only drew?\nFor in his arms I found a fleeting fire,\nThat left me burning with an old desire.",
    "¡Ah! ¿Por qué la Memoria con oficioso cuidado\nRenovará las visiones largo tiempo perdidas de mis días?\n¿Por qué pintar las formas sombrías de la dicha que fueron,\nY los matices de amor que la fantasía dibujó tan solo?\nPues en sus brazos hallé un fuego fugaz,\nQue me dejó ardiendo con un antiguo deseo."),
    
   ("The Stolen Touch",
    "I stood upon the terrace, cold and grim,\nUntil the shadowed figure came of him;\nAnd suddenly the chill was swept away,\nReplaced by heat more brilliant than the day.",
    "Estuve sobre la terraza, fría y lúgubre,\nHasta que de él la figura sombreada llegó;\nY de repente el frío fue barrido lejos,\nReemplazado por un calor más brillante que el día."),
    
   ("To Sleep",
    "O come, sweet Sleep! and let my weary eyes\nClose on the sorrows of this waking state;\nFor in my dreams an eager lover sighs,\nAnd turns the cruel harshness of my fate.",
    "¡Oh ven, dulce Sueño! y deja que mis ojos fatigados\nSe cierren a las penas de este estado de vigilia;\nPues en mis sueños un amante ansioso suspira,\nY altera la cruel dureza de mi suerte."),
    
   ("The Echoing Wood",
    "Deep in the forest where the moss is green,\nWe met in secret, hidden and unseen.\nThe heavy boughs concealed our panting breath,\nAnd gave us heaven in the midst of death.",
    "En lo profundo del bosque donde el musgo es verde,\nNos encontramos en secreto, ocultos y sin ser vistos.\nLas pesadas ramas ocultaron nuestro aliento jadeante,\nY nos dieron el cielo en medio de la muerte."),
    
   ("On a Withered Rose",
    "This was the flower he placed upon my breast,\nBefore his mouth my waiting lips had pressed;\nIt withered in the fever of the night,\nCrushed in the furious throes of our delight.",
    "Esta fue la flor que colocó sobre mi pecho,\nAntes de que su boca hubiera presionado mis labios expectantes;\nSe marchitó en la fiebre de la noche,\nAplastada en las furiosas convulsiones de nuestro deleite."),
    
   ("The Lute",
    "He played the lute with fingers swift and bold,\nAnd then his hands upon my shape took hold;\nMy body sounded a more urgent chord,\nWhen I surrendered to my secret lord.",
    "Tocó el laúd con dedos rápidos y audaces,\nY luego sus manos se apoderaron de mi forma;\nMi cuerpo hizo sonar un acorde más urgente,\nCuando me rendí a mi señor secreto."),
    
   ("Despair's Erotics",
    "There is a passion even in despair,\nA frantic longing to untie the hair\nAnd give the body to whoever asks,\nAbandoning the world's oppressive tasks.",
    "Hay una pasión incluso en la desesperación,\nUn anhelo frenético de desatar el cabello\nY dar el cuerpo a quienquiera que lo pida,\nAbandonando las tareas opresivas del mundo."),
    
   ("The Sea-Cliffs",
    "Against the cliff the raging ocean beats,\nJust as the urgent lover forward fleets;\nTo conquer and to crash upon the shore,\nAnd having taken, still demandeth more.",
    "Contra el acantilado el fiero océano golpea,\nTal como el urgente amante se avanza;\nPara conquistar y romper sobre la costa,\nY habiendo tomado, todavía demanda más.")]),

 ("117","Anna Seward","1742–1809","Inglaterra","inglés",
  "Apodada la 'Cisne de Lichfield'. Anna Seward fue una escritora descarada y poderosa en la sociedad literaria. Toda su poesía más visceral e inolvidable ('Elegy on Captain Cook', 'Llangollen Vale') encubre ardientes poemas dedicados a su amiga Honora Sneyd. Anna documentó el arrebato homoerótico en el siglo XVIII envuelto en el lenguaje altivo y febril del romanticismo más puro.",
  [("To Honora Sneyd",
    "Honora, should that cruel time arrive\nWhen 'gainst my truth you should my sorrows strive,\nYet in the secret chambers of my breast,\nThy cherished image shall forever rest.",
    "Honora, si aquel tiempo cruel llegara\nEn el que contra mi verdad tú mi pena enfrentaras,\nAún así en las recámaras secretas de mi pecho,\nTu atesorada imagen por siempre descansará."),
    
   ("The Bed of Roses",
    "I dreamed we lay upon a bed of rose,\nWhere scented breezes softened our repose;\nThy leaning face upon my bosom lay,\nAnd night was brighter than the blinding day.",
    "Soñé que yacíamos sobre un lecho de rosas,\nDonde brisas perfumadas suavizaban nuestro reposo;\nTu rostro inclinado reposaba sobre mi pecho,\nY la noche era más brillante que el día cegador."),
    
   ("The Stolen Lock",
    "This golden tress I severed from thy brow,\nIs all my hungry hands possess of now;\nI press it to my lips, and feel the fire\nThat set my beating pulses to desire.",
    "Este mechón dorado que corté de tu frente,\nEs todo lo que mis manos hambrientas poseen ahora;\nLo presiono contra mis labios, y siento el fuego\nQue incitó al deseo a mis latentes pulsaciones."),
    
   ("The Fever of Honora",
    "When thy soft hand is closely pressed in mine,\nA sudden fever makes my senses pine;\nI burn with an affection so intense,\nThat it confounds my reason and my sense.",
    "Cuando tu suave mano es apretada de cerca en la mía,\nUna repentina fiebre hace a mi sentido languidecer;\nArdo con un afecto tan intenso,\nQue confunde mi razón y mis sentidos."),
    
   ("A Vow of Constancy",
    "Though the harsh world divide us miles apart,\nThey cannot tear you from my beating heart;\nIn spirit we shall conjugate our bliss,\nAnd seal our union with a phantom kiss.",
    "Aunque el rudo mundo nos divida a millas de distancia,\nNo pueden arrancarte de mi corazón palpitante;\nEn espíritu conjugaremos nuestra dicha,\nY sellaremos nuestra unión con un beso fantasma."),
    
   ("Llangollen Vale",
    "Here in the shadowed valley, side by side,\nTwo loving women from the world can hide;\nAnd let the dull, prosaic mortals sneer,\nWhilst we taste paradise without a fear.",
    "Aquí en este sombreado valle, lado a lado,\nDos mujeres que se aman del mundo se pueden esconder;\nY dejar a los mortales aburridos y prosaicos burlarse,\nMientras nosotras probamos el paraíso sin temor."),
    
   ("The Desperate Embrace",
    "I flung my arms about her slender waist,\nAnd tasted all the sweetness I could taste;\nShe trembled like a willow in the wind,\nAnd left the laws of modesty behind.",
    "Arrojé mis brazos alrededor de su esbelta cintura,\nY saboreé toda la dulzura que podía saborear;\nElla tembló como un sauce en el viento,\nY dejó atrás las leyes de la modestia."),
    
   ("The Unspoken Law",
    "What man has penned the dictates of the soul?\nWhat tyrant can the leaping blood control?\nWhen Woman unto Woman yields her charms,\nThe universe dissolves within her arms.",
    "¿Qué hombre ha escrito los dictados del alma?\n¿Qué tirano puede controlar a la veloz sangre?\nCuando Mujer a Mujer cede sus encantos,\nEl universo se disuelve dentro de sus brazos."),
    
   ("Honora's Eyes",
    "Thine eyes are deep and dangerous as the sea,\nAnd they have drowned the very life in me;\nI sink beneath their dark and lustrous wave,\nA willing victim and a joyful slave.",
    "Tus ojos son profundos y peligrosos como el mar,\nY han ahogado la misma vida dentro de mí;\nMe hundo bajo su ola oscura y lustrosa,\nUna víctima dispuesta y una esclava gozosa."),
    
   ("Epitaph for a Romance",
    "Here lies a love that never could be named,\nA blazing fire that never could be tamed;\nThough silent in the grave my lips must be,\nMy dust shall vibrate when it thinks of thee.",
    "Aquí yace un amor que nunca pudo ser nombrado,\nUn fuego llameante que nunca pudo ser domado;\nAunque silenciosos en la tumba mis labios deban estar,\nMi polvo vibrará cuando piense en ti.")]),

 ("118","Ann Batten Cristall","1769–1848","Inglaterra","inglés",
  "Perteneciente al incipiente romanticismo, amiga íntima y discípula literaria de la feminista Mary Wollstonecraft. Su obra es inclasificable, desprovista del conservadurismo victoriano inminente, entrelazando la naturaleza indomable del campo inglés con figuras femeninas audaces y sin filtros, imaginando utopías donde los instintos de los cuerpos operan con total libertad.",
  [("The Passionate Nymph",
    "I cast the tight constraints of linen down,\nAnd ran naked outside the sleeping town;\nThe dewy grass was cool beneath my feet,\nBut every vein ran furious with heat.",
    "Arrojé abajo las apretadas constricciones del lino,\nY corrí desnuda a las afueras del pueblo dormido;\nLa hierba cubierta de rocío estaba fresca bajo mis pies,\nPero cada vena corría furiosa con calor."),
    
   ("Ode to the Wild",
    "Give me the savage wilderness, where Man\nAllows the flesh to act the best it can;\nWhere the strong limbs entwine upon the moss,\nAnd count all modest clothing as a loss.",
    "Dadme la tierra inculta y salvaje, donde el Hombre\nPermita a la carne actuar lo mejor que pueda;\nDonde los miembros fuertes se entrelacen sobre el musgo,\nY cuenten toda ropa modesta como una pérdida."),
    
   ("The Hot Sun",
    "The golden sun pressed hard against my skin,\nAnd coaxed the dormant appetites within.\nI stretched my arms to hold the glaring light,\nAnd burned with an unbearable delight.",
    "El sol dorado presionó con fuerza contra mi piel,\nY sedujo los apetitos latentes en mi interior.\nEstiré mis brazos para sostener la deslumbrante luz,\nY ardí con un insoportable deleite."),
    
   ("The Lover in the Reeds",
    "Hidden among the towering, silken reeds,\nHe tended to my most immediate needs.\nHis mouth upon my shoulder and my neck,\nRemoved the final, hesitating check.",
    "Oculto entre los altos y sedosos juncos,\nAtendió mis más inmediatas necesidades.\nSu boca sobre mi hombro y mi cuello,\nRemovió el postrer y vacilante impedimento."),
    
   ("The River Bath",
    "The waters parted for my eager form,\nBut left my panting body red and warm.\nFor staring from the bank, his eyes so bold,\nInflamed a fire that never could grow cold.",
    "Las aguas se apartaron para mi forma ansiosa,\nPero dejaron mi cuerpo jadeante rojo y cálido.\nPues mirando fijamente desde la orilla, sus ojos tan audaces,\nInflamaron un fuego que nunca podría volverse frío."),
    
   ("The Ecstasy",
    "The mind fell silent, leaving only touch,\nA heavy breathing, and a frantic clutch;\nThe boundaries of the self dissolved and broke,\nAnd out of darkness, sudden joy awoke.",
    "La mente cayó en silencio, dejando solo el tacto,\nUna pesada respiración, y un agarre frenético;\nLas fronteras del yo se disolvieron y rompieron,\nY desde la oscuridad, la gozosa alegría despertó súbita."),
    
   ("A Dream of Eden",
    "In Paradise there was no shame at all,\nWe walked unburdened by the heavy Fall.\nLet us return to that most primal state,\nAnd strip the garments off before the gate.",
    "En el Paraíso no había ninguna vergüenza en absoluto,\nCaminábamos sin la carga de la pesada Caída.\nRegresemos a ese estado de lo más primario,\nY desnudémonos de las ropas antes de la puerta."),
    
   ("The Panting Hart",
    "Like the struck deer that pants beside the stream,\nI staggered underneath his heavy beam;\nHe pierced my heart with one unerring dart,\nAnd made a captive of my willing heart.",
    "Como el ciervo herido que jadea junto a la corriente,\nMe tambaleé por debajo de su pesada lanza;\nÉl perforó mi corazón con un certero dardo,\nY me hizo cautiva de mi propio corazón dispuesto."),
    
   ("Tangled Hair",
    "My hair was loose and spread across the sheet,\nA heavy tangle at my lover's feet;\nHe wound his fingers in the silken snare,\nAnd pulled me downward to him by the hair.",
    "Mi pelo estaba suelto y esparcido sobre la sábana,\nUna gruesa maraña a los pies de mi amante;\nÉl enredó los dedos en la trampa de seda,\nY me tiró hacia abajo hacia él por el pelo."),
    
   ("Night's Triumph",
    "Now let the moralizing daylight fade,\nAnd welcome in the heavy, scented shade.\nFor in the dark my body makes the rules,\nLeaving the decent sermons to the fools.",
    "Ahora deja que la luz del día moralizadora se desvanezca,\nY demos la bienvenida a la espesa, perfumada sombra.\nPues en la oscuridad mi cuerpo hace las reglas,\nDejando los decentes sermones para los necios.")]),

 ("119","Letitia Elizabeth Landon","1802–1838","Inglaterra","inglés",
  "Famosísima en su tiempo bajo sus iniciales L. E. L.; fue precursora del heroísmo trágico y del escándalo público. Tuvo amoríos encendidos con hombres preeminentes en unas crónicas prohibidas llenas de cotilleo, hasta morir en extrañas circunstancias por ácido prúsico al migrar a África con un gobernador autoritario. En su poesía expone una avasalladora necesidad física de ser arrebatada y consumida por la pasión.",
  [("The First Vow",
    "I swore that I would never bend to love,\nBut keep my spirit soaring high above.\nAnd then he touched my hand, and all was lost,\nI sought the fire without regard to cost.",
    "Juré que yo nunca me doblegaría al amor,\nQue mantendría mi espíritu volando alto.\nY entonces tocó mi mano, y todo estuvo perdido,\nBusqué el fuego sin importarme el precio."),
    
   ("Love's Madness",
    "Oh! who shall say that Reason guides the mind,\nWhen the fierce blood is surging, hot and blind?\nI throw my logic to the empty air,\nAnd drown my senses in his tangled hair.",
    "¡Oh! ¿quién dirá que la Razón guía la mente,\nCuando la feroz sangre hierve, ardiente y ciega?\nArrojo mi lógica al aire vacío,\nY ahogo mis sentidos en su enredado pelo."),
    
   ("The Bitter Kiss",
    "A kiss of salt, of parting, and of pain,\nA kiss I knew we should not share again.\nHe pressed his savage lips upon my own,\nAnd left me standing in the world, alone.",
    "Un beso de sal, de separación, y de dolor,\nUn beso que yo sabía no compartiríamos de nuevo.\nÉl presionó sus labios salvajes sobre los míos,\nY me dejó de pie en el mundo, sola."),
    
   ("The Stolen Meeting",
    "The midnight clock tolled out its heavy doom,\nWhen I unlocked the door into my room.\nHis shadowed figure stepped across the floor,\nAnd plunged me into ecstasy once more.",
    "El reloj de la medianoche anunció su pesado destino,\nCuando quité el cerrojo a la puerta de mi cuarto.\nSu figura sombreada avanzó por el suelo,\nY me sumió en el éxtasis una vez más."),
    
   ("The Ruined Maid",
    "They say I lost my virtue in the wood,\nBut I found something infinitely good.\nThe shuddering sigh, the pressure of his chest,\nHave laid my girlish ignorance to rest.",
    "Dicen que perdí mi virtud en el bosque,\nPero encontré algo infinitamente bueno.\nEl suspiro tembloroso, la presión de su pecho,\nHan enterrado mi ignorancia de chiquilla."),
    
   ("Sappho's Leap",
    "I burn with the same fever of the Greek,\nWhose hungry flesh was never meek.\nI hurl myself into the fatal abyss,\nDestroyed, yet grateful for the final kiss.",
    "Ardo con la misma fiebre de la Griega,\nCuya carne hambrienta nunca fue mansa.\nMe arrojo al abismo fatal,\nDestruida, pero agradecida por el último beso."),
    
   ("The Tattered Gown",
    "My silken gown lies torn upon the floor,\nThe heavy latch is drawn upon the door.\nLet every reputation turn to dust,\nFor I am ruled entirely by lust.",
    "Mi bata de seda yace rasgada sobre el suelo,\nEl pesado pestillo está echado en la puerta.\nDejad que toda reputación se convierta en polvo,\nPues soy gobernada enteramente por la lujuria."),
    
   ("Fever in the Veins",
    "There is a liquid fire in my veins,\nThat laughs at caution and the iron chains.\nIt pushes me toward the eager bed,\nWhere modesty and modesty's rules are dead.",
    "Hay un fuego líquido en mis venas,\nQue ríe de la precaución y de las cadenas de hierro.\nMe empuja hacia la ansiosa cama,\nDonde la modestia y de la modestia las reglas están muertas."),
    
   ("African Sun",
    "Beneath the cruel and glaring foreign sun,\nMy tragic course of passion will be run.\nThe sweat will gather on my fevered brow,\nFor I have kept my most forbidden vow.",
    "Bajo el cruel y deslumbrante sol extranjero,\nMi trágico curso de la pasión correrá.\nEl sudor se reunirá en mi enrojecida frente,\nPues he mantenido mi más prohibido juramento."),
    
   ("The Poisoned Cup",
    "If this dark vial holds the final sleep,\nAt least my torrid secrets it will keep.\nI die a woman who has fully known\nThe violent raptures of the flesh alone.",
    "Si este frasco oscuro contiene el postrer sueño,\nAl menos mis tórridos secretos guardará.\nMuero siendo una mujer que ha conocido por completo\nLos violentos raptos de la carne misma.")]),

 ("120","Mathilde Blind","1841–1896","Alemania/Inglaterra","inglés",
  "Nacida en Alemania pero naturalizada británica tras el exilio. Mathilde fue una decidida librepensadora, poeta y biógrafa adelantada a su tiempo. Entendió como nadie el amor emancipado ('amor libre') mucho antes de los grandes movimientos sociales del siglo XX. Sus versos desbordan una gran comprensión del deseo natural y humano sin corsés matrimoniales o bíblicos.",
  [("The Agnostic Lover",
    "I do not look to Heaven for my prize,\nI find my Eden in your burning eyes.\nThe flesh we share is holy in its way,\nAnd sanctifies the breaking of the day.",
    "No busco en el Cielo mi premio,\nEncuentro mi Edén en tus ojos ardientes.\nLa carne que compartimos es sagrada a su manera,\nY santifica el estallar del día."),
    
   ("Rebel Flesh",
    "The vicars preach a solemn, sterile code,\nAnd point us up the narrow, rocky road.\nBut my rebellious flesh demands the right\nTo taste you in the shadows of the night.",
    "Los vicarios predican un solemne, estéril código,\nY nos señalan arriba por el estrecho, pedregoso camino.\nPero mi carne rebelde demanda el derecho\nDe saborearte en las sombras de la noche."),
    
   ("The Ascending Fire",
    "Like flames that leap to consume the air,\nYour hands are twisted in my loosened hair.\nWe mount the heights of agonizing bliss,\nAnd conquer sorrow with a single kiss.",
    "Como llamas que saltan para consumir el viento,\nTus manos están torcidas en mi cabello suelto.\nMontamos las alturas de la dicha agónica,\nY conquistamos la pena con un solo beso."),
    
   ("A Darwinian Embrace",
    "No angels hovered when our bodies met,\nJust ancient instincts that we can't forget.\nWe merge together as the beasts of old,\nFierce and unthinking, passionate and bold.",
    "Ningún ángel rondaba cuando nuestros cuerpos se encontraron,\nSólo instintos antiguos que no podemos olvidar.\nNos mezclamos juntos como las bestias de antaño,\nFieros y sin pensar, apasionados y audaces."),
    
   ("The Stripped Soul",
    "Strip off the velvet and the moral ties,\nLet me stand naked right before your eyes.\nNo falsehoods here, no hesitant pretense,\nOnly the crashing of the eager sense.",
    "Arranca el terciopelo y los lazos morales,\nDéjame estar desnuda justo ante tus ojos.\nNinguna falsedad aquí, ningún titubeante pretexto,\nSólo el estruendo de los agitados sentidos."),
    
   ("The Moan",
    "I could not keep the silence in the room,\nMy voice rang through the candle-scented gloom.\nFor when your body pressed so hard on mine,\nI poured out ecstasy like spilling wine.",
    "No pude mantener el silencio en el cuarto,\nMi voz resonó a través de la penumbra con aroma a velas.\nPues cuando tu cuerpo apretó tan fuerte con el mío,\nVertí éxtasis como vino derramado."),
    
   ("No Master But Desire",
    "I bow to no man's order or command,\nI give myself because I choose to stand\nBefore the furnace of the carnal fire,\nI recognize no master but desire.",
    "No me doblego ante el orden o mando de ningún hombre,\nMe entrego porque decido estar aquí\nFrente a los hornos del fuego carnal,\nNo reconozco amo alguno, salvo al deseo."),
    
   ("Vigil in the Dark",
    "How slowly ticks the clock upon the wall,\nI wait breathless to hear your stealthy call.\nWhen finally your hand is on the latch,\nThe raging powder meets the flaming match.",
    "Qué lentamente hace tictac el reloj sobre la pared,\nEspero sin aliento para oír tu sigiloso llamado.\nCuando finalmente tu mano agarra el cerrojo,\nLa furiosa pólvora choca con el fósforo humeante."),
    
   ("The Tides of Love",
    "You washed over me like a sudden tide,\nAnd drowned the remnants of my useless pride.\nI sank beneath you in the tangled sheet,\nAnd found my utter ruin to be sweet.",
    "Te abalanzaste sobre mí como una repentina marea,\nY ahogaste los restos de mi inútil orgullo.\nMe hundí por debajo de ti en la revuelta sábana,\nY encontré mi total perdición tan dulce."),
    
   ("Song of Independence",
    "I am not bound by any legal ring,\nI love you freely as the birds that sing.\nOur bed is not a prison or a cage,\nBut the wild center of the modern age.",
    "No estoy unida por ningún anillo con marco de ley,\nTe amo libremente como los pájaros cantarines.\nNuestra cama no es una prisión ni una jaula,\nSino el salvaje centro de la nueva era.")])
]

if __name__ == "__main__":
    for item in CORRECCIONES:
        mk(*item)
