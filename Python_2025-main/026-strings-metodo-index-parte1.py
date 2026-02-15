from my_toolbox import *

'''
Strings - Cadenas

1) Son secuencias de caracteres - (colección)

2) Los espacios en blanco, signos de puntuación, simbolos matemáticos...
   ocupan lugar en un string

   "HOLA"
    0123

3) Se puede identificar la posición de un caracter por su ÍNDICE

4) También es posible hacerlo por el ÍNDICE REVERSO

NOTA: En el siguiente ejemplo el string es HOLA, los espaciós en blanco
      se utilizan para la representación de los índices reversos


               "H  O  L  A"
Índice          0  1  2  3
Índice reverso  0 -3 -2 -1  
               -4 -3 -2 -1  
'''

'''
Método .index()

1) Conocer el índice de determinado caracter
   my_string = "Murciélago"
   my_string.index("r") → 2

   Se produce error si el caracter buscado no se encuentra en el string

2) Conocer cuál caracter está en una determinada posición
   my_string[9] → "o"

   Se produce error cuando el índice está fuera de rango, tanto en 
   positivos (natural) my_string[120], como en negativos my_string[-120]
'''

mess_single('1) Conocer el índice de determinado caracter')
my_string = "Esto es un texto de prueba"

find_char = "E"
print(f"{find_char}", '→', my_string.index(find_char))

find_char = "e"
print(f"{find_char}", '→', my_string.index(find_char))

'''
Arroja un error y detiene la ejecución del programa sino encuentra el 
caracter buscado
'''
# find_char = "z"
# print(f"{find_char}", '→', my_string.index(find_char))



mess_single('2) Conocer cuál caracter está en una determinada posición')

print('my_string[7]', '→', my_string[7])

'''
Arroja un error ya que el índice 35 es mayor que el máximo índice
determinado por la longitud de la cadena len(my_string) = 26
'''
# print('my_string[35]', '→', my_string[35])

sep_double()

'''
Lo común es acceder a la primera posición de la cadena mediante el
índice 0.

Sin embargo es posible hacerlo con un índice negativo igual a la longitud
de la cedena
'''

print('my_string[0]', '→', my_string[0])
print('my_string[-26]', '→', my_string[-26])

