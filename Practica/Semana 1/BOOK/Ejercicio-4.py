"""Dadas dos listas (las que se quiera crear), generar una 
tercera con los elementos que estén presentes en AMBAS 
listas. Retornar esta nueva lista pero sin elementos 
duplicados."""

lista1=[1,2,3,4,5,6,7,8,9,0]
lista2=['a','b','c','d','e','f','g',3,4,5]
print(set(lista1+lista2))