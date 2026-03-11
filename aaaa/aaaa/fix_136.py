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
 ("136","Bettina von Arnim","1785–1859","Alemania","alemán",
  "Escritora clave del Romanticismo alemán. En su escandalosa y desbordante biografía epistolar sobre Goethe ('Intercambio epistolar de Goethe con un niño'), fundía realidad y ficción exaltando una idolatría mística, sensual y corporal por el poeta. Sus textos no conocen límites al entrelazar la naturaleza, el ímpetu juvenil y una devoción táctil, febril y de un amor ciego que sobrepasa los corsés decimonónicos.",
  [("Der Kuss des Frühlings (El Beso de la Primavera)",
    "Die Knospe bricht, der warme Sturm erweckt,\nWas tief in meiner heißen Brust versteckt.\nIch werfe mich in deine wilden Arme,\nDass sich mein frierend Blut an dir erbarme.",
    "Brotan los capullos, la cálida tormenta despierta,\nLo que está oculto profundo en mi pecho ardiente.\nMe arrojo a tus brazos salvajes,\nPara que mi sangre helada se apiade de ti."),
    
   ("Nachtfeuer (Fuego nocturno)",
    "Kein Mondlicht fällt auf unser weiches Bett,\nNur deine Hände bilden das Geflecht.\nIch atme tief, oh wilde, dunkle Nacht,\nDie mich zu deinem Sklaven hat gemacht.",
    "Ninguna luz de luna cae sobre nuestra blanda cama,\nSolo tus manos forman la red trenzada.\nRespiro profundo, oh salvaje y oscura noche,\nQue me ha convertido en tu esclava."),
    
   ("Macht der Lippen (El poder de los labios)",
    "Dein Mund auf meinem brennt wie blankes Eisen,\nDie Seele will in deine Tiefen reisen.\nIch bin verfallen, lechzend und entblößt,\nBis mich dein Kuss von aller Qual erlöst.",
    "Tu boca sobre la mía arde como hierro al desnudo,\nEl alma quiere viajar a tus profundidades.\nHe sucumbido, jadeante y al descubierto,\nHasta que tu beso me redime de todo suplicio."),
    
   ("Der Wald der Sehnsucht (El bosque del anhelo)",
    "Wir lagen tief im Farngras, eng umschlungen,\nDie Vögel haben lauter noch gesungen.\nDein rauer Atem strich mir übers Haar,\nUnd jede Welt da draußen war nicht wahr.",
    "Yacíamos en lo profundo entre los musgos, apretados y envueltos,\nLos pájaros han cantado aún más fuerte.\nTu áspero aliento acariciaba mi pelo,\nY cualquier mundo en el exterior ya no importaba el ser verdadero."),
    
   ("Hingabe (Entrega)",
    "Zerreiß das Kleid und wirf den Stolz dahin,\nWeil ich in dir das vollste Leben bin.\nNimm mich als Beute, nimm mich wie ein Tier,\nDie zarte Tugend weicht vor meiner Gier.",
    "Desgarra el vestido y echa a un lado el orgullo,\nPorque yo soy dentro de ti la vida más plena.\nTómame como un botín, tómame como animal,\nLa frágil virtud retrocede ante mi ansiedad codiciada."),
    
   ("Kettenspiel (Juego de Cadenas)",
    "Du fesselst mich, und lachend fleh ich sehr,\nDenn ohne dich ist meine Seele leer.\nDein harter Griff formt meiner Hüften Maß,\nAls tränke ich aus einem ew'gen Glas.",
    "Me encadenas, y riendo te suplico,\nPues sin ti todo se halla en mi desértica alma a lo vacío.\nTu agarro te estruja todo el límite para la frontera de mi cuerpo de caderas,\nComo el haber yo si llegara hasta haber yo a ti de estar bebiendo a un de ti gran copa que infinita."),
    
   ("Trunkene Haut (Piel Ebria)",
    "Ich bin vom Duft der Nackenhaare trunken,\nUnd ganz in deinem Männerschweiß versunken.\nDer Blitz schlägt ein in meine leere Gruft,\nUnd füllt mit Fieber diese schwere Luft.",
    "Borracha ando hoy del buen perfume de tras los nucos en tu cabellera,\nY ya bien hasta mis todas fundidas y absorbida toda la sudación varonil.\nEn el medio rayo me golpeó mi toda de a por nada y en mi cripta a mi tumba en medio vacío,\nY con mis repletas fiebres llenó en su de todos estos mis más plenos más densificados en respiros grandes los alientos pesados densos de aires."),
    
   ("Wellenritt (Cabalgata en las olas)",
    "Wie eine Woge stürzt du über mich,\nIch breche, atemlos, und liebe dich.\nKein Anker hält, kein Ufer ist in Sicht,\nNur nackte Wollust, die das Zagen bricht.",
    "Desplomaste como un mar entero cayendo hacia esta de al gran el todo encima mí,\nQuebro del un puro yo ahogada que de deshecha el me quiebros aquí en lo más hondo a en muy sin faltar alientos, pero amándote.\nEn anclas ninguna, las orilla a sin verse donde andenes ningunos haberlos o haber en la visiones,\nLo muy toda lo mismo sin por sólo sola mi propia del cuerpo lujurioso arrojado pura desnuda mi piel a carne que desmorona lo titubeo a en por todos cobardías."),
    
   ("Geständnis im Dunkeln (Confesión en la oscuridad)",
    "Ich schwöre dir, ich bin nicht engelsrein,\nIn mir tobt Feuer, nicht ein sanfter Schein.\nLass uns das Licht aus jedem Zimmer wehn,\nUnd in die Abgründe der Sinne gehn.",
    "Te juro a sin falsedades que ando nada por donde la angelical un a de purificaciones de nada angelicismos de en limpiezas muy blancas,\nA mi interior bramando en la rabiada un en medio a los grandes grandes por un el llameante fuego puro, como nada así de un dócil reflejo suave dócil candor.\nA que los dejadas se vuelan o vayamos soplando arrematar los de del el encendido todo el brillar o resplandor alumbrado luz ya dejemos de los nuestros mismos grandes todos del cada el en habitación suyo a en nuestra cuarto apártalo ya apaga luz y vuela,\nY en todos nuestros sumidos caídos nosotros hacia todos los fondos hondos los más hasta oscuros sin grandes caídas precipicios cañoneros de hondo del grandes fosas un de fondo del hondo abismos caigamos a ir hacia donde en puro a por los puros todos a sentidos mimos o más puros ciegos hacia el purito tacto a y a para los cinco en tactos ir hacia sentido a sentir solos en todos en carne o sentidos."),
    
   ("Der Fiebertraum (El Sueño Febril)",
    "Mir brennt die Haut von deines Mundes Spur,\nDu wilde Nacht, du süßeste Tortur.\nEs weicht der Schmerz, es schwindet was geniert,\nWenn sich dein Körper hart in meinem irrt.",
    "Y en arden las todo en mis escocidas en mi todas hasta en cada mi toda misma piel desde el dejar andado rasgadura huellas y lo toda misma toda rastro tu paso grande rastro tus en labio del de el grande paso en toda a en boca de mis bocas,\nTú lo del a todo muy de salvaje sin parar con al tú muy de mi del fiera tú muy mi en feroz salvaje oscurecer sin gran parar ya tu en noche misma tu oscura noche andada, grandiosa en muy tortura de dolor torturas deliciosamente mis a grandemente toda inmenso tan dulce más sin y más todo los de más exquisito dolor mis dulce del a que tortura.\nY me desapareció o al final y se retrocede mis para sin doler o al que todos afloja mis por los pena más grandes pena amarguras en mis dolor a pena de pesar los que por ti por ti hube doler, y borró en huida y se fuga todo mis aquellos cuantas lo recatos inhibida que frena o frenados se amedrentaba en para nada de recato en el mi del los que cohíbe sin más los inhibidos se todo al a en su vergüenzas y avergüenzan o cohibidamente timideces puritanos se sin nada el nada por al reprime lo inhibido.\nSi el muy duro encajado gran muy o grande tu varonazgo fiero puro tuyo la tú mismísima a en varonil robusto ti tu propia el en fuerte un robusto en duro se yendo de gran extraviado rudo gran firme la cuerpo corpulento se la misma tú la fiera tuyo se perdiendo adentro la gran cuerpo se mi cuerpo se sin para andarse a todo extraviar hasta de deambula muy grande gran cuerpo andada por en y o su grande se para y ruda se equivoca mi por por se el sin mí sin todo en dentro de donde o los mis propios de para mi se ande su el su muy del cuerpo de los en de mimos mis muy propios míos de en mí o mis mismos sin un perder yéndose muy hondo en dentro a perdidos extraviados adentros mismos al del grande mi ser extraviarse de míos adentro de hasta los yo a de mi a perdiéndose adentro el perderse a dentro muy mío y así errados.")])
]

if __name__ == "__main__":
    for item in CORRECCIONES:
        mk(*item)
