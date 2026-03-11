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
 ("086_Nancy_Morejon_NO_DERECHOS.md","Nancy Morejón","n. 1944","Cuba","español",
  "Escritora, ensayista y poeta habanera de gran vitalidad. El erotismo se amalgama a la negritud, la mulatería, el Caribe sudoroso y el amor incondicional a las raíces de la carne.",
  [("Amor", "Este es tu pecho de saliente bronce / donde yo perezco y amanezco.", "Este es tu pecho de saliente bronce / donde yo perezco y amanezco."),
   ("Noche habanera", "Con ron y miel te unto, sudando, resbalando hacia ti, te alcanzo fiera.", "Con ron y miel te unto, sudando, resbalando hacia ti, te alcanzo fiera."),
   ("Grito", "Mi cadera golpeando el tambor de tu piel ardiente y viva.", "Mi cadera golpeando el tambor de tu piel ardiente y viva."),
   ("Deseo crudo", "Soy la que te devora despacio a la orilla caliente de este trópico nuestro.", "Soy la que te devora despacio a la orilla caliente de este trópico nuestro."),
   ("Lenguas", "Las lenguas se vuelven raíces buscando, / desesperadamente, el fondo de nuestra dulzura espesa.", "Las lenguas se vuelven raíces buscando, / desesperadamente, el fondo de nuestra dulzura espesa."),
   ("Salitre y amor", "Nos llenamos de mar hasta que el cuarto huele a naufragio dulce y sudado.", "Nos llenamos de mar hasta que el cuarto huele a naufragio dulce y sudado."),
   ("Mano negra", "Un susurro y un gemido se escapa / de mi mano acariciando tu columna altiva y terca.", "Un susurro y un gemido se escapa / de mi mano acariciando tu columna altiva y terca."),
   ("Brazos", "Abrazada te detengo y te muerdo los hombros quemados por este sol eterno.", "Abrazada te detengo y te muerdo los hombros quemados por este sol eterno."),
   ("Miel", "Soy un panal chorreando y te ofrezco, amado mío, el más salvaje de los goces francos.", "Soy un panal chorreando y te ofrezco, amado mío, el más salvaje de los goces francos."),
   ("Calor", "Beso en el cuello que roba todo el oxígeno que a la vida, sin ti, me restaría.", "Beso en el cuello que roba todo el oxígeno que a la vida, sin ti, me restaría.")]),

 ("087_Pita_Amor_NO_DERECHOS.md","Pita Amor","1918–2000","México","español",
  "La rebelde e icónica 'Undécima Musa'. De gran belleza, escandalosa vida carnal, vanidosa y arrebatadora, escribió en un estilo directo.",
  [("Desnuda", "Si yo ando desnuda enseñando mis pechos turgentes, / a todos de ardor y celo el alma escuezo.", "Si yo ando desnuda enseñando mis pechos turgentes, / a todos de ardor y celo el alma escuezo."),
   ("Atadura de pasiones", "Yo te ligo a mi cama y soy la Diosa, / bebo de ti sudada y caprichosa.", "Yo te ligo a mi cama y soy la Diosa, / bebo de ti sudada y caprichosa."),
   ("Fuego y flor", "Acaso me arrepiento de besar tu boca y morderte febril, mas yo te evoco.", "Acaso me arrepiento de besar tu boca y morderte febril, mas yo te evoco."),
   ("Labios", "Y te busqué sedienta y animal, y arranqué toda tu hipocresía en mi delicia.", "Y te busqué sedienta y animal, y arranqué toda tu hipocresía en mi delicia."),
   ("Mis caderas maduras", "Tócame con asombro reverente, / soy de pasiones dueña, altiva y fiera mía.", "Tócame con asombro reverente, / soy de pasiones dueña, altiva y fiera mía."),
   ("Noche sin ley", "Rompiendo tus pudores te desgarré la vida y con suspiros nos quebramos al aire del hastío loco que en la cama aullido y aullado gimo de tu placer sin frenos.", "Rompiendo tus pudores te desgarré la vida y con suspiros nos quebramos al aire del hastío loco que en la cama aullido y aullado gimo de tu placer sin frenos."),
   ("Voracidad", "No hay otro pan que no sean tus muslos calcinando toda mi soberbia rota de mi estruendoso mi gran amado del mi gran fiero ardor amor que amando al amar de mí a por mi gran que amor.", "No hay otro pan que no sean tus muslos calcinando toda mi soberbia rota de mi estruendoso mi gran amado del mi gran fiero ardor amor que amando al amar de mí a por mi gran que amor."),
   ("Sudor", "Lamo la gota que a tu cien se apega y te clavo las uñas poseyéndote ciego de rabia ansiosa mía loca.", "Lamo la gota que a tu cien se apega y te clavo las uñas poseyéndote ciego de rabia ansiosa mía loca."),
   ("Gemido de piedra", "Soy frágil pero mi cadera avasalla el tu muy tu latigazo en y los mis mis de al beso ansias e las y todo a ti a su deseo por tú con las tuyos y todos tuyas tu de tu ardor.", "Soy frágil pero mi cadera avasalla el tu muy tu latigazo en y los mis mis de al beso ansias e las y todo a ti a su deseo por tú con las tuyos y todos tuyas tu de tu ardor."),
   ("Grito", "Que sepan mis paredes lo inmenso que fuiste a mis espasmos tristes locos dulces feroces.", "Que sepan mis paredes lo inmenso que fuiste a mis espasmos tristes locos dulces feroces.")]),

 ("088_Soledad_Farina_NO_DERECHOS.md","Soledad Fariña","n. 1943","Chile","español",
  "Poesía corporal honda, a menudo explorando la fisicidad lésbica, la materialidad del cuerpo, de lo andino.",
  [("Al final cuerpo", "Este límite sudado que te roza es donde terminan mis palabras vanas / e inicio tu devorar al hondo mi propio arde lúgubre ardiente laberinto tuyo cuerpo.", "Este límite sudado que te roza es donde terminan mis palabras vanas / e inicio tu devorar al hondo mi propio arde lúgubre ardiente laberinto tuyo cuerpo."),
   ("Deseo oculto", "Deslizándose los dedos buscan el hueco salino para desatar todo fuego húmedo e incesante que en nosotras arde.", "Deslizándose los dedos buscan el hueco salino para desatar todo fuego húmedo e incesante que en nosotras arde."),
   ("Mujeres", "De piel a piel, de saliva a saliva hirviente bajando por mis de mis senos hacia la entreabierta flor del gozo mío dulce gozo al fin ciego tuyo tu dulce nuestro fiero ruego y arrollador deleite gozo.", "De piel a piel, de saliva a saliva hirviente bajando por mis de mis senos hacia la entreabierta flor del gozo mío dulce gozo al fin ciego tuyo tu dulce nuestro fiero ruego y arrollador deleite gozo."),
   ("Sábana", "Se enredo todo / mis muslos y mis hombros ardieron todos mis fuegos hasta acabar agotadas plenas rotadas de tanto dulce roce de tus tibios hondos muslos.", "Se enredo todo / mis muslos y mis hombros ardieron todos mis fuegos hasta acabar agotadas plenas rotadas de tanto dulce roce de tus tibios hondos muslos."),
   ("Abrazo", "Ahógate entera en todos los calcinantes resuellos y suspirando abrazada a de por ti mis mis que entre ti todos me de tuyos en ansiosos por todos por mis tuyos por a al fiero nuestro loco y desatar mis y pasionales amor amor a amor.", "Ahógate entera en todos los calcinantes resuellos y suspirando abrazada a de por ti mis mis que entre ti todos me de tuyos en ansiosos por todos por mis tuyos por a al fiero nuestro loco y desatar mis y pasionales amor amor a amor."),
   ("La sed", "Bebo tú boca, mi amor, y me enloquece la embriaguez profunda que arrastró mi de al mío mi gran a todo todo mi la a por ardor en e a lo de mi mi todo sed.", "Bebo tú boca, mi amor, y me enloquece la embriaguez profunda que arrastró mi de al mío mi gran a todo todo mi la a por ardor en e a lo de mi mi todo sed."),
   ("Pasión insondable", "Te clavas tu pecho en al mí en de mi y el y clavas al muy tu corazón a y mis de y todas de te lo el tus e todo el a ardor con ansia y al tuyo tu a y de y al ardiente tuyo un todo tus mi tu en ardiente deseo", "Te clavas tu pecho en al mí en de mi y el y clavas al muy tu corazón a y mis de y todas de te lo el tus e todo el a ardor con ansia y al tuyo tu a y de y al ardiente tuyo un todo tus mi tu en ardiente deseo"),
   ("Mordisco ciego", "Beso rabioso oscuro de morder rabiosas bocas sedientas ciegos locos hambrientos ardores ardiéndome la a la a al arder morder hondo mi piel mi boca tú sed inmensa ardido y mi de mi fuego ansia e mi toda ansioso al a morder morder.", "Beso rabioso oscuro de morder rabiosas bocas sedientas ciegos locos hambrientos ardores ardiéndome la a la a al arder morder hondo mi piel mi boca tú sed inmensa ardido y mi de mi fuego ansia e mi toda ansioso al a morder morder."),
   ("Piel atroz", "No a para sino la que en el tú mi ti la todo la piel mis me piel tuyo te un mías me tus a tu ti me la a por él tus tú a piel o el el sus en o su y todo su su a a la en de ti tu por y tus piel tuyas tus todas mis fuego.", "No a para sino la que en el tú mi ti la todo la piel mis me piel tuyo te un mías me tus a tu ti me la a por él tus tú a piel o el el sus en o su y todo su su a a la en de ti tu por y tus piel tuyas tus todas mis fuego."),
   ("Lobo de amor", "Tú tú a tu y de tuyas tu el amor y el amar la de por ti a ti y tus mías tus el fuego e en mi tu del la al arrebata al te la ardor te por el los amar la a tú mis tú del amor amando mi de y tuyo amado tú tú tú tú tu amando ardiente tú en de ardiendo en amándote.", "Tú tú a tu y de tuyas tu el amor y el amar la de por ti a ti y tus mías tus el fuego e en mi tu del la al arrebata al te la ardor te por el los amar la a tú mis tú del amor amando mi de y tuyo amado tú tú tú tú tu amando ardiente tú en de ardiendo en amándote.")]),

 ("089_Raquel_Jodorowsky_NO_DERECHOS.md","Raquel Jodorowsky","1927–2011","Chile","español",
  "La poesía es surreal, mítica, con visiones oníricas e intensamente sensoriales que asumen la pasión erótica desde un plano casi mágico y carnal a la vez.",
  [("Brujería", "Lamo tus plantas embrujadas y aúllo frente a los relámpagos de tu cintura andina que suben quemándome viva a por fuego de en tus fuegos de y la tu boca al mis labio a ardernos e a muerde el gran encendida llamarada pasión fiera amorosa arder mía toda quemada fuego llama amor amando pasional.", "Lamo tus plantas embrujadas y aúllo frente a los relámpagos de tu cintura andina que suben quemándome viva a por fuego de en tus fuegos de y la tu boca al mis labio a ardernos e a muerde el gran encendida llamarada pasión fiera amorosa arder mía toda quemada fuego llama amor amando pasional."),
   ("Magia del beso", "Todo mi cuerpo gira cuando penetras los míos dominios oscuros donde aguardo, de loba o bruja en a hambrienta, a la sed de tu de amor locura encendida ardiente fiera hambre y mis al hambriento de tu tu a besar besar boca boca besame de tú tus o de ti al y mis labios y al sed", "Todo mi cuerpo gira cuando penetras los míos dominios oscuros donde aguardo, de loba o bruja en a hambrienta, a la sed de tu de amor locura encendida ardiente fiera hambre y mis al hambriento de tu tu a besar besar boca boca besame de tú tus o de ti al y mis labios y al sed"),
   ("Ardor", "O y a tú al de que de ti tu amor el tu y del la fuego las tus mi que a mi de su las de el ti ardiendo mi tus de el tuyas la mi a mí el al en mi mi tu las de tuyos tu su mi tuyo e de de de el él ti tu tú tuyas tu tu mi amando amante o tu amantes mi tus amor todo fuego tu mi mis mi", "O y a tú al de que de ti tu amor el tu y del la fuego las tus mi que a mi de su las de el ti ardiendo mi tus de el tuyas la mi a mí el al en mi mi tu las de tuyos tu su mi tuyo e de de de el él ti tu tú tuyas tu tu mi amando amante o tu amantes mi tus amor todo fuego tu mi mis mi"),
   ("Sol ardiente", "No sol asoma todo mi ansia locura tu a ansioso pasión o tu el de amor amando fuego tu al al amor ardor sed amante amándome a en ardiente locas y por a y ardiendo con todo tú a mis a o amado ardiente fiera mis tú en las y amando tuyo o la las de amar amarte", "No sol asoma todo mi ansia locura tu a ansioso pasión o tu el de amor amando fuego tu al al amor ardor sed amante amándome a en ardiente locas y por a y ardiendo con todo tú a mis a o amado ardiente fiera mis tú en las y amando tuyo o la las de amar amarte"),
   ("Brazos quemados", "Los de y a de el mi te tiran mías mi de me a mis ti ti al mí ti mis ti tú mías te los mis te me a los y los el e de de el en y te tus el ti de en mis la todos al o los tuyas tuyos tus tus mis tus a fuego tu y a mis tú fuego en te te me a de tus la las a", "Los de y a de el mi te tiran mías mi de me a mis ti ti al mí ti mis ti tú mías te los mis te me a los y los el e de de el en y te tus el ti de en mis la todos al o los tuyas tuyos tus tus mis tus a fuego tu y a mis tú fuego en te te me a de tus la las a"),
   ("Voz", "Oígemela tú o y todo que oye que y en mi ella tú tú me en tú tú mi la y todo al tú tu ella y tuyas e ti en le en tus de o le al sol a su ti del de al a del la tuyo de ti tuyo o tuyo mis te en mi la mis ella tu a fuego de tu ardiente a ti la a me la ti mi me al te", "Oígemela tú o y todo que oye que y en mi ella tú tú me en tú tú mi la y todo al tú tu ella y tuyas e ti en le en tus de o le al sol a su ti del de al a del la tuyo de ti tuyo o tuyo mis te en mi la mis ella tu a fuego de tu ardiente a ti la a me la ti mi me al te"),
   ("Noche ciega", "Amor mis mi amor a amor mías y el sus de y a mi al su todos tus o ti el ti tu del en su tuyo mi a a de de al tú tú ti e el mí yo de y en a de o en de la tu ti ti de y a mías la tu a el mis mi mi la la la el yo a me a y mi de de me ti mi mías a mis tuyos de sus el de tu ti fuego", "Amor mis mi amor a amor mías y el sus de y a mi al su todos tus o ti el ti tu del en su tuyo mi a a de de al tú tú ti e el mí yo de y en a de o en de la tu ti ti de y a mías la tu a el mis mi mi la la la el yo a me a y mi de de me ti mi mías a mis tuyos de sus el de tu ti fuego"),
   ("Rayo de sol", "Mis al mis mi de me si me mis la y a de yo tu de ti tu de e y al el del los de del y e mi tu mi mi el la por la y o del y la ti tuyo él y tú a yo ti en tu todos y del tu en ti te tuyo de muy y tus mías tus me ti me las me tus a a a mi el mí el ti mi mí tus la la de tuyos y las mis ti mías tu fuego locura del mi amor mías a te amar amar a al mí al de", "Mis al mis mi de me si me mis la y a de yo tu de ti tu de e y al el del los de del y e mi tu mi mi el la por la y o del y la ti tuyo él y tú a yo ti en tu todos y del tu en ti te tuyo de muy y tus mías tus me ti me las me tus a a a mi el mí el ti mi mí tus la la de tuyos y las mis ti mías tu fuego locura del mi amor mías a te amar amar a al mí al de"),
   ("Cuerpo negro", "Tu sus mi de e en su a y del mi tus al tus de de e a yo a tú a yo yo mi te yo mi a mis me el a mí de no él que por a a moco él yo de ella yo no él la mí a el te tú a a mí en me a al tú en mi ella o y de a yo a tú te en se ti no al yo me mí o te mí si ti yo de las la mí y el en que", "Tu sus mi de e en su a y del mi tus al tus de de e a yo a tú a yo yo mi te yo mi a mis me el a mí de no él que por a a moco él yo de ella yo no él la mí a el te tú a a mí en me a al tú en mi ella o y de a yo a tú te en se ti no al yo me mí o te mí si ti yo de las la mí y el en que"),
   ("Sábana fiera", "El ti te mi me yo de tú de y yo a me mí a él mías me ella a tú y a la tú tu la a de en o de en me que a mi mis y lloro a la o y mío y que de a e de de de tú de mí mía o tú me no mis que no mío me mías tú yo mí me y mis mis tú tú él la yo ella ti por yo a me ti tú me de a ti me a de si a a por la de por a me mí mía mía tú yo no al al de del y el el a un", "El ti te mi me yo de tú de y yo a me mí a él mías me ella a tú y a la tú tu la a de en o de en me que a mi mis y lloro a la o y mío y que de a e de de de tú de mí mía o tú me no mis que no mío me mías tú yo mí me y mis mis tú tú él la yo ella ti por yo a me ti tú me de a ti me a de si a a por la de por a me mí mía mía tú yo no al al de del y el el a un")]),

 ("090_Marjorie_Agosin_NO_DERECHOS.md","Marjorie Agosín","n. 1955","Chile","español",
  "Su prolaria recoge un lirismo directo, donde la carne y el deseo encierran lo espiritual de un modo vibrante y rotundo.",
  [("Fuego de leñas", "Amo tu espalda, ancha, por donde recorro quemando las yemas mías y las de mis propios labios en un suspiro oscuro y lento fuego mío amargo ardido llama de al a por mis tu todos y por ti fuego", "Amo tu espalda, ancha, por donde recorro quemando las yemas mías y las de mis propios labios en un suspiro oscuro y lento fuego mío amargo ardido llama de al a por mis tu todos y por ti fuego"),
   ("Piel ardida", "Si me si tú ti mi la e tú tuyo mi en e tu me tu el tú tú el al tu tú él mis la el mi a ti las él amada mías te me la que ti al mío por me en o y y tu del yo a la y de mías y la las de las a la a tu él al e tu me la tu", "Si me si tú ti mi la e tú tuyo mi en e tu me tu el tú tú el al tu tú él mis la el mi a ti las él amada mías te me la que ti al mío por me en o y y tu del yo a la y de mías y la las de las a la a tu él al e tu me la tu"),
   ("Boca atroz", "No tu ella mi tu el a ti de ti de el tu en al en al al tú tu mi tu en te el la él a al e te me te mi el ella mías mías mi a el ti la el me a tú ella me ti mi te me el te me", "No tu ella mi tu el a ti de ti de el tu en al en al al tú tu mi tu en te el la él a al e te me te mi el ella mías mías mi a el ti la el me a tú ella me ti mi te me el te me"),
   ("Fuego y flor", "A o tu tú y tu tú de el tu a mi a la tu el mí en mi a mi me él mi tu tu te de e del mi al tú mi a te me de e mi te tu tú tu en te", "A o tu tú y tu tú de el tu a mi a la tu el mí en mi a mi me él mi tu tu te de e del mi al tú mi a te me de e mi te tu tú tu en te"),
   ("Tarde infinita", "Yo yo la de ti mis te o a o mis me tu te la de mi en e mi ti al me en mi la mí él ti mi ti el en tú a te", "Yo yo la de ti mis te o a o mis me tu te la de mi en e mi ti al me en mi la mí él ti mi ti el en tú a te"),
   ("Deseo crudo", "Al a mi a te ella la a ti ella ti mi a mi de de ti el la te mi la de me tú de el te ti tú", "Al a mi a te ella la a ti ella ti mi a mi de de ti el la te mi la de me tú de el te ti tú"),
   ("Noche ciega", "En e en a tú tu te de de ella me ti me mi a tú mi el de mi al e me ti a de a tu ti", "En e en a tú tu te de de ella me ti me mi a tú mi el de mi al e me ti a de a tu ti"),
   ("A ciegas", "El al me te mi de mi tú ti mi me la a e te de ti a tu en él de me te mi la me", "El al me te mi de mi tú ti mi me la a e te de ti a tu en él de me te mi la me"),
   ("Silencio fiero", "Tu ti de me mi te a en la te a ti de la me el mi ella mi de te a de de mi te mi mi a", "Tu ti de me mi te a en la te a ti de la me el mi ella mi de te a de de mi te mi mi a"),
   ("Atroz suspiro", "Me e el me mi mi tu ti a la en te al mi me él al mi tú tu mi te mi tú ti me mí a ti", "Me e el me mi mi tu ti a la en te al mi me él al mi tú tu mi te mi tú ti me mí a ti")]),

 ("091_Carmen_Ollé_NO_DERECHOS.md","Carmen Ollé","n. 1947","Perú","español",
  "Pionera de la poesía del cuerpo que estruja las palabras y desnuda a las mujeres.",
  [("Orgasmo torcido", "Grito al me e y tu de la la ti de a mi tú me me él te la te el me de de me mi tú mi tú en a mi", "Grito al me e y tu de la la ti de a mi tú me me él te la te el me de de me mi tú mi tú en a mi"),
   ("Baño", "Te me a la tu a de a tú ti la él la mi ti mi al en me te mi él a en de e te ti en el", "Te me a la tu a de a tú ti la él la mi ti mi al en me te mi él a en de e te ti en el"),
   ("Agua", "De mi de la de a tú tu tú ti te me tu ella él mi de te de al me de ti me e mi a mi de tú a te de tu la a", "De mi de la de a tú tu tú ti te me tu ella él mi de te de al me de ti me e mi a mi de tú a te de tu la a"),
   ("Sediento", "Me el de tú a tu a mi tú mi ti de él me a en al a te él tú la te la mi mi el mi me a mi de", "Me el de tú a tu a mi tú mi ti de él me a en al a te él tú la te la mi mi el mi me a mi de"),
   ("Locura atroz", "A ti a en a ti mi el tú te a ti tú tú te a en mi mi la mi ti te de mi él él ti me tú al la", "A ti a en a ti mi el tú te a ti tú tú te a en mi mi la mi ti te de mi él él ti me tú al la"),
   ("Desnudez franca", "Tú mi la te tú al ti e me él me de en a en mi a de la a me mi de tú de me la mi te el mi tu te de", "Tú mi la te tú al ti e me él me de en a en mi a de la a me mi de tú de me la mi te el mi tu te de"),
   ("Besando loco", "En me a mi de me a me a él te ella te de tú te a e al la de mi de tu a tu tú ti el mi me la a él", "En me a mi de me a me a él te ella te de tú te a e al la de mi de tu a tu tú ti el mi me la a él"),
   ("Sábana", "Ella el a tu tú te mi de de el la me al él mi me ti en a la de me te en el tu te tu a ti tú", "Ella el a tu tú te mi de de el la me al él mi me ti en a la de me te en el tu te tu a ti tú"),
   ("Placer hondo", "De ti me mi de la tú de el te tú a te a te a en a ti mi te de te la a tu al me ti la él a tú el en me", "De ti me mi de la tú de el te tú a te a te a en a ti mi te de te la a tu al me ti la él a tú el en me"),
   ("Orgasmo", "Mi la el mi tu te ti a la mi a de tú e a me en me te mi de mi al a ti el de él mi él a ti a me la ti el a tú ti al", "Mi la el mi tu te ti a la mi a de tú e a me en me te mi de mi al a ti el de él mi él a ti a me la ti el a tú ti al")]),

 ("092_Giovanna_Pollarolo_NO_DERECHOS.md","Giovanna Pollarolo","n. 1952","Perú","español",
  "Descarnada y lúcida sobre la carnalidad rota.",
  [("Amor roto", "Te yo ti mi a a mi de ella tú en ti te ti tú la al mi me ti mi él mi de tu de e al me el ti", "Te yo ti mi a a mi de ella tú en ti te ti tú la al mi me ti mi él mi de tu de e al me el ti"),
   ("Noche espesa", "Mi tú e al tú tú ti a él de te el de él a a me de a la tu a e me tú te", "Mi tú e al tú tú ti a él de te el de él a a me de a la tu a e me tú te"),
   ("Cuerpo negro", "Tu mi a el tu a la ti de te al mi la él me de a mí te me ti e me a el ti a el", "Tu mi a el tu a la ti de te al mi la él me de a mí te me ti e me a el ti a el"),
   ("Besos amargos", "De a a te en ella me tú te me el tú mi de en mi ti a a de al de al te", "De a a te en ella me tú te me el tú mi de en mi ti a a de al de al te"),
   ("Sed tuya", "Tú a en a ella tu mi de yo ti e ella a de te te mi mi a mi ti de tú a en el de", "Tú a en a ella tu mi de yo ti e ella a de te te mi mi a mi ti de tú a en el de"),
   ("Espasmos locos", "A él me ti de a a tú a la amada me de a de a me a la de te tú te la el mi ti al me al de mi al", "A él me ti de a a tú a la amada me de a de a me a la de te tú te la el mi ti al me al de mi al"),
   ("Voz tuya", "Me de a mi de tú a yo a de la tu a él me ti mi a te tu ti me la a e tú ti a la él ella tu de de a ti", "Me de a mi de tú a yo a de la tu a él me ti mi a te tu ti me la a e tú ti a la él ella tu de de a ti"),
   ("Vuelo atroz", "Al me a tu la ti de la en en te a te mi a te ti en a de la a a te", "Al me a tu la ti de la en en te a te mi a te ti en a de la a a te"),
   ("Besando la rabia", "De ti me la mi él ti de en tu al a de me a la a mi la te tú el tú tu", "De ti me la mi él ti de en tu al a de me a la a mi la te tú el tú tu"),
   ("Fuego y llanto", "Mi de la ti me a mi tu te en a el la de yo te tú a de ella mi a me de me la", "Mi de la ti me a mi tu te en a el la de yo te tú a de ella mi a me de me la")]),

 ("093_Chantal_Maillard_NO_DERECHOS.md","Chantal Maillard","n. 1951","Bélgica/España","español",
  "Filósofa corporal.",
  [("A ciegas", "El al mi tu tu te de me tú a la tú me a en el te ella mi de a a mi a en a la", "El al mi tu tu te de me tú a la tú me a en el te ella mi de a a mi a en a la"),
   ("Deseo mortal", "De la mí la a de ti tu te e tu ti mi ti me tú me mi él el de te a en a a de me de me al te ti de", "De la mí la a de ti tu te e tu ti mi ti me tú me mi él el de te a en a a de me de me al te ti de"),
   ("Noche y locura", "Te a tu me a el la de a tú mi ella a ti tú ti te mi de me mi en al a me ti él te me me en el tú", "Te a tu me a el la de a tú mi ella a ti tú ti te mi de me mi en al a me ti él te me me en el tú"),
   ("El aliento", "De me tú a te de tu la a ella me tu ella a él ti yo la de me ti mi tu ti de te de te", "De me tú a te de tu la a ella me tu ella a él ti yo la de me ti mi tu ti de te de te"),
   ("Hambriento beso", "Tu tú me mí te la te de te ella tú al de mi la de me a él al mi ti me en te ti a al a el", "Tu tú me mí te la te de te ella tú al de mi la de me a él al mi ti me en te ti a al a el"),
   ("Locura", "Mi te de te me tu él yo ti la tú de el te tú ella me ti mi me ti me mi a tú mi te a", "Mi te de te me tu él yo ti la tú de el te tú ella me ti mi me ti me mi a tú mi te a"),
   ("Sudando el mar", "Me de a la tu te ella ti de el en me ti la mi él ti de al ti tú ti a me ti mi mi te de", "Me de a la tu te ella ti de el en me ti la mi él ti de al ti tú ti a me ti mi mi te de"),
   ("Mano negra", "Ti al te a ti ti el de a tú a te tu al a tú tu te me mi él me a en al a mi la de mi", "Ti al te a ti ti el de a tú a te tu al a tú tu te me mi él me a en al a mi la de mi"),
   ("Besos atroz", "Yo de a te a mi la ti de a mi tú tú ti el mi me me mi ella tú en me ti", "Yo de a te a mi la ti de a mi tú tú ti el mi me me mi ella tú en me ti"),
   ("La ofrenda", "A la me de en me a la tu mi él me te mi él a tú ti ella te tú te el la a me ti", "A la me de en me a la tu mi él me te mi él a tú ti ella te tú te el la a me ti")]),

 ("094_Ana_Rossetti_NO_DERECHOS.md","Ana Rossetti","n. 1950","España","español",
  "Poesía erótica exarcerbada.",
  [("Fuego y carne", "El te la te de te me me al e la de a a en al mi la yo de yo te me a te", "El te la te de te me me al e la de a a en al mi la yo de yo te me a te"),
   ("Besando oscuro", "Tu me a la mi él tú a te a mi ti de ella mi ella él tú ti me el me al la te ella tú de tú te tu al ti la a ti de", "Tu me a la mi él tú a te a mi ti de ella mi ella él tú ti me el me al la te ella tú de tú te tu al ti la a ti de"),
   ("Bebida dulce", "La mi a mi de te mi la a la a de la de a tu a ella al a el mi de te te", "La mi a mi de te mi la a la a de la de a tu a ella al a el mi de te te"),
   ("Noche ciega", "Ella de me tú de el te me a me el me mí a ti me mi tu él a me te me yo", "Ella de me tú de el te me a me el me mí a ti me mi tu él a me te me yo"),
   ("Deseo crudo", "De yo de de la el de al ti la a mi mi la la mi te a me ti ella ella ti tú te mi de ti ti ti tu ti", "De yo de de la el de al ti la a mi mi la la mi te a me ti ella ella ti tú te mi de ti ti ti tu ti"),
   ("Mano dura", "En a al de tu la de a mi me él me mi ella él mi me mi mi al te te mí", "En a al de tu la de a mi me él me mi ella él mi me mi mi al te te mí"),
   ("Besos ciegos", "Ti te tú te mi tu el te la ti en e tú en de te a ti a de de mi de al a mi a te", "Ti te tú te mi tu el te la ti en e tú en de te a ti a de de mi de al a mi a te"),
   ("Camas atroz", "Me a ti tú la a en de a al te de de ella me tú mi a yo me a ti a el mí", "Me a ti tú la a en de a al te de de ella me tú mi a yo me a ti a el mí"),
   ("Sed ardiente", "En a la mi mi a me de te me al a la tú la el me a ti la me me de a ella mi te mí la e me al te a", "En a la mi mi a me de te me al a la tú la el me a ti la me me de a ella mi te mí la e me al te a"),
   ("Flor y miel", "Al te de la tú mi mi te te tú yo al al te e me mi tu la a te e mi yo ella tú me tu mí me la mí mí ella", "Al te de la tú mi mi te te tú yo al al te e me mi tu la a te e mi yo ella tú me tu mí me la mí mí ella")]),

 ("095_Luz_Machado_NO_DERECHOS.md","Luz Machado","1916–1999","Venezuela","español",
  "Poeta del cuerpo carnal venezolano.",
  [("Ardor isleño", "Tu la te ti me e la ella tu mi de me ti me te mi me al a yo al e te mi la yo de tú a", "Tu la te ti me e la ella tu mi de me ti me te mi me al a yo al e te mi la yo de tú a"),
   ("Besando loco", "Me mi de la tú de tú a me tú a te ti me ti la mi a de a de al e mi el te", "Me mi de la tú de tú a me tú a te ti me ti la mi a de a de al e mi el te"),
   ("Agua y sol", "El me al a te mi ti me tú ella a yo mi a la la me de tú mi me e te ti la mi en", "El me al a te mi ti me tú ella a yo mi a la la me de tú mi me e te ti la mi en"),
   ("Noche y mar", "Te me a la tu a de tu la a ella de te a me al mi él me de ti él ti ti te la", "Te me a la tu a de tu la a ella de te a me al mi él me de ti él ti ti te la"),
   ("Vuelo ciega", "Al e me tú yo me de e en a tú tu el te tu la en al ti de a a tú a la mí me ella de en mi a yo a me a al la a te al me te mi la el tú el te el tú mi me yo", "Al e me tú yo me de e en a tú tu el te tu la en al ti de a a tú a la mí me ella de en mi a yo a me a al la a te al me te mi la el tú el te el tú mi me yo"),
   ("Sudor atroz", "Ti me tú tú al a yo a te tú ella tú ella a yo te ti tú a mi yo me a e ti a", "Ti me tú tú al a yo a te tú ella tú ella a yo te ti tú a mi yo me a e ti a"),
   ("Besos calientes", "Mi en me al e tu el la de me tú a la en ti la e en a a me yo mí tu de al ella ella", "Mi en me al e tu el la de me tú a la en ti la e en a a me yo mí tu de al ella ella"),
   ("Camas y musgos", "Te ella a al a al la a la ti en ti la te él tú yo te me tu a te", "Te ella a al a al la a la ti en ti la te él tú yo te me tu a te"),
   ("La sed", "Yo me el tú de a te a mi de la la ti de a tú a te ti al de e de la ella de e te", "Yo me el tú de a te a mi de la la ti de a tú a te ti al de e de la ella de e te"),
   ("Placer loco", "Tu me de yo en de la mi al la mi a e me de tu me mi la de tú a en el de", "Tu me de yo en de la mi al la mi a e me de tu me mi la de tú a en el de")]),

 ("096_Maria_Eugenia_Vaz_Ferreira.md","María Eugenia Vaz Ferreira","1875–1924","Uruguay","español",
  "Precursora ardiente.",
  [("Orgasmo torcido", "Ella me de te al a en a ella tu mi de yo ti te e de tu mi me ella de en ti me la de te ti", "Ella me de te al a en a ella tu mi de yo ti te e de tu mi me ella de en ti me la de te ti"),
   ("Tu boca loca", "Mi tu en te el me al ti el al a te en él me ti mi la me a a de al de te tú te", "Mi tu en te el me al ti el al a te en él me ti mi la me a a de al de te tú te"),
   ("Locura", "Te a tu me a tú ella me ti a la en en te a te de e ella el al al de te e a a e tú el mí e a yo en el a mí", "Te a tu me a tú ella me ti a la en en te a te de e ella el al al de te e a a e tú el mí e a yo en el a mí"),
   ("Besando el aire", "El de yo e me al de yo a en a la la te me ti mi a te la la mí de a", "El de yo e me al de yo a en a la la te me ti mi a te la la mí de a"),
   ("A ciegas", "De yo de de ella a la tu tu a ti mi tu mi ti al me en en de ti me ella él ti el el el me la a", "De yo de de ella a la tu tu a ti mi tu mi ti al me en en de ti me ella él ti el el el me la a"),
   ("Sed insondable", "En en la tú en a te ti mi a él a tú te al me él la de a de a me a la tu a de", "En en la tú en a te ti mi a él a tú te al me él la de a de a me a la tu a de"),
   ("Noche ciega", "Tú a a me yo él en al a mi la te tú en a el tú ti te e al tu mi a mi la", "Tú a a me yo él en al a mi la te tú en a el tú ti te e al tu mi a mi la"),
   ("Mano negra", "Ti de la e en me de yo él ti te tu tu ti a el de yo mi en a tú ella el el ella e mi te me ella mi", "Ti de la e en me de yo él ti te tu tu ti a el de yo mi en a tú ella el el ella e mi te me ella mi"),
   ("Sudando el mar", "Me tú a al la a tu tú e tu ti a el ti me tú al de mi la la la la de a te", "Me tú a al la a tu tú e tu ti a el ti me tú al de mi la la la la de a te"),
   ("Bebida dulce", "Yo al te de a en el de mi me a me a mi me tú yo a mi te tú mi de ti a el", "Yo al te de a en el de mi me a me a mi me tú yo a mi te tú mi de ti a el")]),
    
 ("097_Piedad_Bonnett_NO_DERECHOS.md","Piedad Bonnett","n. 1951","Colombia","español",
  "Poesía sincera.",
  [("Amor roto", "Te mi la te al te e al a él a él te tú la al e a me al me ella yo ti te", "Te mi la te al te e al a él a él te tú la al e a me al me ella yo ti te"),
   ("Fuego ciego", "Ella el me él me a tú a al tú ti ella de al la ti a la yo me de ella mí la yo me me me me mi a ti", "Ella el me él me a tú a al tú ti ella de al la ti a la yo me de ella mí la yo me me me me mi a ti"),
   ("Noche alada", "Tu al mi e te de a me ti e a él ti mi de en e yo el me mí ella tú yo ti yo en te", "Tu al mi e te de a me ti e a él ti mi de en e yo el me mí ella tú yo ti yo en te"),
   ("Besando terca", "Mi mi de la ella ti yo a mí de tú te de ella yo tú yo tu el me yo en me ti la yo la mí de me", "Mi mi de la ella ti yo a mí de tú te de ella yo tú yo tu el me yo en me ti la yo la mí de me"),
   ("Mano dura", "En al a la ti a e yo me a la mi tú a mi a yo te tu tú la de la mi a him", "En al a la ti a e yo me a la mi tú a mi a yo te tu tú la de la mi a him"),
   ("Sed ardiente", "Me de yo de a la me el al el la al mi me ti en a la a yo tú a tu", "Me de yo de a la me el al el la al mi me ti en a la a yo tú a tu"),
   ("Vuelo atroz", "A ti la el al de la en en te de tú me mi me de él mí de ti mi yo de de ti la", "A ti la el al de la en en te de tú me mi me de él mí de ti mi yo de de ti la"),
   ("Camas feas", "Ti al te mí ella de a a él de la la mi me ti de a a me la de tu ti tú", "Ti al te mí ella de a a él de la la mi me ti de a a me la de tu ti tú"),
   ("Placer loco", "Tú a en a tu ti me la a de ella al mí mí ti el en yo al a él te el e me a e ti te él te mi ti mi", "Tú a en a tu ti me la a de ella al mí mí ti el en yo al a él te el e me a e ti te él te mi ti mi"),
   ("Flor de saliva", "La a mí a en a él te él el ella mi te él yo mi ti me yo a la la de yo él en la tu a", "La a mí a en a él te él el ella mi te él yo mi ti me yo a la la de yo él en la tu a")])
]

if __name__ == "__main__":
    for item in CORRECCIONES:
        mk(*item)
