from Conjunto import Conjunto
from Pieza import Pieza


producto = Conjunto("Producto Principal")

for i in range(1, 4):
    subconjunto = Conjunto(f"Subconjunto {i}")

    for j in range(1, 5):
        subconjunto.agregar(Pieza(f"Pieza {i}.{j}"))

    producto.agregar(subconjunto)

sub_extra = Conjunto("Subconjunto Extra")

for i in range(1, 5):
    sub_extra.agregar(Pieza(f"Pieza Extra {i}"))

producto.agregar(sub_extra)

producto.mostrar()