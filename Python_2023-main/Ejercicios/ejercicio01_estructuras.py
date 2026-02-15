#LISTAS
lista = [3,8,10,"Automóvil"]
#Acceso a un elemento
print(lista[0])#Mostrar el primer elemento de la lista
#Recorrer todos los elementos
for elemento in lista:
    print(elemento)

#TUPLA
tupla = (3,8,10,"Automóvil")
tupla2 = (3,)
#Acceso a un elemento
print(tupla[0])#Mostrar el primer elemento de la tupla
#Recorrer todos los elementos
for elemento in tupla:
    print(elemento)

#SET (CONJUNTO)
conjunto = {3,8,10,"Automóvil"}
#Recorrer todos los elementos
for elemento in conjunto:
    print(elemento)

#DICT (DICCIONARIO)
diccionario = {3:"Tres","Ocho":8,"Diez":10,"Objeto":"Automóvil"}
#Acceso a un elemento
print(diccionario["Ocho"])
#Recorrer todos los elementos
#Recorrer todas las claves
for clave in diccionario.keys():
    print(clave)
#Recorrer todas los valores
for valores in diccionario.values():
    print(valores)
#Recorrer claves y valores
for clave,valor in diccionario.items():
    print(clave, ":", valor)