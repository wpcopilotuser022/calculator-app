import math
import unittest

from calculator import Calculator, CalculatorError


class TestCalculatorOperations(unittest.TestCase):
    def setUp(self) -> None:
        self.calc = Calculator()

    def test_basic_arithmetic(self) -> None:
        self.assertEqual(self.calc.add(5, 3), 8)
        self.assertEqual(self.calc.subtract(10, 4), 6)
        self.assertEqual(self.calc.multiply(7, 6), 42)
        self.assertEqual(self.calc.divide(20, 5), 4)

    def test_advanced_arithmetic(self) -> None:
        self.assertEqual(self.calc.power(2, 5), 32)
        self.assertEqual(self.calc.modulus(10, 3), 1)
        self.assertEqual(self.calc.floor_divide(17, 3), 5)
        self.assertEqual(self.calc.percentage(200, 15), 30)

    def test_divide_by_zero_raises(self) -> None:
        with self.assertRaises(ZeroDivisionError):
            self.calc.divide(10, 0)

    def test_modulus_by_zero_raises(self) -> None:
        with self.assertRaises(ZeroDivisionError):
            self.calc.modulus(10, 0)

    def test_floor_divide_by_zero_raises(self) -> None:
        with self.assertRaises(ZeroDivisionError):
            self.calc.floor_divide(10, 0)

    def test_square_root(self) -> None:
        self.assertEqual(self.calc.square_root(81), 9)

    def test_square_root_of_negative_raises(self) -> None:
        with self.assertRaises(ValueError):
            self.calc.square_root(-1)

    def test_factorial(self) -> None:
        self.assertEqual(self.calc.factorial(0), 1)
        self.assertEqual(self.calc.factorial(5), 120)

    def test_factorial_negative_raises(self) -> None:
        with self.assertRaises(ValueError):
            self.calc.factorial(-5)

    def test_factorial_non_integer_raises(self) -> None:
        with self.assertRaises(TypeError):
            self.calc.factorial(4.2)  # type: ignore[arg-type]

    def test_factorial_bool_raises(self) -> None:
        with self.assertRaises(TypeError):
            self.calc.factorial(True)  # type: ignore[arg-type]

    def test_trigonometry(self) -> None:
        self.assertAlmostEqual(self.calc.sin(math.pi / 2), 1.0, places=7)
        self.assertAlmostEqual(self.calc.cos(0), 1.0, places=7)
        self.assertAlmostEqual(self.calc.tan(math.pi / 4), 1.0, places=7)

    def test_logarithm(self) -> None:
        self.assertAlmostEqual(self.calc.log(math.e), 1.0, places=7)
        self.assertAlmostEqual(self.calc.log(100, 10), 2.0, places=7)

    def test_log_invalid_value_raises(self) -> None:
        with self.assertRaises(ValueError):
            self.calc.log(0)

    def test_log_invalid_base_raises(self) -> None:
        with self.assertRaises(ValueError):
            self.calc.log(10, 1)


class TestExpressionEvaluation(unittest.TestCase):
    def setUp(self) -> None:
        self.calc = Calculator()

    def test_expression_arithmetic(self) -> None:
        self.assertEqual(self.calc.evaluate_expression("2 + 3 * 4"), 14.0)
        self.assertEqual(self.calc.evaluate_expression("(2 + 3) * 4"), 20.0)

    def test_expression_with_functions_and_constants(self) -> None:
        self.assertAlmostEqual(self.calc.evaluate_expression("sqrt(81) + log(e)"), 10.0, places=7)
        self.assertAlmostEqual(self.calc.evaluate_expression("sin(pi / 2) + cos(0)"), 2.0, places=7)

    def test_expression_unary(self) -> None:
        self.assertEqual(self.calc.evaluate_expression("-5 + +2"), -3.0)

    def test_expression_divide_by_zero_raises(self) -> None:
        with self.assertRaises(ZeroDivisionError):
            self.calc.evaluate_expression("10 / 0")

    def test_expression_invalid_syntax_raises(self) -> None:
        with self.assertRaises(CalculatorError):
            self.calc.evaluate_expression("2 + * 3")

    def test_expression_unsafe_attribute_access_is_rejected(self) -> None:
        with self.assertRaises(CalculatorError):
            self.calc.evaluate_expression("(1).__class__")

    def test_expression_unknown_identifier_rejected(self) -> None:
        with self.assertRaises(CalculatorError):
            self.calc.evaluate_expression("unknown + 1")

    def test_expression_unknown_function_rejected(self) -> None:
        with self.assertRaises(CalculatorError):
            self.calc.evaluate_expression("eval('2+2')")


if __name__ == "__main__":
    unittest.main()
