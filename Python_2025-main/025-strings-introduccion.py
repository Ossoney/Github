from my_toolbox import *
'''
1) Un string es una colección de caracteres
2) Es un tipo primitivo de dato de Python
3) Comparte algunas características y propiedades de las listas
4) Posee índices para cada uno de los elementos que forman el string 
   (caracteres)
5) Es INMUTABLE
'''

mess_single('String')

my_string = "Esto es un curso de Python"
print(my_string)


mess_single('Longitud de un string')

length_str = len(my_string)
print(my_string,  '→', length_str)

'''
Al igual que en las listas los elementos del string poseen índices
'''

mess_single('Imprimir un determinado elemento del string')

print('string[5] →', my_string[5])


sep_double()
'''
Para demostrar la INMUTABILIDAD de un string, en primer lugar
demostraremos la MUTABILIDAD de las listas
'''

# Transformar el string en lista (casting)

my_list = list(my_string)

print('my_string', '→', my_string, '→', len(my_string))
print('my_list', '→', my_list, '→', len(my_list))


# MUTABILIDAD de una lista
print('string[20] →', my_string[20])
print('list[20] →', my_list[20])

my_list[20] = 'F'
print('my_list', '→', my_list, '→', len(my_list))


# INMUTABILIDAD de un string
# my_string[20] = 'F'
print('my_string', '→', my_string, '→', len(my_string))