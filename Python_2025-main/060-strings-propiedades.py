from my_ostools import *
from my_toolbox import *

clear_screen()

'''
Propiedades de String

1) Inmutabilidad
una vez construido - NO SE PUEDE cambiar orden interno ni alterar su contenido
'''

mess_single("Inmutabilidad")

my_string = "My curso de Python"

my_char = "P"
char_index = my_string.index(my_char)
print("char index :", char_index)

# my_string[char_index] = "Z" DA ERROR. no es posible modificar valor

'''
NOTA: .replace()
Con .replace() da la IMPRESIÓN de que el string es mutable... ¡NO LO ES!
- toma string original, realiza la/s sustituciones indicadas, 
- devuelve nuevo string
- almacena nuevo string en la misma variable donde esaba string original
(no es mutabilidad - es reemplazo de valor)
'''

mess_single(".replace() da la impresión de mutabilidad")

my_string = "My curso de Python"
my_string2 = my_string.replace("o","0")
my_string3 = my_string.replace("c","C")
print(my_string,my_string2,my_string3)

'''
Reescritura de variable

Se reescribe (reasignación de valor), dicho de otro modo, 
SE CAMBIA EL VALOR almacenado en ella
'''

mess_single("Reescritura de variable")

my_string = "Hoy es lunes"
my_string = "Hoy es LUNES"
print(my_string)

# 2) Concatenables

mess_single("Los strings son concatenables")

my_string1 = "Hola"
my_string2 = " "
my_string3 = "chic@s"

my_string = my_string1 + my_string2 + my_string3
print(my_string)

# 3) multiplicables

mess_single("Los strings son multiplicables")
my_string1 = "la"
my_string2 = " ,"
my_string3 = (my_string1+my_string2) * 7

print(my_string3)

# 4) Multilineales

mess_single("Multilineal")

my_string = '''
String multilineal
entre comillas simples
'''
print(my_string)

my_string = """
String multilineal
entre comillas simples
"""
print(my_string)