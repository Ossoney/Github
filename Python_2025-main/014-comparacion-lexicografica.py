mi_lista = ["Olga", "Josefa", "Lidia"]
print("mi lista:", type(mi_lista), len(mi_lista), mi_lista)

max_mi_lista = max(mi_lista)
print(f"El valor máximo de {mi_lista} es {max_mi_lista}")


'''
Comparación lexicográfica

1) Python compara las cadenas caracter por caracter empezando por el primer
caracter de cada cadena

    Si los primeros caracteres son iguales, se compara el siguiente y así 
    sucesicamente

2) Código/Valos Unicode de las letras iniciales

    Olga    → Comienza por "O" (Unicode 79)
    Josefa  → Comienza por "J" (Unicode 74)
    Lidia   → Comienza por "L" (Unicode 76)
'''

abecedario_desordenado = [
    'm', 'a', 'ñ', 'b', 'z', 'c', 'y', 'd', 'x',
    'e', 'w', 'f', 'v', 'g', 'u', 'h', 't', 'i',
    's', 'j', 'r', 'k', 'q', 'l', 'p', 'n', 'o'
]

max_letra = max(abecedario_desordenado)
min_letra = min(abecedario_desordenado)

print(F'La letra con menor valor es "{min_letra}" y la de mayor valor es "{max_letra}"')