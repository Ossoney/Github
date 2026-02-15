from my_ostools import *
from my_toolbox import *

clear_p()

def validar_num(numero):
    print('---------------> validar num')
    try:
        user_num = int(numero)
    except ValueError:
        print(f"{numero} no es un número")
    else:
        remain_number = user_num % 2
        mostrar_res(remain_number)        
    finally:
        print('-------------> FIN de la función validar número')
    
def mostrar_res(n):
    if n == 0:
            print('Par')
    else:
            print('Impar')

            
user_num_str = input('Introduce un número: ').strip()
validar_num(user_num_str)

'''
def validar_num(numero_str):
    print('---------------> validar num')
    try:
        user_num = int(numero_str)  # Intentamos convertir a entero
    except ValueError:
        print(f"'{numero_str}' no es un número válido.")
    else:
        if user_num % 2 == 0:
            print('Par')
        else:
            print('Impar')
    finally:
        print('-------------> FIN de la función validar número')

user_num_str = input('Introduce un número: ').strip()
validar_num(user_num_str)
'''