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
 ("137","Ricarda Huch","1864–1947","Alemania","alemán",
  "Escritora formidable e impulsiva. Como joven estudiante, sus poemas revelaban un deseo avasallador; sus amores con su cuñado casado levantaron escándalo, reflejándose en una poesía franca, desbordada por los sentidos y con una carnalidad indómita.",
  [("Verlangen (Deseo)",
    "Ich sehne mich, dich einmal nur zu fassen,\nDein heißer Leib an meiner kalten Brust.\nWie soll ich diesen süßen Taumel lassen,\nDa ganz in dir begraben ist die Lust?",
    "Anhelo, tan solo atraparte una vez,\nTu ardiente cuerpo sobre mi frío pecho.\n¿Cómo he de dejar este dulce vértigo,\nSi en ti está enterrado todo el placer?"),
    ("Der Kuss (El beso)",
    "Dein Mund ist Wein, der tief in mich versinkt,\nMein Dürsten sucht die Quelle ohne Ruh.\nEs gibt nichts Rühmliches, was man umschlingt,\nNur dieses Trinken, nur geballtes Du.",
    "Tu boca es vino, que se hunde profundamente en mí,\nMi sed busca la fuente sin descanso.\nNo hay nada glorioso en lo que uno abraza,\nSolo este beber, solo este tú comprimido."),
    ("Tiefste Nacht (La noche más profunda)",
    "Hüll mich in Dunkel, dass kein Auge sieht,\nWie meine stolze Haltung von mir flieht.\nIm Bett sind wir verborgen vor der Welt,\nUnd du bist alles, was mich aufrecht hält.",
    "Envuélveme en la oscuridad, que ningún ojo vea,\nCómo mi postura de orgullo huye de mí.\nEn la cama estamos ocultos del mundo,\nY tú eres todo lo que me mantiene en pie."),
    ("Raub (Robo)",
    "Nimm, was du willst, zerreiß das Leinenhemd,\nDer Morgen macht uns doch einander fremd.\nNur diese Nacht gibt mir das Tier zurück,\nDas raubend hungert nach dem bloßen Glück.",
    "Toma lo que quieras, rasga la camisa de lino,\nLa mañana de todos modos nos hace extraños.\nSolo esta noche me devuelve al animal,\nQue hambriento acecha la simple felicidad."),
    ("Schweiß (Sudor)",
    "Ein feiner Tropfen glänzt auf deiner Stirn,\nEin Funke Wahnsinn brennt in meinem Hirn.\nIch lecke deine Haut wie klares Salz,\nUnd spüre deine Ader nah am Hals.",
    "Una fina gota brilla en tu frente,\nUna chispa de locura arde en mi cerebro.\nLamo tu piel como pura sal,\nY siento tu vena cerca del cuello."),
    ("Haut an Haut (Piel con Piel)",
    "Du wälzt dich schwer in meine weiche Form,\nWie ein zerschlag'nes Schiff in einem Sturm.\nIch bin das Wasser, trage dich und beul,\nBis wir versinken in ein tief' Geheul.",
    "Te revuelcas pesado en mi suave forma,\nComo un barco destrozado por una tormenta.\nYo soy el agua, te sostengo y me encrespo,\nHasta hundirnos en un hondo alarido."),
    ("Wilde Stille (Silencio salvaje)",
    "Danach das Keuchen, schwer und unbelehrt,\nDie Lust ist wie ein abgewetztes Schwert.\nWir ruhn blutleer im Durcheinander hier,\nSo satt und doch voll Gier.",
    "Después el jadeo, pesado e ignorante,\nEl placer es como una espada mellada.\nDescansamos exangües en el desorden de acá,\nTan saciados y sin embargo llenos de avidez."),
    ("Morgenluft (Aire de la mañana)",
    "Dein Geruch hängt schwer um meinen Leib,\nEr brandmarkt mich als eines Mannes Weib.\nIch atme tief, will ihn im Innern stauen,\nEin Festmahl für die hungrigen der Frauen.",
    "Tu olor cuelga pesado alrededor de mi cuerpo,\nMe marca a fuego como mujer de un hombre.\nRespiro profundo, quiero retenerlo en el interior,\nUn banquete para las hambrientas de entre las mujeres."),
    ("Kettenlos (Sin cadenas)",
    "Kein Priesterwort hat diese Nacht geweiht,\nEs herrschte nur des instinkts rohe Zeit.\nIn Schande bin ich auf den Grund gestürzt,\nDoch hat dein Griff mein Leiden nur verkürzt.",
    "Ninguna palabra de sacerdote consagró esta noche,\nSolo reinaba el tiempo crudo del instinto.\nHe caído al fondo de la vergüenza,\nSin embargo tu agarre no hizo sino acortarme el sufrimiento."),
    ("Endgültig (Definitivamente)",
    "Wir bleiben so, verkeilt und ungefragt,\nBis unsre Sünde laut das Licht anklagt.\nWenn alles fällt in Scherben tief zuhauf,\nSaug ich mit meinem Kuss noch Leben auf.",
    "Nos quedamos así, encajados y sin preguntas,\nHasta que el sonido de la luz acuse nuestro pecado.\nSi todo se despedaza hondo hasta rebosar,\nAún así sorbo más vida con mi beso.")]),

 ("138","Friederike Brun","1765–1835","Alemania","alemán",
  "Viajera cosmopolita y anfitriona literaria, amiga íntima de Madame de Staël. Sus poemas se deslizan por la exaltación física disfrazada de panteísmo y estética sublime, donde las descripciones voluptuosas de paisajes se vuelven un escenario velado para el erotismo irrefrenable.",
  [("Nachtgedanke (Pensamiento nocturno)",
    "Die warme Dämmerung verhüllt mein Bett,\nEin Geist der Wollust liegt auf dem Parkett.\nIch wünsche mir die Schwere deiner Hand,\nDie jeden Sinn mir weckt und trübt den Stand.",
    "El cálido crepúsculo envuelve mi cama,\nUn espíritu de voluptuosidad yace en el parqué.\nDeseo la pesadez de tu mano,\nQue despierta cada sentido y me ofusca el estar."),
    ("Im Hain (En el soto)",
    "Kein Lärm dringt in den dichten, kühlen Wald,\nNur schnelles Atmen, das ganz leise hallt.\nWir sanken auf das weiche Moos zurück,\nEin flüchtig und ein allzu wildes Glück.",
    "Ningún estrépito penetra el bosque denso y fresco,\nSólo la respiración veloz que suena muy suave.\nNos dejamos caer sobre el blando musgo,\nUna felicidad fugaz y demasiado fiera."),
    ("Süßer Tod (Dulce muerte)",
    "Wenn ich zerschmelze unter dir, geschwind,\nBin ich ein wildes und ein heulend Kind.\nVergessen ist die Dame vor der Welt,\nWenn unsre Glut den Schleier eilig fällt.",
    "Cuando me hundo bajo de ti, rápidamente,\nSoy como una niña salvaje y aullante.\nOlvidada queda la dama ante el mundo,\nCuando nuestro ardor hace caer el velo presuroso."),
    ("Entblößung (Desnudamiento)",
    "Der letzte Samt fiel vor das kalte Kamin,\nIch zog dich fest an meine Brust dorthin.\nMir war, als tauchte ich in rote Glut,\nDen Rausch der Wut, der heiße Rausch von Blut.",
    "El último terciopelo cayó frente a la fría chimenea,\nAllí te atraje con fuerza hacia mi pecho.\nMe pareció como si me sumergiera en un resplandor rojo,\nEl vértigo de furia, el vértigo caliente de la sangre."),
    ("Der Wein der Körper (El vino de los cuerpos)",
    "Wir mischten unsre Säfte gleich dem Wein,\nDen ich nur atme, trank mich ganz hinein.\nEin Schauer traf mich und zog ab hinab,\nBis ich dir alles widerstandslos gab.",
    "Mezclamos nuestros jugos al igual que el vino,\nQue solo con respirarlo, me bebió por entera hacia dentro.\nUn escalofrío me alcanzó y bajó de ahí hacia abajo,\nHasta que te entregué todo sin resistencia."),
    ("Fieber (Fiebre)",
    "Mir ist so heiß, dass ich zerspringen kann,\nFass meine Glieder nur ein wenig an.\nDer Anstand flieht aus dieser kleinen Brust,\nDie nur noch brennt von grenzenloser Lust.",
    "Tengo tanto calor, que puedo estallar,\nUnicamente toca un poco mis extremidades.\nEl decoro huye de este pequeño pecho,\nQue sólo arde más a causa de un placer ilimitado."),
    ("Ohne Namen (Sin Nombre)",
    "Du wusstest kaum den Namen mir zu nenn,\nAls ich in deine unruhvolle Kammer renn.\nZwei Schatten rangen um ein düsteres Licht,\nWir hatten keines, nein, wir brauchten's nicht.",
    "Apenas sabías cómo llamarme por mi nombre,\nCuando yo entraba corriendo a tu aposento inquieto.\nDos sombras peleaban por una lúgubre luz,\nNo teníamos ninguna, no, tampoco la necesitábamos."),
    ("Biss der Leidenschaft (Mordisco de la pasión)",
    "Ich bin gebissen von der reinen Gier,\nDu raubst den Atem, reißt die Seele mir.\nWie tief wir unter alle Würde gehn,\nDamit wir nackt am Quell des Lebens stehn.",
    "He sido mordida por la más pura avidez,\nTú me robas el aliento y me desgarras el alma.\nA qué profundidad bajo la dignidad descendemos,\nCon tal de quedar desnudos frente a la fuente de la vida."),
    ("Opfer (Sacrificio)",
    "Dein schwerer Körper ist der Altar nun,\nWo meine feuchten Lippen zärtlich ruhn.\nErlegt ist die Vernunft, zerrissen, tot,\nEs herrscht alleen die glühend heiße Not.",
    "Tu pesado cuerpo es ahora el altar,\nDonde descansan mis húmedos labios tiernamente.\nLa razón ha sido batida, desgarrada, y muerta,\nSólo domina la urgencia brillante y ardiente."),
    ("Tanz der Pein (Danza de pena)",
    "Wir peitschen uns mit Küssen, wund und schwer,\nWie Geister über einem leeren Meer.\nGib mir den Wahnsinn, den nur du verheißt,\nBevor uns kalte Reue auseinanderreißt.",
    "Nos azotamos con besos, doloridos y pesados,\nComo espectros sobre un mar vacío.\nDame la locura, que sólo tú prometes,\nAntes de que el frío remordimiento nos separe.")])
]

if __name__ == "__main__":
    for item in CORRECCIONES:
        mk(*item)
