def censor(palabra):
    palabras_prohibidas = ("mameluco","monopatín","hereje")
    if palabra in palabras_prohibidas:
        return "***"
    return palabra

texto = "El hereje agarró el monopatín y se lo prestó al mameluco"
lista_palabras = texto.split()
print (lista_palabras)

texto_censurado = [ censor(palabra) for palabra in lista_palabras]
print (texto_censurado)
#reconstruimos texto listas con join
texto_censurado = " ".join(texto_censurado)
print (texto_censurado)
