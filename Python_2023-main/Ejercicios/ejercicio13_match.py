nombre="Fe"
match nombre:
    case "Ab":
        print("Ab")
    case "Fe":
        print("Fe")
    case _:
        print ("No sé")

#solicitar al usuario una receta
#si es paella mostrar los ingredientes
#si es estofado, mostrar ingredientes
#si es otra cosa, mostrar "no tengo esa receta"
#debe dar igual mayúsculas o minúsculas
#en la versión 2 utilizaremos funciones

receta=" "
receta = (input ("¿Qué receta quieres preparar?")).upper()

match receta:
    case "PAELLA":
        print ("PAELLA")
    case "ESTOFADO":
        print ("ESTOFADO")
    case other:
        print ("Esa receta no me la sé")

#2.0

def leer_receta(nombre_receta):
    nombre_fichero = "./recetas/" + nombre_receta + ".txt"
    fichero = open(nombre_fichero, encoding="utf-8", mode="r")
    info = fichero.read()
    fichero.close()
    return info







    