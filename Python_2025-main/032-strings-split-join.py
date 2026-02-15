from my_ostools import *

clear_screen()

'''
.split() Transforma un string en una lista de palabras o caracateres
         producto de dividir el string mediante un "separador" que le
         proporcionamos a este método
'''


my_string = " Esto es una cadena de texto que vamos a utilizar para desarrollar ejemplos en el curso de Python "

'''
.strip() → Remueve caracteres en blanco al principio y al final de la cadena

.lstrip() → Remueve caracteres en blanco a la izquierda de la cadena

.rstrip() → Remueve caracteres en blanco a la derecha de la cadena
'''

my_trimmed_str = my_string.strip()

my_splitted_str = my_trimmed_str.split("de")
print(my_splitted_str, "→", len(my_splitted_str))

my_splitted_str = my_trimmed_str.split(" ")
print(my_splitted_str, "→", len(my_splitted_str))

'''
.join() → Une diferentes strings mediante un "separador" que le proporcionamos
          a este método
'''

word_1 = "Esto"
word_2 = "es"
word_3 = "Python 3"

my_joined_str = "-".join([word_1, word_2, word_3])
print(my_joined_str, "→", len(my_joined_str))

my_joined_str = " ".join([word_1, word_2, word_3])
print(my_joined_str, "→", len(my_joined_str))

my_joined_str = "".join([word_1, word_2, word_3])
print(my_joined_str, "→", len(my_joined_str))



