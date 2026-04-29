from abc import ABC, abstractmethod

# Productos abstractos
class Celular(ABC):
    @abstractmethod
    def info(self):
        pass

class Notebook(ABC):
    @abstractmethod
    def info(self):
        pass

# Productos concretos Apple
class iPhone(Celular):
    def info(self):
        return "iPhone creado"

class Macbook(Notebook):
    def info(self):
        return "Macbook creada"

# Productos concretos Samsung
class Galaxy(Celular):
    def info(self):
        return "Samsung Galaxy creado"

class SamsungBook(Notebook):
    def info(self):
        return "Samsung Book creada"

# Abstract Factory
class FabricaElectronica(ABC):
    @abstractmethod
    def crear_celular(self):
        pass

    @abstractmethod
    def crear_notebook(self):
        pass

# Fábricas concretas
class AppleFactory(FabricaElectronica):
    def crear_celular(self):
        return iPhone()

    def crear_notebook(self):
        return Macbook()

class SamsungFactory(FabricaElectronica):
    def crear_celular(self):
        return Galaxy()

    def crear_notebook(self):
        return SamsungBook()


# Uso
factory = AppleFactory()

cel = factory.crear_celular()
note = factory.crear_notebook()

print(cel.info())
print(note.info())
