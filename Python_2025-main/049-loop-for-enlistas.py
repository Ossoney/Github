from my_toolbox import *
from my_ostools import *

clear_p

'''
for - para
es un ciclo determinado
'''

mess_single('for en una lista')

my_list = ["Carlos","Olga","Tita","Carmen","JC"]

for persona in my_list:
    print(persona)

mess_single('mostrar índices de la lista')

for persona in my_list:
    my_index = my_list.index(persona)
    print(f"El indice de {persona} es {my_index}")

#

people_names = ["Jose", " Ainhoa", "Javier", "Ana", "Julio", "Amelia"]

for persona in people_names:
    if persona.strip().lower().startswith("a"):
        print(f"{persona}, tu nombre empieza por A")
    else:
        print(f"{persona}, tu nombre no empieza por A")
        

# for anidado

people_dict = {
    "Carlos" : ["Tita", "JC"],
    "Luisa" : ["Inés", "Rosa"],
    "Amalia" : [],
    "Celia" : ["Eduardo", "Jose Antonio", "Celia", "Manuel"]
}

for p,h in people_dict.items():
    if (len(h)>0):
        print (f"{p} tiene {len(h)} hijo/s")    
        

sep_double()
 
people_dict = {
    "Carlos" : ["Tita", 
                ["Nelson", "Erick"], 
                "JC",
                []
                ],
    "Luisa" : ["Inés",
               ["Marcos", "Mónica"], 
               "Rosa",
               ["Alejandro", "María"]
               ],
    "Amalia" : [],
    "Celia" : ["Eduardo", "Jose Antonio", "Celia", "Manuel"]
}

'''
for p,h in people_dict.items():
    if len(h)>0:
        #print (f"{p} tiene {len(h)} hijo/s")    
        
        for a, n in h:
            if len(n)>0:
                print(f"{h} tiene {len(n)} nietos")
'''
        
'''
for abuelo, hijos in people_dict.items():
    print(f"{abuelo}:")
    for hijo in hijos:
        if isinstance(hijo, list):
            for nieto in hijo:
                print(f"  Nieto: {nieto}")
        else:
            print(f"  Hijo: {hijo}")
'''

my_p = [["patatas", "zanahorias"],["Queso","jamón"],["leche","zumo"]]

for a,b in my_p:
    for d in a,b:
        print(d)
    
