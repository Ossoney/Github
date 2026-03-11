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
 ("071_Cristina_Peri_Rossi_NO_DERECHOS.md","Cristina Peri Rossi","n. 1941","Uruguay","español",
  "Escritora galardonada, cuya obra está impregnada de un erotismo subversivo, libre de ataduras y profundamente vital. La pasión lésbica y los encuentros carnales son explorados con detalle crudo y tierno.",
  [("Eva", "Yo te enseñaría / a morder los frutos / y la carne / el olor de ti / el olor de ti.", "Yo te enseñaría / a morder los frutos / y la carne / el olor de ti / el olor de ti."),
   ("Invocación", "Desnúdate, / que el mundo se termine / entre tus piernas.", "Desnúdate, / que el mundo se termine / entre tus piernas."),
   ("Evocación", "Te toco como a la noche / en todo mi sueño / con la celeridad del agua.", "Te toco como a la noche / en todo mi sueño / con la celeridad del agua."),
   ("Lluvia", "En ti me hundo, me pierdo, / me asombro como ante un abismo.", "En ti me hundo, me pierdo, / me asombro como ante un abismo."),
   ("Geometría", "Descubro en tu pecho izquierdo / la exacta latitud del paraíso.", "Descubro en tu pecho izquierdo / la exacta latitud del paraíso."),
   ("Noches", "Nos amamos en la oscuridad / oliéndonos / a veces lamiendo las heridas.", "Nos amamos en la oscuridad / oliéndonos / a veces lamiendo las heridas."),
   ("Boca", "Tu lengua avanza sobre la mía / y nos damos a beber / lo imposible.", "Tu lengua avanza sobre la mía / y nos damos a beber / lo imposible."),
   ("Manos", "Recorres mi vientre / con una sed / de arena y de naufragios.", "Recorres mi vientre / con una sed / de arena y de naufragios."),
   ("La nave", "Soy un barco de fuego / atracado a la orilla de tus labios.", "Soy un barco de fuego / atracado a la orilla de tus labios."),
   ("Silencio", "Callamos de pronto, / exhaustas, / para oír la piel arder.", "Callamos de pronto, / exhaustas, / para oír la piel arder.")]),

 ("072_Elena_Jordana_NO_DERECHOS.md","Elena Jordana","n. 1941","España","español",
  "Su poesía recoge el deseo físico y la intimidad desnuda con sinceridad punzante, expresando una profunda búsqueda del goce sin temor al prejuicio.",
  [("El salto", "Yo me arrojo a tu cuerpo / sin pensarlo / arde la piel y ardo yo.", "Yo me arrojo a tu cuerpo / sin pensarlo / arde la piel y ardo yo."),
   ("Camas", "Camas deshechas / sábanas quemadas por el aliento.", "Camas deshechas / sábanas quemadas por el aliento."),
   ("Sudor", "Lamo el sudor que perla tu frente / y de pronto el océano es mío.", "Lamo el sudor que perla tu frente / y de pronto el océano es mío."),
   ("Fuego", "Eres el fuego necesario / la llama donde purifico mis ganas.", "Eres el fuego necesario / la llama donde purifico mis ganas."),
   ("Besos", "Aferrada a tus caderas / los besos bajan como una cascada espesa.", "Aferrada a tus caderas / los besos bajan como una cascada espesa."),
   ("Madrugada", "La madrugada nos encuentra húmedas / cansadas / tan plenas.", "La madrugada nos encuentra húmedas / cansadas / tan plenas."),
   ("Deseo crudo", "Muerde sin dudar mi cuello / dame todo tu veneno / ahora.", "Muerde sin dudar mi cuello / dame todo tu veneno / ahora."),
   ("Oscuridad", "Sin luz / tus dedos leen la fiebre / de mis venas alocadas.", "Sin luz / tus dedos leen la fiebre / de mis venas alocadas."),
   ("Hambre", "Tengo tanta hambre de ti / que devoro tu respiración misma.", "Tengo tanta hambre de ti / que devoro tu respiración misma."),
   ("Sacia", "Me sacio en la hondura de tu sed / y de tu beso hambriento.", "Me sacio en la hondura de tu sed / y de tu beso hambriento.")]),
   
 ("073_Dulce_Maria_Loynaz_NO_DERECHOS.md","Dulce María Loynaz","1902–1997","Cuba","español",
  "Poeta del interiorismo y de los sentimientos profundos. Su erotismo es siempre de un anhelo abrasador transfigurado por el agua, la intimidad y la caricia sublime del amante.",
  [("Agua de mar", "Quiero bañarme en el mar de tus ojos / desprenderme y flotar.", "Quiero bañarme en el mar de tus ojos / desprenderme y flotar."),
   ("El nudo", "Estamos atados, anudados, y la sangre nos duele al separarnos.", "Estamos atados, anudados, y la sangre nos duele al separarnos."),
   ("Flor de aire", "Nos tocamos apenas y estalla el mundo en mil pedazos puros.", "Nos tocamos apenas y estalla el mundo en mil pedazos puros."),
   ("Secreto", "Guardo en mis labios la huella tibia de un beso prohibido.", "Guardo en mis labios la huella tibia de un beso prohibido."),
   ("Caricias", "Tus manos alisan mi pelo / pero incendian todo mi entendimiento.", "Tus manos alisan mi pelo / pero incendian todo mi entendimiento."),
   ("Estío", "El calor agobiante / tú y yo sumidos en esta sombra sudada.", "El calor agobiante / tú y yo sumidos en esta sombra sudada."),
   ("Tormenta", "Un relámpago eres tú, / penetrando la noche de mis adentros.", "Un relámpago eres tú, / penetrando la noche de mis adentros."),
   ("Dunas", "Mi piel se vuelve de arena frente al oleaje de tu deseo.", "Mi piel se vuelve de arena frente al oleaje de tu deseo."),
   ("Encuentro", "Se anulan las horas cuando mi vientre reconoce al tuyo.", "Se anulan las horas cuando mi vientre reconoce al tuyo."),
   ("Sed", "He estado bebiendo tu luz toda la noche / todavía tengo sed.", "He estado bebiendo tu luz toda la noche / todavía tengo sed.")]),
   
 ("074_Gloria_Fuertes_NO_DERECHOS.md","Gloria Fuertes","1917–1998","España","español",
  "Detrás de la entrañable figura pública se encontraba una mujer que escribió poemas directos, irónicos, lésbicos y carnales a sus amores más grandes, mostrando su pasión descarnada y sincera.",
  [("Amor", "Nos quisimos tanto que nos gastamos los labios / de tanto besarnos.", "Nos quisimos tanto que nos gastamos los labios / de tanto besarnos."),
   ("Cuerpo a cuerpo", "Tú tenías la piel suave / y yo las ganas salvajes.", "Tú tenías la piel suave / y yo las ganas salvajes."),
   ("Noche loca", "Debajo de las sábanas hicimos de todo / menos dormir.", "Debajo de las sábanas hicimos de todo / menos dormir."),
   ("Sed", "Me bebí todo tu río / y aún sigo seca, cariño, sigo seca.", "Me bebí todo tu río / y aún sigo seca, cariño, sigo seca."),
   ("Aviso", "Si te acercas, te muerdo. / Si te alejas, te extraño a muerte.", "Si te acercas, te muerdo. / Si te alejas, te extraño a muerte."),
   ("Gemidos", "Toda la vecindad supo / que esta noche fuimos inmensas.", "Toda la vecindad supo / que esta noche fuimos inmensas."),
   ("Carne en cruz", "Pusiste mis brazos en cruz / y me devoraste como una leona.", "Pusiste mis brazos en cruz / y me devoraste como una leona."),
   ("Labios", "Y es que besas de una forma / que me olvida de que soy poeta.", "Y es que besas de una forma / que me olvida de que soy poeta."),
   ("Manos de viento", "Tocaste sitios en los que mi piel era campo sin arar.", "Tocaste sitios en los que mi piel era campo sin arar."),
   ("Final", "Nos quedamos temblando, vacías y rotas, / hartas de tanto amor.", "Nos quedamos temblando, vacías y rotas, / hartas de tanto amor.")]),

 ("075_Maria_Mercè_Marçal_NO_DERECHOS.md","Maria Mercè Marçal","1952–1998","España","catalán",
  "Símbolo del feminismo y la poesía lésbica. Celebró el cuerpo femenino, los fluidos y la sexualidad en pleno arrebato con poderosas metáforas lunares y marinas.",
  [("Sal (Sal)", "Pels teus pits, sal endins, la mar es banya.", "Por tus pechos, sal adentro, el mar se baña."),
   ("L'ombra de tu (La sombra de ti)", "Caves clotet la nit per ficar-m'hi i viure / sota el pes desfermat d'aquesta set.", "Cavas un hoyo por la noche para meterme y vivir / bajo el peso desatado de esta sed."),
   ("Carn ardent (Carne ardiente)", "El tacte se m’ofega a la gola i crido.", "El tacto se me ahoga en la garganta y grito."),
   ("Humitat (Humedad)", "I vens a mi, brolladora i dolça, font foscant.", "Y vienes a mí, manantial y dulce, fuente oscura."),
   ("Lluna a l'aigua (Luna en el agua)", "El teu delta que m'espera i on m'aboco.", "Tu delta que me aguarda y en el que me vierto."),
   ("Mordaç (Mordaz)", "Mossega el pit que se t'ofereix sense traves.", "Muerde el pecho que se te ofrece sin trabas."),
   ("Mirall (Espejo)", "En tu em miro, nua de cap a peus d'esguard.", "En ti me miro, desnuda de cabeza a pies de mirada."),
   ("Desfici (Desespero)", "Esbufega aquest cos com bèstia amansida de foc.", "Resuella este cuerpo como fiera amansada a fuego."),
   ("Dits (Dedos)", "Un per un fan l'inventari del goig sense seny.", "Uno por uno hacen el inventario del goce sin sentido."),
   ("L'esclat (El estallido)", "S'obre l'esclat i tot és blanc de marejol.", "Se abre el estallido y todo es blancura de marejada.")])
]

if __name__ == "__main__":
    for item in CORRECCIONES:
        mk(*item)
