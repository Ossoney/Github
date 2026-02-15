from my_toolbox import *
from my_ostools import *

clear_screen()

'''
Objetos:
    Existen dos tipos:
    a) Del sistema / lenguaje (programación)
    b) Definidos por el usuario


    En python el tipo de dato equivalente a archivos JSON y
    objetos JavaScript es el diccionario (dict)

    {
        "clave": valor  ← Item (Par Clave: Valor)
           |       ↓
           ↓       Value
           Key

    }
'''


my_dict = {
    "key_1": "String value",
    "key_2": 5,
    "key_3": [1,2,3]
}


mess_single('Keys')

print("KEYS:", type(my_dict.keys()), my_dict.keys()) # Devuelve un iterable

for key in my_dict.keys():
    print("Key:", type(key), key)


mess_single('Values')

print("Values:", type(my_dict.values()), my_dict.values()) # Devuelve un iterable

for value in my_dict.values():
    print("Values:", type(value), value)


mess_single('Items')

print("Items:", type(my_dict.items()), my_dict.items()) # Devuelve un iterable

for item in my_dict.items():
    print("Item:", type(item), item)


mess_single('Desempaquetado de Items')

for k, v in my_dict.items():
    print(k, v)


mess_single('Desempaquetando values')
print("El diccionario tiene", len(my_dict.values()), "values")

v1, v2, v3 = my_dict.values()

print("Value 1: ", v1)
print("Value 2: ", v2)
print("Value 3: ", v3)


mess_single('Keys numéricas en Python')

'''
NOTA: En python SI se pueden utilizar KEYS NUMÉRICAS
'''

my_dict = {
    0: "Cero",
    1: 1,
    2: "Dos"
}

print("my_dict[1]:", my_dict[1])


'''
Programa que sume las numéricas de un diccionario
'''
mess_double("Programa que sume las numéricas de un diccionario")


mess_single("Suma mediante desempaquetado")

k1, k2, k3 = my_dict.keys()

print('La suma de claves es:', k1 + k2 + k3)


mess_single("Mediante un acumulador")

res_suma = 0

for key in my_dict.keys():
    res_suma = res_suma + key

print('La suma de claves es:', res_suma)


mess_single("Mediante un acumulador (Optimizado)")

res_suma = 0

for key in my_dict.keys():
    res_suma += key

print('La suma de claves es:', res_suma)



