'''
Ejercicio que muestre por pantalla:

Estimado D.Manuel Montesinos, usted ha realizado una compra por importe 
de 1573,75 € con lo cual procede aplicar un descuento del 15% que
representan 236,06 €.

Importe:        1573,75€
Descuento: 15%  -236,06€
                =========    
Total a pagar:  1337,69€
                =========
                '''
                
nombre_cliente = "D.Manuel Montesinos"
importe = 1573.75
l_campo = 8
l_dec = 2
#importe_str = str(  importe ) triangulación
importe_str = f"{float(importe):{l_campo},.{l_dec}f}".replace(",","M").replace(".",",").replace("M",".")

descuento = importe * 0.15
total_a_pagar = importe - descuento

print(f"Estimado {nombre_cliente}, usted ha realizado una compra por importe ")
print(f"de {importe_str}€ con lo cual procede aplicar un descuento del 15% que")
print(f"representan {descuento:6,.2f}€.\n")

print(f"Importe:        €{importe_str}")
print(f"Descuento: 15%  €{-descuento:9,.2f}")
print("                ===========")    
print(f"Total a pagar:  €{total_a_pagar:9,.2f}")
print("                ===========")


