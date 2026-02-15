import math
from my_toolbox import *

# Redondeo hacia abajo

# con floor
mess_single('con .floor')
my_num = 3.8
res = math.floor(my_num)
print (my_num, '->', res)
# con //
mess_single('con //')
my_num = 4.8
res = my_num // 1
print (my_num, '->', res)

# Redondeo hacia arriba
mess_single('con .ceil')
my_num = 3.8
res = math.ceil(my_num)
print (my_num, '->', res)
my_num = 7.8
res = math.ceil(my_num)
print (my_num, '->', res)

