from my_toolbox import *
from my_ostools import *

clear_screen()

'''
IF - ELIF - ELSE → Si - Sino Si - Sino

            Toma de deciciones / Control de flujo

    if   → Si 
    elif → Sino si (else if)
    else → Sino


    if (condicion_A):
        bloque de instrucciones A
    
    elif (condicion_B):
        bloque de instrucciones B

    elif (condicion_C):
        bloque de instrucciones C

    ... (Puedes utilizar todos los elif que necesites)

    else:
        bloque de instrucciones Z


Se ejecuta el "bloque de instrucciones A" SI y SOLO SI la condicion_A se cumple ← if
Se ejecuta el "bloque de instrucciones B" SI y SOLO SI la condicion_B se cumple ← elif
...
Se ejecuta el "bloque de instrucciones Z" SINO se cumple alguna de las condiones anteriores ← else

NOTA: El uso de else ES OPCIONAL
'''

'''
En este caso sólo tenemos dos opciones
'''
# Opción 1
mess_double("Opción 1 - Hard code de colores")

mess_single('IF - ELIF - ELSE Toma de decisiones / Control de flujo')

hair_color = input("¿Cuál es tu color de cabello? ").strip()

print(hair_color, len(hair_color))


if(hair_color.lower() == "negro"):
    pass
elif(hair_color.lower() == "marron"):
    pass
elif(hair_color.lower() == "amarillo"):
    pass
else:
    pass


# Opción 2
mess_double("Opción 2 - Utilizar variables")

mess_single('IF - ELIF - ELSE Toma de decisiones / Control de flujo')

hair_color = input("¿Cuál es tu color de cabello? ").strip()

print(hair_color, len(hair_color))

color_a = "negro"
color_b = "marron"
color_c = "amarillo"

if(hair_color.lower() == color_a):
    pass
elif(hair_color.lower() == color_b):
    pass
elif(hair_color.lower() == color_c):
    pass
else:
    pass


'''
Introducción al operador "in"

Operador in

Lo podemos utilizar para determinar si "algo" está presente en un iterable

Iterables:
    strings
    listas
    tuplas
    sets
    objetos
'''

app_colors = ["negro", "marron", "amarillo"]

if(hair_color.lower() in app_colors):
    print(f"Tu color de pelo es {hair_color}")
else:
    print(f"Tíñete el pelo")


sep_double()    

to_find = 'u'
my_str = "Murciélago"

if (to_find in my_str):
    print(f"{to_find} está en {my_str}")


