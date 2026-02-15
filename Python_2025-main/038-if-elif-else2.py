from my_ostools import *
from my_toolbox import *

clear_p()


#pedir numero entre 10 y 30, clasificar de 5 en 5

user_num_str = input('Dame un número entre 10 y 30, carallán: ')
user_num = float(user_num_str)

if (user_num >= 10 and user_num <= 15):
    print('Estás entre 10 y 15')
elif(user_num > 15 and user_num <= 20):
    print('Estás entre 16 y 20')
elif(user_num > 20 and user_num <= 25):
    print('Estás entre 21 y 25')
elif(user_num > 15 and user_num <= 30):
    print('Estás entre 26 y 30')
else:
    print('Te sales del ámbito, fenómeno')