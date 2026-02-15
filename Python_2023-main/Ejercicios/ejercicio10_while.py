import random

numero_secreto = int(random.random()*10)

encontrado = False
intento = 0
while encontrado==False and intento <3:
    numero_candidato = int(input("Introduce un número entre 0 y 10: "))
    intento = intento + 1
    if numero_candidato == numero_secreto:
        print("Eres un adivino espectacular")
        encontrado=True
    else:
        print("Eres un fraude de adivino")

#o
intento=0
while encontrado==False:
    numero_candidato = int(input("Introduce un número entre 0 y 10: "))
    if numero_candidato == numero_secreto:
        encontrado=True
    else:
        print("Eres un fraude de adivino")
    intento+=1
    if intento==3:
        print ("Eres un fraude")
        break
else:
    print ("Has acertado, eres un gran adivino")




    