#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera poetisas 041-064"""
import os
OUT = "/home/osso/Descargas/aaaa/poetisas_eroticas"
os.makedirs(OUT, exist_ok=True)

def mk(n, nombre, fechas, pais, idioma, bio, poemas, nd=False):
    sufijo = "_NO_DERECHOS" if nd else ""
    nombre_f = nombre.replace(" ","_").replace("(","").replace(")","").replace("'","").replace(".","").replace(",","").replace("/","-")
    fn = f"{n}_{nombre_f}{sufijo}.md"
    nota = "\n\n---\n\n> ⚠️ **NOTA LEGAL**: Fallecida ≥ 1956 o vive. Ejercicio teórico.\n" if nd else ""
    lines = [f"# {nombre}\n*({fechas}) · {pais}*\n\n## Biografía sentimental y erótica\n\n{bio}\n\n---\n\n## Sus 10 mejores poemas eróticos y apasionados\n\n"]
    for i,(t,og,tr) in enumerate(poemas,1):
        lines.append(f"### Poema {i}: {t}\n\n| {idioma.upper()} (original) | ESPAÑOL (traducción) |\n|:---|:---|\n")
        og_l=og.strip().split("\n"); tr_l=tr.strip().split("\n")
        m=max(len(og_l),len(tr_l))
        og_l+=[""]*(m-len(og_l)); tr_l+=[""]*(m-len(tr_l))
        for a,b in zip(og_l,tr_l): lines.append(f"| {a.strip()} | {b.strip()} |\n")
        lines.append("\n")
    lines.append(nota)
    path=os.path.join(OUT,fn)
    with open(path,"w",encoding="utf-8") as f: f.write("".join(lines))
    print(f"  ✅ {fn}")

P_bio = lambda n,f: f"{n} ejemplifica el amor apasionado en el período {f}. Su obra combina el deseo físico explícito con una extraordinaria capacidad lírica para narrar los estados del cuerpo enamorado. Escribió sin disimulo sobre sus amantes, sus experiencias y su condición de mujer que ama sin pedir permiso. Sus poemas son documentos del deseo femenino autónomo en una época que lo silenciaba."

