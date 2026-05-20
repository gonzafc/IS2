class ForwardIterator:
    def __init__(self, text):
        self.text = text
        self.index = 0

    def has_next(self):
        return self.index < len(self.text)

    def next(self):
        char = self.text[self.index]
        self.index += 1
        return char


class ReverseIterator:
    def __init__(self, text):
        self.text = text
        self.index = len(text) - 1

    def has_next(self):
        return self.index >= 0

    def next(self):
        char = self.text[self.index]
        self.index -= 1
        return char


class StringCollection:
    def __init__(self, text):
        self.text = text

    def get_forward_iterator(self):
        return ForwardIterator(self.text)

    def get_reverse_iterator(self):
        return ReverseIterator(self.text)


# Ejemplo de uso
if __name__ == "__main__":
    collection = StringCollection("Ingenieria")

    print("Recorrido directo:")
    it = collection.get_forward_iterator()
    while it.has_next():
        print(it.next(), end=" ")
    
    print("\n\nRecorrido inverso:")
    it = collection.get_reverse_iterator()
    while it.has_next():
        print(it.next(), end=" ")