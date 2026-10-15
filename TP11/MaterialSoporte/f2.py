import unittest


# Asumimos que estas son las funciones del programa principal
def factorial(n):
    if n > 1000:
        return None
    if n == 0 or n == 1:
        return 1
    elif n > 1:
        return n * factorial(n - 1)


def imprimir_factorial(n):
    if n < 0:
        return "El número debe ser un entero positivo."
    else:
        resultado = factorial(n)
        if resultado is not None:
            return f"El factorial de {n} es {resultado}"
        else:
            return "El valor de n es demasiado grande."


def obtener_valor():
    pass  # En este caso no probamos funciones con entrada directa por input en test unitarios


# Clase de pruebas unitarias
class TestFactorialProgram(unittest.TestCase):

    # Prueba para el cálculo correcto del factorial
    def test_factorial(self):
        self.assertEqual(factorial(0), 1)
        self.assertEqual(factorial(1), 1)
        self.assertEqual(factorial(4), 24)
        self.assertEqual(factorial(5), 120)

    # Prueba para controlar los límites superiores del valor de n
    def test_factorial_max_limit(self):
        self.assertIsNone(factorial(1001))  # Debería devolver None si n es mayor a 1000

    # Prueba para el caso de número negativo
    def test_factorial_negative(self):
        self.assertEqual(
            imprimir_factorial(-5), "El número debe ser un entero positivo."
        )

    # Prueba para el caso de factorial grande que sobrepasa el límite
    def test_imprimir_factorial_large(self):
        self.assertEqual(imprimir_factorial(1001), "El valor de n es demasiado grande.")

    # Prueba para la función imprimir_factorial
    def test_imprimir_factorial(self):
        self.assertEqual(imprimir_factorial(5), "El factorial de 5 es 120")
        self.assertEqual(imprimir_factorial(0), "El factorial de 0 es 1")
        self.assertEqual(imprimir_factorial(1), "El factorial de 1 es 1")


# Permite ejecutar los test si este archivo se ejecuta directamente
if __name__ == "__main__":
    unittest.main()
