from concretaimplementacion import Tren5mts, Tren10mts
from abstraccion import Lamina


tren1 = Tren5mts()
tren2 = Tren10mts()

lamina1 = Lamina(tren1)
lamina2 = Lamina(tren2)

lamina1.fabricar()
lamina2.fabricar()