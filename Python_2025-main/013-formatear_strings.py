# La concatenación no formatea strings

color_ojos = "negro"
edad_usuario = 27

print("Tienes " + str(edad_usuario) + " años y tus ojos son de color " + color_ojos + ".")  # Concatenación

# en python hay 2 formas de formatear strings:
# 1. Usando el método format()
# insertar un par de llaves {} donde se visualizará el valor
print("Tienes {} años y tus ojos son de color {}.".format(edad_usuario, color_ojos))

# 2. Usando f-strings (a partir de Python 3.6) cadenas literales
# anteponiendo la letra f antes de las comillas
print(f"Tienes {edad_usuario} años y tus ojos son de color {color_ojos}.")

mi_lista = ["Olga", "Josefa", "Lidia"]

print("Mi lista:", type[mi_lista], len(mi_lista), mi_lista)

max_mi_lista = max(mi_lista)

print(f"El valor máximo de mi {mi_lista} es: {max_mi_lista}")





