

'''
Solicita un número al usuario
Haz una función que lo transforme en entero y otra en float
'''
def casting_int(ni):
    return int(ni)

def casting_flo(nf):
    return float(nf)

my_num = input('Ingresa un número: ')
print('El número introducido por el usuario es', my_num)

res_flo = casting_flo(my_num)
print('El número float es',f"{res_flo:>10,.2f}")

res_int = casting_int(res_flo)
print('y el número entero es',f"{res_int:>10,.0f}")



