"""Pruebas unitarias para el modulo json2csv.py."""

import json

import pytest

from tp11_is2.json2csv import json_to_csv, main


def test_convierte_arreglo_de_objetos():
    """Transforma un arreglo de diccionarios en filas CSV con su cabecera."""
    datos_json = json.dumps([{"id": 1, "nombre": "Lucas"}, {"id": 2, "nombre": "Ana"}])
    resultado = json_to_csv(datos_json)
    filas = resultado.strip().split("\n")
    assert filas[0] == "id,nombre"
    assert filas[1] == "1,Lucas"
    assert filas[2] == "2,Ana"


def test_convierte_objeto_individual():
    """Transforma un diccionario suelto en una unica fila CSV."""
    datos_json = json.dumps({"producto": "Mouse", "precio": 25})
    resultado = json_to_csv(datos_json)
    filas = resultado.strip().split("\n")
    assert filas[0] == "producto,precio"
    assert filas[1] == "Mouse,25"


def test_usa_delimitador_configurado():
    """Respeta el delimitador alternativo (por ejemplo, punto y coma)."""
    datos_json = json.dumps([{"a": 10, "b": 20}])
    resultado = json_to_csv(datos_json, delimiter=";")
    assert "a;b" in resultado
    assert "10;20" in resultado


def test_ignora_marca_bom_utf8():
    """Acepta cadenas precedidas por la marca BOM (tipica de Windows/PowerShell)."""
    datos_json = "\ufeff" + json.dumps([{"item": "PC"}])
    resultado = json_to_csv(datos_json)
    assert "item" in resultado


def test_falla_con_json_malformado():
    """Eleva ValueError cuando la sintaxis JSON es incorrecta."""
    with pytest.raises(ValueError, match="Formato JSON invalido"):
        json_to_csv("{invalido}")


def test_falla_con_entrada_en_blanco():
    """Eleva ValueError cuando la entrada no contiene caracteres utiles."""
    with pytest.raises(ValueError, match="vacia"):
        json_to_csv("   ")


def test_falla_con_estructura_no_valida():
    """Eleva ValueError si el JSON no es un objeto ni una lista de objetos."""
    with pytest.raises(ValueError, match="debe contener un objeto"):
        json_to_csv("[1, 2, 3]")


def test_cli_lee_stdin_y_escribe_stdout(monkeypatch, capsys):
    """La CLI toma el JSON de stdin y vuelca el CSV en stdout."""
    monkeypatch.setattr("sys.argv", ["json2csv.py"])
    monkeypatch.setattr("sys.stdin.read", lambda: '[{"x": 1, "y": 2}]')
    main()
    salida = capsys.readouterr()
    assert "x,y" in salida.out
    assert "1,2" in salida.out


def test_cli_usa_archivos_entrada_salida(tmp_path, monkeypatch):
    """La CLI respeta los argumentos -i y -o para leer y escribir archivos."""
    origen = tmp_path / "in.json"
    destino = tmp_path / "out.csv"
    origen.write_text('[{"col1": "val1"}]', encoding="utf-8")

    monkeypatch.setattr(
        "sys.argv", ["json2csv.py", "-i", str(origen), "-o", str(destino)]
    )
    main()

    contenido = destino.read_text(encoding="utf-8")
    assert "col1" in contenido
    assert "val1" in contenido


def test_cli_reporta_archivo_ausente(monkeypatch):
    """La CLI finaliza con codigo 1 cuando el archivo de entrada no existe."""
    monkeypatch.setattr(
        "sys.argv", ["json2csv.py", "-i", "archivo_que_no_existe_123.json"]
    )
    with pytest.raises(SystemExit) as excinfo:
        main()
    assert excinfo.value.code == 1


def test_arreglo_vacio_produce_cadena_vacia():
    """Una lista JSON sin registros se traduce en una cadena vacia."""
    assert json_to_csv("[]") == ""


def test_cli_captura_error_de_validacion(monkeypatch, capsys):
    """La CLI escribe en stderr y sale con codigo 1 ante un JSON invalido."""
    monkeypatch.setattr("sys.argv", ["json2csv.py"])
    monkeypatch.setattr("sys.stdin.read", lambda: "{json_invalido: 123}")
    with pytest.raises(SystemExit) as excinfo:
        main()
    assert excinfo.value.code == 1
    salida_error = capsys.readouterr()
    assert "Error:" in salida_error.err


def test_json2csv_ejecutado_como_script(monkeypatch, capsys):
    """El modulo se comporta como programa principal al ejecutarse con runpy."""
    import runpy
    import sys

    monkeypatch.setattr("sys.argv", ["json2csv.py"])
    monkeypatch.setattr("sys.stdin.read", lambda: '[{"a": 1}]')
    sys.modules.pop("tp11_is2.json2csv", None)
    runpy.run_module("tp11_is2.json2csv", run_name="__main__")
    salida = capsys.readouterr()
    assert "a\n1\n" in salida.out
