# 20 ejercicios de Python con `if`, `try/except` y `for` anidados – Enunciados y soluciones

## Ejercicios de complejidad media-baja (1–10)

---

### Ejercicio 1 (media-baja): Suma de filas válidas
Pide al usuario el número de filas y columnas de una matriz de enteros. Luego pide los valores fila por fila.

Debes:
- Usar `try/except` al convertir cada valor a `int` para ignorar entradas no numéricas (si falla la conversión, reemplázalo por 0).
- Recorrer la matriz con un `for` anidado para calcular la suma de cada fila.
- Usar `if` para mostrar solo las filas cuya suma sea mayor que 0.

#### Solución orientativa
```python
matriz = []
try:
    filas = int(input("Número de filas: "))
    columnas = int(input("Número de columnas: "))
except ValueError:
    print("Entrada inválida. Usando 2x2 por defecto.")
    filas, columnas = 2, 2

for i in range(filas):
    fila = []
    for j in range(columnas):
        valor_str = input(f"Valor en posición ({i}, {j}): ")
        try:
            valor = int(valor_str)
        except ValueError:
            print("Valor no numérico, se usará 0.")
            valor = 0
        fila.append(valor)
    matriz.append(fila)

for i, fila in enumerate(matriz):
    suma = 0
    for valor in fila:
        suma += valor
    if suma > 0:
        print(f"Fila {i} -> {fila}, suma = {suma}")
```

---

### Ejercicio 2 (media-baja): Contar vocales por palabra
Pide una frase al usuario y divídela en palabras.

Debes:
- Usar `for` anidado para recorrer palabras y, dentro, caracteres.
- Usar `if` para contar solo vocales (a, e, i, o, u, mayúsculas o minúsculas).
- Usar `try/except` para capturar cualquier error inesperado (por ejemplo, si la frase es `None`) y mostrar un mensaje de error sin que el programa termine.

#### Solución orientativa
```python
frase = input("Introduce una frase: ")

try:
    palabras = frase.split()
    vocales = "aeiouAEIOU"
    for palabra in palabras:
        contador = 0
        for ch in palabra:
            if ch in vocales:
                contador += 1
        print(f"'{palabra}' tiene {contador} vocal(es)")
except Exception as e:
    print("Ha ocurrido un error al procesar la frase:", e)
```

---

### Ejercicio 3 (media-baja): Tabla de multiplicar validada
Pide un número al usuario y muestra su tabla de multiplicar del 1 al 10.

Debes:
- Usar `try/except` para validar que el número introducido es un entero.
- Si no lo es, mostrar un mensaje y asignar por defecto el valor 1.
- Usar un `for` externo para recorrer los multiplicadores y un `for` interno para mostrar el resultado como `n * i = resultado`.
- Usar `if` para marcar con un texto especial las multiplicaciones cuyo resultado sea par.

#### Solución orientativa
```python
num_str = input("Introduce un número entero: ")
try:
    n = int(num_str)
except ValueError:
    print("No es un entero válido. Usando 1 por defecto.")
    n = 1

for i in range(1, 11):
    resultado = n * i
    linea = f"{n} * {i} = {resultado}"
    if resultado % 2 == 0:
        linea += " (par)"
    print(linea)
```

---

### Ejercicio 4 (media-baja): Filtrado de números positivos
Pide al usuario una lista de números separados por comas.

Debes:
- Dividir la cadena y recorrerla con un `for`.
- Dentro de un `try/except`, convertir cada elemento a `float` y, si falla, ignorar ese elemento.
- Usar `if` dentro de un `for` anidado (por ejemplo, recorrer una lista de listas con los números ya agrupados) para quedarte solo con los positivos.
- Mostrar la lista final de números positivos válidos.

#### Solución orientativa
```python
entrada = input("Introduce números separados por comas: ")
partes = entrada.split(",")

todos = []
sublista = []
for p in partes:
    p = p.strip()
    try:
        num = float(p)
        sublista.append(num)
    except ValueError:
        print(f"'{p}' no es un número válido y se ignora.")

# metemos la sublista en una lista de listas para usar for anidado
todos.append(sublista)

positivos = []
for fila in todos:
    for num in fila:
        if num > 0:
            positivos.append(num)

print("Números positivos válidos:", positivos)
```

