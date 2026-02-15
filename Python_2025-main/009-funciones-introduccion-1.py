from my_toolbox import *
'''
Introducción a las funciones de usuario

    Son un tipo de objeto en Python

    Un función SIEMPRE debe devolver "algo" mediante
    la sentencia return (Para cumplir con la definición
    firmal de función)

    Debe hacer una única cosa (principio de responsabilidad
    simple)

    En la deficióń de una función:
        def my_function() ← No posee parámetros ← Aridad 0

        def my_function(param1, param2) ← Posee dos parámetros ← Aridad 2

        def my_function(param1, param2, *args) ← Posee parámetros ← Aridad 2 + n

        def my_function(param1, param2, *args, **kwargs) ← Posee parámetros ← Aridad 2 + n + m

            - param1, param2: Parámetros posicionales, fijos o normales

            - *args: Permite aceptar un número variable de parámetros
        
            - **kwargs: Permite aceptar un número variable de parámetros en formato {clave: valor}
'''

mess_single('Función con aridad 0')

def my_func_aridad0():
    num_1 = 7
    num_2 = 25
    num_3 = 4

    return  num_1 + num_2 + num_3

res = my_func_aridad0()
type_var(res)

sep_double()

mess_single("Función con aridad 3")

def my_func_aridad3(n1, n2, n3):
    # n2 = 100 # Cualquier parámetro recibido será una variable dentro
               # de la función 
    print(n2)
    return n1 + n2 + n3

print("Introduce tres números")
num_1 = float(input("Número1: ")) # ← 11
num_2 = float(input("Número2: ")) # ← 7
num_3 = float(input("Número3: ")) # ← 22

res = my_func_aridad3(num_1, num_2, num_3,)
type_var(res)

# print(n2) # Arroja error porque n2 pertenece al scope (ámbito) de la función

sep_double()

mess_single("Función con aridad3 + n")

def my_func_aridad3_n(n1, n2, n3, *args):

    print("n1: ", n1 )
    print("n2: ", n2)
    print("n3: ", n3)
    print("args: ", args)


my_func_aridad3_n(70, "Olga", True, 100, 200, 300)
my_func_aridad3_n(70, "Olga", True, [100, 200, 300])
my_func_aridad3_n(70, "Olga", True, (100, 200, 300))
my_func_aridad3_n(70, "Olga", True, {100, 200, 300})
my_func_aridad3_n(70, "Olga", True, {"a": 100, "b":200, "c": 300})

sep_double()

mess_single("Función con aridad2 + n + m")

def my_func_aridad2_n_m(p1, p2, *args, **kwargs):

    print("p1: ", p1 )
    print("p2:", p2) 
    print("args: ", args)
    print("kwargs: ", kwargs)



# Defines loa KWARGS con propiedad=Valor
my_func_aridad2_n_m("Carlos", "Varela", "González", name="Carlos", family_name1="Varela", family_name2="González")

# El diccionario en este caso no es un KWARG
my_func_aridad2_n_m("Carlos", "Varela", "González", {"name": "Carlos", "family_name1": "Varela", "family_name2":"González"})

sep_double()

mess_single("Función con aridad2 + n + m + m")

def my_func_aridad2_n_m_m(p1, p2, *args, **kwargs):
    print("p1: ", p1 )
    print("p2:", p2) 
    print("args: ", args)
    print("kwargs: ", kwargs)
    print(kwargs["my_father"]["family_name2"])

father_name = "Carlos"
father_family_name = "Varela"
my_args = "González"

my_family = {
    "my_father": {
        "name": "Carlos", 
        "family_name1": "Varela", 
        "family_name2":"González"
    },
    
    "my_mother": {
        "name": "Olga", 
        "family_name1": "Iglesias", 
        "family_name2":"Ferreiro"
    }
}

print(my_family)

my_func_aridad2_n_m_m(father_name, father_family_name, my_args, **my_family)

