from my_ostools import *
from my_toolbox import *

clear_p()


nombre = nombreapellido.split(" ")
print (nombre)

def pedir_nombreapellido():
    try:
        nombreapellido = input ('Dime tu nombre y apellido').strip()
    except ValueError:
        
    except 
        
    else:
        
        
    finally:
        



'''
def pedir_nombre_apellido():
    while True:
        try:
            nombre = input("Introduce tu nombre: ").strip()
            apellido = input("Introduce tu apellido: ").strip()

            if not nombre or not apellido:
                raise ValueError("El nombre y apellido no pueden estar vacíos.")

            if not nombre.isalpha():
                raise ValueError("El nombre solo debe contener letras.")

            if not apellido.isalpha():
                raise ValueError("El apellido solo debe contener letras.")

        except ValueError as e:
            print("Error:", e)
            print("Por favor, vuelve a intentarlo.\n")
        else:
            print(f"Nombre: {nombre}, Apellido: {apellido}")
            break

pedir_nombre_apellido()
'''
