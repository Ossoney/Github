from my_toolbox import *

# String colección de caracteres
# tipo primitivo de dato de Python, es INMUTABLE

mess_single('String')
my_string = "Esto es un curso de Python"
print(my_string)

mess_single('Longitud de un string')
length_str = len(my_string)
print(my_string,"->",length_str)

# Al igual que en las listas los elementos del string poseen índices

mess_single('Imprimir determinado elemento del string')
print(my_string[5:26])

# Mutabilidad de una lista - inmutabilidad de un string

mess_single('Mutabilidad')
my_list = list(my_string)
print('my_string', '->', my_string, '->', len(my_string))
print('my_list', '->', my_list, '->', len(my_list))

my_list[20] = "F"
print('my_string', '->', my_string, '->', len(my_string))
print('my_list', '->', my_list, '->', len(my_list))



