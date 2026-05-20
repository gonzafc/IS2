class Decorador:
    def __init__(self, numero):
        self.numero = numero

    def operar(self):
        return self.numero.operar()