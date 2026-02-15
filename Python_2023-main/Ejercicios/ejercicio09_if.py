ingresos = 25_000
if ingresos<10_000:
    print("Menos de 10.000")
    print("Necesitas mejorar")
elif ingresos<20.000:
    print("Menos de 20.000")
    print("No está mal")
else:
    print("Tienes 20.000 de ingresos o más")

#operador ternario
edad=18
#modo normal
if edad>=18:
    autorizado = True
else:
    autorizado= False
#modo ternario
autorizado = True if edad>=18 else False

