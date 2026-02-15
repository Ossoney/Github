from my_toolbox import *
from my_ostools import *

clear_screen()

'''
.find() → Busca un substring

          Devuelve -1 si no lo encuentra
          No detiene la ejecución del programa

          Es posible utilizar índices reversos
'''


'''
En este string aparece la palabra Python
0123456789012345678901234567890123456789
          1         2         3   
'''
mess_double('.find()')

mess_single('.find() en una cadena completa')

my_string = "En este string aparece la palabra Python"

res = my_string.find("Python")

print(res)

sep_double()

mess_single('.find() en un substring')

'''
Cuando se utilizan los índices DESDE - HASTA, para Python el indice 0 será
el que corresponda con el caracter que ocupa la posición 0 del substring

my_string = "Esto es un string"
             01234567890123456
                       1

res = my_string[5:14]
    Se almacena en res un NUEVO objeto que se corresponde con el substring
    "es un stri"

    Por lo tanto sus índices serán:
    "es un stri"
     0123456789

'''

my_string = 'Esto es un string'

res = my_string[5:14].find("s")
print(res)


sep_double()

'''
.replace() → Reemplaza un substring

    my_string.replace(param1, param2, contador)

        param1: String a reemplazar
        param2: String que reemplaza
        contador: Número de reemplazos a realizar
'''

my_string = "Los pájaros son aves, los pájaros tienen plumas pero no todos los pájaros vuelan"

mess_single('.replace() por defecto -- SIN EL CONTADOR ')

res = my_string.replace("pájaros", "vacas").replace("los", "las").replace("Los", "Las").replace("todos", "todas")
print(res)

mess_single('.replace() CON EL CONTADOR ')

res = my_string.replace("pájaros", "vacas", 2)
print(res)

mess_single('.replace() CON EL CONTADOR en 0')
res = my_string.replace("pájaros", "vacas", 0).replace('pájaros', 'pájaras', 1)
print(res)

'''
Reemplazar SÓLO la segunda aparición de "pájaros"
'''
my_string = "Los pájaros son aves, los pájaros tienen plumas pero no todos los pájaros vuelan"

### Solución 1
res = my_string.replace("pájaros tienen", "dinosaurios tienen", 1)
print(res)


### Solución 2
my_string = "Los pájaros son aves, los pájaros tienen plumas pero no todos los pájaros vuelan"
my_list = my_string.split("pájaros", 1)

print("my_list", '→', my_list, '→', len(my_list))

replace_str_old = "pájaros"
replace_new_new = "dinosaurios"
my_new_string = my_list[0] + replace_str_old + my_list[1].replace(replace_str_old, replace_new_new, 1)

print(my_new_string)

parte_1 = my_string[:26]
parte_2 = my_string[26:].replace('pájaros', "dinosaurios", 1)
print(parte_1 + parte_2)
