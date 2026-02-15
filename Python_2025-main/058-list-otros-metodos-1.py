from my_ostools import *
from my_toolbox import *

clear_screen()

'''
Ya vistos
    .append() → Añade elementos (al final)
    .pop()    → Elimina el último elemento, devuelve el elemento eliminado
    .pop(n)   → Elimina el elemento n, devuelve el elemento eliminado
    .sort()   → Ordena la lista, NO devuelve aldo, es decir, actúa "in situ"
'''

'''
.clear() 
    Elimina TODOS los elementos de la lista
    NO devuelve algo, método "in situ"

    Para mantener la lista "original" trabajar sobre una copia con la referencia
    rota
'''
mess_single('.clear()')

my_list = [555, 777, 999]
 
my_list_cleared = list(my_list)
my_list_cleared.clear()

type_obj("Mi lista:", my_list_cleared)


'''

    Inserta el valor en el índice especificado
'''

mess_single('.insert(index, value)')

my_list = [555, 777, 999]
type_obj("Lista", my_list)

my_list.insert(1, True)
type_obj("Lista", my_list)

sep_single()

mess_single("Índice reverso en strings")
my_string = "Esto es un string"
print("my_string[-1]", my_string[-1])

mess_single("Índice reverso en list")
my_list.insert(-1, "Este NO es el último elemento")
type_obj("Lista", my_list)

mess_single("Insertar al final / equivalente a .append()")
my_list.insert(len(my_list), "Este SI es el último elemento")
type_obj("Lista", my_list)

'''
.index(valor, [desde, [hasta]])
'''
mess_single('.index(valor, [desde, [hasta]])')

my_list = ["perro", "gato", "tortuga", "conejo", "hamster", "camaleón", "loro"]

res = my_list.index("tortuga")
print(res)

# res = my_list.index("murciélago")
# print(res)


try:
    res = my_list.index("murciélago")
except ValueError:
    print("'murciélago' no existe en la lista")

sep_single()

try:
    res = my_list.index("hamster", 3, len(my_list)-1 )
except ValueError:
    print("Elemento no encontrado")
else:
    type_var(res)

'''
.count → Cuenta la cantidad de apariciones del "valor" en la lista
'''
mess_single(".count()")

my_list = ["perro", "gato", "tortuga", "conejo", "perro", "hamster", "camaleón", "loro", "perro"]

try:
    res = my_list.count("perro")
except ValueError:
    print("Elemento no encontrado")
else:
    type_var(res)    

sep_single

my_list = [None, True, None, False, None]

try:
    res = my_list.count(None)
except ValueError:
    print("Elemento no encontrado")
else:
    type_var(res)    





