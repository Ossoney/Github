from my_toolbox import *
from my_ostools import *

clear_screen()

my_list = [1,2,3]

my_dict = {
    "padre": "Carlos",
    "madre": "Olga",
    "hermana": "Tita"
}


res_list_srt = input('Índice de la lista: ')

res_dict_str = input('Propiedad del diccionario: ')
res_dict = res_dict_str.strip()


try:
    print("---> Estoy en try")
    res_list = int(res_list_srt) # Puede generar error en casting por el
                                 # tipo de dato introducido

    list_item = my_list[res_list]  # Puede generar error, por ejemplo, con el
                                   # uso de un índice que NO existe en la cadena

    dict_item = my_dict[res_dict] # Puede generar error si se utiliza una clave
                                  # del diccionario que no existe


except AttributeError:
    print("---> Estoy en except")
    
    print("El índice / propiedad no existe")

else:
    print("Estoy en else")
    
    print(my_list[list_item])
    print(my_dict[dict_item])
finally:
    print("---> Estoy en finally")
    
    print("Colorín, colorado, este programa se ha acabado")    