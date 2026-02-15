'''
.upper() → Trasforma toda la cadena a mayúsculas 

.lower() → Trasforma toda la cadena a minúsculas 
'''
# --- Importaciones
from my_toolbox import *
from my_ostools import *

# --- Funciones
def to_lower(texto):
    return texto.lower()

def to_upper(texto):
    return texto.upper()

def show_user_msg(msg, name):
    print(msg, name)
    
# --- Función principal main()
def main():
    clear_screen()

    user_name = input('Cuál es tu nombre: ') 

    res_lower = to_lower(user_name)
    res_upper = to_upper(user_name)

    show_user_msg('Hola', user_name)

    show_user_msg(f'Hola {user_name} tu nombre es mayúsculas es', res_upper)


if __name__ == "__main__":
    main()
