#!/usr/bin/python
#*-------------------------------------------------------------------------*
#* factorial.py                                                            *
#* calcula el factorial de un número                                       *
#* Dr.P.E.Colla (c) 2022                                                   *
#* Creative commons                                                        *
#*-------------------------------------------------------------------------*
import sys

def factorial(num): 
    if num < 0: return 0
    elif num == 0: return 1
    else: 
        fact = 1
        while(num > 1): 
            fact *= num 
            num -= 1
        return fact 

def parsear_rango(entrada):
    """
    Intenta parsear la entrada. Si falla, lanza ValueError 
    para que el bucle principal lo capture.
    """
    LIMITE_MIN = 1
    LIMITE_MAX = 60

    if not entrada or entrada == "-":
        raise ValueError("Entrada vacía")

    pos_guion = entrada.rfind("-")

    if pos_guion == 0:  # Caso "-10"
        inicio, fin = LIMITE_MIN, int(entrada[1:])
    elif pos_guion == len(entrada) - 1:  # Caso "50-"
        inicio, fin = int(entrada[:-1]), LIMITE_MAX
    elif pos_guion > 0:  # Caso "-2-3" o "4-8"
        inicio = int(entrada[:pos_guion])
        fin = int(entrada[pos_guion + 1:])
    else:  # Caso número único
        return [int(entrada)]

    return list(range(min(inicio, fin), max(inicio, fin) + 1))

# --- Lógica de Interacción ---
entrada_valida = False
lista_numeros = []

# Verificamos si vino por argumento primero
if len(sys.argv) >= 2:
    try:
        lista_numeros = parsear_rango(sys.argv[1])
        entrada_valida = True
    except ValueError:
        print(f" El argumento '{sys.argv[1]}' tiene un formato incorrecto.")

# Si no hubo argumento o el argumento falló, entramos al bucle
while not entrada_valida:
    entrada_usuario = input("\n Ingrese un número o rango válido (ej: -10, 50- o -2-5): ").strip()
    try:
        lista_numeros = parsear_rango(entrada_usuario)
        entrada_valida = True # Si llega acá, el parseo fue exitoso
    except ValueError:
        print(" Formato incorrecto. Intente de nuevo (ejemplos: 5, -10, 20- o 2-8).")

# Mostrar resultados
print(f"\n--- Procesando {len(lista_numeros)} valores ---")
for n in lista_numeros:
    if n < 0:
        print(f"Factorial {n}! = No existe (negativo)")
    else:
        print(f"Factorial {n}! = {factorial(n)}")