---

### Ejercicio 5 (media-baja): Buscar un valor en una matriz
Crea en código una matriz (lista de listas) de enteros predefinida.

Debes:
- Pedir al usuario un número a buscar y validarlo con `try/except`.
- Usar dos `for` anidados para recorrer la matriz.
- Usar `if` para comprobar si el número aparece y mostrar su posición (fila, columna) cada vez que se encuentre.
- Si no se encuentra, mostrar un mensaje indicándolo.

#### Solución orientativa
```python
matriz = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

num_str = input("Número a buscar en la matriz: ")
try:
    objetivo = int(num_str)
except ValueError:
    print("Valor inválido, se buscará el número 0.")
    objetivo = 0

encontrado = False
for i in range(len(matriz)):
    for j in range(len(matriz[i])):
        if matriz[i][j] == objetivo:
            print(f"Encontrado en fila {i}, columna {j}")
            encontrado = True

if not encontrado:
    print("El número no se encuentra en la matriz.")
```

---

### Ejercicio 6 (media-baja): Promedio de notas válidas
Pide al usuario varias listas de notas (por ejemplo, tres asignaturas), cada una separada por comas.

Debes:
- Guardar cada lista en una lista de listas (matriz).
- Usar `for` anidados para recorrer cada asignatura y sus notas.
- Usar `try/except` para convertir las notas a `float`; si falla, ignora esa nota.
- Usar `if` para contar solo las notas entre 0 y 10.
- Calcular y mostrar el promedio por asignatura.

#### Solución orientativa
```python
num_asignaturas = 3
matriz_notas = []

for i in range(num_asignaturas):
    entrada = input(f"Notas de la asignatura {i+1} (separadas por comas): ")
    partes = entrada.split(",")
    fila = []
    for p in partes:
        p = p.strip()
        try:
            nota = float(p)
            if 0 <= nota <= 10:
                fila.append(nota)
            else:
                print(f"Nota fuera de rango [0,10]: {nota}")
        except ValueError:
            print(f"'{p}' no es una nota válida y se ignora.")
    matriz_notas.append(fila)

for i, fila in enumerate(matriz_notas):
    if len(fila) > 0:
        promedio = sum(fila) / len(fila)
        print(f"Promedio asignatura {i+1}: {promedio:.2f}")
    else:
        print(f"Asignatura {i+1} sin notas válidas.")
```

---

### Ejercicio 7 (media-baja): Contar caracteres especiales
Pide una lista de palabras y una lista de caracteres especiales (por ejemplo, `!`, `?`, `@`).

Debes:
- Usar un `for` anidado para comparar cada carácter de cada palabra con cada carácter especial.
- Usar `if` para aumentar un contador cuando haya coincidencia.
- Usar `try/except` para capturar errores si el usuario no escribe nada o introduce un tipo no esperado.
- Mostrar cuántas veces aparece cada carácter especial en total.

#### Solución orientativa
```python
palabras_str = input("Introduce palabras separadas por comas: ")
especiales_str = input("Introduce caracteres especiales separados por comas: ")

try:
    palabras = [p.strip() for p in palabras_str.split(",") if p.strip()]
    especiales = [e.strip() for e in especiales_str.split(",") if e.strip()]
    conteos = {e: 0 for e in especiales}

    for palabra in palabras:
        for ch in palabra:
            for esp in especiales:
                if ch == esp:
                    conteos[esp] += 1

    for esp, cant in conteos.items():
        print(f"'{esp}' aparece {cant} vez/veces")
except Exception as e:
    print("Error procesando la entrada:", e)
```

---

### Ejercicio 8 (media-baja): Lista de listas de enteros
Pide al usuario cuántas sublistas quiere crear y cuántos elementos tendrá cada una.

