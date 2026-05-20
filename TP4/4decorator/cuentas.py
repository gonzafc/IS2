from cuentas import Decorador


class Sumar2(Decorador):
    def operar(self):
        return self.numero.operar() + 2


class Multiplicar2(Decorador):
    def operar(self):
        return self.numero.operar() * 2


class Dividir3(Decorador):
    def operar(self):
        return self.numero.operar() / 3