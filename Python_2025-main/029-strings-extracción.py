from my_toolbox import *

'''
Slicing - extraer substrings
                0
RIndex       76543211987654321
my_string = "Esto es un string"
Index        01234567891123456
'''

my_string = "Esto es un string"

mess_single('Extraer un caracter')

sub_str = my_string[3]
print('my_string[3]','->',my_string[3])

mess_single('Extraer varios caracteres')

sub_str = my_string[6:12]
print('my_string[3]','->',my_string[6:12])

# sub_str = my_string[5: 12: 2] <- desde,hasta y

# Extraer por partes

mess_single('Extraer varios caracteres cada dos')

sub_str = my_string[::2]
print('sub_str[,,2]','->',sub_str)

sub_str = my_string[::11]
print('sub_str[,,11]','->',sub_str)

sub_str = my_string[::55]
print('sub_str[,,55]','->',sub_str)

sub_str = my_string[55::55]  #no genera error salirse de rangos
print('sub_str[55,,55]','->',sub_str)

type_var(sub_str)



