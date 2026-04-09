import unittest
import math
import sys
import io
from unittest.mock import patch
from rpn import evaluate_rpn, RPNError, main

class TestRPNDefinitivo(unittest.TestCase):

    def test_todos_los_operadores(self):
        self.assertEqual(evaluate_rpn("3 4 +"), 7.0)
        self.assertEqual(evaluate_rpn("10 4 -"), 6.0)
        self.assertEqual(evaluate_rpn("5 6.5 *"), 32.5)
        self.assertEqual(evaluate_rpn("10 2 /"), 5.0)
        self.assertEqual(evaluate_rpn("2 3 YX"), 8.0)
        self.assertEqual(evaluate_rpn("4 1/X"), 0.25)
        self.assertEqual(evaluate_rpn("16 SQRT"), 4.0)
        self.assertEqual(evaluate_rpn("100 LOG"), 2.0)
        self.assertAlmostEqual(evaluate_rpn("1 LN"), 0.0)
        self.assertAlmostEqual(evaluate_rpn("0 EX"), 1.0)
        self.assertEqual(evaluate_rpn("2 10X"), 100.0)
        self.assertEqual(evaluate_rpn("5 CHS"), -5.0)

    def test_trigonometria_y_constantes(self):
        self.assertAlmostEqual(evaluate_rpn("30 SIN"), 0.5)
        self.assertAlmostEqual(evaluate_rpn("60 COS"), 0.5)
        self.assertAlmostEqual(evaluate_rpn("45 TG"), 1.0)
        self.assertAlmostEqual(evaluate_rpn("0.5 ASIN"), 30.0)
        self.assertAlmostEqual(evaluate_rpn("0.5 ACOS"), 60.0)
        self.assertAlmostEqual(evaluate_rpn("1 ATG"), 45.0)
        self.assertAlmostEqual(evaluate_rpn("P"), math.pi)
        self.assertAlmostEqual(evaluate_rpn("E"), math.e)
        self.assertAlmostEqual(evaluate_rpn("J"), (1 + math.sqrt(5)) / 2)

    def test_manipulacion_pila_memoria(self):
        self.assertEqual(evaluate_rpn("42 STO 05 RCL 05"), 42.0)
        self.assertEqual(evaluate_rpn("10 DUP +"), 20.0)
        self.assertEqual(evaluate_rpn("2 10 SWAP /"), 5.0)
        self.assertEqual(evaluate_rpn("5 10 DROP"), 5.0) # Test para probar que DROP funciona
        with self.assertRaises(RPNError):
            evaluate_rpn("1 2 3 CLEAR")

    def test_todos_los_errores(self):
        with self.assertRaises(RPNError): evaluate_rpn("5 0 /")
        with self.assertRaises(RPNError): evaluate_rpn("0 1/X")
        with self.assertRaises(RPNError): evaluate_rpn("3 +")
        with self.assertRaises(RPNError): evaluate_rpn("2 3 4 +")
        with self.assertRaises(RPNError): evaluate_rpn("5 HOLA +")
        with self.assertRaises(RPNError): evaluate_rpn("-4 SQRT")
        with self.assertRaises(RPNError): evaluate_rpn("1000 1000 YX")
        with self.assertRaises(RPNError): evaluate_rpn("5 STO")
        with self.assertRaises(RPNError): evaluate_rpn("5 STO 15")

    # --- PROBANDO EL MAIN CON CONTEXT MANAGERS SEGUROS ---
    def test_main_con_argumentos(self):
        with patch('sys.argv', ['rpn.py', '3', '4', '+']), patch('sys.stdout', new_callable=io.StringIO) as mock_out:
            main()
            self.assertEqual(mock_out.getvalue().strip(), "7")

    def test_main_con_stdin(self):
        with patch('sys.argv', ['rpn.py']), patch('sys.stdin', io.StringIO("5 6 *")), patch('sys.stdout', new_callable=io.StringIO) as mock_out:
            main()
            self.assertEqual(mock_out.getvalue().strip(), "30")

    def test_main_vacio(self):
        with patch('sys.argv', ['rpn.py']), patch('sys.stdin', io.StringIO("")), patch('sys.stderr', new_callable=io.StringIO) as mock_err:
            with self.assertRaises(SystemExit): 
                main()
            self.assertIn("Uso: python", mock_err.getvalue())

    def test_main_con_error(self):
        with patch('sys.argv', ['rpn.py', '5', '0', '/']), patch('sys.stderr', new_callable=io.StringIO) as mock_err:
            with self.assertRaises(SystemExit): 
                main()
            self.assertTrue(len(mock_err.getvalue()) > 0)

if __name__ == '__main__':
    unittest.main()