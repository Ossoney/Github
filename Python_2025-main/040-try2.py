from my_ostools import *
from my_toolbox import *

clear_p()

# programa que divide el número 10 entre otro número

my_value = 10

try:
    user_num_str = (input('Introduce un número: '))
    user_num = int(user_num_str)
    res = my_value / user_num

except ValueError:
    print(f'{user_num_str} no es un número')

except ZeroDivisionError:
    print(f'{user_num_str} no se puede dividir entre 0')
    
else:
    print(f'{my_value} / {user_num} = {res}')

finally:
    print('Tú si que sabes')