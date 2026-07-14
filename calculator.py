"""Advanced calculator functionality.

This module provides an ``Calculator`` class with arithmetic, scientific,
and expression-evaluation helpers.
"""

from __future__ import annotations

import ast
import math
from typing import Any, Callable, Dict


class CalculatorError(Exception):
    """Raised when calculator input is invalid or unsafe."""


class Calculator:
    """A calculator with advanced arithmetic and scientific operations."""

    def add(self, a: float, b: float) -> float:
        return a + b

    def subtract(self, a: float, b: float) -> float:
        return a - b

    def multiply(self, a: float, b: float) -> float:
        return a * b

    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return a / b

    def power(self, base: float, exponent: float) -> float:
        return base**exponent

    def modulus(self, a: int, b: int) -> int:
        if b == 0:
            raise ZeroDivisionError("Cannot perform modulus by zero")
        return a % b

    def floor_divide(self, a: int, b: int) -> int:
        if b == 0:
            raise ZeroDivisionError("Cannot perform floor division by zero")
        return a // b

    def square_root(self, value: float) -> float:
        if value < 0:
            raise ValueError("Cannot calculate square root of a negative number")
        return math.sqrt(value)

    def factorial(self, n: int) -> int:
        if not isinstance(n, int):
            raise TypeError("Factorial is defined only for integers")
        if n < 0:
            raise ValueError("Factorial is not defined for negative integers")
        return math.factorial(n)

    def percentage(self, value: float, percent: float) -> float:
        return (value * percent) / 100.0

    def sin(self, angle_radians: float) -> float:
        return math.sin(angle_radians)

    def cos(self, angle_radians: float) -> float:
        return math.cos(angle_radians)

    def tan(self, angle_radians: float) -> float:
        return math.tan(angle_radians)

    def log(self, value: float, base: float = math.e) -> float:
        if value <= 0:
            raise ValueError("Logarithm input must be positive")
        if base <= 0 or base == 1:
            raise ValueError("Logarithm base must be positive and not equal to 1")
        return math.log(value, base)

    def evaluate_expression(self, expression: str) -> float:
        """Safely evaluate a numeric expression with limited operations."""
        try:
            tree = ast.parse(expression, mode="eval")
        except SyntaxError as exc:
            raise CalculatorError("Invalid expression syntax") from exc

        return float(self._eval_node(tree.body))

    def _eval_node(self, node: ast.AST) -> float:
        bin_ops: Dict[type, Callable[[Any, Any], Any]] = {
            ast.Add: lambda a, b: a + b,
            ast.Sub: lambda a, b: a - b,
            ast.Mult: lambda a, b: a * b,
            ast.Div: self.divide,
            ast.Pow: lambda a, b: a**b,
            ast.Mod: self.modulus,
            ast.FloorDiv: self.floor_divide,
        }

        unary_ops: Dict[type, Callable[[Any], Any]] = {
            ast.UAdd: lambda x: +x,
            ast.USub: lambda x: -x,
        }

        allowed_funcs: Dict[str, Callable[..., Any]] = {
            "sqrt": self.square_root,
            "sin": self.sin,
            "cos": self.cos,
            "tan": self.tan,
            "log": self.log,
            "factorial": self.factorial,
            "abs": abs,
            "round": round,
        }

        allowed_names: Dict[str, float] = {
            "pi": math.pi,
            "e": math.e,
        }

        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return float(node.value)
            raise CalculatorError("Only numeric constants are allowed")

        if isinstance(node, ast.BinOp):
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)
            op_type = type(node.op)
            if op_type not in bin_ops:
                raise CalculatorError(f"Unsupported operator: {op_type.__name__}")
            return float(bin_ops[op_type](left, right))

        if isinstance(node, ast.UnaryOp):
            operand = self._eval_node(node.operand)
            op_type = type(node.op)
            if op_type not in unary_ops:
                raise CalculatorError(f"Unsupported unary operator: {op_type.__name__}")
            return float(unary_ops[op_type](operand))

        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise CalculatorError("Only direct function calls are allowed")
            func_name = node.func.id
            if func_name not in allowed_funcs:
                raise CalculatorError(f"Function not allowed: {func_name}")
            args = [self._eval_node(arg) for arg in node.args]
            return float(allowed_funcs[func_name](*args))

        if isinstance(node, ast.Name):
            if node.id in allowed_names:
                return float(allowed_names[node.id])
            raise CalculatorError(f"Unknown identifier: {node.id}")

        raise CalculatorError(f"Unsupported expression node: {type(node).__name__}")
