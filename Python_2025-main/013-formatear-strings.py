from my_toolbox import *

'''
NOTA: La CONCATENACIÓN NO formatea strings
'''

color_ojos = "negro"
edad_usuario = 27

print("Tu color de ojos es" + " " + color_ojos + " " + "y tu edad es" + " " + str(edad_usuario))

sep_double()


'''
En Python esisten dos maneras de formatear strings
    a) Función format()
    b) Cadenas literales
'''

mess_single(".format()")

'''
a) Función format()

    Insertar {} en el lugar de ka cadena en el cual se visualizará el valor de 
    la(s) variable(s), al finalizar la cadena se añadirá .format(var_1, var_2, ...)

    NOTA: Las variebles TIENEN que estar ordenadas de forma que coincidan con
    el orden de aparcición de las llaves
'''

var_1 = 33
var_2 = "Python 3"
var_3 = True


# Mostramos la frase sin formatear
print("En este curso de Python 3 tendremos 33 alumnos y un valor booleano True")

print("En este curso de {} tendremos {} alumnos y un valor booleano {}".format(var_2, var_1, var_3 ))

sep_double()

mess_single("Cadenas literales / f-strings")

'''
b) Cadenas literales

    Anteponer la letra f ó F antes de la cadena y entre llaves la(s) variable(s)
'''

print(f"En este curso de {var_2} tendremos {var_1} alumnos y un valor booleano {var_3}")