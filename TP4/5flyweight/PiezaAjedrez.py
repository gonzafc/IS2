class PiezaAjedrez:
    def __init__(self, tipo):
        self.tipo = tipo

    def mostrar(self, posicion):
        print(f"{self.tipo} en {posicion}")