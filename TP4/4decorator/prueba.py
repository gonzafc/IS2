from numero import Numero
from cuentas import Sumar2, Multiplicar2, Dividir3

numero = Numero(9)

print(numero.operar())

numero = Sumar2(numero)
print(numero.operar())

numero = Multiplicar2(numero)
print(numero.operar())

numero = Dividir3(numero)
print(numero.operar())