from my_ostools import *
from my_toolbox import *

clear_screen()


'''
while → mientras

Loop que se repite MIENTRAS la condición se cumpla

while (condición):
    instrucciones
else:
    instrucciones    
'''

'''
While controlado por la respuesta del usuario
'''

mess_single("While controlado por la respuesta del usuario")

while (True):
    print("Dentro del while")

    res = input("¿Continuar? [S/N]").lower()

    if (res != 's'):
        break


mess_single("While controlado por un contador")

cont = 0
while (cont <= 5):
    print("Dentro del while","→ Contador:", cont)

    cont += 1