class Factorial:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
        return cls._instancia

    def calcular(self, n):
        if n < 0:
            raise ValueError("No existe factorial de negativos")
        resultado = 1
        for i in range(1, n + 1):
            resultado *= i
        return resultado


# Uso
f1 = Factorial()
f2 = Factorial()

print(f1.calcular(5))  # 120
print(f1 is f2)        # True → misma instancia
