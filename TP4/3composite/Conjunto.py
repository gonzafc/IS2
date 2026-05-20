from Componente import Componente


class Conjunto(Componente):
    def __init__(self, nombre):
        self.nombre = nombre
        self.elementos = []

    def agregar(self, componente):
        self.elementos.append(componente)

    def mostrar(self):
        print(f"Conjunto: {self.nombre}")
        for elemento in self.elementos:
            elemento.mostrar()