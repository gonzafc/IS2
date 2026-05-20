from Componente import Componente


class Pieza(Componente):
    def __init__(self, nombre):
        self.nombre = nombre

    def mostrar(self):
        print(self.nombre)