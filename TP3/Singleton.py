class CalculadoraImpuestos:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
        return cls._instancia

    def calcular(self, base):
        iva = base * 0.21
        iibb = base * 0.05
        municipal = base * 0.012
        return base + iva + iibb + municipal


# Uso
calc = CalculadoraImpuestos()
print(calc.calcular(1000))  # 1272.0
