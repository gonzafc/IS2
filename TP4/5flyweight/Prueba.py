from FabricaPiezas import FabricaPiezas

pieza1 = FabricaPiezas.obtener_pieza("Peón")
pieza2 = FabricaPiezas.obtener_pieza("Peón")
pieza3 = FabricaPiezas.obtener_pieza("Torre")

pieza1.mostrar("A2")
pieza2.mostrar("B2")
pieza3.mostrar("A1")

print(pieza1 is pieza2)  