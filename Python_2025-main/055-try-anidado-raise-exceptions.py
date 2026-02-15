from my_toolbox import *
from my_ostools import *

clear_screen()

# Bloque externo que captura y maneja las excepciones relanzadas desde el bloque interno
try:
    # Bloque interno que procesa la entrada del usuario
    user_num = input("Introduce un número entero ")

    try:
        # Validación explícita para detectar si la entrada es un booleano literal
        if user_num == "True" or user_num == "False":
            # Si es booleano, se lanza una excepción ValueError personalizada
            raise ValueError("No se acepta un valor booleano")

        # Intento de conversión a entero
        user_num_int = int(user_num)

        # Ejemplo adicional para lanzar ZeroDivisionError cuando el número es cero
        if user_num_int == 0:
            raise ZeroDivisionError("División por cero no permitida")

    except ValueError as ve:
        # Captura la excepción ValueError, ya sea por entrada booleana o error de conversión no numérica
        print(f"Error de valor: {ve}")
        # Relanza la excepción para que el bloque externo pueda también manejarla o informarla
        raise ve

    except ZeroDivisionError as zde:
        # Captura explícita de ZeroDivisionError para mostrar mensaje específico
        print(f"Error específico: {zde}")
        # Vuelve a lanzar para manejo externo
        raise zde

    except Exception as e:
        # Captura cualquier otra excepción no anticipada
        print("Se ha producido un error")
        # Se relanza para no ocultar el error
        raise e

    else:
        # Si no hubo excepciones, ejecuta este bloque: muestra tabla de multiplicar con condiciones
        for i in range(0, 11):
            if (i % 2 == 1):
                continue  # omitir impares
            elif (i == 4):
                pass  # no hace nada, solo marcador
            elif (i == 0):
                pass  # idem
            elif (i > 7):
                break  # salir si i es mayor a 7
            else:
                print(f"{user_num_int} x {i} =", user_num_int * i)

except Exception as e_outer:
    # Bloque externo captura cualquier excepción relanzada desde el bloque interno
    # Esto permite centralizar manejo, logging o mostrar mensaje final
    print(f"Excepción capturada en el nivel externo: {e_outer}")
