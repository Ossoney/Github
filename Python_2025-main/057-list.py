from my_toolbox import *
from my_ostools import *
clear_screen()

'''
Listas: Secuencia de primitivos u objetos

NOTA: En otros leguajes de programación se conocen como:

    Arrays - Arreglos unidimensionales
    Matrix - Arreglos multidimensionalews


        
1) Se escriben entre corchetes
2) Sus elementos se separan por comas
3) Pueden ser asignadas a una variable
4) Pueden contener cualquier tipo de dato
5) Pueden almacenar datos heterogéneos
6) Se pueden indexar y fraccionar IGUAL que los strings
7) Poseen métodos para su manipulación y análisis
8) Mutabilidad:
    8.1) Si es posible modificarla
    8.2) Si es posible ordenarla
9) Poseen longitud
10) Son concatenables (como los strings)
11) Son multiplicables
12) Pueden ser declaradas vacías
12) Pueden ser declaradas con None → La lista no está vacía
'''

mess_single("1) Se escriben entre corchetes")

my_list = []

mess_single("2) Sus elementos se separan por comas")

my_list = [1, 2, 3]


mess_single("3) Pueden ser asignadas a una variable")

my_list = [1, 2, 3]


mess_single("4) Pueden contener cualquier tipo de dato")
mess_single("5) Pueden almacenar datos heterogéneos")

my_list = [1, "string", ["a", "b", "c"], {"usuario": "Samuel"}]

mess_single("6) Se pueden indexar y fraccionar IGUAL que los strings")

my_list = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
print("Mi lista:", "Tipo:", type(my_list), "len:", len(my_list), my_list)

my_sub_list = my_list[7]
print("Mi lista[7]:", "Tipo:", type(my_sub_list), "len:", len(my_sub_list), my_sub_list)

my_sub_list = my_list[1:3]
print("Mi lista[1:3]:", "Tipo:", type(my_sub_list), "len:", len(my_sub_list), my_sub_list)


sep_double()

mess_single("7) Poseen métodos para su manipulación y análisis")

'''
Añadir un elemento

.append() → Añade al final de la lista
'''
mess_single(".append()")

my_list = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]

my_list.append([1,2,3])

print(my_list)

insert_list = [{2, 5,"tortuga"}, {"padre": "Carlos", "madre": "Olga"}, True]

for e in insert_list:
    # print(e)
    my_list.append(e)


print(my_list)


'''
Eliminar un elemento

.pop() → Elimina el último elemento de la lista
'''
mess_single(".pop()")

my_list.pop()

print(my_list)


'''
Eliminar un elemento n

.pop(n) → Elimina el elemento n de la lista
'''

mess_single(".pop(n)")

my_list.pop(0)


'''
Almacenar elementos eliminados
'''

deleted_element = my_list.pop()
print(deleted_element)

deleted_element = my_list.pop(5)
print(deleted_element)


deleted_element = []
deleted_element.append(my_list.pop())
deleted_element.append(my_list.pop(1))
print(deleted_element)

sep_double()

print("8) Mutabilidad")
print("8.1) Si es posible modificarla")
'''
Es posible modificar una lista modificando uno de los elementos que la componen
'''

my_list = ["Albania", "Halemania", "Argentina"]
print("Mi lista:", "Tipo:", type(my_list), "len:", len(my_list), my_list)

my_list[1] = "Alemania"
print("Mi lista:", "Tipo:", type(my_list), "len:", len(my_list), my_list)



print("8.2) Si es posible ordenarla")
'''
.sort() → Ordena los elementos de una lista

    NOTA 1: 
        - .sort NO DEVUELVE ALGO
        - Opera sobre la lista (in situ)

    NOTA2: 
        Ya que .sort() NO DEVUELVE ALGO (opera in situ) si es necesario mantener
        las lista original hay que operar sobre una lista auxiliar que no comparta
        la referencia con la lista original, es decir: 
            copy_of_my_list = list(my_list)
'''

n1 = 5
n2 = 3
res = n1 + n2

print(res)
print(res + 4)
print(res)


my_list = [3, 100, 25, 4, -2, 0, -300]
print("Lista original", my_list)

print("Lista ordenada", my_list.sort())

print("Lista original", my_list)


'''
Rompiendo referencias
'''

my_list = [3, 100, 25, 4, -2, 0, -300]
my_list_copy = list(my_list) # Rompiendo la referencia

print("Mi lista:", "Tipo:", type(my_list), "len:", len(my_list), my_list)
print("Mi lista → copia:", "Tipo:", type(my_list_copy), "len:", len(my_list_copy), my_list_copy)

my_list_copy.sort()
print("Mi lista → ordenada:", "Tipo:", type(my_list_copy), "len:", len(my_list_copy), my_list_copy)

sep_double()

mess_single("9) Poseen longitud")

my_full_name = ["Juan", "Carlos", "Varela", "Iglesias"]
print("Mi lista:", "Tipo:", type(my_full_name), "len:", len(my_full_name), my_full_name)


mess_single("10) Son concatenables (como los strings)")

my_name = ["Juan", "Carlos"]
my_family_name = ["Varela", "Iglesias"]

my_full_name = my_name + my_family_name
print("Mi lista:", "Tipo:", type(my_full_name), "len:", len(my_full_name), my_full_name)

sep_single()

my_list1 = []
my_list2 = [[],[]]
my_list = my_list1 + my_list2
print("Mi lista:", "Tipo:", type(my_list), "len:", len(my_list), my_list)


mess_single("11) Son multiplicables")

my_list = ["Alumno"]
print("Mi lista:", "Tipo:", type(my_list), "len:", len(my_list), my_list)

my_list = my_list * 3
print("Mi lista:", "Tipo:", type(my_list), "len:", len(my_list), my_list)

sep_single()

my_list = ["Perro", "Gato"]
print("Mi lista:", "Tipo:", type(my_list), "len:", len(my_list), my_list)

my_list = my_list * 2
print("Mi lista:", "Tipo:", type(my_list), "len:", len(my_list), my_list)



mess_single("12) Pueden ser declaradas vacías")

my_list = []
print("Mi lista:", "Tipo:", type(my_list), "len:", len(my_list), my_list)

my_list = list()
print("Mi lista:", "Tipo:", type(my_list), "len:", len(my_list), my_list)



mess_single("12) Pueden ser declaradas con None → La lista no está vacía")

my_list = [None]
print("Mi lista:", "Tipo:", type(my_list), "len:", len(my_list), my_list)


my_list = my_list * 7
print("Mi lista:", "Tipo:", type(my_list), "len:", len(my_list), my_list)