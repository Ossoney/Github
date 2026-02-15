from my_toolbox import *
import math

'''
round - Redondeo

round (param1, cant_de_decimales)

- param1:
    - Un número
    - Una operación matemática
    - Una variable
    - Una función

- cant_de_decimales
    Autoexplicado

NOTA: Si NO se especifica cant_de_decimales Python interpreta que
      NO quieres decimales
'''

mess_single('Redondear')

my_num = 5.1234567

my_round_num = round(my_num)
type_var(my_round_num)

my_round_num = round(my_num, 7)
type_var(my_round_num)

my_round_num = round(my_num, 6)
type_var(my_round_num)

my_round_num = round(my_num, 5)
type_var(my_round_num)

my_round_num = round(my_num, 4)
type_var(my_round_num)

my_round_num = round(my_num, 3)
type_var(my_round_num)

my_round_num = round(my_num, 2)
type_var(my_round_num)

my_round_num = round(my_num, 1)
type_var(my_round_num)

my_round_num = round(my_num, 0)
type_var(my_round_num)


sep_double()


'''
Redondear vs Truncar
'''

mess_single('Truncar')

my_trunc_num = (math.floor(my_num))
type_var(my_trunc_num)

print(math.floor(1/2))


'''
Operador // (división al piso / suelo)
'''

mess_single('Operador // (división al piso / suelo')

my_num = 1
mi_num_res = my_num // 2
type_var(mi_num_res)

my_num = 5.8
mi_num_res = my_num // 2
type_var(mi_num_res)



'''
Casting con int
'''

my_num = 5.8
my_round_num = int(my_num)
type_var(my_round_num)

sep_double()

'''
Reglas de redondeo automático
'''

mess_double('Reglas de redondeo automático')

mess_single('a) número < 0.5 ← Redondeo hacia abajo')
my_num = 4.3
print("Mi número:", my_num, '→', round(my_num))

my_num = 5.4
print("Mi número:", my_num, '→', round(my_num))


'''
Redondeo al número pas más cercano
Round half to even
Redondeo Bancario

    even → par
    odd → impar
'''
mess_single('b) número = 0.5 ← Redondeo hacia arriba')
my_num = 4.5 # Redondeo bancario por ser par
print("Mi número:", my_num, '→', round(my_num))

my_num = 5.5
print("Mi número:", my_num, '→', round(my_num))


mess_single('c número > 0.5 ← Redondeo hacia arriba')


my_num = 4.7
print("Mi número:", my_num, '→', round(my_num))

my_num = 5.8
print("Mi número:", my_num, '→', round(my_num))

sep_double()

'''
Redondear un float sin especificar cantidad de decimales
'''
mess_single('Redondear un float sin especificar cantidad de decimales')

my_num = 77.7777777777777777777777777777777777777777
my_round_num = round(my_num)
type_var(my_round_num)


'''
Redondear un float especificando cantidad de decimales
'''
mess_single('Redondear un float especificando cantidad de decimales')

my_num = 77.7777777777777777777777777777777777777777
my_round_num = round(my_num, 3)
type_var(my_round_num)