Debes:
- En un `for` externo, crear cada sublista.
- En un `for` interno, pedir cada valor y validarlo con `try/except` (si falla, usar 0).
- Usar `if` para contar cuántos números son mayores que un umbral dado (p. ej., 10).
- Al final, mostrar la lista de listas y el número de elementos que superan el umbral.

#### Solución orientativa
```python
try:
    n_listas = int(input("¿Cuántas sublistas quieres?: "))
    n_elementos = int(input("¿Cuántos elementos por sublista?: "))
    umbral = float(input("Umbral (por ejemplo 10): "))
except ValueError:
    print("Entrada inválida, se usarán valores por defecto.")
    n_listas, n_elementos, umbral = 2, 3, 10.0

listas = []
mayores = 0

for i in range(n_listas):
    fila = []
    for j in range(n_elementos):
        valor_str = input(f"Valor para lista {i}, posición {j}: ")
        try:
            valor = float(valor_str)
        except ValueError:
            print("No es número, usando 0.")
            valor = 0.0
        fila.append(valor)
        if valor > umbral:
            mayores += 1
    listas.append(fila)

print("Listas:")
for fila in listas:
    print(fila)
print("Elementos mayores que el umbral:", mayores)
```

---

### Ejercicio 9 (media-baja): Matriz booleana
Crea una matriz de enteros (por ejemplo, 3x3) solicitados al usuario.

Debes:
- Validar con `try/except` cada entero introducido.
- Usar `for` anidado para generar otra matriz del mismo tamaño con valores `True` o `False` según si el número original es par.
- Usar `if` para decidir el valor booleano.
- Mostrar ambas matrices.

#### Solución orientativa
```python
filas = columnas = 3
matriz = []

for i in range(filas):
    fila = []
    for j in range(columnas):
        valor_str = input(f"Entero para posición ({i},{j}): ")
        try:
            valor = int(valor_str)
        except ValueError:
            print("No es entero, usando 0.")
            valor = 0
        fila.append(valor)
    matriz.append(fila)

matriz_bool = []
for i in range(filas):
    fila_bool = []
    for j in range(columnas):
        if matriz[i][j] % 2 == 0:
            fila_bool.append(True)
        else:
            fila_bool.append(False)
    matriz_bool.append(fila_bool)

print("Matriz original:")
for fila in matriz:
    print(fila)

print("Matriz booleana (True = par):")
for fila in matriz_bool:
    print(fila)
```

---

### Ejercicio 10 (media-baja): Longitud de palabras y filtrado
Pide al usuario una lista de palabras separadas por comas.

Debes:
- Crear una lista de listas donde cada sublista contenga la palabra y su longitud.
- Usar `for` anidado para recorrer esta estructura y aplicar un `if` que seleccione solo las palabras con longitud mayor o igual a 5.
- Usar `try/except` para gestionar cualquier error al calcular longitudes (por ejemplo, si algún elemento es `None`).
- Mostrar las palabras que cumplen la condición y su longitud.

#### Solución orientativa
```python
entrada = input("Palabras separadas por comas: ")
partes = [p.strip() for p in entrada.split(",") if p.strip()]

palabras_info = []

for p in partes:
    try:
        longitud = len(p)
        palabras_info.append([p, longitud])
    except Exception as e:
        print(f"Error calculando longitud de '{p}':", e)

print("Palabras con longitud >= 5:")
for palabra, longitud in palabras_info:
    if longitud >= 5:
        print(f"{palabra} (longitud {longitud})")
```

---

## Ejercicios de complejidad media (11–20)

---

### Ejercicio 11 (media): Validación de matriz numérica y suma diagonal
Pide al usuario el tamaño de una matriz cuadrada y luego los elementos fila por fila.

Debes:
- Usar `try/except` para validar tanto el tamaño como cada elemento numérico (si falla la conversión, usar 0).
- Usar `for` anidado para construir la matriz.
- Usar `if` dentro del recorrido para calcular la suma de la diagonal principal.
- Mostrar la matriz y la suma de la diagonal.

