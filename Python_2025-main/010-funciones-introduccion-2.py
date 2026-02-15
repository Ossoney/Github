from my_toolbox import *
from funciones_introduccion2_data import *

'''
Desarrolla un programa que permita mostrar los datos de una persona:
- Su dirección o direcciónes y tipo
- Su correo/s electrónicos y tipo
- Su coche/s:
    - Marca
    - Modelo
    - Año
    - Matrícula
- Su numero/s de teléfono y tipo
'''

def cant_elementos(lista, nombre):
    res = len(lista)
    print(f"La longitud de la lista {nombre} es {res}")


cant_elementos(user_address, "direcciones")

    
