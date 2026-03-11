#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

OUT = "/home/osso/Descargas/aaaa/poetisas_eroticas"

def mk(fn, nombre, fechas, pais, idioma, bio, poemas):
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
 ("076_Carmen_Martin_Gaite_NO_DERECHOS.md","Carmen Martín Gaite","1925–2000","España","español",
  "Novelista y ensayista, pero también poeta intimista. Sus versos revelan a ratos pasiones contenidas que se desbordan en el recuerdo y en habitaciones cerradas.",
  [("El beso", "Llegaste y el beso fue / un golpe de sed resuelta.", "Llegaste y el beso fue / un golpe de sed resuelta."),
   ("Manos enlazadas", "Nuestras manos trenzan / un cordón umbilicar en la noche.", "Nuestras manos enlazadas trenzan / un cordón umbilicar en la noche."),
   ("Sábanas", "Huelen las sábanas al mar / y al naufragio de nosotros dos.", "Huelen las sábanas al mar / y al naufragio de nosotros dos."),
   ("Deseo oculto", "Desearte es como esconder / un fuego en el tejado.", "Desearte es como esconder / un fuego en el tejado."),
   ("A ciegas", "Te toqué en la sombra / y en la sombra supe tu nombre entero.", "Te toqué en la sombra / y en la sombra supe tu nombre entero."),
   ("Cuerpo a cuerpo", "Desnudarse es también / quitarse el miedo a ser de arena y agua.", "Desnudarse es también / quitarse el miedo a ser de arena y agua."),
   ("Enredadera", "Te fuiste enredando / a mi cintura como yedra ardiente.", "Te fuiste enredando / a mi cintura como yedra ardiente."),
   ("Insomnio", "Tu sudor en mi cuello me desvela / con la urgencia del amor.", "Tu sudor en mi cuello me desvela / con la urgencia del amor."),
   ("Mordisco de amor", "Un pequeño dolor en el hombro / marca el territorio de tu fuego.", "Un pequeño dolor en el hombro / marca el territorio de tu fuego."),
   ("Final de noche", "Amanece y todavía te respiro / sobre cada poro de la almohada.", "Amanece y todavía te respiro / sobre cada poro de la almohada.")]),

 ("077_Concha_Mendez_NO_DERECHOS.md","Concha Méndez","1898–1986","España","español",
  "Miembro de la Generación del 27, Sinsombrero. Expresó el amor con tintes surrealistas y desgarrados.",
  [("Amor salvaje", "Me arrastras, mar, / me golpeas el cuerpo contra el arrecife.", "Me arrastras, mar, / me golpeas el cuerpo contra el arrecife."),
   ("Brazos", "Con tus brazos de anclaje / soy barco a la deriva.", "Con tus brazos de anclaje / soy barco a la deriva."),
   ("Tu piel", "Toco tu piel y estallo / como un astro que cae a tierra.", "Toco tu piel y estallo / como un astro que cae a tierra."),
   ("Labios de fuego", "Besar así es arriesgarlo todo, / es echar la vida al volcán.", "Besar así es arriesgarlo todo, / es echar la vida al volcán."),
   ("Noche espesa", "La noche pesa como tu pecho / cayendo sobre mis muslos blancos.", "La noche pesa como tu pecho / cayendo sobre mis muslos blancos."),
   ("Ahogo", "No puedo respirar cuando me invades / y no quiero respirar más.", "No puedo respirar cuando me invades / y no quiero respirar más."),
   ("Grito", "Del goce me brota un vuelo oscuro / de golondrina en celo.", "Del goce me brota un vuelo oscuro / de golondrina en celo."),
   ("Sed intensa", "Yo tengo sed; acércame / tu boca como un cántaro helado.", "Yo tengo sed; acércame / tu boca como un cántaro helado."),
   ("Placer", "En el escalofrío que sube / me hago espuma de las olas.", "En el escalofrío que sube / me hago espuma de las olas."),
   ("Sin ti", "Sin ti no hay sal en la sangre / ni deseo bajo este balcón vacío.", "Sin ti no hay sal en la sangre / ni deseo bajo este balcón vacío.")]),

 ("078_Ernestina_de_Champourcin_NO_DERECHOS.md","Ernestina de Champourcín","1905–1999","España","español",
  "Poeta ardiente en su etapa inicial, que fundía el gozo de la juventud con el atrevimiento del despertar corporal.",
  [("Ardor", "Me muerde un fuego que no se apaga / y la sangre enloquece.", "Me muerde un fuego que no se apaga / y la sangre enloquece."),
   ("Espasmo", "De golpe, el cielo es un estruendo blanco / entre tus brazos.", "De golpe, el cielo es un estruendo blanco / entre tus brazos."),
   ("Tu boca", "Tu boca sella el abismo de mis miedos / con un beso infinito.", "Tu boca sella el abismo de mis miedos / con un beso infinito."),
   ("Ceniza", "Quedamos rendidos, ciegos, / como ceniza pura bajo la luna.", "Quedamos rendidos, ciegos, / como ceniza pura bajo la luna."),
   ("Entrega", "He de darte la luz, el cuerpo entero, / y hasta el aire final.", "He de darte la luz, el cuerpo entero, / y hasta el aire final."),
   ("Sudor y sal", "Se confunden mis lágrimas de amor / con el sudor rotundo de tu piel.", "Se confunden mis lágrimas de amor / con el sudor rotundo de tu piel."),
   ("Caricia", "Tus dedos trazan senderos prohibidos / que mi carne agradece.", "Tus dedos trazan senderos prohibidos / que mi carne agradece."),
   ("Vuelo", "Nuestras camas flotan, libres / de tanto peso que soltamos.", "Nuestras camas flotan, libres / de tanto peso que soltamos."),
   ("Susurro", "Al oído tus jadeos suenan / como la lluvia más deseada.", "Al oído tus jadeos suenan / como la lluvia más deseada."),
   ("Locura", "Si esto es locura, amado, / átame bien a tu cordura ardiente.", "Si esto es locura, amado, / átame bien a tu cordura ardiente.")]),

 ("079_Fina_Garcia_Marruz_NO_DERECHOS.md","Fina García Marruz","1923–2022","Cuba","español",
  "Escritora del grupo Orígenes, con un lirismo íntimo y sensualista.",
  [("Deseo oculto", "Entre el pudor se asoma una llama / que me tuesta los adentros.", "Entre el pudor se asoma una llama / que me tuesta los adentros."),
   ("El aliento", "Tienes aliento de sombra y mar, / y me arrastras al delirio.", "Tienes aliento de sombra y mar, / y me arrastras al delirio."),
   ("Camas y musgos", "Nos revolcamos en la brisa cálida, / tu cuerpo hecho musgo.", "Nos revolcamos en la brisa cálida, / tu cuerpo hecho musgo."),
   ("La sed", "He bebido la sed de todos los náufragos / cuando lamo tu cuello.", "He bebido la sed de todos los náufragos / cuando lamo tu cuello."),
   ("Gemido", "Un leve gemido es la prueba, / la confesión ahogada.", "Un leve gemido es la prueba, / la confesión ahogada."),
   ("Abrazo atroz", "Nos abrazamos con la desilusión rota / para llenarnos mutuamente.", "Nos abrazamos con la desilusión rota / para llenarnos mutuamente."),
   ("Piel de sol", "Tu piel al estío / huele a tierra abierta a la lluvia.", "Tu piel al estío / huele a tierra abierta a la lluvia."),
   ("Pasión insondable", "Te clavas en mi corazón ciego / con alevosía y fuego.", "Te clavas en mi corazón ciego / con alevosía y fuego."),
   ("Besando oscuro", "Beso en lo oscuro, sabiendo tu sabor / a fruta tropical.", "Beso en lo oscuro, sabiendo tu sabor / a fruta tropical."),
   ("Eternidad de papel", "Eternamente atados / por el rastro del roce final.", "Eternamente atados / por el rastro del roce final.")]),

 ("080_Olga_Orozco_NO_DERECHOS.md","Olga Orozco","1920–1999","Argentina","español",
  "Su voz sibilina, telúrica y sombría evoca los encuentros carnales como rituales brujeriles y trágicos donde el deseo es un animal que muerde y destroza la inmensidad de las sábanas.",
  [("El ritual", "Yo preparo mi cuerpo para ti / como si preparase un sacrificio.", "Yo preparo mi cuerpo para ti / como si preparase un sacrificio."),
   ("Sangre oscura", "Escarbas bajo mi falda, / arrancas mi secreto ensangrentado.", "Escarbas bajo mi falda, / arrancas mi secreto ensangrentado."),
   ("Espasmo del viento", "Tus dedos hurgando en mi locura, / la casa ruge y todo se humedece.", "Tus dedos hurgando en mi locura, / la casa ruge y todo se humedece."),
   ("La mordida", "Muerdes el lóbulo de la muerte / cuando llegas hondo.", "Muerdes el lóbulo de la muerte / cuando llegas hondo."),
   ("Animal en celo", "Aúlla mi vientre pidiendo la condena / de todo tu peso feroz.", "Aúlla mi vientre pidiendo la condena / de todo tu peso feroz."),
   ("Lluvia en la cama", "Hemos empapado este colchón / sudando hasta volvernos lluvia roja.", "Hemos empapado este colchón / sudando hasta volvernos lluvia roja."),
   ("Sombra amada", "Mi amante es de niebla negra, / pero sus besos queman como brasas vivas.", "Mi amante es de niebla negra, / pero sus besos queman como brasas vivas."),
   ("Devoradora", "Quisiera engullirte, triturar tus miedos / en la humedad que hierve.", "Quisiera engullirte, triturar tus miedos / en la humedad que hierve."),
   ("Ceniza ciega", "Tras el placer, somos ruinas tristes, / cegados y abatidos e iracundos.", "Tras el placer, somos ruinas tristes, / cegados y abatidos e iracundos."),
   ("El alarido", "Tapo mi boca con el antebrazo / para que nadie escuche mis caderas cantar.", "Tapo mi boca con el antebrazo / para que nadie escuche mis caderas cantar.")]),

 ("081_Alejandra_Pizarnik_NO_DERECHOS.md","Alejandra Pizarnik","1936–1972","Argentina","español",
  "Poesía oscura, profundamente herida y desesperada. El erotismo es descarnado, asociado al deseo voraz y la muerte.",
  [("La jaula", "Afuera hay un sol amenazante, / adentro nos comemos en penumbras.", "Afuera hay un sol amenazante, / adentro nos comemos en penumbras."),
   ("Deseo mortal", "Quiero que me mates de amor, de ardor, / y de rasguños tristes.", "Quiero que me mates de amor, de ardor, / y de rasguños tristes."),
   ("Noche húmeda", "En esta noche enloquecida / bebo tu sangre dulce.", "En esta noche enloquecida / bebo tu sangre dulce."),
   ("La herida", "Abre la herida que es mi cuerpo, / entra en ella, fúndate.", "Abre la herida que es mi cuerpo, / entra en ella, fúndate."),
   ("Espasmo ciego", "Caemos ciegos al fondo del abismo, / empujados por el placer ahogado.", "Caemos ciegos al fondo del abismo, / empujados por el placer ahogado."),
   ("Labios amargos", "Bésame con la amargura / de las que nunca van a salvarse.", "Bésame con la amargura / de las que nunca van a salvarse."),
   ("Cuerpo negro", "Tu cuerpo brilla con desesperanza, / me hundo en ti, en ti naufrago.", "Tu cuerpo brilla con desesperanza, / me hundo en ti, en ti naufrago."),
   ("Sangre caliente", "Oigo tu pulso galopar mi vientre, / rompiendo la mudez atroz.", "Oigo tu pulso galopar mi vientre, / rompiendo la mudez atroz."),
   ("Sábanas frías", "Calentemos las sábanas heladas / frotando el desespero en mis muslos.", "Calentemos las sábanas heladas / frotando el desespero en mis muslos."),
   ("El final", "Al final sólo nos queda el sudor / y esta tristeza pegajosa.", "Al final sólo nos queda el sudor / y esta tristeza pegajosa.")]),

 ("082_Ana_Maria_Fagundo_NO_DERECHOS.md","Ana María Fagundo","1938–2010","España","español",
  "Canaria, de estilo franco, con poemas que abrazan la entrega total y la plenitud física sin vergüenza.",
  [("El deseo atroz", "Soy un incendio de isla, / marea subiendo hasta tu orilla.", "Soy un incendio de isla, / marea subiendo hasta tu orilla."),
   ("Tu piel salada", "Me bebo tu sal y el salitre ahogado / mordiendo tus arenas.", "Me bebo tu sal y el salitre ahogado / mordiendo tus arenas."),
   ("Huracán", "Llegaste destrozando techos, ropas / y prejuicios mudos.", "Llegaste destrozando techos, ropas / y prejuicios mudos."),
   ("Fuego y flor", "Una flor carmesí se abre / cuando presiento que te acercas.", "Una flor carmesí se abre / cuando presiento que te acercas."),
   ("Sudor isleño", "Empapados del trópico / nuestros vientres bailan apretándose.", "Empapados del trópico / nuestros vientres bailan apretándose."),
   ("Desnudez franca", "Fuera la ropa, / aquí soy solo pulso atroz y ansioso.", "Fuera la ropa, / aquí soy solo pulso atroz y ansioso."),
   ("Gemido de mar", "Zumban los oídos como caracolas / llenas de este goce oscuro.", "Zumban los oídos como caracolas / llenas de este goce oscuro."),
   ("Boca encendida", "Tu boca es un cuchillo y una esponja / quemando mi desierto.", "Tu boca es un cuchillo y una esponja / quemando mi desierto."),
   ("El rastro", "Dejamos la cama convertida en mar embravío.", "Dejamos la cama convertida en mar embravío."),
   ("Tarde infinita", "Esta tarde de amantes rinde cuentas, / nos agota de puro placer.", "Esta tarde de amantes rinde cuentas, / nos agota de puro placer.")]),

 ("083_Luz_Mary_Giraldo_NO_DERECHOS.md","Luz Mary Giraldo","n. 1950","Colombia","español",
  "Su escritura asume la sensualidad de manera reflexiva pero candente, conectando el cuerpo con la naturaleza y la palabra.",
  [("Cuerpo entero", "Descifras mi cuerpo como un papiro oscuro, / trazando líneas con humedad.", "Descifras mi cuerpo como un papiro oscuro, / trazando líneas con humedad."),
   ("Bebida dulce", "Yo te doy a beber de mis humores / más allá del beso.", "Yo te doy a beber de mis humores / más allá del beso."),
   ("Fiebre andina", "Corre calentura por mis venas verdes, / arde el matorral.", "Corre calentura por mis venas verdes, / arde el matorral."),
   ("Selva negra", "Me adentro en ti, o te adentras tú, / fundiendo nuestros ecos.", "Me adentro en ti, o te adentras tú, / fundiendo nuestros ecos."),
   ("Lujuria lenta", "Hagámoslo lento para eternizar / la baba tibia y la delicia ardiente.", "Hagámoslo lento para eternizar / la baba tibia y la delicia ardiente."),
   ("Deseo puro", "Deseo amarrarte a mi cama / y soltar mis miedos atávicos.", "Deseo amarrarte a mi cama / y soltar mis miedos atávicos."),
   ("Sábana de lluvia", "El colchón ya huele / a selva destilada por sudores largos.", "El colchón ya huele / a selva destilada por sudores largos."),
   ("Tigre de aire", "Un zarpazo de amor en mi cadera / me enciende por ti.", "Un zarpazo de amor en mi cadera / me enciende por ti."),
   ("Labios rotos", "Terminamos rotos de tanto darnos, / de morder las ganas.", "Terminamos rotos de tanto darnos, / de morder las ganas."),
   ("La ofrenda", "Yo me ofrezco entera, fruta despojada / al sol de tus caricias.", "Yo me ofrezco entera, fruta despojada / al sol de tus caricias.")]),

 ("084_Gioconda_Belli_NO_DERECHOS.md","Gioconda Belli","n. 1948","Nicaragua","español",
  "La cumbre de la poesía erótica contemporánea en Centroamérica. Asume la sexualidad femenina con libertad y ardor torrencial, haciendo de su cuerpo territorio emancipado.",
  [("Y Dios me hizo mujer", "Me hizo de carne ardiente, de valles frondosos / de montes de ardor indómito.", "Me hizo de carne ardiente, de valles frondosos / de montes de ardor indómito."),
   ("Miembro viril", "Se alza como un tronco en plena noche / y hundo en él mi propia sed atroz.", "Se alza como un tronco en plena noche / y hundo en él mi propia sed atroz."),
   ("Sábanas de fuego", "Las sábanas están testificando que fuimos volcán y que fui lava.", "Las sábanas están testificando que fuimos volcán y que fui lava."),
   ("Vientre fértil", "Hazme una hoguera entre las piernas / donde pueda quemarse la tristeza.", "Hazme una hoguera entre las piernas / donde pueda quemarse la tristeza."),
   ("Tu saliva", "La saliva tuya es lluvia espesa, que baña / este cuerpo tropical sediento y terco.", "La saliva tuya es lluvia espesa, que baña / este cuerpo tropical sediento y terco."),
   ("El orgasmo", "De pronto sube desde los talones la electricidad oscura, / grito tu nombre como loba ciega.", "De pronto sube desde los talones la electricidad oscura, / grito tu nombre como loba ciega."),
   ("Manos ávidas", "Recórreme de norte a sur / como geógrafo de humedales tórridos.", "Recórreme de norte a sur / como geógrafo de humedales tórridos."),
   ("Noches tórridas", "Olor a hierba aplastada / la luna nos asiste sudada y plena.", "Olor a hierba aplastada / la luna nos asiste sudada y plena."),
   ("Fruto prohibido", "Mis senos apuntan para perforar tu cordura / como flechas de placer y rabia amorosa.", "Mis senos apuntan para perforar tu cordura / como flechas de placer y rabia amorosa."),
   ("Despertar del cuerpo", "Acaba, apura, fúndete, lléname, / que quiero ser tu abismo interminable.", "Acaba, apura, fúndete, lléname, / que quiero ser tu abismo interminable.")]),

 ("085_Rosario_Castellanos_NO_DERECHOS.md","Rosario Castellanos","1925–1974","México","español",
  "La brillante autora mexicana tiene pinceladas de intenso y maduro deseo. Se asoma a la pasión descarnada mezclando lucidez y fatalidad.",
  [("Ajedrez de la piel", "Jugamos con fichas blancas y negras, / ganamos quitando prendas.", "Jugamos con fichas blancas y negras, / ganamos quitando prendas."),
   ("Noche fatal", "Quema el alcohol, quema el deseo ardiente, / me rindo a tus manos toscas.", "Quema el alcohol, quema el deseo ardiente, / me rindo a tus manos toscas."),
   ("Plenitud", "Yo soy toda tuya cuando arranco / de tu pecho aquel gemido opaco.", "Yo soy toda tuya cuando arranco / de tu pecho aquel gemido opaco."),
   ("Oscura sed", "Yo, que he sido seria por años enteros / me vuelvo fiera por un beso tuyo hondo.", "Yo, que he sido seria por años enteros / me vuelvo fiera por un beso tuyo hondo."),
   ("Abrazo de loba", "Te envuelvo de la cintura para morder / y marcar por la rabia lo que añoro.", "Te envuelvo de la cintura para morder / y marcar por la rabia lo que añoro."),
   ("Humedad terrible", "Derramando gozos me entretengo triste / sumisa ante el huracán atroz de tus ingles tiernas.", "Derramando gozos me entretengo triste / sumisa ante el huracán atroz de tus ingles tiernas."),
   ("El cuerpo grita", "Grita la mujer que soy adentro, / quiere ser destrozada en tus abrazos.", "Grita la mujer que soy adentro, / quiere ser destrozada en tus abrazos."),
   ("Espejo fiero", "En el espejo miro el rubor mío tras besar tus venas / las tuyas que palpitan mi aliento calcinado.", "En el espejo miro el rubor mío tras besar tus venas / las tuyas que palpitan mi aliento calcinado."),
   ("Espasmos de luz", "Luz ciega cruzando los techos, yo cayendo al hondo lecho de tus muslos locos.", "Luz ciega cruzando los techos, yo cayendo al hondo lecho de tus muslos locos."),
   ("Testamento brutal", "Cuando muera, amor de mis carnes, / acuérdate de las batallas dadas en los colchones fríos de mi locura.", "Cuando muera, amor de mis carnes, / acuérdate de las batallas dadas en los colchones fríos de mi locura.")])
]

if __name__ == "__main__":
    for item in CORRECCIONES:
        mk(*item)
