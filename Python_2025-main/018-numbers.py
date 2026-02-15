from my_toolbox import *

'''
Integers - Enteros
    Enteros positivos y negativos

    45, -125, 0, 32, -0

    
Floats - Flotantes / Decimales
    Decimales positivos y negativos

    -3.5, 69.83, 49.0, 0.0, -0.0


Complex - Complejos
    Incluyen la parte real y la imaginaria

    NOTA: En python se escriben con j en lugar de i

        Ejemplos:
            num_complex = 2 + 3j
            num_complex = -1j


Booleanos
    Son un subtipo de int

    True  ≈ 1
    False ≈ 0


Decimal - Decimal

    NOTA: NO son nativos de Python

    from decimal import Decimals

    Ejemplo:
        x = Decimal("1.1")



Fraction - Fracción  

    NOTA: NO son nativos de Python

    from fractions import Fraction

    Ejemplo:
        x = Fraction(3, 4)
'''


mess_double('Integers')
my_num1 = -8

type_var(my_num1)

sep_single()

mess_single('Integers - Operaciones matemáticas')
mess_single('Suma')

my_num1 = 1
my_num2 = 2
my_num3 = 3

suma = my_num1 + my_num2 + my_num3
type_var(suma)

mess_single('Resta')
resta = my_num1 - my_num2 - my_num3
type_var(resta)


mess_single('Multiplicación')
multiplicacion = my_num1 * my_num2 * my_num3
type_var(multiplicacion)

mess_single('División')
division = my_num1 / my_num2 / my_num3
type_var(division)

division = 5 / 5
type_var(division)

'''
Las mismas operaciones matématicas aplican a float o a la combinación
de float e int

NOTA: El resultado SIEMPRE será float
'''