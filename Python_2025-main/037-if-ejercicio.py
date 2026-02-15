from my_ostools import *
from my_toolbox import *

clear_p()


#pedir numero entre 10 y 30, clasificar de 5 en 5

numero = round(float(input('Dame un número entre 10 y 30, carallán: ')))
# numero-str = float(numero)

if(numero in [10,15]):
    print('Estás entre 10 y 15')
elif(numero in [16,20]):
    print('Estás entre 16 y 20')
elif(numero in [21,25]):
    print('Estás entre 21 y 25')
elif(numero in [26,30]):
    print('Estás entre 26 y 30')
else:
    print('Te sales del ámbito, fenómeno')



