from my_toolbox import *
from my_ostools import *

clear_screen()

'''
try → Intentar

- Se utiliza para manejar errores (o excepciones) que pueden ocurrir
  durante la ejecución de un programa

- Si ocurre un error o excepción permite que el programa continúe 
  corriendo en lugar de detenerse y arrojar un mensaje de error

try:
    Código que puede ejecutarse correctamente o generar una excepción

except Tipo_de_excepción:
    Código que se ejecuta si ocurre la excepción

else: [OPCIONAL]
    Código que se ejecuta si NO ocurre una excepción

finally: [OPCIONAL]
    Código que siempre se ejecuta (se pridujese excepción o no)
'''


'''
try: Bloque de código qie Python intentará ejecutar
    
    Si durante esta ejecución ocurre una excepción, el control de flujo
    pasa al bloque except

except: Si se produce una excepción en bloque try,
        se ejecuta el código de este bloque

        Se pueden manejar tipos específicos de excepciones, como ValueError,
        ZeroDivisionError, entre otras.

        Si no se especifica un tipo, atrapará cualquier excepción.

else: [OPCIONAL]  Se ejecuta si no se produce una excepción el el bloque try
    

finally: [OPCIONAL] Se ejecuta siempre, exista excepción o no
'''

try:
    a = "2" * "2"
except Exception as e:
    raise e     # ← NO HEMOS programado qué hacer en caso de excepción
else:
    print("ELSE → No ha ocurrido una excepción")
finally:
    print('FINALLY → Sí o sí esto se ejecuta')    
# end try

