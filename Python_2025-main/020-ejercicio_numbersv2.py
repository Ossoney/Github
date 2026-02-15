import math

def casting_int(ni):
    return int(ni)

def casting_float(nf):
    return float(nf)

my_num = input('Ingresa un numero: ')

print('El nuḿero introducido por el usuario es', my_num)

factor = input('¿cuántos decimales?: ')
factor = int(factor)

factor_str = '1'+'0'* factor
print("factor_str",factor_str)

factor_mult = int(factor_str)
print("factor_mult",factor_mult)

res_float= casting_float(my_num)
res_int = casting_int(res_float)

res_float = math.trunc(res_float *factor_mult)
res_float = res_float/ factor_mult

print("Float..:", f"{res_float:>20,.{factor}f}")
print("Entero.:", f"{res_int:>20,.0f}")


