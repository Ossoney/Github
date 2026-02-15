from my_toolbox import *

'''
Slicing (rebanar) - Extraer substrings

Extraer fragmentos de una cadena y "normalmente" almacenarlos en una
variable

                    0
RIndex     - 76543211987654321    
my_string = "Esto es un string"
Index        01234567891123456
                       0

                    DESDE
                    ↑      
                    |      PASO (Cada X caracteres)
                    |      ↑
sub_str = my_string[5: 13: 2]
                        ↓
                        HASTA (Sin incluirlo)
'''

'''
Extraer un caracter
'''

my_string = "Esto es un string"

mess_single('Extraer un caracter')
sub_str = my_string[3]

print('my_string[3]', '→', sub_str)

'''
Extraer varios caracteres
'''
mess_single('Extraer varios caracteres')
sub_str = my_string[5: 13]

print('my_string[5: 13]', '→', sub_str)


sub_str = my_string[5: 12 + 1]

print('my_string[5: 12 + 1]', '→', sub_str)


'''
Extraer cada 2 caracteres de la cadena
'''
mess_single('Extraer cada 2 caracteres de la cadena')

print('my_string', '→', my_string)

sub_str = my_string[::2]
print('my_string[::2]', '→', sub_str)

sub_str = my_string[::11]
print('my_string[::2]', '→', sub_str)

sub_str = my_string[::555]
print('my_string[::2]', '→', sub_str)

# Desde - Hasta  - Paso de posiciones que NO EXISTEN por el len(my_string)
sub_str = my_string[-1800:3600:555]
print('my_string[1800:3600:555]', '→', sub_str)

print('sub_str:', sub_str, 'type:', type(sub_str))

