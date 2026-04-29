import copy

class Prototipo:
    def clonar(self):
        return copy.deepcopy(self)


class Documento(Prototipo):
    def __init__(self, contenido):
        self.contenido = contenido

    def mostrar(self):
        print(self.contenido)


# Uso
doc1 = Documento("Original")
doc2 = doc1.clonar()
doc3 = doc2.clonar()

doc2.contenido = "Copia 1"
doc3.contenido = "Copia 2"

doc1.mostrar()
doc2.mostrar()
doc3.mostrar()
