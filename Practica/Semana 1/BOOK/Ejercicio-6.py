# Contar cuantas veces aparece un elemento en una lista

def contar(elemento,lista):
    b=0
    for i in lista:
        if(i==elemento):
         b+=1
    return b     
a=['a','b','c','c',1,2,2,2,'a']
print(contar("c",a))