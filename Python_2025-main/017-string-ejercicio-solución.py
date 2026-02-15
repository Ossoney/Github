from my_toolbox import *

mess_single("Paso 1. Reproducir lo solicitado")

print('''
Estimado D. Manuel Montesinos usted ha realizado una compra por importe
de 1573.75 € con lo lo cual procede aplicar un descuento del 15% que 
representan 236.06 €.

Importe:                € 1.573,75
Descuento:  % 15        €  -236,06

                        ==========
Total a pagar:          € 1.337,69
                        ==========
''')


sep_double()



mess_single("Paso 2. Utilizar f-strings")

tratamiento_cliente = "D."
nombre_cliente = "Manuel Montesinos"

long_campo = 11
long_dec = 2

importe_compra = 1573.75
importe_compra_str = f"{float(importe_compra):{long_campo},.{long_dec}f}".replace(",", "M").replace(".",",").replace("M", ".")


porc_descuento = 15
moneda_simb = "€"


importe_desc = importe_compra * porc_descuento / 100
importe_desc_str = f"{float(-1 * importe_desc):{long_campo},.{long_dec}f}".replace(",", "M").replace(".",",").replace("M", ".")


total_fact = importe_compra - importe_desc
total_fact_str = f"{float(total_fact):{long_campo},.{long_dec}f}".replace(",", "M").replace(".",",").replace("M", ".")

print(f'''
Estimado {tratamiento_cliente} {nombre_cliente} usted ha realizado una compra por importe
de {importe_compra_str} {moneda_simb} con lo lo cual procede aplicar un descuento del {porc_descuento}% que 
representan {importe_desc_str} {moneda_simb}.

Importe:                {moneda_simb} {importe_compra_str}
Descuento:  % {porc_descuento}        {moneda_simb} {importe_desc_str}

                        ==============
Total a pagar:          {moneda_simb} {total_fact_str}
                        ==============
''')
