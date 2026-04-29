from abc import ABC, abstractmethod

# Producto
class Hamburguesa(ABC):
    @abstractmethod
    def entregar(self):
        pass

# Productos concretos
class Mostrador(Hamburguesa):
    def entregar(self):
        print("Entregada en mostrador")

class RetiroCliente(Hamburguesa):
    def entregar(self):
        print("Retirada por el cliente")

class Delivery(Hamburguesa):
    def entregar(self):
        print("Enviada por delivery")

# Factory
class HamburguesaFactory:
    @staticmethod
    def crear(tipo):
        if tipo == "mostrador":
            return Mostrador()
        elif tipo == "retiro":
            return RetiroCliente()
        elif tipo == "delivery":
            return Delivery()
        else:
            raise ValueError("Tipo inválido")


# Uso
pedido = HamburguesaFactory.crear("delivery")
pedido.entregar()
