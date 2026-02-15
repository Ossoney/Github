from my_toolbox import *
from my_ostools import *

clear_screen()

'''
>= 10 .. <= 15
>  15 .. <= 20
>  20 .. <= 25
>  25 .. <= 30
'''

'''
# Opción 1
input numero usuario → verificar si es un número

if (>= 10 .. <= 15):
    pass
elif (>  15 .. <= 20):
    pass
elif (>  20 .. <= 25):
    pass
elif (>  25 .. <= 30):
    pass
else:
    pass ← si no es un número o no está en el rango    
'''

'''
# Opción 2
input numero usuario → verificar si es un número

if anidado
'''

user_num_str = input("Introduce un número entre 10 y 30 incluidos ")
user_num = float(user_num_str)
print(user_num)

if (user_num >= 10 and user_num <= 15):
    print("Es mayor o igual que 10 y menor o igual a 15")

elif (user_num > 15 and user_num <= 20):
    print("Es mayor que 15 y menor o igual a 20")

elif (user_num >20 and user_num <= 25):
        print("Es mayor que 20 y menor o igual a 25")

elif (user_num > 25 and user_num <= 30):
        print("Es mayor que 25 y menor o igual a 30")

else:
    print("Número fuera de rango")    