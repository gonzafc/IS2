"""
Modulo para comprobar la Conjetura de Collatz y contar iteraciones.
Copyright UADER_FCyT_IS2 (c) 2026 Todos los derechos reservados.
"""


def collatz(num: int) -> int:
    """Calcula el numero de iteraciones necesarias para alcanzar 1 segun Collatz."""
    if not isinstance(num, int) or isinstance(num, bool) or num <= 0 or num > 1999:
        raise ValueError("El numero debe ser un entero positivo menor o igual a 1999.")
    iteraciones = 0
    while num != 1:
        if num % 2 == 0:
            num = num // 2
        else:
            num = 3 * num + 1
        iteraciones += 1
    return iteraciones


def main() -> None:
    """Funcion principal que interactua con el usuario por teclado."""
    print("=== Comprobacion de la Conjetura de Collatz ===")
    try:
        entrada = input("Ingrese un numero entero positivo (1 a 1999): ")
        num = int(entrada)
        iteraciones = collatz(num)
        print(
            f"El numero de partida es {num} y el numero de iteraciones es {iteraciones}."
        )
    except ValueError as e:
        print(f"Error de validacion: {e}")


if __name__ == "__main__":
    main()
