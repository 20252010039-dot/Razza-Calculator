import unittest
from decimal import Decimal

from app.core.engine import CalculationError, evaluate


class EngineTests(unittest.TestCase):
    def test_decimal_arithmetic_is_exact(self):
        self.assertEqual(evaluate("0,1 + 0,2"), Decimal("0.3"))

    def test_operator_precedence_and_parentheses(self):
        self.assertEqual(evaluate("12+3*4"), Decimal(24))
        self.assertEqual(evaluate("(12+3)*4"), Decimal(60))

    def test_smart_percentage(self):
        self.assertEqual(evaluate("200 + 10%"), Decimal(220))
        self.assertEqual(evaluate("50 - 20%"), Decimal(40))
        self.assertEqual(evaluate("15%*300"), Decimal("45"))
        self.assertEqual(evaluate("15% dari 300"), Decimal("45"))

    def test_scientific_functions_and_angle_modes(self):
        self.assertEqual(evaluate("sin(30)"), Decimal("0.49999999999999994"))
        self.assertEqual(evaluate("sin(pi/6)", angle_unit="rad").quantize(Decimal("0.0001")), Decimal("0.5000"))
        self.assertEqual(evaluate("sqrt(81)"), Decimal(9))
        self.assertEqual(evaluate("factorial(5)"), Decimal(120))

    def test_ans_and_constants(self):
        self.assertEqual(evaluate("Ans*2", answer=Decimal(4)), Decimal(8))
        self.assertGreater(evaluate("pi"), Decimal("3.14"))

    def test_zero_division_has_friendly_error(self):
        with self.assertRaisesRegex(CalculationError, "Tidak bisa dibagi nol"):
            evaluate("5/0")

    def test_rejects_code_execution_and_attributes(self):
        for expression in ("__import__('os')", "().__class__", "open('file')"):
            with self.subTest(expression=expression):
                with self.assertRaises(CalculationError):
                    evaluate(expression)

    def test_rejects_incomplete_expression(self):
        with self.assertRaises(CalculationError):
            evaluate("12+")


if __name__ == "__main__":
    unittest.main()
