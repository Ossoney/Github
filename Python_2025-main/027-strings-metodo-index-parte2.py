from my_toolbox import *

'''
Todo string posee sub-strings
'''

my_string = "Esto es un texto de prueba"
#            01234567891123456789212345
#                      0         0

print('my_string[8:12]', '→', my_string[8:12])
print('my_string[ :18]', '→', my_string[:18])
print('my_string[11:]', '→', my_string[11:])

my_string = ""
print('my_string[:]', '→', my_string[:])

'''
Arroja error ya que una cadena vacía es un conjunto vacío
y un conjunto vacío no posee elementos, por lo tanto el elemento
con índice 0 NO EXISTE
'''
# print('my_string[0]', '→', my_string[0])

sep_double()


my_string = "Esto es un texto de prueba"
#            01234567891123456789212345
#                      0         0

'''
Búsqueda a partir de una determinada posición
'''
mess_single('Búsqueda a partir de una determinada posición')

print('.index("x", 10)', '→', my_string.index("x", 10))

print('.index("x", 10)', '→', my_string.index("x"))


'''
Búsqueda entre dos posiciones
    .index("lo que se busca", desde, hasta)
                                       ↑  
                                     NO SE INCLUYE

'''
mess_single('Búsqueda entre dos posiciones')

print('.index("n", 5, 20)', '→', my_string.index("n", 5, 20))
