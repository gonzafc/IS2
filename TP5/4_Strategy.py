from abc import ABC, abstractmethod

# Strategy
class RadioMode(ABC):
    @abstractmethod
    def tune(self, frequency):
        pass


class AMMode(RadioMode):
    def tune(self, frequency):
        print(f"Sintonizando AM {frequency} kHz")


class FMMode(RadioMode):
    def tune(self, frequency):
        print(f"Sintonizando FM {frequency} MHz")


# Memoria de radio
class Memory:
    def __init__(self, name, mode, frequency):
        self.name = name
        self.mode = mode
        self.frequency = frequency

    def play(self):
        print(f"{self.name} → ", end="")
        self.mode.tune(self.frequency)


# Scanner
class RadioScanner:
    def __init__(self):
        self.memories = []

    def add_memory(self, memory):
        self.memories.append(memory)

    def scan(self):
        print("\nBarrido de memorias:")
        for mem in self.memories:
            mem.play()


# Programa principal
if __name__ == "__main__":
    scanner = RadioScanner()

    # Definición de memorias
    scanner.add_memory(Memory("M1", AMMode(), 820))
    scanner.add_memory(Memory("M2", FMMode(), 99.5))
    scanner.add_memory(Memory("M3", AMMode(), 1010))
    scanner.add_memory(Memory("M4", FMMode(), 103.3))

    # Simular ciclos de barrido
    for i in range(2):
        print(f"\nCiclo de barrido {i + 1}")
        scanner.scan()