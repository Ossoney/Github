from my_toolbox import *
from my_ostools import *

#clear_screen()

def validar_list(lista, indice):
    print("===> validar_list()", indice)

    try:
        res_list = int(indice)
        list_item = lista[res_list]
    
    except IndexError:
        print("except IndexError → Valor fuera de rango")
    
    except ValueError:
        print("except ValueError → No es un número")
        
    else:
        print ("ELSE → El índice es correcto")
        
        res_list = int(indice)
        list_item = lista[res_list]
    
    finally:
        print ("---> FIN validar_list()")
    # end try

    sep_double()


def validar_dict(clave):
    print("===> validar_dict()", clave)
    
    try:
        pass
    except:
        pass
    else:
        print ("ELSE → La clave es correcta")
    finally:
        print ("---> FIN validar_dict()")
    # end try

    sep_double()

my_list = [1,2,3]

my_dict = {
    "padre": "Carlos",
    "madre": "Olga",
    "hermana": "Tita"
}

res_list_srt = input('Índice de la lista: ')
# res_dict_str = input('Propiedad del diccionario: ')

res_list = validar_list(my_list, res_list_srt)
#res_dict = validar_dict(res_dict_str)