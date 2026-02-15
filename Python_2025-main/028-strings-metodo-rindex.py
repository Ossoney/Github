from my_toolbox import *

'''
Método .rindex()

BUSCA DE DERECHA A IZQUIERDA

El índice que muestra siempre será positivo (orden natural)
'''

my_string = "Curso de Python3"
#            0123456789112345
#                      0


str_length = len(my_string)
print("len(my_string)", '→', str_length)

mess_single('.index()')

print('my_string[15]', '→', my_string[15])
print('my_string[str_length - 1]', '→', my_string[str_length - 1])
print('my_string[len(my_string)- 1', '→', my_string[len(my_string)- 1])

mess_single('.rindex()')
print('my_string[-1]', '→', my_string[-1])

print('my_string.rindex("P")', '→', my_string.rindex("P"))


# print('my_string.rindex("de", -1, -16)', '→', my_string.rindex("de", -1, -16))

print('my_string.index("de",    0, 15)', '→', my_string.index("de",    0, 15))
print('my_string.rindex("de", -16, -1)', '→', my_string.rindex("de", -16, -1))
