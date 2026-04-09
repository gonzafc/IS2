"""
Módulo rpn.py - Evaluador de Expresiones RPN
"""

import sys
import math


class RPNError(Exception):
    """Excepción personalizada para errores en la evaluación RPN."""


# --- 1. FUNCIONES DE APOYO Y DICCIONARIOS DE DESPACHO ---
def safe_div(num_a, num_b):
    """Realiza una división segura, previniendo la división por cero."""
    if num_b == 0:
        raise RPNError("División por cero")
    return num_a / num_b


def safe_inv(num_a):
    """Calcula la inversa de un número, previniendo división por cero."""
    if num_a == 0:
        raise RPNError("División por cero en 1/x")
    return 1.0 / num_a


# Diccionario de Operaciones: Mapea el token a (Cantidad argumentos, Función)
OPERADORES = {
    "+": (2, lambda a, b: a + b),
    "-": (2, lambda a, b: a - b),
    "*": (2, lambda a, b: a * b),
    "/": (2, safe_div),
    "YX": (2, lambda a, b: a**b),
    "1/X": (1, safe_inv),
    "SQRT": (1, math.sqrt),
    "LOG": (1, math.log10),
    "LN": (1, math.log),
    "EX": (1, math.exp),
    "10X": (1, lambda a: 10**a),
    "CHS": (1, lambda a: -a),
    "SIN": (1, lambda a: math.sin(math.radians(a))),
    "COS": (1, lambda a: math.cos(math.radians(a))),
    "TG": (1, lambda a: math.tan(math.radians(a))),
    "ASIN": (1, lambda a: math.degrees(math.asin(a))),
    "ACOS": (1, lambda a: math.degrees(math.acos(a))),
    "ATG": (1, lambda a: math.degrees(math.atan(a))),
}

CONSTANTES = {"P": math.pi, "E": math.e, "J": (1 + math.sqrt(5)) / 2}  # Número Áureo


# --- 2. MOTOR DE EVALUACIÓN PRINCIPAL ---
# pylint: disable=too-many-branches, too-many-statements, too-many-locals
def evaluate_rpn(expression):
    """Evalúa una expresión matemática en Notación Polaca Inversa."""
    stack = []
    mem = [0.0] * 10

    token_iterator = iter(expression.strip().split())

    def pop_n(num=1):
        """Extrae elementos de la pila de forma segura."""
        if len(stack) < num:
            raise RPNError("Pila insuficiente para operar")
        if num == 1:
            return stack.pop()
        res = stack[-num:]
        del stack[-num:]
        return res

    for t in token_iterator:
        t_upper = t.upper()

        try:
            if t_upper in OPERADORES:
                n_args, func = OPERADORES[t_upper]
                args = pop_n(n_args)
                resultado = func(args) if n_args == 1 else func(*args)
                stack.append(resultado)

            elif t_upper in CONSTANTES:
                stack.append(CONSTANTES[t_upper])

            elif t_upper in ("STO", "RCL"):
                idx_str = next(token_iterator, None)
                if idx_str is None:
                    raise RPNError(f"Falta índice para {t_upper}")
                if not (idx_str.isdigit() and 0 <= int(idx_str) <= 9):
                    raise RPNError("El índice de memoria debe ser de 00 a 09")

                idx = int(idx_str)
                if t_upper == "STO":
                    mem[idx] = pop_n()
                else:
                    stack.append(mem[idx])

            elif t_upper == "DUP":
                val = pop_n()
                stack.extend([val, val])

            elif t_upper == "SWAP":
                val_a, val_b = pop_n(2)
                stack.extend([val_b, val_a])

            elif t_upper == "DROP":
                pop_n()

            elif t_upper == "CLEAR":
                stack.clear()

            else:
                stack.append(float(t))

        except ValueError as exc:
            if "math domain" in str(exc):
                raise RPNError(f"Error de dominio matemático en '{t}'") from exc
            raise RPNError(f"Token inválido: '{t}'") from exc

        except OverflowError as exc:
            raise RPNError(f"Desbordamiento matemático en '{t}'") from exc

    if len(stack) != 1:
        raise RPNError(
            f"Al final debe quedar exactamente 1 valor en la pila. Quedaron: {len(stack)}"
        )

    return stack[0]


# --- 3. ENTRADA Y SALIDA ---
def main():
    """Punto de entrada principal para línea de comandos y stdin."""
    args = sys.argv[1:]
    expr = " ".join(args) if args else sys.stdin.read().strip()

    if not expr:
        print("Uso: python rpn.py 'expresión'", file=sys.stderr)
        sys.exit(1)

    try:
        res = evaluate_rpn(expr)
        if isinstance(res, float) and res.is_integer():
            print(int(res))
        else:
            print(res)
    except RPNError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
