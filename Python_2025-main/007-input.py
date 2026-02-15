from my_toolbox import *

'''
input() de forma directa
'''

print(input("¿Nombre?: "))

sep_double()

'''
input() asignado a una variable
'''

nombre = input("Nombre?: ")
edad = input("Edad: ")

mess_single('Cadena literal')
print(f"Tu nombre es {nombre} y tu edad es {edad}") # ← Cadena literal

mess_single("Separado con comas")
print("Tu edad es", edad)