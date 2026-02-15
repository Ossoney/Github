from my_ostools import *
from my_toolbox import *
clear_screen()

my_string = "Este texto no tiene la letra h y tiene una letra z casi al final"

'''
No es cierto que el texto no contenga la letra h

Desarrollaremos la lógica para SIMULAR que NO la tiene
'''


'''
Condiciones:

a) ch == "z" → romper y salir del ciclo

b) ch == "e" → no ejecutar

c) ch == "t" → hacer nada
'''

my_string_list = []

print(my_string)
for ch in my_string:
    if (ch == "z"):
        break
        
    elif (ch == "e"):
        continue

    elif (ch == 'h'):
        pass

    else:
        print(ch)
        my_string_list.append(ch)
        

print(my_string_list)

# my_string_list = str(my_string_list)
# 
# print(my_string_list)


print("Código fuera del ciclo")


