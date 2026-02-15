'''
print()

Mostrar algo por pantalla

Sintaxis: 
print(Lo que se va a mostrar)

Lo que se va a mostrar:
    - Uno o más strings
    - Una o más variables
    - Combinaciones de strings y variables
    - Operaciones
    - ...
'''

def sep():
    print("===========================" + "\n")


'''
Imprimir strings (cadenas de texto)
    Usar comillas dobles ("), comillas simples ('), 
    comillas anidadas
'''

print("Curso Python 3 entre comillas dobles")
sep()

print('Curso Python 3 entre comillas simples')
sep()

# Anidación
print("Curso Python 3 'con comillas simples' entre comillas dobles")
sep()

print('Curso Python 3 "con comillas dobles" entre comillas simples')
sep()

'''
Concatenar strings (+)
'''

print("Curso" + "Python" + "3")
sep()

print("Curso" + " Python " + "3")
sep()

print("Curso" + " " + "Python" + ' ' + "3")
sep()


'''
Números
'''

print(9)
sep()

print(-19)
sep()

print(138.26)
sep()

print(-2569.37)
sep()


'''
Operaciones
'''

print(25 * 4)
sep()

print((2 + 2) / 2)


'''
Multiplicar strings
'''

print("Hola" * 4)
sep()

print(("Hola" + "." + " " ) * 4)
sep()

print(10 * 4 )
print("10" * 4 )
sep()

'''
NOTA:
    NO es posible CONCATENAR números y strings
'''

# print("Cadena de texto" + 5)


'''
Usar coma (,) como separador
'''

print("7 x 3 =", 7 * 3)
sep()

print("Curso", "Python", "3")
sep()

'''
Variables
'''

my_name = 'JC'
my_age = 54

# ERROR: Mezcla de strings con números
# print("Soy " + my_name + " y tengo " + my_age + " años")

print("Soy", my_name, "y tengo", my_age, "años")

sep()
'''
Caracteres especiales
'''

'''
1) Escape (\)
'''

print("El \ es el caracter de escape")
print("El \\ es el caracter de escape")

sep()

'''
2) Tabulador (\t)
'''

print("\t" + "Esta línea comienza con un tabulador y a continuación" + "\t" + "tiene otro")

sep()

'''
3) Salto de línea (\n)
'''

print("Esto es una línea" + "\n" + "Esto es otra línea")

sep()

'''
4) Retorno de carro (\r)
'''

print("Esto es una línea" + "\r" + "Esto es otra línea")

sep()

'''
5) Escpar secuencias especiales
'''
print("El \\n es un salto de línea en un string")