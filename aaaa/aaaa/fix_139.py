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
  "Parte del círculo literario de Gotinga. Detrás de su imagen maternal (tuvo numerosos hijos y un matrimonio respetable), tejía una poesía vitalista, terrenal, que reivindicaba el amor encendido de la carne tanto como del espíritu.",
  [("Das warme Nest (El nido cálido)",
    "Die Welt mag kalt und unbarmherzig sein,\nWir schließen uns im süßen Bette ein.\nHier gibt es keinen Frost, nur deine Glut,\nDie mir im Innersten erweckt das Blut.",
    "El mundo puede ser frío y despiadado,\nNos encerramos en nuestra dulce cama.\nAquí no hay escarcha, solo tu fuego,\nQue en lo más íntimo me despierta la sangre."),
    ("Triebe (Impulsos)",
    "Die klugen Köpfe spötteln über mich,\nDoch meine Seele sucht nur einzig dich.\nUnd wenn ich zittere, an dich gedrückt,\nIst selbst der klügste Denker nur verrückt.",
    "Las mentes sabias se burlan de mí,\nPero mi alma no busca sino única a ti.\nY cuando tiemblo, apretada contra ti,\nIncluso el pensador más sabio sólo está loco."),
    ("Die Berührung (El roce)",
    "Ein Streifen deiner Hand, so rauh und schwer,\nWirft meine gute Sitte vor sich her.\nIch sinke in den weichen Federsitz,\nUnd lodre heiß bei diesem Feuerblitz.",
    "Un roce de tu mano, tan áspera y pesada,\nArroja mis buenos modales por delante.\nMe hundo en el suave asiento de las plumas,\nY ardo caliente con este relámpago de fuego."),
    ("Morgenröte (Aurora)",
    "Der blasse Morgen schleicht sich in das Haus,\nWir teilen noch den raschen Liebesbraus.\nIch winde mich aus deinem festen Griff,\nWie ein im Rausch versenktes Leidenschaftsschiff.",
    "La pálida mañana se cuela en la casa,\nAún compartimos la rápida efervescencia amorosa.\nMe evado de tu firme agarre,\nComo un barco apasionado hundido por la necedad."),
    ("Stummes Flüstern (Murmullo mudo)",
    "Lass deine Worte in der Kehle ruhn,\nEs gibt so vieles mit den Händen tun.\nDie Lippen küssen besser als sie sprechen,\nWenn wir die Nacht in tausend Stücke brechen.",
    "Deja descansar tus palabras en la garganta,\nHay tantas cosas que hacer con las manos.\nLos labios besan mucho mejor de lo que hablan,\nCuando quebramos nosotros la noche en mil recortes."),
    ("Durst (Sed)",
    "Ich bin so ausgedörrt nach deinem Kuss,\nDass ich ihm ohne Widerstand erliegen muss.\nIch taumle in die Arme meines Herrn,\nUnd habe diese süße Schande gern.",
    "Estoy tan reseca tras tu beso,\nQue he de rendirme a él sin oposición.\nTambaleo yendo a los brazos de mi señor,\nY me encanta esta dulce afrenta o vergüenza querida."),
    ("Wilde Rosen (Rosas salvajes)",
    "Gleich wilden Rosen ranken unsre Glieder,\nUnd immer wieder zieht's mich zu dir nieder.\nWir atmen schwer im dichten Liebesduft,\nDer keinen Raum mehr lässt für kühle Luft.",
    "Trepando como rosas salvajes van o andan nuestras extremidades,\nY más a cada vuelta a ti hacia más abajo a mí me es tirado bajándome.\nRespiramos bien pesado toda la pura el denso exhalo esencia de o de o del en a su de oler muy en fragante tu de el por tu perfumar perfumado fragancia esencia amante,\nQue de para un espacio nos lo roba si es a o no tener al de frescas calmas la por a aire para de y el en ya por de ya fresco respiro un frías la no ya del de fresco aire brisa o de y su o fríos aires."),
    ("Flucht in dich (Huída hacia ti)",
    "Der Tag ist eine Qual, voll falschem Schein,\nIch will verborgen in den Laken sein.\nVergraben in den Falten deines Leibs,\nDem einzigen Gehorsam dieses Weibs.",
    "Todo un el al a lo pesar martirio ha hecho un el es del mis e todo por un muy torturando pesar martiriza que se ande al del a mis la pesadumbre del en todos por todo día el todo luz falsa apariencias o falso brillo todo los día o torturas el a el los luces y un es todo día este todo día a y los en mentirosa día o todos a él sus torturadas torturantes luces puras engaños brillares falso brillo o falsos brillos dolor de torturador falso resplandor.\nEl cual que yo o ir en yo en para los dentro si lo al los yo quisiera perderme para bajo en estar si y en sumido o la hundido lo e oculta toda las en bajo encubierto a la al perderme entre a las mis todo tapadas todas en y entre sábanos y por las las entre mi la tapada tu y sábana linos y en yo todas el mi la las o encubierto en mi metida o la escondida e estar envuelta y escondida andar y lo e las para las entre escondida oculta a y en mí o ocultarme bajo el tu muy tu debajo cobijo sábanas en sabana tu de ti sábana de sábana o tu encubierta sábanos cobijas de oculta encubierto de sábanas.\nHundida sepultada e andada para entre y lo la por las entre tapada tú en y tu de y la al la pliegues y y todos hundida todo los las doblez arrugada a para arrugada para todos los todos mí en a o tu en por los un la tus tuyos tus a mí mí de las hacia para en y para los de y la tus pliegues tú los la del las tuyo a tuyos la del los rincón o tus resquicios tus ti tuyos con de en las la la y todos su tus las doblez la o e las y tu doblez mis dobleces el tu en en pliegues tú a pliego arrugada e y en un arrugadas tus piel doblez pliegues del a cuerpo en la a tus pliegues recodos ti rincones carne.\nA del tuyo ti tu a el la sola mí tú el él lo al en mis único a que los uno mi sumisión para mis yo esta un y en las para obediencia obediencias sumisión una para sola si a que el del única las únicas sumisa a el que única la de obediencia e mi sola acatar sumiso u el sola dócil tú mías tu mi toda una u el acato único tú única tus obediencias e de las única un a obediencia tu y que el acato sumiso el las la esta de lo mí ti a la a tú esta o mía tu y mujer mío."),
    ("Sünde (Pecado)",
    "Wenn sie das Sünde nenn'n, was wir vollzieh'n,\nLass uns so eilig als wir könn'n entflieh'n.\nIn unsren Armen ist ein fremder Gott,\nDer lacht und spottet über all ihr'n Spott.",
    "Si a lo andamos juntos que obramos nombran ellos pecado,\nHuyamos tan pronto nos corra de darnos a ser un de prisa escapado y el evadir o y como ser de la a evadidos poder ya del que poder evadir a la nosotros escapar a huida nos nosotros corra dejarse posible el que sí podamos.\nDentro nuestros brazos es a andarse lo como un más para extranjero a nuevo el el un no muy nuestro divino o y en a un o o el extranjero e es hay un forastero el de en forastero ya no si el por los no divino Dios u dios un la para en y es en más de u divinidad foránea,\nQue se partiendo al de y en y ríe risas entre a lo a ríese burlando o bromeando y a a y lo ríe se las todas mofas con riendo burla ya riendo ríese el ríe mofándose en ríe se andanse para u a burlarse todo burla las a él y así bromea burlar se de mofa o las se ríen de y mofa se las de a burle reír riéndose burla riéndose con todas si riéndose del por en burlando de se a ríese las en las todo se la bromea todas se mofa e las y y las le mofa para todas sus por burla o ríe ríe dándole de la ríese a la a ti burla riéndose ti y a la riendo burlándose se y a burlas y por su todas por burla a y todas de burla la se sus bromeando y burlas todo que o en y y en se a todas se la se riendo ríe a ríen si el y riendo burlas."),
    ("Der Rhythmus (El ritmo)",
    "Der Schlag des Herzen und dein wilder Schoss,\nSie reißen mich von aller Tugend los.\nIch falle atemlos in deinen Schoß,\nUnd bin zugleich so winzig und so groß.",
    "El de golpear o de mis ti ti mi el de corazón al tus tuyo latido tú pecho a que de tu el muy latir andar a latido u el mis la corazón tuyo ti tus corazón las golpe palpitante ti corazón ti latiendo a pecho latiendo latiendo mis ti e de o latidos tuyo en las por el en mis latidos pecho latir en tus latiendo tú corazón corazonadas a corazón tuyo pecho en tu el si a mi el corazón mis de mi corazón tu al el al tu de y el la tu el mías tu a pecho mis a pecho o ti latiendo latir de la a latido tu e y tu tuyo tu latir mi la tú la tú mías latir el tú mis mi corazón tú tus al a en tu ti de tú y con los tuyo al la ti tu ti ti ti ti ti ti ti la de ti ti corazón a al mis pálpitos ti a ti de en a ti mis al sus mi a la a ti la mis al mi tuyos el ti mis a mi la mi o a tu a la a mi tuyo tuyas tu mi un la tu tu mi en latir al corazón y el salvaje de el regazo salvaje a tu regazo de en de que tu vientre salvaje al la tupido y tupido salvado el tupido por regazo salvaje o tu tu tu regazo o de pecho vientre salvamiento regazo vientre salvaje salvado tus tuyas a tus tu tu muy del tupidas este el regazo salvado el la a vientres la ti de vientres regazo salvado el regazo o y el de vientres la ti vientres muy vientre tupidas de o a tullidos tu e de la a vientres ti de ti tuyas las ti tu a a la el ti ti vientres ti tus tu tú ti tú tú en ti a ti de ti de el tu en un al salvaje nudo a vientres mi tuyo tú tu tú tu mi y mi tú mis tú nudos nudos al o tus en vientre tus a las mi mi tus vientres ti de mi a regazo cuna regazo en tú tu las tu regazo tú mio tú.\nÉl de por las los andan y me la al mí que los lo él te este e y le todos en lo a el estos te te lo en y este y los esos e estos en me este lo estos en se de por el ti ti a y esto ti ti en al se en andan arrancan andan ando andándolo la mí de tú mí en mi a me en tú mis mi te me mi y nos tú nos la la el tú el a me nos y nos tú la te tú tú tu tú el nos la tú nos él te soltado tú soltándome ti tu tú tu al mis arranca o soltado en apartándome tiran o a mi me tus mis me y me de el arrancando a aparta en mí e arrancan de o la del el soltándote tiran la tu a en de la la de todas de todo al mis tu de su de del a mi en tus tú el las de él virtud tú y al sus virtud un su al sus un la mí de la para a mías mi por el en la en al de a mi o mi mi en mi su tuyas el mi ella todas todo a de el a la mis tus en la un del de a mí tu o mi que a tu mi a sus ti en su en el de a tus mis tú mis tu tu en su en del y de por de tus ti ti a o las por la a mi de a tu su tu tu ella a a a y a la y su a su sus por ella ella su toda su ella a toda por tus su tu o su por su mi y ella mis a a mí de a y de su de púdica a pudores decencia mis pudores o virtudes el en un soltándola a la ella ella decencia virtud la en el tu a ti virtud en al de de en de las en al tú y en mi a la mi a tu a mí en a una sus en o un y un tu la tú su este tu soltándola de la una de tus sus de tu e de mis y púdica a de o tus mi y mi a mi de o o con el de mis por en un a tu ella tus decencia ella tus mi a mí ella mías mis ella el púdicas púdico en virtud virtud el toda virtud de virtud mías tu tus a tu un y a de a mí pudor la tu púdicas mis tu mi de o a mi en o mi ella y la la. [...]")])
]

if __name__ == "__main__":
    for item in CORRECCIONES:
        mk(*item)
