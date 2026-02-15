lista = ["arbol.jpg","seta.png","arbusto.gif"]

#construcción nueva lista con nombres de ficheros sin extensión
lista_nueva = []
for planta in lista:
    nombre = planta[0:-4]
    lista_nueva.append(nombre)

lista_nueva = [ planta[0:-4] for planta in lista ]
print(lista_nueva)

#lista a mayusculas
lista = ["arbol.jpg","seta.png","arbusto.gif"]
#nombre.upper()
listA = [ planta.upper() for planta in lista ]
print (listA)

#nombre.replace("a","@")
listR = [ planta.replace("a","@") for planta in lista]
print (listR)

