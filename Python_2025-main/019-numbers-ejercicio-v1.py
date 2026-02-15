import math
from decimal import Decimal

'''
Solicita un número al usuario
Haz una función que lo transforme en entero y otra en float
'''

def casting_int(ni):
    return int(ni)

def casting_float(nf):
    return float(nf)

my_num = input('Ingresa un número: ')

print('El número introducido por el usario es', my_num)

res_float = casting_float(my_num)

factor = 1000

factor_f = len(str(factor))
print("factor_f", factor_f)

factor_f = len(str(factor)) - 1
print("factor_f", factor_f)


res_float = math.trunc(res_float * factor)
res_float = res_float / factor

res_int = casting_int(res_float)

print("Float..:", f"{res_float:>20,.{factor_f}f}")

print("Integer:", f"{res_int:>20,.0f}")