#### Solución orientativa
```python
try:
    n = int(input("Tamaño de la matriz cuadrada: "))
    if n <= 0:
        raise ValueError("El tamaño debe ser positivo")
except Exception as e:
    print("Tamaño inválido, usando 3x3. Detalle:", e)
    n = 3

matriz = []
for i in range(n):
    fila = []
    for j in range(n):
        valor_str = input(f"Valor para ({i},{j}): ")
        try:
            valor = int(valor_str)
        except ValueError:
            print("No es entero, usando 0.")
            valor = 0
        fila.append(valor)
    matriz.append(fila)

suma_diagonal = 0
for i in range(n):
    for j in range(n):
        if i == j:
            suma_diagonal += matriz[i][j]

print("Matriz:")
for fila in matriz:
    print(fila)
print("Suma de la diagonal principal:", suma_diagonal)
```

---

### Ejercicio 12 (media): Normalización de datos
Pide al usuario una matriz de enteros (lista de listas) representando medidas.

Debes:
- Usar `try/except` para validar cada número al crear la matriz.
- Usar `for` anidado para encontrar el valor máximo.
- Usar de nuevo `for` anidado para crear una nueva matriz con valores normalizados entre 0 y 1 usando la fórmula `valor / maximo`.
- Usar `if` para evitar división entre cero (si el máximo es 0).

#### Solución orientativa
```python
try:
    filas = int(input("Número de filas: "))
    columnas = int(input("Número de columnas: "))
except ValueError:
    print("Entrada inválida, se usará 2x2.")
    filas, columnas = 2, 2

matriz = []
for i in range(filas):
    fila = []
    for j in range(columnas):
        valor_str = input(f"Medida para ({i},{j}): ")
        try:
            valor = float(valor_str)
        except ValueError:
            print("No es número, usando 0.")
            valor = 0.0
        fila.append(valor)
    matriz.append(fila)

maximo = None
for fila in matriz:
    for valor in fila:
        if maximo is None or valor > maximo:
            maximo = valor

if maximo == 0:
    print("Todas las medidas son 0, no se puede normalizar.")
else:
    normalizada = []
    for fila in matriz:
        fila_norm = []
        for valor in fila:
            fila_norm.append(valor / maximo)
        normalizada.append(fila_norm)

    print("Matriz original:")
    for fila in matriz:
        print(fila)

    print("Matriz normalizada:")
    for fila in normalizada:
        print(fila)
```

---

### Ejercicio 13 (media): Matriz de coincidencias de caracteres
Pide una palabra al usuario.

Debes:
- Crear una matriz cuadrada donde la celda (i, j) sea `1` si el carácter i es igual al carácter j, y `0` en caso contrario.
- Usar `for` anidado para construir la matriz.
- Usar `if` para decidir si poner 1 o 0.
- Usar `try/except` para manejar errores si la palabra es vacía o no es una cadena.

#### Solución orientativa
```python
palabra = input("Introduce una palabra: ")

try:
    if not isinstance(palabra, str) or len(palabra) == 0:
        raise ValueError("Debes introducir una cadena no vacía")

    n = len(palabra)
    matriz = []
    for i in range(n):
        fila = []
        for j in range(n):
            if palabra[i] == palabra[j]:
                fila.append(1)
            else:
                fila.append(0)
        matriz.append(fila)

    print("Matriz de coincidencias:")
    for fila in matriz:
        print(fila)
except Exception as e:
    print("Error:", e)
```

---

### Ejercicio 14 (media): Filtrado de matriz por rango
Define en código una matriz de números enteros de tamaño 4x4.

Debes:
- Pedir al usuario un rango `[min, max]` y validarlo con `try/except`.
- Usar `for` anidado para recorrer la matriz.
- Usar `if` para crear una nueva matriz con solo los valores dentro del rango (los que no estén en el rango se reemplazan por `None`).
- Mostrar la matriz original y la filtrada.

