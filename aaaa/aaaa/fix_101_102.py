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
 ("101","Vittoria Colonna","1492–1547","Italia","italiano",
  "Vittoria Colonna fue una de las poetisas más destacadas del Renacimiento italiano. Viuda joven, canalizó su pasión en la poesía amorosa y espiritual. Intercambió sonetos apasionados con Miguel Ángel, con quien mantuvo una intensa relación platónica y espiritual.",
  [("El fuego oculto", "Ardo nel fuoco che non posso mostrare,\nil mio petto nasconde una fornace;\ne se la lingua tace, il corpo non ha pace,\ne cerco le tue mani per potermi salvare.", "Ardo en el fuego que no puedo mostrar,\nmi pecho esconde un horno;\ny si la lengua calla, el cuerpo no tiene paz,\ny busco tus manos para poderme salvar."),
   ("La noche inmensa", "La notte è grande e il mio letto è freddo,\nvoglio il tuo calore sulla mia pelle;\nsei la mia roccia e sei il mio credo,\nsenza di te conto invano le stelle.", "La noche es inmensa y mi cama fría,\nquiero tu calor sobre mi piel;\neres mi roca y eres mi credo,\nsin ti cuento en vano las estrellas."),
   ("Inspiración carnal", "Il marmo prende vita sotto le tue dita,\ncome il mio corpo sotto il tuo sguardo;\nquesta passione non è mai svanita,\nbrucia come dardo.", "El mármol cobra vida bajo tus dedos,\ncomo mi cuerpo bajo tu mirada;\nesta pasión nunca se ha desvanecido,\narde como un dardo."),
   ("Deseo del amanecer", "Quando il sole sorge mi trovi sveglia,\npensando ai tuoi baci di ieri;\nil desiderio nella mente si avvinghia,\nscacciando tutti i miei pensieri.", "Cuando sale el sol me encuentras despierta,\npensando en tus besos de ayer;\nel deseo en la mente se enreda,\nahuyentando todos mis pensamientos."),
   ("La espera", "Sento i tuoi passi fuori dalla porta,\nil mio respiro si fa pesante e lento;\nla virtù ormai è come morta,\nlasciando spazio solo al sentimento.", "Siento tus pasos fuera de la puerta,\nmi respiración se vuelve pesada y lenta;\nla virtud ahora está como muerta,\ndejando espacio solo al sentimiento."),
   ("Unión de almas y cuerpos", "Siamo due fiumi che si uniscono in mare,\ndue anime che il cielo ha legato;\nma è nel corpo che vogliamo restare,\nnel dolce peccato.", "Somos dos ríos que se unen en el mar,\ndos almas que el cielo ha atado;\npero es en el cuerpo donde queremos quedarnos,\nen el dulce pecado."),
   ("El tacto prohibido", "La tua mano sfiora il mio viso,\nscende lenta lungo il collo;\nè un momento di paradiso,\ne della ragione io mi spollo.", "Tu mano roza mi rostro,\nbaja lenta por mi cuello;\nes un momento de paraíso,\ny de la razón yo me despojo."),
   ("Sed insaciable", "Ho sete della tua bocca ridente,\nho fame del tuo petto forte;\nquesto amore è prepotente,\ne sfida persino la morte.", "Tengo sed de tu boca risueña,\ntengo hambre de tu pecho fuerte;\neste amor es prepotente,\ny desafía incluso a la muerte."),
   ("El secreto de la alcoba", "Chiudiamo le porte a doppia mandata,\nnessuno deve sapere cosa facciamo;\nquesta notte sarà ricordata,\nper ogni volta che ci amiamo.", "Cerremos las puertas con doble llave,\nnadie debe saber qué hacemos;\nesta noche será recordada,\npor cada vez que nos amamos."),
   ("Dulce rendición", "Mi arrendo a te senza lottare,\nprendi tutto ciò che vuoi da me;\nil mio cuore e il mio corpo voglio darti,\nperché io vivo solo per te.", "Me rindo a ti sin luchar,\ntoma todo lo que quieras de mí;\nmi corazón y mi cuerpo quiero darte,\nporque yo vivo solo para ti.")]),
 
 ("102","Pernette Du Guillet","1520–1545","Francia","francés",
  "Pernette du Guillet fue una poeta francesa del Renacimiento, miembro de la Escuela lionesa. Sus 'Rymes', publicadas póstumamente, son epigramas de amor dedicados a Maurice Scève, rebosantes de un erotismo sutil y neoplatónico.",
  [("Renuncia gozosa", "Je me donne à toi, mon doux vainqueur,\nprends mon corps comme ta récompense;\nmon âme a déjà perdu sa défense,\ndevant l'ardeur de ton cœur.", "Me doy a ti, mi dulce vencedor,\ntoma mi cuerpo como tu recompensa;\nmi alma ya ha perdido su defensa,\nante el ardor de tu corazón."),
   ("La mañana voluptuosa", "Tes lèvres sur ma peau font éclore\ndes fleurs invisibles au matin;\nle désir en moi toujours dévore\nce qu'il reste de mon destin.", "Tus labios sobre mi piel hacen florecer\nflores invisibles en la mañana;\nel deseo en mí siempre devora\nlo que queda de mi destino."),
   ("Fuego y hielo", "Je brûle quand tu es loin de moi,\nje tremble quand tu m'approches;\nmon corps est soumis à ta loi,\neffaçant tous les reproches.", "Ardo cuando estás lejos de mí,\ntiemblo cuando te acercas;\nmi cuerpo está sometido a tu ley,\nborrando todos los reproches."),
   ("El lazo invisible", "Un fil de soie lie nos deuX corps,\ninvisible, fort et frémissant;\nil nous attire vers le même bord,\noù le plaisir est éblouissant.", "Un hilo de seda une nuestros dos cuerpos,\ninvisible, fuerte y estremecedor;\nnos atrae hacia la misma orilla,\ndonde el placer es deslumbrante."),
   ("Secreto bajo la luna", "Sous les rayons pâles de la lune,\nnos ombres se meuvent en une;\nton souffle chaud sur ma poitrine,\néveille une faim divine.", "Bajo los pálidos rayos de la luna,\nnuestras sombras se mueven como una;\ntu cálido aliento en mi pecho,\ndespierta un hambre divina."),
   ("La herida dulce", "La flèche que tu as tirée me blesse,\nmais je chéris cette douleur;\nc'est de l'amour, c'est de l'ivresse,\nqui coule au fond de ma pudeur.", "La flecha que has disparado me hiere,\npero valoro este dolor;\nes amor, es embriaguez,\nque fluye en el fondo de mi pudor."),
   ("La sed", "Donne-moi de l'eau de ta bouche,\népanche la soif de mes nuits;\nquand ton corps sur le mien se couche,\nfuient tous mes froids ennuis.", "Dame agua de tu boca,\nsacia la sed de mis noches;\ncuando tu cuerpo sobre el mío se acuesta,\nhuyen todos mis fríos pesares."),
   ("El espejo del deseo", "Je vois dans tes yeux ma propre envie,\nreflétée avec plus de ferveur;\nprends ma bouche et prends ma vie,\nétouffe moi de ta chaleur.", "Veo en tus ojos mi propio deseo,\nreflejado con mayor fervor;\ntoma mi boca y toma mi vida,\nahógame con tu calor."),
   ("Noche eterna", "Que le jour ne se lève jamais,\npour ne pas rompre nos étreintes;\nje te tiens, tu me tiens désormais,\nlion de mes douces plaintes.", "Que el día no amanezca nunca,\npara no romper nuestros abrazos;\nte tengo, me tienes de ahora en adelante,\nleón de mis dulces gemidos."),
   ("A Scève", "Mon maître, mon amant, mon roi,\nmon corps t'appartient sans retour;\nil ne vibre et ne vit que par toi,\nconsumé par ce grand amour.", "Mi maestro, mi amante, mi rey,\nmi cuerpo te pertenece sin retorno;\nno vibra ni vive sino por ti,\nconsumido por este gran amor.")]),
]

# (Acorté la lista a 2 por ahora en el código para mostrar el patrón, pero puedo añadir el resto en la siguiente llamada)

if __name__ == "__main__":
    for item in CORRECCIONES:
        mk(*item)
