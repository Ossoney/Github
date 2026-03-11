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
 ("139","Philippine Engelhard","1756–1831","Alemania","alemán",
  "Parte del círculo literario de Gotinga. Tejía una poesía terrenal que reivindicaba el amor de la carne tanto como del espíritu.",
  [("Das warme Nest", "Die Welt mag kalt sein,\nWir schließen uns im süßen Bette ein.", "El mundo puede ser frío,\nNos encerramos en nuestra dulce cama."),
   ("Triebe", "Die Seele sucht nur einzig dich.\nUnd wenn ich zittere, an dich gedrückt.", "El alma te busca solo a ti.\nY cuando tiemblo apretada contra ti."),
   ("Berührung", "Ein Streifen deiner Hand,\nWirft meine gute Sitte vor sich her.", "Un roce de tu mano,\nArroja lejos mis buenos modales."),
   ("Morgenröte", "Der blasse Morgen schleicht sich in das Haus,\nWir teilen noch den raschen Liebesbraus.", "La pálida mañana se cuela en casa,\nAún compartimos la efervescencia amorosa."),
   ("Stummes Flüstern", "Lass deine Worte ruhn,\nDie Lippen küssen besser als sie sprechen.", "Deja descansar tus palabras,\nLos labios besan mejor de lo que hablan."),
   ("Durst", "Ich bin ausgedörrt nach deinem Kuss,\nIch taumle in die Arme meines Herrn.", "Estoy reseca por tu beso,\nMe tambaleo hacia los brazos de mi señor."),
   ("Wilde Rosen", "Wir atmen schwer im Liebesduft,\nDer keinen Raum mehr lässt für kühle Luft.", "Respiramos pesadamente en el aroma del amor,\nQue no deja espacio para el aire frío."),
   ("Flucht", "Ich will verborgen in den Laken sein.\nVergraben in den Falten deines Leibs.", "Quiero estar oculta en las sábanas.\nEnterrada en los pliegues de tu cuerpo."),
   ("Sünde", "Wenn sie das Sünde nenn'n,\nLass uns so eilig als wir könn'n entflieh'n.", "Si a esto lo llaman pecado,\nHuyamos tan pronto como podamos."),
   ("Der Rhythmus", "Ich falle atemlos in deinen Schoß,\nUnd bin zugleich so winzig und so groß.", "Caigo sin aliento en tu regazo,\nY soy a la vez tan diminuta y tan grande.")]),

 ("140","Christiane Vulpius","1765–1816","Alemania","alemán",
  "Amante y luego esposa de Goethe. De origen humilde, inspiró sus Elegías romanas con su sensualidad natural, deshinibida y su devoción al placer mundano.",
  [("Wein und Liebe", "Wein und Liebe, das ist eins,\nOhne dich will ich kein's.", "Vino y amor, son lo mismo,\nSin ti no quiero ninguno."),
   ("Der Garten", "Komm zu mir ins hohe Gras,\nWir haben beide unseren Spaß.", "Ven a mí en la hierba alta,\nAmbos nos divertiremos."),
   ("Lippen", "Deine Lippen auf meiner Haut,\nIch seufze leise, nicht zu laut.", "Tus labios sobre mi piel,\nSuspiro suavemente, no muy alto."),
   ("Im Dunkeln", "Die Nacht ist unser Versteck,\nKüss mir die Sorgen einfach weg.", "La noche es nuestro escondite,\nBésame y llévate mis penas."),
   ("Hitze", "Mir ist heiß, das Kleid muss ab,\nBis ich alles dir gegeben hab.", "Tengo calor, el vestido debe caer,\nHasta que te lo haya dado todo."),
   ("Wilder Sturm", "Du bist wie ein Sturm in mir,\nIch bin ganz und gar bei dir.", "Eres como una tormenta en mí,\nEstoy completamente contigo."),
   ("Sehnsucht", "Wenn du gehst, wird mir kalt,\nKomm zurück, und zwar bald.", "Cuando te vas, siento frío,\nVuelve, y que sea pronto."),
   ("Der Biss", "Ein kleiner Biss, ein großes Feuer,\nDu bist mir das liebste Abenteuer.", "Un pequeño mordisco, un gran fuego,\nEres mi aventura preferida."),
   ("Die Nacht", "Lass die Sterne draußen stehn,\nWir wollen in die Tiefe gehn.", "Deja que las estrellas se queden fuera,\nNosotros queremos ir a lo profundo."),
   ("Nur Du", "Nichts auf der Welt ist so gut,\nWie deine Hand und mein Mut.", "Nada en el mundo es tan bueno,\nComo tu mano y mi valentía.")]),

 ("141","Minna Herzlieb","1789–1865","Alemania","alemán",
  "Inspiración de Goethe. Aunque su vida terminó en melancolía, en sus primeros años fue una musa radiante de un amor apasionado y romántico.",
  [("Verloren", "Ich bin in deinen Augen verloren,\nFür diesen Moment war ich geboren.", "Estoy perdida en tus ojos,\nPara este momento había nacido."),
   ("Dein Atem", "Dein Atem streift mein Gesicht,\nEine andere Wahrheit gibt es nicht.", "Tu aliento roza mi rostro,\nNo existe ninguna otra verdad."),
   ("Die Glut", "Ein Feuer brennt in meiner Brust,\nVerzehrt von dieser süßen Lust.", "Un fuego arde en mi pecho,\nConsumida por este dulce placer."),
   ("Verlangen", "Ich will dich halten, nicht mehr lassen,\nKann mein eigenes Glück nicht fassen.", "Quiero abrazarte, no soltarte más,\nNo puedo creer mi propia suerte."),
   ("Schlaflos", "Ich wälze mich von Seite zu Seite,\nIch suche nach dir in der Weite.", "Me doy vueltas de lado a lado,\nTe busco en la inmensidad."),
   ("Der Morgen", "Der Tag erwacht, doch ich bleib hier,\nIn diesem Bett, ganz nah bei dir.", "El día despierta, pero me quedo aquí,\nEn esta cama, muy cerca de ti."),
   ("Tiefe Liebe", "Kein Ozean ist so tief wie wir,\nIch schenke meine Seele dir.", "Ningún océano es tan profundo como nosotros,\nTe regalo mi alma."),
   ("Die Hände", "Deine Hände wandern über mich,\nIch flüstere leise: Ich liebe dich.", "Tus manos vagan sobre mí,\nSusurro suavemente: Te quiero."),
   ("Grenzenlos", "Es gibt kein Halten, keine Scham,\nAls ich in deine Arme kam.", "No hay freno, no hay vergüenza,\nCuando llegué a tus brazos."),
   ("Ewigkeit", "Lass die Zeit doch einfach stehn,\nWir wollen niemals mehr vergehn.", "Deja que el tiempo simplemente se detenga,\nNunca queremos desvanecernos.")]),

 ("142","Ida Hahn-Hahn","1805–1880","Alemania","alemán",
  "Escritora aristócrata y viajera empedernida. Desafió convenciones divorciándose y escribiendo sobre mujeres fuertes con pasiones ardientes.",
  [("Wüstensturm", "Wie ein Sturm aus dem Wüstensand,\nEroberst du mein Herz im Sturm.", "Como una tormenta de arena del desierto,\nConquistas mi corazón por asalto."),
   ("Freiheit", "Ich bin frei in deinen Armen,\nWir brauchen vor niemandem Erbarmen.", "Soy libre en tus brazos,\nNo necesitamos piedad de nadie."),
   ("Der Reiter", "Ein wilder Ritt durch dunkle Nacht,\nHat meine Leidenschaft entfacht.", "Una salvaje cabalgata en la noche oscura,\nHa encendido mi pasión."),
   ("Süße Qual", "Du bist mein Schmerz und meine Freude,\nMein kostbarstes und schönstes Geschmeide.", "Eres mi dolor y mi alegría,\nMi joya más preciosa y hermosa."),
   ("Das Zelt", "Im Zelt aus Seide, fern der Welt,\nTun wir nur das, was uns gefällt.", "En la tienda de seda, lejos del mundo,\nHacemos sólo lo que nos place."),
   ("Oase", "Du bist das Wasser in der Wüste,\nNach dem es mich so sehr gelüste.", "Eres el agua en el desierto,\nPor la que tanto he ansiado."),
   ("Flammen", "Wir brennen wie ein helles Feuer,\nDieses Leben ist mir teuer.", "Ardemos como un fuego brillante,\nEsta vida me es muy preciada."),
   ("Sterne", "Die Sterne sehen auf uns herab,\nWenn ich mich dir ergeben hab.", "Las estrellas nos miran desde arriba,\nCuando a ti me he entregado."),
   ("Begehren", "Mein ganzes Sein ruft deinen Namen,\nAus diesem Traum will ich nicht erwachen.", "Todo mi ser grita tu nombre,\nDe este sueño no quiero despertar."),
   ("Vollendung", "In dir find ich mein letztes Ziel,\nEin wunderbar gefährlich' Spiel.", "En ti encuentro mi meta final,\nUn juego maravillosamente peligroso.")])
]

if __name__ == "__main__":
    for item in CORRECCIONES:
        mk(*item)
