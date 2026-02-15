from my_ostools import *
from my_toolbox import *

clear_screen()

'''
.sort()   → Ordena la lista, NO devuelve aldo, es decir, actúa "in situ"
'''

'''
Ordenar listas con números y caracteres
'''
mess_single("Ordenar listas con números y caracteres")

'''
NOTA:

    NO es posible comparar strings con números ni booleanos
        Se ordenan:
            Primero: Los números (almacenados como strings. Ej: "1") y caracteres especiales
                     según su código en la tabla utilizada
            Segundo: Las letras MAYÚSCULAS
            Tercero: Las letras minúsculas
            Cuarto: Las MAYÚSCULAS con caracteres especiales
            Quinto: Las minúsculas con caracteres especiales
'''

my_list = ["a", "A", 0, 1, True, "?", "!"]
type_obj("Mi lista:", my_list)
my_list_sorted = list(my_list)

try:
    my_list_sorted.sort()
except TypeError:
    print("No es posible ordenar la lista")
    print("Revise los tipos de datos")
else:
    type_obj("Lista ordenada:", my_list_sorted)


'''
Ordenar una lista con letras, números, booleanos como caracter
'''

mess_single('Ordenar una lista con letras, números, booleanos como caracter')

my_list = ["a", "á", "â", "à", "ä", "A", "Á", "Â", "Â", "Ä", "0", "1", "True", "False", "?", "!"]
type_obj("Mi lista:", my_list)
my_list_sorted = list(my_list)

try:
    my_list_sorted.sort()
except TypeError:
    print("No es posible ordenar la lista")
    print("Revise los tipos de datos")
else:
    type_obj("Lista ordenada:", my_list_sorted)


'''
Ordenar una lista con números
'''
mess_single('Ordenar una lista con números')

my_list = [8, 6, -10, -4, -0, 25, 7, -0, 0]
type_obj("Mi lista:", my_list)
my_list_sorted = list(my_list)

try:
    my_list_sorted.sort()
except TypeError:
    print("No es posible ordenar la lista")
    print("Revise los tipos de datos")
else:
    type_obj("Lista ordenada:", my_list_sorted)


'''
Ordenar una lista en orden inverso
'''
mess_single('Ordenar una lista con números')

my_list = [8, 6, -10, -4, -0, 25, 7]
type_obj("Mi lista:", my_list)
my_list_sorted = list(my_list)

try:
    my_list_sorted.sort(reverse = True)
except TypeError:
    print("No es posible ordenar la lista")
    print("Revise los tipos de datos")
else:
    type_obj("Lista ordenada:", my_list_sorted)



'''
Ordenar una lista en base a una clave
'''
mess_single('Ordenar una lista en base a una clave')

my_list = ["manzana", "Kiwi", "cereza", "Ananás", "pera", "sandía", "Mango"]
type_obj("Mi lista:", my_list)
my_list_sorted = list(my_list)

my_list_sorted.sort()
type_obj("Lista ordenada:", my_list_sorted)

my_list_sorted.sort(key = str.lower)
type_obj("Lista ordenada:", my_list_sorted)

my_list_sorted.sort(key = len)
type_obj("Lista ordenada:", my_list_sorted)


'''
No puedes repetir el "key argument" ni inventarte un nombre para el "key argument'
'''
# my_list_sorted.sort(key = len, key = str.lower)
# my_list_sorted.sort(key = len, key2 = str.lower)
#type_obj("Lista ordenada:", my_list_sorted)

'''
Ordenar con key y reverse
'''
my_list_sorted.sort(key = str.lower, reverse=True)
type_obj("Lista ordenada:", my_list_sorted)

my_list_sorted.sort(key = str.lower, reverse=1)
type_obj("Lista ordenada:", my_list_sorted)