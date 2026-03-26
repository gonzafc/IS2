import sys
# Importamos la función original desde factorial.py
from factorial import factorial as calcular_fact, parsear_rango

class Factorial:
    def __init__(self):
        """
        Constructor de la clase. 
        Podría inicializar configuraciones si fuera necesario.
        """
        print("Instanciando la clase Factorial...")

    def run(self, min_val, max_val):
        """
        Utiliza la función importada para calcular el rango.
        """
        # Normalizamos el rango
        inicio = min(min_val, max_val)
        fin = max(min_val, max_val)

        print(f"\n--- [OOP] Ejecutando rango {inicio} a {fin} ---")
        
        for n in range(inicio, fin + 1):
            # Llamamos a la función que reside en factorial.py
            resultado = calcular_fact(n)
            
            if resultado == 0 and n < 0:
                print(f"Factorial {n}! = No existe (negativo)")
            else:
                print(f"Factorial {n}! = {resultado}")

# --- Lógica de Interacción ---
if __name__ == "__main__":
    # Creamos el objeto
    procesador = Factorial()
    
    # Reutilizamos también la lógica de parseo del archivo original
    entrada_valida = False
    rango_numeros = []

    # Verificamos argumentos de sistema
    fuente_entrada = sys.argv[1] if len(sys.argv) >= 2 else None

    while not entrada_valida:
        try:
            if fuente_entrada:
                raw_input = fuente_entrada
                fuente_entrada = None # Para que si falla, pida input()
            else:
                raw_input = input("\n Ingrese rango (ej: 1-5): ").strip()
            
            rango_numeros = parsear_rango(raw_input)
            entrada_valida = True
        except ValueError:
            print(" Formato incorrecto.")

    # Ejecución del método solicitado
    if rango_numeros:
        procesador.run(min(rango_numeros), max(rango_numeros))