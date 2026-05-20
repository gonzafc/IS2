# Memento
class Memento:
    def __init__(self, state):
        self.state = state


# Originator
class Memory:
    def __init__(self):
        self.state = None

    def set_state(self, state):
        self.state = state
        print(f"Estado actual: {self.state}")

    def save(self):
        return Memento(self.state)

    def restore(self, memento):
        self.state = memento.state
        print(f"Estado restaurado: {self.state}")


# Caretaker
class History:
    def __init__(self, max_size=4):
        self.mementos = []
        self.max_size = max_size

    def add(self, memento):
        if len(self.mementos) == self.max_size:
            self.mementos.pop(0)  # elimina el más antiguo
        self.mementos.append(memento)

    def get(self, index):
        if index < len(self.mementos):
            return self.mementos[-1 - index]
        else:
            return None


# Programa principal
if __name__ == "__main__":
    memory = Memory()
    history = History()

    # Cambios de estado
    for state in ["A", "B", "C", "D", "E"]:
        memory.set_state(state)
        history.add(memory.save())

    print("\nUndo inmediato:")
    memory.restore(history.get(0))

    print("\nUndo anterior:")
    memory.restore(history.get(1))

    print("\nUndo más antiguo:")
    memory.restore(history.get(3))