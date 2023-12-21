#Escribir un programa que sume todos los números enteros impares desde el 0 hasta el 100
b=0
for i in range(0,101):
    if (i%2==1) :
        b+=i
print(b)