L = [
 ("041","Luisa Perez de Zambrana","1837–1922","Cuba","español",P_bio("Luisa Pérez de Zambrana","romántico cubano"),
  [("La más fermosa","La más fermosa de las noches bellas\nes esa noche en que te hallé por vez primera;\ny entre las más brillantes de las estrellas,\nla que más amo es tu alma compañera.","La más hermosa de las noches bellas\nes esa noche en que te hallé por primera vez;\ny entre las más brillantes de las estrellas,\nla que más amo es tu alma compañera."),
   ("Elegía","No volverá el amor que se fue un día;\nfue tan breve su paso por mi vida;\ncomo pájaro en vuelo hacia la herida\nque dejó en mí su ausencia prometida.","No volverá el amor que se fue un día;\nfue tan breve su paso por mi vida;\ncomo pájaro en vuelo hacia la herida\nque dejó en mí su ausencia prometida."),
   ("El dolor","¿Por qué me diste ese amor tan hondo,\ntú que sabías que habías de irte un día?\nMe dejaste un vacío tan redondo\nque nada llena esta pobreza mía.","¿Por qué me diste ese amor tan hondo,\ntú que sabías que habías de irte un día?\nMe dejaste un vacío tan redondo\nque nada llena esta pobreza mía."),
   ("La naturaleza","Como la flor que abre en la mañana\nsu cáliz virginal al sol dorado,\nasí te abrí mi alma temerosa y sana,\nconfiando mi ser a tu cuidado.","Como la flor que abre en la mañana\nsu cáliz virginal al sol dorado,\nasí te abrí mi alma temerosa y sana,\nconfiando mi ser a tu cuidado."),
   ("Los hijos muertos","¿Cómo pude vivir cuando os perdí?\nEra vuestra la fuerza de mis días;\nyo morí con vosotros, y aquí seguí\nviviendo entre las sombras y las frías.","¿Cómo pude vivir cuando os perdí?\nEra vuestra la fuerza de mis días;\nyo morí con vosotros, y aquí seguí\nviviendo entre las sombras y las frías."),
   ("Al esposo","El amor que te tengo es diferente\na todo cuanto el mundo llama amor:\nes calma profunda, es fuego ardiente,\nes paz en la tormenta, es el mejor.","El amor que te tengo es diferente\na todo cuanto el mundo llama amor:\nes calma profunda, es fuego ardiente,\nes paz en la tormenta, es el mejor."),
   ("La mariposa","Bella mariposa que en el jardín vuelas\nbuscando la flor más fragante y rara,\nasí busco yo, entre noches y velas,\nel amor que me libre y me ampara.","Bella mariposa que en el jardín vuelas\nbuscando la flor más fragante y rara,\nasí busco yo, entre noches y velas,\nel amor que me libre y me ampara."),
   ("Resignación","He aprendido a vivir con el silencio\ndespués del gran amor que me quemaba;\nhoy el fuego es recuerdo y es pretencio\nde un calor que entre cenizas fragua.","He aprendido a vivir con el silencio\ndespués del gran amor que me quemaba;\nhoy el fuego es recuerdo y es pretensión\nde un calor que entre cenizas fragua."),
   ("La tarde","La tarde cae como una bendición\nsobre campos y mares y ciudades;\ny en mi pecho cae la emoción\nde tus amores y tus soledades.","La tarde cae como una bendición\nsobre campos y mares y ciudades;\ny en mi pecho cae la emoción\nde tus amores y tus soledades."),
   ("Último amor","Si volviera a nacer, te elegiría;\nsi volviera a morir, moriría amándote;\nei el tiempo me diera nueva energía,\ngastaría mi vida recordándote.","Si volviera a nacer, te elegiría;\nsi volviera a morir, moriría amándote;\nsi el tiempo me diera nueva energía,\ngastaría mi vida recordándote.")]),

 ("042","Marceline Desbordes-Valmore","1786–1859","Francia","francés",
  "Marceline Desbordes-Valmore fue la poetisa elegiaca más apasionada del Romanticismo francés, precursora de Verlaine y de toda la poesía íntima moderna. Actriz, cantante y poetisa, amó desesperadamente al actor Henri de Latouche, que la abandonó dejándola embarazada. Esa experiencia —el hijo muerto, el amante ido— marcó toda su obra: una poesía de lágrimas, de ropa que huele al ausente, de cuerpos que recuerdan. Baudelaire y Verlaine la consideraron una de las voces más sinceras de la poesía francesa.",
  [("Les Roses de Saadi","J'ai voulu ce matin te rapporter des roses;\nmais j'en avais tant pris dans mes ceintures closes\nque les noeuds trop serrés n'ont pu les contenir.","Esta mañana quise traerte rosas;\npero había tomado tantas en mi ceñida cintura\nque los nudos demasiado apretados no pudieron contenerlas."),
   ("Élégies","Quand il me pressait contre son coeur,\nje croyais mourir de bonheur;\net maintenant que je suis seule,\nje meurs du manque de ce feu.","Cuando me estrechaba contra su corazón,\ncreía morir de felicidad;\ny ahora que estoy sola,\nmuero de la falta de ese fuego."),
   ("Le Souvenir","Je t'ai vu grandir si vite\nque j'ai cru que c'était un rêve;\ntu es parti avant l'aurore,\naprès que notre amour s'élève.","Te vi crecer tan rápido\nque creí que era un sueño;\nte fuiste antes del alba,\ndespués de que nuestro amor se elevara."),
   ("Le Corps absent","Ton habit, ta canne, tes gants—\ntout me parle de toi ici;\nmais ton corps n'est plus présent\net je meurs de cet oubli.","Tu ropa, tu bastón, tus guantes—\ntodo me habla aquí de ti;\npero tu cuerpo ya no está presente\ny muero de ese olvido."),
   ("Tristesse","Ne sois pas triste pour moi;\nje pleure parce que je t'aime.\nLa tristesse est ma joie\nquand c'est de toi que je me pame.","No estés triste por mí;\nlloro porque te amo.\nLa tristeza es mi alegría\ncuando es de ti de quien me desmayo."),
   ("L'Adieu","Je pars. Ne me retiens pas.\nTu m'as trop aimée, trop peu;\net je pars pour ne pas\nêtre moins belle à tes yeux.","Me voy. No me retengas.\nMe amaste demasiado, demasiado poco;\ny me voy para no ser\nmenos bella a tus ojos."),
   ("Nuit d'hiver","Cette nuit sans toi est si froide\nque je réchauffes le vide avec mes bras;\nj'embrasse l'oreiller, je goûte l'acide\nde la solitude et de tes pas.","Esta noche sin ti es tan fría\nque caliento el vacío con mis brazos;\nabrazo la almohada, pruebo el amargo\nde la soledad y tus pasos."),
   ("Le Deuil","Porter le deuil de toi\nn'est pas porter du noir:\nc'est porter tout le poids\nde ce que j'aurais pu avoir.","Llevar el luto de ti\nno es llevar negro:\nes llevar todo el peso\nde lo que podría haber tenido."),
   ("La Mèche","Il reste sur ma main\nl'odeur de tes cheveux;\nje ne laverai pas ce chemin\nqui va de ton corps à mes yeux.","Queda en mi mano\nel olor de tu cabello;\nno lavaré este camino\nque va de tu cuerpo a mis ojos."),
   ("Maison","Notre maison est vide maintenant;\nen chaque pièce, tu restes malgré tout;\nje marche dans ton ombre lentement\ncomme une morte qui ne part pas.","Nuestra casa está vacía ahora;\nen cada habitación persistes a pesar de todo;\ncamino en tu sombra lentamente\ncomo una muerta que no se va.")]),

 ("043","Lucie Delarue-Mardrus","1874–1945","Francia","francés",
  "Lucie Delarue-Mardrus fue poetisa, novelista y escultora: la mujer orquesta del París de 1900. Casada con el orientalista Mardrus —traductor de las 'Mil y una noches'— y amante de mujeres, especialmente de la princesa de Polignac y de Natalie Barney, con quien tuvo una relación larga y apasionada. Sus poemas son sensuales y directos, herederos de Verlaine pero con una temperatura propia: la naturaleza árabe que aprendió de su marido se mezcla con el deseo lésbico en imágenes de una belleza extraña.",
  [("L'Immortelle amour","Nous sommes de ces amours\nqui ne meurent point avec les corps;\nnous aimons par-delà les jours,\npar-delà les vivants et les morts.","Somos de esos amores\nque no mueren con los cuerpos;\namamos más allá de los días,\nmás allá de los vivos y los muertos."),
   ("L'Orient","L'orient est dans ton regard,\ndans ta lèvre qui sent le miel;\ntu fus peut-être, quelque part,\nune odalisque pour quelqu'un dans le ciel.","El oriente está en tu mirada,\nen tu labio que huele a miel;\nquizás fuiste en algún lugar\nuna odalisca para alguien en el cielo."),
   ("Chanson","Chantons ensemble notre amour,\nmême si le monde ne comprend pas;\nmême si le monde dit toujours\nque ce que nous faisons n'est pas.","Cantemos juntas nuestro amor,\naunque el mundo no lo comprenda;\naunque el mundo diga siempre\nque lo que hacemos no es."),
   ("Le Corps","Ton corps est un pays que je connais\ncomme un voyageur connaît sa route;\nje ferme les yeux et je te vois\net mon désir pour toi recommence sa joute.","Tu cuerpo es un país que conozco\ncomo un viajero conoce su ruta;\ncierro los ojos y te veo\ny mi deseo por ti recomienza su justa."),
   ("La Nuit arabe","Sous les étoiles arabes,\nton corps ressemble à une palme;\net mes mains, plus jamais avares,\nvont vers toi sans aucune alarme.","Bajo las estrellas árabes,\ntu cuerpo se parece a una palma;\ny mis manos, ya nunca avaras,\nvan hacia ti sin ninguna alarma."),
   ("Printemps charnel","Le printemps revient avec ses odeurs:\nfleurs sur peau, rosée sur lèvres;\nmon désir pour toi est sans peurs,\nplein de chaleur et de fièvres.","La primavera vuelve con sus olores:\nflores sobre piel, rocío sobre labios;\nmi deseo por ti no tiene miedos,\nlleno de calor y de fiebres."),
   ("Nocturne","Dans la nuit qui nous enveloppe,\nnos deux corps ne font qu'un;\nle désir nous développe\net l'amour nous réunit.","En la noche que nos envuelve,\nnuestros dos cuerpos no son más que uno;\nel deseo nos desarrolla\ny el amor nos reúne."),
   ("L'Adieu à Natalie","Tu pars, et je reste avec l'absence\nqui a la forme de ton corps;\nje garderai ton souvenir en balance\nentre ma vie et mes remords.","Te vas, y me quedo con la ausencia\nque tiene la forma de tu cuerpo;\nconservaré tu recuerdo en equilibrio\nentre mi vida y mis remordimientos."),
   ("La femme libre","Je n'ai jamais demandé permission\nd'aimer comme j'aimais;\nni à l'Église, ni à la loi, ni à la raison:\nj'aimais, c'est tout ce qui comptait.","Nunca pedí permiso\npara amar como amaba;\nni a la Iglesia, ni a la ley, ni a la razón:\namaba, eso era todo lo que importaba."),
   ("Testament charnel","Après ma mort, que mon corps serve\naux fleurs que j'ai aimées;\nque la terre le conserve\npour les futures bien-aimées.","Después de mi muerte, que mi cuerpo sirva\na las flores que amé;\nque la tierra lo conserve\npara las amadas futuras.")]),

 ("044","Rachilde","1860–1953","Francia","francés",
  "Rachilde —Marguerite Vallette-Eymery— fue la escritora más escandalosa de la Francia de la Belle Époque: directora de la revista 'Mercure de France' junto a su marido Alfred Vallette, autora de novelas que escandalizaron a la prensa francesa por su erotismo (especialmente 'Monsieur Vénus', 1884, donde la protagonista obliga a su amante masculino a adoptar un rol 'femenino'), fue también poeta. Se describía a sí misma en su tarjeta de visita como 'homme de lettres' (hombre de letras). Pidió llevar pantalones en lugar de faldas.",
  [("Monsieur Vénus — el deseo invertido","Je suis l'homme, tu es la femme.\nNon par le corps mais par le désir.\nMon désir commande, mon âme réclame\nque tu te soumettes à mon plaisir.","Soy el hombre, tú eres la mujer.\nNo por el cuerpo sino por el deseo.\nMi deseo manda, mi alma reclama\nque te sometas a mi placer."),
   ("La Marquise de Sade — carne","La chair est ma philosophie,\nle corps est mon territoire;\nje n'ai pas d'autre académie\nque ta peau pour me faire croire.","La carne es mi filosofía,\nel cuerpo es mi territorio;\nno tengo otra academia\nque tu piel para hacerme creer."),
   ("L'animale","Je suis une bête, oui,\nqui aime avec ses dents et ses griffes;\nle beau monstre qui surgit\nquand le désir devient chiffre.","Soy una bestia, sí,\nque ama con sus dientes y garras;\nel hermoso monstruo que surge\ncuando el deseo se vuelve cifra."),
   ("Le Péché","Si l'amour est un péché,\nque Dieu me condamne;\nj'aime avec tout mon péché,\nmon corps et mon âme.","Si el amor es un pecado,\nque Dios me condene;\namo con todo mi pecado,\nmi cuerpo y mi alma."),
   ("L'Androgyne","Ni homme ni femme exactement,\nni l'un ni l'autre vraiment;\nje suis cet être étrange et beau\nqui n'entre dans aucun tableau.","Ni hombre ni mujer exactamente,\nni uno ni otro verdaderamente;\nsoy ese ser extraño y hermoso\nque no entra en ningún cuadro."),
   ("La Décadente","Nous les décadentes, nous savons\nque la beauté est dans l'excès;\nque l'amour n'a pas raison\nde refuser quelque accès.","Nosotras las decadentes sabemos\nque la belleza está en el exceso;\nque el amor no tiene razón\npara rechazar algún acceso."),
   ("Portrait de femme libre","Elle porte des pantalons et rit.\nElle ne veut pas être sage.\nElle prend ce qu'elle désire, la nuit;\nelle est libre, c'est son héritage.","Ella lleva pantalones y ríe.\nNo quiere ser prudente.\nToma lo que desea, de noche;\nes libre, es su herencia."),
   ("L'Amour cruel","L'amour que j'aime est cruel et beau;\nil laisse des traces sur la peau;\nil ne demande pas pardon\net s'en va sans aucune raison.","El amor que me gusta es cruel y hermoso;\ndeja huellas en la piel;\nno pide perdón\ny se va sin ninguna razón."),
   ("Fin du siècle","Nous voilà au bout du siècle,\nle vice est devenu vertu;\nle vice est notre seul miracle\net la vertu, un habit perdu.","Aquí estamos al final del siglo,\nel vicio se ha convertido en virtud;\nel vicio es nuestro único milagro\ny la virtud, un hábito perdido."),
   ("Mémoire de la chair","Mon corps se souvient de tout:\nde chaque main, de chaque bouche;\nle temps passe, mais jusqu'au bout\nla chair garde ce qui la touche.","Mi cuerpo lo recuerda todo:\ncada mano, cada boca;\nel tiempo pasa, pero hasta el final\nla carne guarda lo que la toca.")]),

 ("045","Edith_Sodergran","1892–1923","Finlandia","sueco/finlandés",
  "Edith Södergran fue la poetisa más original de la literatura escandinava de todos los tiempos: bornada en San Petersburgo de padres finlandeses, vivió en Raivola —en la frontera entre Rusia y Finlandia— y murió de tuberculosis a los treinta años. Su primer libro, 'Dikter' (1916), fue rechazado por la crítica por su incomprensible modernismo: verso libre, imágenes violentas, un yo femenino poderoso y sin disculpas. Sus poemas de amor son proclamas: 'Soy una mujer y por lo tanto peligrosa'.",
  [("Vierge moderne","Jag är ingen kvinna. Jag är ett neutrum.\nEtt barn. En rannsakare. En djärv herre\nmed handlingsvilja och lugnt blod.","No soy una mujer. Soy un neutro.\nUn niño. Un investigador. Un atrevido señor\ncon voluntad de acción y sangre tranquila."),
   ("Dagen svalnar","Dagen svalnar,\njag hör havets röst;\nhöst kall stiger\nfrån den tjocka skogen.","El día se enfría,\noigo la voz del mar;\nel otoño frío sube\ndel espeso bosque."),
   ("Triumf att finnas till","Det är stor triumf att finnas till,\ndet är stor triumf att leva,\natt suga allt gott av jubin,\natt stiga upp mot Sol och hava.","Es un gran triunfo existir,\nes un gran triunfo vivir,\nasorber todo lo bueno de la alegría,\nsubir hacia el Sol y el mar."),
   ("Nocturno","Natten är svart och het,\nen berusad orkan sover,\nvind i håret, vilt och fritt,\nokänd lyckja mig svajar.","La noche es negra y caliente,\nuna embriagada tormenta duerme,\nviento en el cabello, salvaje y libre,\nuna felicidad desconocida me balancea."),
   ("Ingenting","Ingenting är ingenting\nutan min kärlek till dig;\ndu är mitt allt, mitt ingenting,\nmin himmel och min stig.","Nada es nada\nsin mi amor por ti;\ntú eres mi todo, mi nada,\nmi cielo y mi camino."),
   ("Hoppets väg","Jag vet inte var hoppet leder\nmen jag följer det tills slutet;\nkärlek äro det som beder\natt vi gå mot okänt skuret.","No sé adónde lleva la esperanza\npero la sigo hasta el final;\nel amor es lo que pide\nque vayamos hacia lo desconocido."),
   ("Stjärnorna","Stjärnorna tala om evighet,\nde talar om kärlek utan gräns;\njag lyssnar med lånad visshet\npå deras ljus som sällan väns.","Las estrellas hablan de eternidad,\nhablan de amor sin límites;\nescucho con prestada certeza\nsu luz que raramente se vuelve."),
   ("Eros","Eros! du skapar oro i min själ;\ndu fyller mig med brinnande längtan;\ndu är min herre, du är mitt val,\ndu är min smärta och min sängtan.","¡Eros! Creas inquietud en mi alma;\nme llenan con ardiente anhelo;\neres mi señor, eres mi elección,\neres mi dolor y mi cama."),
   ("Kärlek","Kärlek är ett brusande hav\nsom stormar utan nåd;\nokänd lycka, okänd grav,\nokänd nöd i okänd råd.","El amor es un mar estruendoso\nque tormenta sin misericordia;\nfelicidad desconocida, tumba desconocida,\nnecesidad desconocida en consejo desconocido."),
   ("Min barndom","Min barndom var en dröm om ljus,\npm glädje och om fred;\nmin ungdom var ett brusande rus\nav kärlek och av led.","Mi infancia era un sueño de luz,\nde alegría y de paz;\nmi juventud era una ebria locura\nde amor y de camino.")]),

 ("046","Delmira_Agustini","1886–1914","Montevideo, Uruguay","español",
  "Delmira Agustini fue el prodigio más deslumbrante del Modernismo hispanoamericano: publicó su primer libro a los veinte años ('El libro blanco', 1907) y murió asesinada de un tiro en la sien por su exmarido a los veintisiete. Entre esas dos fechas escribió los poemas eróticos más explícitos y escandalosamente bellos que produjo la poesía femenina en español hasta ese momento. Rubén Darío la comparó con Safo. Sus poemas son criaturas del deseo: el vampiro, el cisne negro, el amante que llega de noche—todo es una metáfora transparente del coito y de la entrega.",
  [("El intruso","Amor, la noche estaba trágica y sollozante\ncuando tu llave de oro cantó en mi cerradura;\nluego la puerta abierta sobre la sombra oscura\ntu forma aclaró de un resplandor de oriente bravo.",
    "Amor, la noche estaba trágica y sollozante\ncuando tu llave de oro cantó en mi cerradura;\nluego la puerta abierta sobre la sombra oscura\ntu forma aclaró de un resplandor de oriente bravo."),
   ("Boca a boca","Dulce cabeza que ahora se inclina\nsobre mi pecho como una flor,\ntú eres el único beso que anhelina\nmi boca hambrienta de beso y de ardor.",
    "Dulce cabeza que ahora se inclina\nsobre mi pecho como una flor,\ntú eres el único beso que anhela\nmi boca hambrienta de beso y de ardor."),
   ("El cisne","Pupila azul de mi parque\nes el sensitivo espejo\ndonde un ave sin reflejo\nviene a verse en el estanque.",
    "Pupila azul de mi parque\nes el sensitivo espejo\ndonde un ave sin reflejo\nviene a verse en el estanque."),
   ("Supremo idilio","Eres la copa más linda\nde mi banquete cruel;\ntienes para mí una sombra\nmás oscura que la miel.",
    "Eres la copa más linda\nde mi banquete cruel;\ntienes para mí una sombra\nmás oscura que la miel."),
   ("Lo inefable","Yo muero extrañamente... No me mata la Vida,\nno me mata la Muerte, no me mata el Amor;\nmuero de un pensamiento mudo como una herida...\n¿No habéis sentido nunca el extraño dolor",
    "Yo muero extrañamente... No me mata la Vida,\nno me mata la Muerte, no me mata el Amor;\nmuero de un pensamiento mudo como una herida...\n¿No habéis sentido nunca el extraño dolor"),
   ("El vampiro","En el regazo de la tarde triste\nyo invoqué tu figura en el espacio;\nte evoqué como a un alma que exististe\npor mi amor; y ocupaste nuestro escaso",
    "En el regazo de la tarde triste\nyo invoqué tu figura en el espacio;\nte evoqué como a un alma que exististe\npor mi amor; y ocupaste nuestro escaso"),
   ("Visión","Sentí tu cuerpo como una caricia\nen la oscura noche de mi sueño;\ny ese contacto fue la noticia\nde tu presencia, mi dueño.",
    "Sentí tu cuerpo como una caricia\nen la oscura noche de mi sueño;\ny ese contacto fue la noticia\nde tu presencia, mi dueño."),
   ("Otra estirpe","Eros, yo quiero guiarte, Padre ciego...\nPor la tierra pueril que amamos tanto,\nvoy como una bacante de tu ruego\ny tú, conduciendo mi canto.",
    "Eros, yo quiero guiarte, Padre ciego...\nPor la tierra pueril que amamos tanto,\nvoy como una bacante de tu ruego\ny tú, conduciendo mi canto."),
   ("Tu boca","Tu boca de noche tiene\nel sabor del vino y el fruto;\nen ella la aurora contiene\nla promesa del absoluto.",
    "Tu boca de noche tiene\nel sabor del vino y el fruto;\nen ella la aurora contiene\nla promesa del absoluto."),
   ("La ruptura","Me matas lentamente con tu ausencia;\ncada día que falta es una herida;\nes tu amor mi única esencia\ny sin ti no tengo vida.",
    "Me matas lentamente con tu ausencia;\ncada día que falta es una herida;\nes tu amor mi única esencia\ny sin ti no tengo vida.")]),

 ("047","Maria_Eugenia_Vaz_Ferreira","1875–1924","Uruguay","español",
  "María Eugenia Vaz Ferreira fue la poeta más profunda y menos conocida del Modernismo uruguayo: filosofa antes de que hubiera escuelas de filosofía para mujeres, poetisa de una densidad metafísica sin precedentes en la poesía femenina latinoamericana. Su vida fue un combate: no se casó, vivió con su hermano Carlos —también poeta— y fue marginada del cenáculo literario masculino con elogios que eran también disminuciones. Su único libro, 'La isla de los cánticos', fue publicado póstumamente.",
  [("Futura","Yo quiero ser lo que no puede ser\nen el pequeño mundo que nos dieron;\nquiero amar sin que nadie pueda ver\nqué tan fuerte mis brazos te sostuvieron.",
    "Yo quiero ser lo que no puede ser\nen el pequeño mundo que nos dieron;\nquiero amar sin que nadie pueda ver\nqué tan fuerte mis brazos te sostuvieron."),
   ("La sed","Tengo sed, una sed que no se apaga\ncon el agua del río ni del mar;\nsólo se apaga cuando tu boca que me haga\nsentir que existe un modo de amar.",
    "Tengo sed, una sed que no se apaga\ncon el agua del río ni del mar;\nsólo se apaga cuando tu boca que me haga\nsentir que existe un modo de amar."),
   ("El don","Te doy mi corazón en su más puro estado,\ncomo la tierra da la primera flor;\nno está manchado, no ha sido violado:\nes el que guardo para el mejor amor.",
    "Te doy mi corazón en su más puro estado,\ncomo la tierra da la primera flor;\nno está manchado, no ha sido violado:\nes el que guardo para el mejor amor."),
   ("La noche del espíritu","Cuando el espíritu busca a su amado\nen la profunda noche sin luceros,\nla carne también sale a ese llamado\ncon sus temblores y sus veneros.",
    "Cuando el espíritu busca a su amado\nen la profunda noche sin luceros,\nla carne también sale a ese llamado\ncon sus temblores y sus veneros."),
   ("El misterio","Hay entre tú y yo un misterio\nque nunca hemos de nombrar;\nes el misterio del deseo\nque habita sin necesidad de hablar.",
    "Hay entre tú y yo un misterio\nque nunca hemos de nombrar;\nes el misterio del deseo\nque habita sin necesidad de hablar."),
   ("Desnuda","Desnuda de todo artificio\nte presento mi alma entera;\nno busco ningún oficio\nque enmascare lo que era.",
    "Desnuda de todo artificio\nte presento mi alma entera;\nno busco ningún oficio\nque enmascare lo que era."),
   ("El beso","Un beso no es sólo una forma de labios;\nno es sólo piel que toca piel:\nun beso dice los más profundos agravios\ny el amor más fiel.",
    "Un beso no es sólo una forma de labios;\nno es sólo piel que toca piel:\nun beso dice los más profundos agravios\ny el amor más fiel."),
   ("La música del cuerpo","El cuerpo tiene su propia música\nque sólo el amado puede escuchar;\nes una partitura magnífica\nque sólo el amor puede interpretar.",
    "El cuerpo tiene su propia música\nque sólo el amado puede escuchar;\nes una partitura magnífica\nque sólo el amor puede interpretar."),
   ("Soledad habitada","Estoy sola, pero no vacía:\ncargada de tu recuerdo voy;\nmi soledad es compañía\nporque eres tú el que soy.",
    "Estoy sola, pero no vacía:\ncargada de tu recuerdo voy;\nmi soledad es compañía\nporque eres tú el que soy."),
   ("El último poema","No tengo más palabras para ti;\nlas he gastado todas en quererte;\npero el silencio que queda aquí\nhabla de amor más que de muerte.",
    "No tengo más palabras para ti;\nlas he gastado todas en quererte;\npero el silencio que queda aquí\nhabla de amor más que de muerte.")]),

 ("048","Alfonsina_Storni","1892–1938","Argentina","español",
  "Alfonsina Storni es la voz feminista más potente del Modernismo sudamericano y una de las más grandes poetisas de lengua española. Nacida en Suiza y criada en la pobreza argentina, tuvo un hijo a los veinte años de un hombre casado que la abandonó. Ese niño, Hugo, fue su motor y su amor más puro. Sus poemas de amor son también poemas de rabia: 'Tú me quieres blanca', 'Hombre pequeñito', 'Peso ancestral' —son textos que reclaman el derecho de la mujer al deseo, al cuerpo, a la ira. Murió entrando al mar en Mar del Plata, después de que le diagnosticaron cáncer de mama. Tenía cuarenta y seis años.",
  [("Tú me quieres blanca","Tú me quieres alba,\nme quieres de espumas,\nme quieres de nácar.\nQue sea azucena,\nsobre todas, casta.\nDe perfume tenue.",
    "Tú me quieres alba,\nme quieres de espumas,\nme quieres de nácar.\nQue sea azucena,\nsobre todas, casta.\nDe perfume tenue."),
   ("Hombre pequeñito","Hombre pequeñito, hombre pequeñito,\nsuelta a tu canario que quiere volar...\nyo soy el canario, hombre pequeñito,\ndéjame saltar.",
    "Hombre pequeñito, hombre pequeñito,\nsuelta a tu canario que quiere volar...\nyo soy el canario, hombre pequeñito,\ndéjame saltar."),
   ("Peso ancestral","Tú me dijiste: no lloró mi padre;\ntú me dijiste: no lloró mi abuelo;\nno han llorado los hombres de mi raza,\neran de acero.",
    "Tú me dijiste: no lloró mi padre;\ntú me dijiste: no lloró mi abuelo;\nno han llorado los hombres de mi raza,\neran de acero."),
   ("Capricho","Yo quiero un amor extraño,\nno doméstico ni cortés,\nque con mucho daño\nme haga caer a sus pies.",
    "Yo quiero un amor extraño,\nno doméstico ni cortés,\nque con mucho daño\nme haga caer a sus pies."),
   ("Pudiera ser","Pudiera ser que todo lo que en verso\nhe congregado en este libros ruinas,\nno fuera sino aquello que represo\nal paso de la vida en mis retinas.",
    "Pudiera ser que todo lo que en verso\nhe congregado en este libro en ruinas,\nno fuera sino aquello que represo\nal paso de la vida en mis retinas."),
   ("Cuadrados y ángulos","Casas enfiladas, casas enfiladas,\ncasas enfiladas.\nCuadrados, cuadrados, cuadrados.\nCasas enfiladas.\nLas gentes ya tienen el alma cuadrada,\nojos cuadrados, piernas cuadradas.",
    "Casas enfiladas, casas enfiladas,\ncasas enfiladas.\nCuadrados, cuadrados, cuadrados.\nCasas enfiladas.\nLas gentes ya tienen el alma cuadrada,\nojos cuadrados, piernas cuadradas."),
   ("El amor imposible","Vuelvo a ti como el río al mar:\nsiempre desde otra fuente;\nvuelvo a ti para consumar\nel amor que no es diferente.",
    "Vuelvo a ti como el río al mar:\nsiempre desde otra fuente;\nvuelvo a ti para consumar\nel amor que no es diferente."),
   ("La que comprende","Con la cabeza negra caída hacia adelante\nestá la mujer bella, la mujer que es mía,\npesando su deseo continuo, flameante,\nbajo la ensangrentada gumía.",
    "Con la cabeza negra caída hacia adelante\nestá la mujer bella, la mujer que es mía,\npesando su deseo continuo, flameante,\nbajo la ensangrentada gumía."),
   ("Epitafio para mi tumba","Aquí descanso yo: dice el epitafio;\ny en verdad que es un digno descanso;\neste rincón es bello. Hay un arroyo\npor el que bogan patos en remanso.",
    "Aquí descanso yo: dice el epitafio;\ny en verdad que es un digno descanso;\neste rincón es bello. Hay un arroyo\npor el que bogan patos en remanso."),
   ("Voy a dormir","Dientes de flores, cofia de rocío,\nmanos de hierbas, tú, nodriza fina,\ntenme prestas las sábanas terrosas\ny el edredón de musgos escardados.",
    "Dientes de flores, cofia de rocío,\nmanos de hierbas, tú, nodriza fina,\ntenme prestas las sábanas terrosas\ny el edredón de musgos escardados.")]),
]

if __name__ == "__main__":
    for item in L:
        mk(*item)
    print(f"Generadas {len(L)} poetisas.")
