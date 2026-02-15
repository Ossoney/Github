lista = [8,4,3,10,15,25]
#bucle normal
for elemento in lista:
    print(elemento)
    if elemento == 15:
        break #detiene la ejecución del bucle
else:
    print("Else")

#bucle con slicing
for elemento in lista[1::2]:
    print(elemento,end=":")

#bucle con rango
for i in range(100):
    print (i,end="-")

#bucle for con rango 100 y 0 decreciente
for i in range(100,-1,-1):
    print(i,end="-")


