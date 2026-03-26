import matplotlib.pyplot as plt

def iteraciones_collatz(n):
    """
    Calcula cuántas iteraciones tarda el número n en llegar a 1
    siguiendo la conjetura de Collatz.
    """
    if n <= 0:
        return 0
    
    contador = 0
    while n > 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        contador += 1
    return contador

# --- Configuración ---
NUMERO_INICIAL = 1
NUMERO_FINAL = 10000

print(f"Calculando secuencias de Collatz para n=[{NUMERO_INICIAL}...{NUMERO_FINAL}]...")

# --- Procesamiento ---
numeros_inicio = []
convergencias = []

# Bucle estándar de Python sin tqdm
for n in range(NUMERO_INICIAL, NUMERO_FINAL + 1):
    intentos = iteraciones_collatz(n)
    
    # Eje Y: Número inicial n
    numeros_inicio.append(n)
    # Eje X: Iteraciones hasta llegar a 1
    convergencias.append(intentos)

print("Cálculo finalizado. Generando gráfico...")

# --- Configuración del Gráfico (Matplotlib) ---
plt.figure(figsize=(10, 6))

# Gráfico de Dispersión
# Recordá: plt.scatter(x, y) -> x = iteraciones, y = número inicial
plt.scatter(convergencias, numeros_inicio, s=1, alpha=0.5, c=convergencias, cmap='viridis')

plt.title(f'Conjetura de Collatz: Rango n = {NUMERO_INICIAL} a {NUMERO_FINAL}')
plt.xlabel('Número de Iteraciones hasta Convergencia (Eje Abscisas)')
plt.ylabel('Número Inicial n (Eje Ordenadas)')

plt.grid(True, linestyle='--', alpha=0.7)

# Mostrar el gráfico directamente
plt.show()