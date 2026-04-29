from abc import ABC, abstractmethod

class Factura(ABC):
    def __init__(self, importe):
        self.importe = importe

    @abstractmethod
    def mostrar(self):
        pass


class FacturaResponsable(Factura):
    def mostrar(self):
        print(f"Factura A - Responsable Inscripto: ${self.importe}")


class FacturaNoInscripto(Factura):
    def mostrar(self):
        print(f"Factura B - No Inscripto: ${self.importe}")


class FacturaExento(Factura):
    def mostrar(self):
        print(f"Factura C - Exento: ${self.importe}")


class FacturaFactory:
    @staticmethod
    def crear(tipo, importe):
        if tipo == "responsable":
            return FacturaResponsable(importe)
        elif tipo == "no_inscripto":
            return FacturaNoInscripto(importe)
        elif tipo == "exento":
            return FacturaExento(importe)
        else:
            raise ValueError("Tipo inválido")


# Uso
f = FacturaFactory.crear("responsable", 5000)
f.mostrar()
