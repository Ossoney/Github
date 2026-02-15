from my_toolbox import *

# Todo string posee substrings

# Búsqueda a partir de una determinada posición

mess_single('Búsqueda a partir de una det.posición')

my_string = ('Esto es un texto de prueba')
#            01234567890123456789012345
#            0         1         2

print('my_string[8:12]','->',my_string[8:12])
print('my_string[:12]','->',my_string[:12])
print('my_string[8:]','->',my_string[8:])

my_string = ''
print('my_string[8:12]','->',my_string[8:12])
print('my_string[:12]','->',my_string[:12])
print('my_string[8:]','->',my_string[8:])
# da error imprimir posición 0 en cadena vacía

# Búsqueda a partir de una det.posición

mess_single('Bśuqueda a partir de una det.posición')
my_string = ('Esto es un texto de prueba')
print('my_string.index("x",10)','->',my_string.index("x",10))

mess_single('Búsqueda entre dos posiciones')
my_string = ('Esto es un texto de prueba')
print('my_string.index("n")','->',my_string.index("n",5,20+1))
my_string = ('Esto es un texto de prueba')
print('my_string.index("e")','->',my_string.index("e",5,20+1))










