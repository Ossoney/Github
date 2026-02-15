from my_toolbox import *
'''
Strings-cadenas
1) Son secuencias de caracteres - colección
2) Los espacios en blanco, signos de puntuación, símbolos matemáticos...
"H O L A"
 0 1 2 3
3) Se puede identificar la posición de un caracter por su ÍNDICE
4) También es posible hacerlo por el INDICE REVERSO 
"H O L A"
 0 1 2 3  <- índice
 0-3-2-1  <- índice reverso
-4-3-2-1  <- índice reverso
'''

'''
Método .index()
1) conocer el índice de det.carácter
    my_string = "Murciélago"
    my_string.index("r") -> 2
    ERROR - si caracter buscado fuera de string
2) conocer cúal carácter está en una det.posición
    my_string[9] -> "o"
    ERROR - si caracter buscado fuera de rango    
'''

mess_single('1) Conocer el indice de un det.carácter')
my_string = "Esto es un texto de prueba"
find_char = "E"
print (f"{find_char}",'->',my_string.index(find_char))

find_char = "e"
print (f"{find_char}",'->',my_string.index(find_char))

# find_char = "z" --- metodo index si arroja error interrumpe el programa
# print (f"{find_char}",'->',my_string.index(find_char))

mess_single('2) Conocer qué carácter está en una det.posición')
print('my_string[7]','->',my_string[7])
print('my_string[20]','->',my_string[20])
# print('my_string[35]','->',my_string[35]) más allá de la len de la cadena

# primera posición de la cadena con índice 0
# también con indice negativo igual a la len de la cadena

print('my_string[0]','->',my_string[0])
print('my_string[-26]','->',my_string[-26])


# find_char = "z" # find no rompe nada
# print (f"{find_char}",'->',my_string.find(find_char))



