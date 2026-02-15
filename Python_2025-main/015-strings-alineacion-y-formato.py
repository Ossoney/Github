from my_toolbox import *

num_1 = 54321.22
num_2 = 1234.55

'''
NOTA:
-----
En este ejercicio se utilizará el símbolo pipe (|) para delimitar los
campos y facilitar visualizar las distintas alineaciones.

Ejemplo:
    print(f"El importe es: |{importe},.2f|)
'''

mess_single("Alineación por defecto")

'''
Alineación por defecto

Siempre que el ancho de campo sea mayor o igual a la longitud del
número formateado con # (,) miles y (.) decimales

Formato:
:cant-de-num-enteros(n)separador-de-miles(,)separador-decimal(.)cant-de-num-decimales(n)f

numero:nX,.nYf

Donde:

nX: El tamaño del campo una vez que ha sido formateado

, : Separador de miles

. : Separador decimal

nY: El número de decimales

f : Formato de punto flotante, se incluirá la parte decimal aunque el número
    no tenga decimales
'''

print("num_1:", num_1)

print("num_1 con formato:", f"|{float(num_1):10,.0f}|")

print("longitud del campo de num_1:", len(f"{float(num_1):10,.0f}"))

sep_single()

print("num_1 con formato:", f"|{float(num_1):10,.5f}|")

print("num_1 con formato:", len(f"{float(num_1):10,.5f}"))


sep_double()



mess_single("Alineación explícita a la izquierda")

'''
Alineación explícita a la izquierda

Formato:
    numero:<nX,.nYf
'''

print(f"num_1: |{float(num_1):15,.2f}|")
print(f"num_2: |{float(num_2):<15,.2f}|")

sep_double()



mess_single("Alineación explícita al centro")

'''
Alineación explícita al centro

Formato:
    numero:^nX,.nYf
'''

print(f"num_1: |{float(num_1):15,.2f}|")
print(f"num_2: |{float(num_2):^15,.2f}|")

sep_double()


mess_single("Alineación explícita a la derecha")

'''
Alineación explícita a la derecha

Formato:
    numero:>nX,.nYf
'''

print(f"num_1: |{float(num_1):^15,.2f}|")
print(f"num_2: |{float(num_2):>15,.2f}|")

sep_double()

