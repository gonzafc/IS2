#!/usr/bin/env python3
"""
===============================================================================
COMPANY PROPERTY NOTICE
copyright UADER_FCyT_IS2 © 2022,2024 todos los derechos reservados.
===============================================================================
Módulo para el cálculo y gestión de números primos dentro de un intervalo,
refactorizado mediante programación orientada a objetos (POO) y aplicando
la estrategia "Branching by Abstraction".
===============================================================================
"""

from abc import ABC, abstractmethod
import math


class PrimeChecker(ABC):
    """
    Abstracción (Interface/Clase Base) para validadores de números primos.
    Permite aplicar 'Branching by Abstraction' intercambiando implementaciones.
    """
    @abstractmethod
    def compute(self, num: int) -> bool:
        """
        Evalúa si un número dado es primo.
        :param num: Número entero a evaluar.
        :return: True si es primo, False en caso contrario.
        """
        pass


class ClassPrimes(PrimeChecker):
    """
    Implementación optimizada y orientada a objetos para la validación
    de números primos.
    """
    
    def compute(self, num: int) -> bool:
        """
        Implementa el método compute heredado de la abstracción.
        Aplica optimización matemática evaluando divisores hasta la raíz cuadrada.
        """
        # Los números menores o iguales a 1 no son primos
        if num <= 1:
            return False
        
        # El 2 es el único primo par
        if num == 2:
            return True
        
        # Descartar números pares mayores a 2
        if num % 2 == 0:
            return False
        
        # Optimización O(√N): Evaluar impares desde 3 hasta la raíz cuadrada de 'num'
        root = int(math.isqrt(num))
        for i in range(3, root + 1, 2):
            if num % i == 0:
                return False  # Encontró un divisor, no es primo
                
        return True  # Es primo


def main() -> None:
    """
    Flujo principal del programa que interactúa con la abstracción.
    """
    lower_limit: int = 1
    upper_limit: int = 500

    print(f"Prime numbers between {lower_limit} and {upper_limit} are:")

    # Branching by Abstraction: El cliente depende de la interfaz/clase abstracta.
    # Si se deseara volver al algoritmo viejo o usar otra estrategia, solo se cambia la instancia.
    checker: PrimeChecker = ClassPrimes()

    # Bucle de control principal que delega la lógica a la clase encargada
    for num in range(lower_limit, upper_limit + 1):
        if checker.compute(num):
            print(num)


if __name__ == "__main__":
    main()