
#solicitar al usuario una receta
#si es paella mostrar los ingredientes
#si es estofado, mostrar ingredientes
#si es otra cosa, mostrar "no tengo esa receta"
#debe dar igual mayúsculas o minúsculas
#en la versión 2 utilizaremos funciones

nombre_receta =" "
nombre_receta = (input ("¿Qué receta quieres preparar?")).upper()
print(nombre_receta)

def leer_receta(nombre_receta):
    nombre_fichero = "./recetas/" + nombre_receta + ".txt"
    fichero = open(nombre_fichero, encoding="utf-8", mode="r")
    info = fichero.read()
    fichero.close()
    return info

from gtts import gTTS
import os
  
audio = gTTS(text=nombre_fichero,lang="es",slow=False)
audio.save("receta.mp3")

os.system("start receta.mp3")
