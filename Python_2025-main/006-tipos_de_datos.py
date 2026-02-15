'''
type()
    Devuelve el tipo del ol objeto o nuevo tipo basado en los argumentos
    pasados o devueltos
'''

def sep():
    print("===========================" + "\n")

'''
Datos primitivos
'''


'''
Strings → Cadenas de caracateres
Primitivo
'''

my_str = "Esto es un string"

print(my_str)

print(type(my_str))

sep()

'''
Number → Número
Primitivo
'''

# int → Enteros
my_number = 5
print(type(my_number), my_number)

my_number = -9
print(type(my_number), my_number)

# float → Punto flotnte
my_number = 0
print(type(my_number), my_number)

my_number = 0.0
print(type(my_number), my_number)

my_number = -0.0
print(type(my_number), my_number)

my_number = 3.75
print(type(my_number), my_number)

my_number = -1.33
print(type(my_number), my_number)

sep()

'''
Bool → Booleano
Primitivo
'''

# Asignación directa
my_bool = True
print(type(my_bool), my_bool)

my_bool = False
print(type(my_bool), my_bool)

# Asignación inderecta

# Igualdad (==)
my_bool = 3 == 3
print(type(my_bool), my_bool)

my_bool = 7 == (5 + 2)
print(type(my_bool), my_bool)

my_bool = "Pepe" == "Pepe"
print(type(my_bool), my_bool)

my_bool = "Pepe" == "pepe"
print(type(my_bool), my_bool)


# Mayor que (>)
my_bool = 0 > -1
print(type(my_bool), my_bool)

my_bool = -1 > 0
print(type(my_bool), my_bool)


# Mayor o igual que (>=)
my_bool = 0 >= -1
print(type(my_bool), my_bool)

my_bool = -1 >= 0
print(type(my_bool), my_bool)

my_bool = -0.0 >= 0
print(type(my_bool), my_bool)

my_bool = 0.0 >= -0
print(type(my_bool), my_bool)

# Menor que (<)
my_bool = 5 < 9
print(type(my_bool), my_bool)

my_bool = 8 < 3
print(type(my_bool), my_bool)

# Menor o igual que (<=)
my_bool = 8 <= 8
print(type(my_bool), my_bool)

my_bool = 8 <= 10
print(type(my_bool), my_bool)

my_bool = 8 <= 4
print(type(my_bool), my_bool)

# Distinto que, no igual a (!=)

my_bool = 8 != 4
print(type(my_bool), my_bool)

my_bool = 7 != 7
print(type(my_bool), my_bool)

my_bool = 7 != 7.0
print(type(my_bool), my_bool)

'''
Operadores de comparación
==  Igual que (comparación estricta)
<   Menor que
<=  Menor o igual que
>   Mayor que
>=  Mayor o igual que
!= Distinto, no igual
'''

'''
Null → Nulo
Formalmente NO existe en Python
'''

my_null = None
print(type(my_null), my_null)


my_var = 32

sep()
'''
Undefined → No definido
Formalmente NO existe en Python
'''
sep()

'''
None → Equivale a Null
Primitivo
'''

my_none = None
print(type(my_none), my_none)

print("0 == None:", type(0 == None), 0 == None)


sep()
sep()
sep()

'''
Datos compuestos / complejos / no primitivos

Structures → Estructuras
'''

'''
list → Lista (Mutable)
    Conocido en otros leguajes como:
    - Array → Arreglo
    - Vector - Vector
    - Unidimension Array → Arreglo unidimensional

Colección homogénea o heterogénea de datos

Definimos entre corchetes []
'''

# Lista vacía
my_list = []
print(type(my_list), my_list)


# Lista de elementos homogéneos
my_list = ["Mazda"]
print(type(my_list), my_list)

my_list = ["Getz", "León"]
print(type(my_list), my_list)

my_list = [0, 1, 2]
print(type(my_list), my_list)

my_list = [True, False, 7 == 7]
print(type(my_list), my_list)


# Lista de elementos heterogéneos

my_list = [
    "palabra",          # string
    0.3,                # number
    True,               # boolean
    None,               # none
    ["a", 1],           # list
    (3,"pepe"),         # tuple → tupla
    {1,0,1},            # set → conjunto
    {"clave": "valor"}  # dict → diccionario (Objetos, JSON)
    ]

print(type(my_list), my_list)

sep()

# Mutabilidad de la lista
my_list = ["Perro", "Gato"]
print(type(my_list), my_list)

my_list = ["Perro", True] # Es una nueva lista
print(type(my_list), my_list)

my_list[0] = "Loro" # ← Confirma la mutabilidad
print(type(my_list), my_list)

sep()

'''
tuple → Tupla (Inmutable)
Colección homogénea o heterogénea de datos

Definimos entre paréntesis ()
'''

my_tuple = ("Coche", "Autobus", "Bicicleta")
print(type(my_tuple), my_tuple)

my_tuple = ("Coche", True, "Bicicleta") # Es una nueva tupla
print(type(my_tuple), my_tuple)

# my_tuple[0] = "Avión" # ← Confirma la inmutabilidad

sep()

'''
set → Conjunto (Inmutable)

Colección homogénea o heterogénea de datos

Definimos entre llaves {}
'''

my_set = {1, 2, 3}
print(type(my_set), my_set)

my_set = {1, 2, "Tres"}
print(type(my_set), my_set)

# my_set[2] = 8 # ← Confirma la inmutabilidad

# Un set no posee orden, por lo tanto NO es posible
# seleccionar un elemento por su índice

'''
dict → Diccionario (Mutable)

Colección homogénea o heterogénea de datos

Definimos entre llaves {clave: valor}
'''

my_dict = {
    "nombre": "Juan Carlos",
    "apellidos": "Varela Iglesias",
    "edad": 54,
    "respira": True,
    "familia": {
        "padre": "Carlos",
        "madre": "Olga",
        "hermana": "Tita",
        "cunado": "Nelson",
        "esposa": "Carmen"
    },
    0: True,
    1: False,

    True: "Verdadero",
    False: "No verdadero"
}

print(type(my_dict), my_dict)

print(my_dict["edad"])
print(my_dict["familia"]["madre"])

sep()
print("0:", my_dict[0])
print("1:", my_dict[1])

sep()
print("True:", my_dict[True])
print("False:", my_dict[False])

sep()

'''
User Objects → Objetos creados por el usuario
'''

'''
Function → Función
'''


'''
Función que recibe tres parámetros (valores de cualquier tipo)
y los retorna.

El retorno será en este caso una tupla

Params:
    a (any): Descripción
    b (any): Descripción
    c (any): Descripción

Returns:
    tuple(a, b, c)        
'''
def my_function(a, b, c): # a, b y c se denominan parámetros
    print("Estamos dentro de la función")
    print("a →", a)
    print("b →", b)
    print("c →", c)

    return a, b, c

'''
ASIGNAR la función a una variable
-------

La variable "res" ahora es una referencia a la función my_function

Con esto se demuestra que las funciones en Python
son ciudadanos de primer orden/primera clase
'''

res = my_function # En la asignación NO lleva paréntesis
print("res:", type(res), res)


'''
INVOCAR a la función con los argumentos a, b, c
'''
edad = 25
nombre = "María"

res = my_function(edad, nombre, ["x", "y", "z"]) # edad, nombre, ["x", "y", "z"] son argumentos
print("res:", type(res), res)

