import math
from decimal import Decimal

'''
Solicita un número al usuario
Haz una función que lo transforme en entero y otra en float
'''

def casting_int(ni):
    ni = int(ni)
    return ni

def casting_float(nf):
    return float(nf)

def print_msg(texto, var):
    print(texto, var)

def input_usr(texto):
    res = input(texto + " ")
    return res

def convert_to_str(num_dec):
    num_dec = casting_int(num_dec)
    res = '1' + "0" * num_dec
    return res


def trunc_float(num_f, f_dec):
    res = math.trunc(num_f * f_dec)
    res = res / f_dec
    return res
    

mess_txt = 'Ingresa un número:'
my_num = input_usr(mess_txt)

mess_txt = 'El número introducido por el usario es:'
print_msg(mess_txt, my_num)

mess_txt = '¿Cuántos decimales?:'
factor = input_usr(mess_txt)

mess_txt = 'El usuario quiere el número con # decimales:'
print_msg(mess_txt, factor)

factor_str = convert_to_str(factor)

mess_txt = 'El factor de multiplicacón en string es:'
print_msg(mess_txt, factor_str)

factor_mult = casting_int(factor_str)

res_float = casting_float(my_num)
res_int = casting_int(res_float)

res_float_t = trunc_float(res_float, factor_mult)

print("Float..:", f"{res_float:>20,.{factor}f}")
print("Float-t:", f"{res_float_t:>20,.{factor}f}")
print("Integer:", f"{res_int:>20,.0f}")