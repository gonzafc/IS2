from abc import ABC, abstractmethod

# Observer base
class Observer(ABC):
    @abstractmethod
    def update(self, emitted_id):
        pass


# Observer concreto
class ConcreteObserver(Observer):
    def __init__(self, observer_id):
        self.observer_id = observer_id

    def update(self, emitted_id):
        if self.observer_id == emitted_id:
            print(f"Observer {self.observer_id}: ID coincidente detectado")


# Publisher
class Publisher:
    def __init__(self):
        self.subscribers = []

    def subscribe(self, observer):
        self.subscribers.append(observer)

    def notify(self, emitted_id):
        print(f"\nID emitido: {emitted_id}")
        for observer in self.subscribers:
            observer.update(emitted_id)


# Programa principal
if __name__ == "__main__":
    publisher = Publisher()

    # Crear 4 observers con IDs específicos
    o1 = ConcreteObserver("A123")
    o2 = ConcreteObserver("B456")
    o3 = ConcreteObserver("C789")
    o4 = ConcreteObserver("D321")

    publisher.subscribe(o1)
    publisher.subscribe(o2)
    publisher.subscribe(o3)
    publisher.subscribe(o4)

    # Emitir 8 IDs (al menos 4 coinciden)
    ids_to_emit = [
        "A123", "XXXX",
        "B456", "YYYY",
        "C789", "ZZZZ",
        "D321", "AAAA"
    ]

    for eid in ids_to_emit:
        publisher.notify(eid)