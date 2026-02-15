from my_ostools import *
from my_toolbox import *

clear_screen()

'''
for → para

for es un ciclo determinado
'''
mess_single("for en una lista")

my_list = ["Carlos", "Olga", "Tita", "Carmen", "JC"]

for persona in my_list:
    print(persona)

'''
Para elemento en iterable:
    hacer algo

En este caso:

Para cada persona en mi lista:
    imprimir persona
'''

mess_single('Mostrar índices de la lista')

print(my_list)

for persona in my_list:
    my_index = my_list.index(persona)

    print(f"El índice de la {persona} es {my_index}")

sep_double()


'''
if anidado en for
'''

mess_single("if anidado en for")

people_names  = ["José", " Ainoha", "Javier", "Ana ", "Julio", "Amelia"]

print(people_names)

for name in people_names:
    name = name.strip()

    if name.upper().startswith("A"):
        print(f"{name} tu nombre comienza por 'A'")
    else:
        print(f"{name} tu nombre NO comienza por 'A'")


'''
for anidado - Ejemplo 1
'''
mess_single('for anidado - Ejemplo 1')

people_dict = {
    "Carlos": [["Tita", ["Nelson", "Erick"]], ["JC",[]]],
    "Luisa" : [["Inés", ["Marcos", "Mónica"]], ["Rosa", ["Alejandro", "María"]]],
    "Amalia": [],
    "Celia":  [["Eduardo", []], ["José Antonio", []], ["Celia", []], ["Manuel", []]]
}
sep_double()

for padre, hijos in people_dict.items():
    
    if len(hijos) > 0: # Se fitra a Amalia por no tener hijos
        print(type(hijos), 'Hijos:', hijos)

        for nombre_hijo, nietos in hijos:
            if len(nietos) > 0: # Se fitran a todos los hijos que no tienen descencia
                print(type(nietos), "Nietos:", nietos)




'''
for anidado - Ejemplo 2
'''
mess_single('for anidado - Ejemplo 2')


my_products = [[], ["patatas", "zanahorias"], ["queso", "jamón"], ["leche", "zumo"], ["zamburiñas"], []]

for products in my_products:
    if (len(products) >= 1):
        print(type(products), '→', products)
    
        for e in products:
            print(type(e), '→',e)