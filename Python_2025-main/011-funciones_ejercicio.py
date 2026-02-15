from my_toolbox import *

'''
Ejercicio:

Escribe un programa que posea una función que recibe tres parámetros
posicionales y construye un diccionario con ellos

La función debe retornar el diccionario
'''

def my_function(a, b, c):
    my_dict = {
        "a": a,
        "b": b,
        "c": c
    }

    return my_dict

my_string = "Esto es un string"
my_bool = True
my_number = 7

res = my_function(my_string, my_bool, my_number)
type_var(res)
