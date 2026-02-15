import math
from my_toolbox import *

'''
round - Redondeo
round (param1, cant_de_decimales)
    param1 = nº?, op.matemática, variable, funciòn
    cant_decimales - si no hay, se interpreta que no quieres
'''

mess_single('Redondear')
my_num = 5.123456

my_round_num = round(my_num,7)
type_var(my_round_num)
my_round_num = round(my_num,6)
type_var(my_round_num)
my_round_num = round(my_num,5)
type_var(my_round_num)
my_round_num = round(my_num,4)
type_var(my_round_num)
my_round_num = round(my_num,3)
type_var(my_round_num)
my_round_num = round(my_num,2)
type_var(my_round_num)
my_round_num = round(my_num,1)
type_var(my_round_num)
my_round_num = round(my_num)
type_var(my_round_num)

sep_double()

# Redondear vs Truncar
mess_single('Truncar')

my_trunc_num = (math.floor(my_num))
type_var(my_trunc_num)

print(math.floor(1/2))

# Operador // división al piso-suelo
mess_single('Operador // divisor al piso-suelo')

my_num = 1
my_num_res = my_num // 2
type_var(my_num_res)

my_num = 5.8
my_num_res = my_num // 2
type_var(my_num_res)

# Casting con int
my_num = 5.8
my_round_num = int(my_num)
type_var(my_round_num)

sep_double()

# reglas redondeo automático

mess_double('Reglas de redondeo automático')
mess_single('a) número < 0.5 Redondeo hacia abajo')
my_num = 4.3
print("Mi número: ", my_num, round(my_num))
my_num = 5.4
print("Mi número: ", my_num, round(my_num))
mess_single('b) El número = 0.5 Redondeo bancario o al par más cercano')
my_num = 4.5
print("Mi número: ", my_num, round(my_num))
my_num = 5.5
print("Mi número: ", my_num, round(my_num))
mess_single('c) número > 0.5 Redondeo hacia arriba')
my_num = 4.6
print("Mi número: ", my_num, round(my_num))
my_num = 5.7
print("Mi número: ", my_num, round(my_num))

# Redondear un float sin especificar cantidad de decimales

mess_single('Redondear un float sin especificar decimales')
my_num = 77.777777777777777777777777777777777777777
my_round_num = round(my_num)
type_var(my_round_num)

# Redondear un float especificando cantidad de decimales

mess_single('Redondear un float especificando decimales')
my_num = 77.777777777777777777777777777777777777777
my_round_num = round(my_num,3)
type_var(my_round_num)



