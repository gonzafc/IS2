class Avion:
    def __init__(self):
        self.partes = []

    def agregar(self, parte):
        self.partes.append(parte)

    def mostrar(self):
        print("Avión construido con:")
        for p in self.partes:
            print("-", p)


class AvionBuilder:
    def __init__(self):
        self.avion = Avion()

    def construir_body(self):
        self.avion.agregar("Body")

    def construir_turbinas(self):
        self.avion.agregar("2 Turbinas")

    def construir_alas(self):
        self.avion.agregar("2 Alas")

    def construir_tren(self):
        self.avion.agregar("Tren de aterrizaje")

    def obtener_avion(self):
        return self.avion


class Director:
    def construir_avion(self, builder):
        builder.construir_body()
        builder.construir_turbinas()
        builder.construir_alas()
        builder.construir_tren()


# Uso
builder = AvionBuilder()
director = Director()
director.construir_avion(builder)

avion = builder.obtener_avion()
avion.mostrar()
