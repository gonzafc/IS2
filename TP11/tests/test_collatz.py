"""Pruebas unitarias para el modulo collatz.py."""

import pytest

from tp11_is2.collatz import collatz, main


def test_collatz_uno_devuelve_cero_iteraciones():
    """El valor inicial 1 ya es el destino, por lo tanto no hay iteraciones."""
    assert collatz(1) == 0


def test_collatz_veinte_recorre_ambas_ramas():
    """El valor 20 ejercita los caminos par e impar y finaliza en 7 pasos."""
    assert collatz(20) == 7


def test_collatz_limite_superior_1999():
    """El maximo valor admitido (1999) produce 50 iteraciones."""
    assert collatz(1999) == 50


def test_collatz_rechaza_no_positivos():
    """Los valores 0 y negativos no son validos y deben rechazarse."""
    with pytest.raises(ValueError):
        collatz(0)
    with pytest.raises(ValueError):
        collatz(-5)


def test_collatz_rechaza_valores_fuera_de_rango():
    """El valor 2000 supera la cota superior y debe rechazarse."""
    with pytest.raises(ValueError):
        collatz(2000)


def test_collatz_dos_devuelve_una_iteracion():
    """El menor valor par valido (2) requiere exactamente una iteracion."""
    assert collatz(2) == 1


def test_collatz_rechaza_tipos_no_enteros():
    """Valores que no son enteros puros (str, float, bool) deben rechazarse."""
    with pytest.raises(ValueError):
        collatz("texto")  # type: ignore
    with pytest.raises(ValueError):
        collatz(12.5)  # type: ignore
    with pytest.raises(ValueError):
        collatz(True)  # type: ignore


def test_main_con_entrada_valida_por_consola(monkeypatch, capsys):
    """main procesa un numero valido ingresado por teclado y reporta el resultado."""
    monkeypatch.setattr("builtins.input", lambda _: "20")
    main()
    salida = capsys.readouterr()
    assert "El numero de partida es 20 y el numero de iteraciones es 7." in salida.out


def test_main_con_entrada_no_numerica(monkeypatch, capsys):
    """main informa el error de validacion cuando el usuario ingresa texto."""
    monkeypatch.setattr("builtins.input", lambda _: "abc")
    main()
    salida = capsys.readouterr()
    assert "Error de validacion" in salida.out


def test_collatz_ejecutado_como_script(monkeypatch, capsys):
    """El modulo se comporta como programa principal al ejecutarse con runpy."""
    import runpy
    import sys

    monkeypatch.setattr("builtins.input", lambda _: "20")
    sys.modules.pop("tp11_is2.collatz", None)
    runpy.run_module("tp11_is2.collatz", run_name="__main__")
    salida = capsys.readouterr()
    assert "El numero de partida es 20 y el numero de iteraciones es 7." in salida.out
