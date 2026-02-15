from my_toolbox import *
from my_ostools import *

clear_screen()

'''
IF - ELSE → Si - Sino

            Toma de deciciones / Control de flujo

    if (condicion):
        instrucciones
    else:
        instrucciones       

Se ejecuta el bloque de instrucciones del "IF" SI y SOLO SI la condición se cumple, 
SINO se ejecuta el bloue de instrucciones del "ELSE"
'''

mess_single('IF - ELSE Toma de decisiones / Control de flujo')

hair_color = input("¿Cuál es tu color de cabello? ").strip()

print(hair_color, len(hair_color))

color_to_compare = "verde"

if(hair_color.lower() == color_to_compare):
    print('True IF', f'tu pelo es de color {color_to_compare}')
else:
    print('False ELSE', f'tu pelo no es {color_to_compare}')

sep_single()


if(hair_color.lower() != color_to_compare):
    print('False IF', f'tu pelo no es {color_to_compare}')
else:
    print('True ELSE', f'tu pelo es de color {color_to_compare}')