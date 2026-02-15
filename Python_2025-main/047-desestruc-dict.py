from my_toolbox import *
from my_ostools import *

clear_p

'''
2 tipos de objetos:
a) del sistema o del lenguaje
b) definidos por el usuario

En python el tipo de dato equivalente a archivos JSON
y objetos JavaScript es el diccionario (dict) 
{
    "clave" : valor
    key       value    (todo)=item
}
'''

mess_single('keys')

my_dict = {
    "key_1": "String value",
    "key_2": 5,
    "key_3": [1,2,3]
}

print ("KEYS: ", type(my_dict.keys()), my_dict.keys())
# devuelve una lista, que es iterable

for key in my_dict.keys():
    print("key:", key)
    
mess_single('values')

print ("VALUES: ", type(my_dict.values()), my_dict.values())

for value in my_dict.values():
    print("values:", type(my_dict.values()),value)

mess_single('items')

print ("ITEMS: ", type(my_dict.items()), type(my_dict.items()), my_dict.items())

for item in my_dict.items():
    print("item:", type(item),item)

# desestructurar item
val1 = my_dict["key_1"]
val2 = my_dict["key_2"]
val3 = my_dict["key_3"]
val1, val2, val3 = my_dict["key_1"], my_dict["key_2"], my_dict["key_3"]

for key, value in my_dict.items():
    print(key, "-",value)

mess_single('desempaquetando ahora los valores')

my_dict = {
    "key_1": "String value",
    "key_2": 5,
    "key_3": [1,2,3]
}

v1,v2,v3 = my_dict.values()
print(v1,v2,v3)
print(len(my_dict.values()))

#o 

for v in my_dict.values():
    print (v)
    
    
mess_single('keys numericas en python')

my_dict = {
    0 : "Cero",
    1 : 1,
    2 : "Dos"
}
print("mi_dict[1]", my_dict[1])

suma = 0
for v in my_dict.keys():
    suma += v
print (suma)