#### Solución orientativa
```python
matriz = [
    [1, 5, 10, 15],
    [20, 25, 30, 35],
    [40, 45, 50, 55],
    [60, 65, 70, 75]
]

try:
    minimo = int(input("Mínimo del rango: "))
    maximo = int(input("Máximo del rango: "))
    if minimo > maximo:
        raise ValueError("El mínimo no puede ser mayor que el máximo")
except Exception as e:
    print("Rango inválido, se usará [0, 100]. Detalle:", e)
    minimo, maximo = 0, 100

filtrada = []
for fila in matriz:
    fila_filtrada = []
    for valor in fila:
        if minimo <= valor <= maximo:
            fila_filtrada.append(valor)
        else:
            fila_filtrada.append(None)
    filtrada.append(fila_filtrada)

print("Matriz original:")
for fila in matriz:
    print(fila)

print("Matriz filtrada:")
for fila in filtrada:
    print(fila)
```

---

### Ejercicio 15 (media): Conteo de errores en lista de listas
Pide al usuario varias listas de números (por ejemplo, 3 líneas, cada una separada por comas).

Debes:
- Crear una lista de listas con estos datos.
- Usar `for` anidado para intentar convertir cada valor a `int`.
- Usar `try/except` para contar cuántos valores han dado error de conversión.
- Usar `if` para almacenar solo los enteros válidos en una nueva estructura.
- Mostrar la lista limpia y el número total de errores.

#### Solución orientativa
```python
num_listas = 3
listas_originales = []

for i in range(num_listas):
    entrada = input(f"Lista {i+1} de números (separados por comas): ")
    partes = entrada.split(",")
    listas_originales.append(partes)

listas_limpias = []
errores = 0

for lista in listas_originales:
    fila = []
    for elemento in lista:
        elemento = elemento.strip()
        try:
            valor = int(elemento)
            fila.append(valor)
        except ValueError:
            errores += 1
    listas_limpias.append(fila)

print("Listas limpias:")
for fila in listas_limpias:
    print(fila)

print("Número total de errores de conversión:", errores)
```

---

### Ejercicio 16 (media): Buscador de subcadenas en matriz de texto
Pide al usuario varias frases y una palabra clave.

Debes:
- Guardar las frases en una lista.
- Usar `for` anidado: el externo recorre las frases, el interno recorre palabras.
- Usar `if` para comprobar si la palabra clave aparece en cada frase.
- Usar `try/except` para evitar errores si alguna frase es vacía o no tiene formato esperado.
- Mostrar en qué frases (índice) y cuántas veces aparece la palabra clave.

#### Solución orientativa
```python
try:
    n = int(input("¿Cuántas frases quieres introducir?: "))
except ValueError:
    print("Valor inválido, se usarán 3 frases.")
    n = 3

frases = []
for i in range(n):
    frase = input(f"Frase {i+1}: ")
    frases.append(frase)

clave = input("Palabra clave a buscar: ")

for i, frase in enumerate(frases):
    try:
        palabras = frase.split()
        contador = 0
        for palabra in palabras:
            if palabra == clave:
                contador += 1
        print(f"Frase {i}: '{frase}' -> {contador} coincidencia(s)")
    except Exception as e:
        print(f"Error procesando la frase {i}:", e)
```

---

### Ejercicio 17 (media): Triángulo de números con validación
Pide al usuario un número entero `n` para construir un triángulo de números.

Debes:
- Validar `n` con `try/except` y, si es inválido o menor que 1, usar 1 por defecto.
- Usar `for` anidado para imprimir filas donde la fila i contiene los números del 1 a i.
- Usar `if` para marcar visualmente las filas pares (por ejemplo, añadiendo un texto al final de la línea).

#### Solución orientativa
```python
n_str = input("Altura del triángulo: ")
try:
    n = int(n_str)
    if n < 1:
        raise ValueError("n debe ser >= 1")
except Exception as e:
    print("Valor inválido, se usará n = 1. Detalle:", e)
    n = 1

for i in range(1, n + 1):
    linea = ""
    for j in range(1, i + 1):
        linea += str(j) + " "
    if i % 2 == 0:
        linea += "<- fila par"
    print(linea)
```

---

### Ejercicio 18 (media): Verificación de cuadrado mágico simplificado
Pide al usuario una matriz 3x3 de enteros.

