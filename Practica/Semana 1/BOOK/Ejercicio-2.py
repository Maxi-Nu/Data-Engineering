import numpy as p
#Escribir un programa que pida al usuario cuántos números 
#quiere introducir. Luego que lea todos los números y realice 
#una media aritmética
a=int(input('Cantidad de numeros a leer:'))
numeros= list()
for i in range(a):
    b=int(input(f'inserte numero {i+1}:'))
    numeros.append(b)
print(numeros)
print(p.mean(numeros))