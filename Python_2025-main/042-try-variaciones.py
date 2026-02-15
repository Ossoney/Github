
def validar_list(lista,indice):
    print('===> validar list', indice)
    try:
        res_list = int(indice)
        list_item = lista[res_list]
    except IndexError:
        print('except IndexError - fuera de rango')
    except ValueError:
        print('except ValueError - no es un número')
    else:
        print('El indice es correcto')
        res_list = int(indice)
        list_item = lista[res_list]
    finally:
        print('FIN función validar_list')
        
def validar_dict(dict,clave):
    print('===> validar dict', clave)
    
    try:
        res_dict = clave.strip().lower()
        
    except:
        pass
    
    else:
        print('La clave dict es correcta')
        
    finally:
        print('FIN función validar_dict')
    

my_list = [1, 2, 3]
my_dict = {
    "padre": "Carlos",
    "madre": "Olga",
    "hermana": "Tita"
}
res_list_str = input('Indice de la lista: ')
#res_dict_str = input('Propiedad del diccionario: ')

res_list = validar_list(my_list,res_list_str)
#res_dict = validar_dict(my_dict,res_dict_str)


'''

def convertir_a_entero(cadena):
    try:
        return int(cadena)
    except ValueError:
        print('Error: No se pudo convertir a entero.')
        return 

def obtener_elemento_lista(lista, indice):
    try:
        return lista[indice]
    except IndexError:
        print('Estoy en except IndexError')
        print('El indice no existe')
        return 

def obtener_elemento_diccionario(diccionario, clave):
    try:
        return diccionario[clave]
    except KeyError:
        print('Estoy en except KeyError')
        print('El key no existe')
        return

def main():
    res_list_str = input('Indice de la lista: ')
    res_dict_str = input('Propiedad del diccionario: ')
    res_dict = res_dict_str.strip().lower()

    print('Estoy en try')
    res_list = convertir_a_entero(res_list_str)
    if res_list is None:
        return

    list_item = obtener_elemento_lista(my_list, res_list)
    if list_item is None:
        return

    dict_item = obtener_elemento_diccionario(my_dict, res_dict)
    if dict_item is None:
        return

    print('Estoy en else')
    print(my_list, res_list, "->", list_item)
    print(my_dict, res_dict, "->", dict_item)

    print('Estoy en finally')
    print('Colorin, colorado, este programa se ha acabado')

main()
'''