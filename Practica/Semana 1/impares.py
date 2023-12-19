a=int(input('Ingrese un numero impar: '))
while(a%2==0):
        print('incorrecto')
        a=int(input('Ingrese otro numero: '))
print(f'el numero impar es: {a}')