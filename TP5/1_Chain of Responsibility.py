from abc import ABC, abstractmethod

# Clase base del patrón
class Handler(ABC):
    def __init__(self, next_handler=None):
        self.next_handler = next_handler

    @abstractmethod
    def handle(self, number):
        pass


# Handler para números primos
class PrimeHandler(Handler):
    def handle(self, number):
        if self.is_prime(number):
            print(f"{number} consumido por PrimeHandler")
        elif self.next_handler:
            self.next_handler.handle(number)

    def is_prime(self, n):
        if n < 2:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True


# Handler para números pares
class EvenHandler(Handler):
    def handle(self, number):
        if number % 2 == 0:
            print(f"{number} consumido por EvenHandler")
        elif self.next_handler:
            self.next_handler.handle(number)


# Handler final: no consumido
class DefaultHandler(Handler):
    def handle(self, number):
        print(f"{number} no consumido")


# Construcción de la cadena
if __name__ == "__main__":
    chain = PrimeHandler(EvenHandler(DefaultHandler()))

    for i in range(1, 101):
        chain.handle(i)