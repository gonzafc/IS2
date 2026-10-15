"""Modulo para convertir archivos o flujos JSON a formato CSV como filtro Unix."""

import argparse
import csv
import io
import json
import sys


def json_to_csv(json_str: str, delimiter: str = ",") -> str:
    """Convierte una cadena JSON con objetos a formato CSV."""
    cleaned_str = json_str.strip().lstrip("\ufeff")
    if not cleaned_str:
        raise ValueError("La entrada JSON esta vacia.")

    try:
        data = json.loads(cleaned_str)
    except json.JSONDecodeError as err:
        raise ValueError(f"Formato JSON invalido: {err}") from err

    if isinstance(data, dict):
        data = [data]

    if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
        raise ValueError("El JSON debe contener un objeto o una lista de objetos.")

    if not data:
        return ""

    # Recolectar todas las cabeceras conservando el orden de aparicion
    headers: list[str] = []
    for item in data:
        for key in item:
            if key not in headers:
                headers.append(key)

    output = io.StringIO()
    writer = csv.DictWriter(
        output, fieldnames=headers, delimiter=delimiter, lineterminator="\n"
    )
    writer.writeheader()
    writer.writerows(data)
    return output.getvalue()


def main() -> None:
    """Punto de entrada principal para ejecucion por linea de comandos."""
    parser = argparse.ArgumentParser(description="Filtro para convertir JSON a CSV.")
    parser.add_argument("-i", dest="input_file", help="Archivo JSON de entrada.")
    parser.add_argument("-o", dest="output_file", help="Archivo CSV de salida.")
    parser.add_argument(
        "-d", dest="delimiter", default=",", help="Delimitador (por defecto ',')."
    )

    args = parser.parse_args()

    try:
        # Lectura: archivo o entrada estandar (stdin)
        if args.input_file:
            with open(args.input_file, "r", encoding="utf-8-sig") as f:
                json_content = f.read()
        else:
            json_content = sys.stdin.read()

        csv_content = json_to_csv(json_content, delimiter=args.delimiter)

        # Escritura: archivo o salida estandar (stdout)
        if args.output_file:
            with open(args.output_file, "w", encoding="utf-8", newline="") as f:
                f.write(csv_content)
        else:
            sys.stdout.write(csv_content)

    except FileNotFoundError:
        sys.stderr.write(f"Error: No se encontro el archivo '{args.input_file}'.\n")
        sys.exit(1)
    except (ValueError, OSError) as e:
        sys.stderr.write(f"Error: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
