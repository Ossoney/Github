#Comparación lexicográfica
#1) python compara cadenas caracter por caracter empezando por primer caracter
#Si los primeros caracteres son iguales, se compara el siguiente y así sucesivamente
#2) código/valor Unicode de cada caracter inicial
#Olga - comienza or O (79)
#Josefa - comienza por J (74)
#Lidia - comienza por L (76)
#Por lo tanto, el valor máximo es Olga

abecedario = ['ñ', 'q', 'm', 'x', 'a', 'j', 'v', 'g', 'n', 'e', 'r', 's', 'd', 'k', 'c', 'u', 'i', 'f', 'h', 'l', 'y', 't', 'w', 'o', 'b', 'p', 'z']

print(f"El valor máximo del abecedario es: {max(abecedario)}")  # El valor máximo es 'z'
print(f"El valor mínimo del abecedario es: {min(abecedario)}")  # El valor mínimo es 'a'

