from my_toolbox import *

num_1 = 5432.22
num_2 = 1234.55

'''
Para este ejercicio se utilizará el símbolo pipe (|) para delimitar los
campos y así poder visualizar mejor la alineación y el formato.
Ejemplo:
print(f"El importe es: | {importe},.2f |")
'''

mess_single("Alineación por defecto")    

'''
Alineación por defecto - siempre que ancho de campo sea mayor o igual a longitud
del número formateado con # (,) miles y (.) decimales

Formato: 
:cant_núm_enteros(n)sep_miles(,)sep_decimal().)cant_num_decimales(n)f

número:nE,.nDf

donde:
nE: El tamaño del campo una vez formateado
, : separador de miles
. : separador decimal
nD: número de decimales
f : formato de punto flotante, tenga decimales o no
'''

print(num_1)

print(f"|{num_1:8,.2f}|")

print("num_1 con formato",f"|{float(num_1):10,.0f}|")

print("longitud num_1",len(f"|{float(num_1):10,.0f}|"))

sep_single()

print("num_1 con formato",f"|{float(num_1):10,.5f}|")

print("longitud num_1",len(f"|{float(num_1):10,.5f}|"))

sep_double()
mess_single("Alineación explicita a la izquierda")

print(f"num_1: |{float(num_1):15,.2f}|")
print(f"num_2: |{float(num_2):<15,.2f}|")

# número:<nX,.nYf

sep_double()
mess_single("Alineación explicita al centro")

print(f"num_1: |{float(num_1):15,.2f}|")
print(f"num_2: |{float(num_2):^15,.2f}|")

# número:^nX,.nYf

sep_double()
mess_single("Alineación explicita a derecha")

print(f"num_1: |{float(num_1):^15,.2f}|")
print(f"num_2: |{float(num_2):>15,.2f}|")

# número:>nX,.nYf

