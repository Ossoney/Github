from my_toolbox import *

'''
Casting → Conversiones de tipo

Consideraciones:
    Python 3 es un lenguaje débilmente tipado, es decir, una variable
    puede contener cualquier tipo de dato durante la ejecuón del 
    programa.


Tipos de casting:

a) Implícito:
    Lo realiza Python automáticamente.

    Sucede cuando se efectúan cierto tipo de operaciones en las que
    están involucrados tipos de datos diferentes.

b) Explícito:
    Se efectúa mediante código escrito por el programador.

    El código fuente expresa que se desea convertir un tipo de dato en
    otro
'''

mess_single("Casting Implícito")

print(type(8 / 2), (8 / 2)) # La división → float

print(type(6 * 3), (6 * 2)) # La multiplicación → int / float

sep_double()

res = (10 / 3)
type_var(res)

sep_double()

res = "Una cadena de texto " * 4
type_var(res)

sep_double()

'''
Casting Explícito
'''
mess_single("Casting Explícito")

mess_single("int")

my_float = 25.8
my_int = int(my_float)
type_var(my_float)
type_var(my_int)
 

mess_single("float → int") 

my_string = "100.5"
my_float = float(my_string)
type_var(my_float)

my_int = int(my_float)
type_var(my_int)


'''
list → Listas
'''
num_1 = 7
num_2 = 11.5
num_3 = 26

my_list = list()
type_var(my_list)

my_list = []
type_var(my_list)

sep_single()

my_list = [1, "Padre", "Madre", True]
type_var(my_list)

my_list = list((3, "Padre", "Madre", True))
type_var(my_list)

sep_single()

my_list = [1, "Padre", "Madre", True]
type_var(my_list)

my_list = list((3, "Padre", "Madre", True))
type_var(my_list)

sep_single()

my_list = [num_1, num_2, num_3]
type_var(my_list)

my_list = list((num_1, num_2, num_3))
type_var(my_list)

sep_single()

my_set = {1, "Ornitorrinco", 1, 1, 2, 1, 2, 3, True}
type_var(my_set)

my_list = list(my_set)
type_var(my_list)

sep_single()

my_dict = {
    "propiedad_1": "P1",
    "propiedad_2": True,
    "propiedad_3": 77,
    "propiedad_4": [],
}

type_var(my_dict)

my_list_prop = list(my_dict)
type_var(my_list_prop)

my_list_val = list(my_dict.values())
type_var(my_list_val)

