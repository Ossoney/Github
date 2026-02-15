import math
from my_toolbox import *

'''
Redondeo hacia abajo
'''

mess_single('Con .floor()')

my_num = 3.8
res = math.floor(my_num)
print(my_num, '→', res)

mess_single('Con //')
my_num = 4.8
res = my_num // 1
print(my_num, '→', res)

'''
Redondeo hacia ARRIBA
'''

mess_single('Con .ceil()')

my_num = 7.8
res = math.ceil(my_num)
print(my_num, '→', res)


my_num = 8.8
res = math.ceil(my_num)
print(my_num, '→', res)


my_num = 4.5
res = math.ceil(my_num)
print(my_num, '→', res)


my_num = 5.5
res = math.ceil(my_num)
print(my_num, '→', res)