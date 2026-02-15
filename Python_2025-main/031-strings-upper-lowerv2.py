from my_toolbox import *
from my_ostools import *

def to_lower(texto):
    return texto.lower()

def to_upper(texto):
    return texto.upper()

def show_user_msg(msg, name):
    print(msg, name)

def main():
    
    user_name = input('¿Cúal es tu nombre? ')
    res_lower = to_lower(user_name)
    res_upper = to_upper(user_name)

    show_user_msg('Hola', user_name)
    show_user_msg(f'Hola {user_name}, tu nombre en mayúsculas es', res_upper)

if __name__ == "__main__":
    main()



