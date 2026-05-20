from PiezaAjedrez import PiezaAjedrez

class FabricaPiezas:
    piezas = {}

    @classmethod
    def obtener_pieza(cls, tipo):
        if tipo not in cls.piezas:
            cls.piezas[tipo] = PiezaAjedrez(tipo)
        return cls.piezas[tipo]