Debes:
- Validar cada entrada con `try/except` (si falla, usar 0).
- Usar `for` anidado para calcular la suma de cada fila y cada columna.
- Usar `if` para comprobar si todas las filas y columnas tienen la misma suma.
- Mostrar si la matriz cumple la condición de "cuadrado mágico" simplificado (ignorando diagonales).

#### Solución orientativa
```python
n = 3
matriz = []

for i in range(n):
    fila = []
    for j in range(n):
        valor_str = input(f"Valor para ({i},{j}): ")
        try:
            valor = int(valor_str)
        except ValueError:
            print("No es entero, usando 0.")
            valor = 0
        fila.append(valor)
    matriz.append(fila)

sumas_filas = []
for fila in matriz:
    sumas_filas.append(sum(fila))

sumas_columnas = []
for j in range(n):
    suma_col = 0
    for i in range(n):
        suma_col += matriz[i][j]
    sumas_columnas.append(suma_col)

es_magico = True
if len(set(sumas_filas + sumas_columnas)) != 1:
    es_magico = False

print("Matriz:")
for fila in matriz:
    print(fila)

if es_magico:
    print("La matriz cumple la condición de cuadrado mágico simplificado.")
else:
    print("La matriz NO cumple la condición de cuadrado mágico simplificado.")
```

---

### Ejercicio 19 (media): Agrupar números por paridad
Pide al usuario una lista de listas de números (cada sublista, en una línea distinta, separando por comas).

Debes:
- Usar `try/except` para validar la conversión a `int`.
- Usar `for` anidado para recorrer todos los números.
- Usar `if` para agrupar los números en dos nuevas listas: pares e impares.
- Mostrar estas dos listas al final.

#### Solución orientativa
```python
try:
    n = int(input("¿Cuántas sublistas vas a introducir?: "))
except ValueError:
    print("Valor inválido, se usarán 2 sublistas.")
    n = 2

listas = []
for i in range(n):
    entrada = input(f"Sublista {i+1} (números separados por comas): ")
    partes = entrada.split(",")
    listas.append(partes)

pares = []
impares = []

for lista in listas:
    for elem in lista:
        elem = elem.strip()
        try:
            num = int(elem)
            if num % 2 == 0:
                pares.append(num)
            else:
                impares.append(num)
        except ValueError:
            print(f"'{elem}' no es un entero y se ignora.")

print("Pares:", pares)
print("Impares:", impares)
```

---

### Ejercicio 20 (media): Matriz de diferencias absolutas
Pide al usuario el tamaño `n` de una matriz cuadrada y luego los elementos.

Debes:
- Validar todo con `try/except` (tamaño y elementos).
- Usar `for` anidado para crear la matriz original.
- Calcular una segunda matriz donde cada posición contiene la diferencia absoluta entre el valor original y la media de todos los valores.
- Usar `if` si es necesario para controlar casos especiales (por ejemplo, si no hay datos válidos).
- Mostrar ambas matrices y la media calculada.

#### Solución orientativa
```python
try:
    n = int(input("Tamaño de la matriz cuadrada: "))
    if n <= 0:
        raise ValueError("n debe ser positivo")
except Exception as e:
    print("Valor inválido, se usará n=2. Detalle:", e)
    n = 2

matriz = []
for i in range(n):
    fila = []
    for j in range(n):
        valor_str = input(f"Valor para ({i},{j}): ")
        try:
            valor = float(valor_str)
        except ValueError:
            print("No es número, usando 0.")
            valor = 0.0
        fila.append(valor)
    matriz.append(fila)

valores = []
for fila in matriz:
    for v in fila:
        valores.append(v)

if len(valores) == 0:
    print("No hay datos válidos.")
else:
    media = sum(valores) / len(valores)
    matriz_diff = []
    for fila in matriz:
        fila_diff = []
        for v in fila:
            fila_diff.append(abs(v - media))
        matriz_diff.append(fila_diff)

    print("Matriz original:")
    for fila in matriz:
        print(fila)

    print(f"Media de los valores: {media:.2f}")

    print("Matriz de diferencias absolutas:")
    for fila in matriz_diff:
        print(fila)
```

