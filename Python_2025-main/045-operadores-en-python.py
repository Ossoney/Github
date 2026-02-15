'''
1. OPERADORES ARITMÉTICOS
----------------------------------------------------
Operador   | Descripción        | Ejemplo
----------------------------------------------------
+          | Suma               | x + y
-          | Resta              | x - y
*          | Multiplicación     | x * y
/          | División           | x / y
%          | Módulo (resto)     | x % y
**         | Exponenciación     | x ** y
//         | División entera    | x // y


2. OPERADORES DE COMPARACIÓN
----------------------------------------------------
Operador   | Descripción        | Ejemplo
----------------------------------------------------
==         | Igual a            | x == y
!=         | Diferente a        | x != y
>          | Mayor que          | x > y
>=         | Mayor o igual que  | x >= y
<          | Menor que          | x < y
<=         | Menor o igual que  | x <= y


3. OPERADORES LÓGICOS
--------------------------------------------------------------------------
Operador     | Descripción                    | Ejemplo
--------------------------------------------------------------------------
and          | Verdadero si ambas condiciones | x > 5 and x < 10
             | son verdaderas                 |
-------------+--------------------------------+---------------------------
or           | Verdadero si al menos una      |
(o inclusivo)| condición es verdadera         |
-------------+--------------------------------+---------------------------
xor          | Funciona a nivel de bits y con | Se puede simular con
(o exclusivo)| booleanos                      | con:
             |                                |
             | Verdadero cuando exactamente   | (x or y) and not (x and y)
             | uno de los operandos es        | 
             | verdadero, pero no ambos       | 
-------------+--------------------------------+---------------------------
not          | Invierte el valor lógico       | not(x > 5)


4. OPERADORES DE ASIGNACIÓN
----------------------------------------------------
Operador   | Descripción              | Ejemplo
----------------------------------------------------
=          | Asignación simple        | x = 5
+=         | Suma y asigna            | x += 3  (equivalente a x = x + 3)
-=         | Resta y asigna           | x -= 3
*=         | Multiplica y asigna      | x *= 3
/=         | Divide y asigna          | x /= 3
%=         | Módulo y asigna          | x %= 3
**=        | Exponenciación y asigna  | x **= 3
//=        | División entera y asigna | x //= 3


5. OPERADORES BIT A BIT (BITWISE)
----------------------------------------------------
Operador   | Descripción                   | Ejemplo
----------------------------------------------------
&          | AND bit a bit                 | x & y
|          | OR bit a bit                  | x | y
^          | XOR bit a bit                 | x ^ y
~          | Complemento a uno             | ~x
<<         | Desplazamiento a la izquierda | x << 2
>>         | Desplazamiento a la derecha   | x >> 2

Los operadores bit a bit (bitwise) en Python se utilizan para realizar 
operaciones a nivel de bits sobre números enteros. 

Cada número entero se representa en binario, y estos operadores permiten
manipular directamente los bits individuales que componen esos números.

Son útiles en áreas como la programación de sistemas embebidos, la 
criptografía, la compresión de datos, o cuando se trabaja con banderas 
o máscaras de bits.



6. OPERADORES DE MEMBRESÍA
---------------------------------------------------------------------
Operador   | Descripción                       | Ejemplo
---------------------------------------------------------------------
in         | Devuelve True si un valor está    | "a" in "manzana"
           | en la secuencia                   | 
---------------------------------------------------------------------
not in     | Devuelve True si un valor no está | "x" not in "manzana"
           | en la secuencia                   |
---------------------------------------------------------------------



7. OPERADORES DE IDENTIDAD
------------------------------------------------------------------------
Operador   | Descripción                                    | Ejemplo
------------------------------------------------------------------------
is         | Devuelve True si ambos objetos son el mismo    | x is y
is not     | Devuelve True si ambos objetos no son el mismo | x is not y
'''
