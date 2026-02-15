from my_toolbox import *

# método index

my_string = "Curso de Python3"
#            0123456789012345

str_length = len(my_string)
print("len(my_string)",'->',len(my_string))

print(my_string[15])
print(my_string[len(my_string) -1])
print(my_string[str_length-1])

# método rindex Busca de derecha a izquierda
mess_single(".rindex")

print('my_string[-1]','->', my_string[-1])
print('my_string.rindex("o")','->',my_string.rindex("o"))
print('my_string.index("o")','->',my_string.index("o"))

print('my_string.rindex("de",-16,-1)','->',my_string.rindex("de",-16,-1))
print('my_string.index ("de",  0,15)','->',my_string.index ("de",  0,15))







