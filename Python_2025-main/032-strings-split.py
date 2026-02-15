from my_toolbox import *
from my_ostools import *

# Método split divide textos por espacio sen blanco o por lo que le digas
# Método strip remueve caracteres en blanco al principio y al final de la cadena
# lstrip y rstrip

my_string = " Esto es una cadena de texto que vamos a utilizar para desarrollar ejemplos "

my_splitted_str = my_string.split("de")
print(my_splitted_str,"-",len(my_splitted_str))

my_splitted_str = my_string.split(" ")
print(my_splitted_str,"-", len(my_splitted_str))

# .join

word1 = "Esto"
word2 = "es"
word3 = "Python"
my_joined_string = " ".join([word1,word2,word3])
print(my_joined_string,"-",len(my_joined_string))

my_joined_string = "*".join([word1,word2,word3])
print(my_joined_string,"-",len(my_joined_string))

