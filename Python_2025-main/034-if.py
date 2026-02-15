from my_toolbox import *
from my_ostools import *

clear_screen()


'''
IF → Si (silogismo hipotético)

if (condición):
    instrucciones

Las instrucciones internas se ejecutan SI y SOLO SI la condición se cumple (True)
'''

mess_single('IF - Toma de decisiones / Control de flujo')

my_num1 = 5
my_num2 = 7

if (my_num1 > 0):
    print("La condición (", "my_num1 > 0", ") arroja", "True"  )

sep_single()

if (my_num1 == my_num2):
    print("La condición (", "my_num1 = my_num2", ") arroja", "False")

sep_single()

if (my_num1 * my_num2 == my_num2 * my_num1):
    print("La condición (", "my_num1 * my_num2 == my_num2 * my_num1", ") arroja", "True")

