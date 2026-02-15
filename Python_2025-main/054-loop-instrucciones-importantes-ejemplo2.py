from my_toolbox import *
from my_ostools import *
clear_screen()

'''
Programa que:
Crea la tabla de multiplicar con el número introducido por el usuario y:
- Muestra sólo los multiplicadores pares
- No muestra la multiplicación por 4
----------------------------------------
- Sólo multiplica hasta el 7
- No multiplica el 0
'''

mess_single('Solución 1')


try:
    user_num = input("Introduce un número entero ")
    
    try:
        user_num_int = int(user_num)
    except Exception as e:
        print("Se ha producido un error")
        raise e
    else:
        for i in range(0, 11):

            if (i % 2 == 1):
                continue # podría ser utilizado pass
            elif (i == 4):
                pass # podría ser utilizado continue
            elif (i == 0):
                pass # podría ser utilizado continue
            elif (i > 7):
                break
            else:
                print(f"{user_num_int} x {i} =",  user_num_int * i )
except Exception as e_outer:
    print(f"Excepción capturada en try externo: {e_outer} ")






'''
mess_single('NO Solución 2 - IF anidados - NO VIABLE por el CONTINUE')

for i in range(0, 11):
    if (i % 2 == 1):
        continue # podría ser utilizado pass
        if (i == 4):
            pass # podría ser utilizado continue
    else:
        print(f"{user_num_int} x {i} =",  user_num_int * i )



mess_single('NO Solución 3 - IF anidados - VIABLE por el PASS - PERO CON LOGICA ERRÓNEA')
print("Si es 4 cómo va a ser impar???")

for i in range(0, 11):
    if (i % 2 == 1):
        pass # podría ser utilizado pass
        if (i == 4):
            pass # podría ser utilizado continue
    else:
        print(f"{user_num_int} x {i} =",  user_num_int * i )

sep_double()

'''