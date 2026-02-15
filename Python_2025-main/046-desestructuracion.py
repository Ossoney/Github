from my_toolbox import *
from my_ostools import *

clear_screen()

'''
Desestructuracción - Desempaquetado - Desempacado - Unpacking

- Se apñica a datos estructurales (listas, ...)

- Consiste en estraer elementos del dato estructural (iterable)
'''

'''
Listas / Tuplas / Sets
'''
mess_single('Listas')

my_list = [1, "Mesa", True]

x, y, z = my_list

print("x", x)
print("y", y)
print("z", z)

'''
Simutáneamente CREAR y DESEMPAQUETAR una lista
'''

mess_single('Simutáneamente CREAR y DESEMPAQUETAR una lista')

n1, n2, n3 = my_list = [333, 444, 555]
print("n3", n3)
print("my_list", my_list)

'''
Introduccion a for
'''

mess_single('Introduccion a for')

my_string = "ABCDEFGHIJ"

for letra in my_string:
    print(letra)

sep_single()

my_list = ["Pera", "Manzana", "Uva", "Cereza", "Mango"]

for fruta in my_list:
    print(fruta)

sep_single()

my_list = list(my_string)
print(my_list)

for letra in my_list:
    print(letra)
    
sep_single()

mess_single('Desempaquetar con for Ejemplo 1')
# a, b = [3, 7]

my_list = [[1,2], [3,4], [5,6]]

for e in my_list:
    print(e)

for n1, n2 in my_list:
    print('n1', n1, 'n2', n2)


for lista in my_list:
    for elemento in lista:
        n1 = elemento
        n2 = elemento
        print('n1', n1, 'n2', n2)


sep_single

mess_single('Desempaquetar con for Ejemplo 2')

my_list = [[["a", "b"],["c","d"]], [["e","f"],["g","h"]], [["i","j"],["k","l"]], [["m","ñ"],["o", "p"]]]


'''
ANÁLISIS
'''

print('Cant. listas Nivel 1:', len(my_list))

'''
Creando listas de NIVEL 1
'''

l1_nivel1, l2_nivel1, l3_nivel1, l4_nivel1 = my_list

print("Listas de nivel 1:", l1_nivel1, l2_nivel1, l3_nivel1, l4_nivel1)

'''
Creando listas de NIVEL 2
'''

l1_nivel2, l2_nivel2 = l1_nivel1
print("Listas de nivel 2", l1_nivel2, l2_nivel2)

l1_nivel2, l2_nivel2 = l2_nivel1
print("Listas de nivel 2", l1_nivel2, l2_nivel2)


l1_nivel2, l2_nivel2 = l3_nivel1
print("Listas de nivel 2", l1_nivel2, l2_nivel2)

l1_nivel2, l2_nivel2 = l4_nivel1
print("Listas de nivel 2", l1_nivel2, l2_nivel2)

'''
nivel 0 []
nivel 1 [ [], [], ...]
nivel 2 [ [[], []], [[], []], [[], []] ]
nivel 3 [[[e1, e2], [e3, e4]]]
'''

'''
FIN ANÁLISIS
'''

for (e1, e2), (e3, e4) in my_list:
    print(e1, e2, e3, e4)

sep_double()

my_list = [[["a", "b"],["c","d"]], [["e","f"],["g","h"]], [["i","j"],["k","l"]], [["m","ñ"],["o", "p"]]]

'''
nivel 0
'''

print('Nivel 0:' , my_list)

'''
nivel 1
'''

for elem_de_nivel_1 in my_list:
    print("Elementos de nivel 1", elem_de_nivel_1)


'''
nivel 2
'''

for elem_de_nivel_1 in my_list:
    for elem_de_nivel_2 in elem_de_nivel_1:
        print("Elementos de nivel 2", elem_de_nivel_2)    


'''
nivel 3
'''

for elem_de_nivel_1 in my_list:
    for elem_de_nivel_2 in elem_de_nivel_1:
        for elem_de_nivel_3 in elem_de_nivel_2:
            print("Elementos de nivel 3", elem_de_nivel_3)   