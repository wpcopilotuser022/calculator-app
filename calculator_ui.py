"""Tkinter user interface for the calculator project.

Run this file directly to launch a local desktop calculator UI.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from calculator import Calculator, CalculatorError


class CalculatorUI:
    """Desktop calculator interface backed by Calculator.evaluate_expression."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Calculator")
        self.root.resizable(False, False)

        self.calculator = Calculator()

        self.expression_var = tk.StringVar()
        self.result_var = tk.StringVar(value="Result: 0")
        self.error_var = tk.StringVar(value="")

        self._build_layout()
        self._bind_keys()

    def _build_layout(self) -> None:
        main = ttk.Frame(self.root, padding=12)
        main.grid(row=0, column=0, sticky="nsew")

        entry = ttk.Entry(main, textvariable=self.expression_var, font=("TkDefaultFont", 13), width=38)
        entry.grid(row=0, column=0, columnspan=6, sticky="ew", pady=(0, 8))
        entry.focus_set()

        result_label = ttk.Label(main, textvariable=self.result_var, font=("TkDefaultFont", 12, "bold"))
        result_label.grid(row=1, column=0, columnspan=6, sticky="w")

        error_label = ttk.Label(main, textvariable=self.error_var, foreground="#b00020")
        error_label.grid(row=2, column=0, columnspan=6, sticky="w", pady=(2, 10))

        buttons = [
            ["C", "<-", "(", ")", "pi", "e"],
            ["7", "8", "9", "/", "sqrt", "log"],
            ["4", "5", "6", "*", "sin", "cos"],
            ["1", "2", "3", "-", "tan", "^"],
            ["0", ".", "%", "//", "+", "="],
        ]

        for r, row_buttons in enumerate(buttons, start=3):
            for c, token in enumerate(row_buttons):
                ttk.Button(
                    main,
                    text=token,
                    command=lambda t=token: self._on_button_press(t),
                    width=7,
                ).grid(row=r, column=c, padx=2, pady=2, sticky="nsew")

        for col in range(6):
            main.columnconfigure(col, weight=1)

    def _bind_keys(self) -> None:
        self.root.bind("<Return>", lambda _event: self._evaluate())
        self.root.bind("<KP_Enter>", lambda _event: self._evaluate())
        self.root.bind("<BackSpace>", lambda _event: self._backspace())
        self.root.bind("<Escape>", lambda _event: self._clear())

    def _on_button_press(self, token: str) -> None:
        if token == "=":
            self._evaluate()
            return

        if token == "C":
            self._clear()
            return

        if token == "<-":
            self._backspace()
            return

        insert_map = {
            "sqrt": "sqrt(",
            "sin": "sin(",
            "cos": "cos(",
            "tan": "tan(",
            "log": "log(",
            "^": "**",
        }

        self.error_var.set("")
        self.expression_var.set(self.expression_var.get() + insert_map.get(token, token))

    def _clear(self) -> None:
        self.expression_var.set("")
        self.result_var.set("Result: 0")
        self.error_var.set("")

    def _backspace(self) -> None:
        expression = self.expression_var.get()
        if expression:
            self.expression_var.set(expression[:-1])
        self.error_var.set("")

    def _evaluate(self) -> None:
        expression = self.expression_var.get().strip()
        if not expression:
            self.result_var.set("Result: 0")
            self.error_var.set("Enter an expression to evaluate")
            return

        try:
            value = self.calculator.evaluate_expression(expression)
        except (CalculatorError, ZeroDivisionError, ValueError, TypeError) as exc:
            self.result_var.set("Result: Error")
            self.error_var.set(str(exc))
            return
        except Exception:
            # Keep a safe fallback for unexpected UI/runtime issues.
            self.result_var.set("Result: Error")
            self.error_var.set("Unexpected error while evaluating expression")
            return

        self.result_var.set(f"Result: {value:g}")
        self.error_var.set("")


def main() -> None:
    root = tk.Tk()
    CalculatorUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
