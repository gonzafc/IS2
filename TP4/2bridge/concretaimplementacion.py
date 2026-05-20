from implementador import TrenLaminador


class Tren5mts(TrenLaminador):
    def producir(self):
        return "Plancha de 5 metros"


class Tren10mts(TrenLaminador):
    def producir(self):
        return "Plancha de 10 metros"