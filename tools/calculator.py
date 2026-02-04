from __future__ import annotations

import ast
import operator as op
from typing import Any, Dict

from .base import Tool


_ALLOWED = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg,
}


def _eval(node: ast.AST) -> float:
    if isinstance(node, ast.Num):  # py<3.8
        return float(node.n)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)
    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED:
        return _ALLOWED[type(node.op)](_eval(node.left), _eval(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED:
        return _ALLOWED[type(node.op)](_eval(node.operand))
    raise ValueError("Unsupported expression")


class CalculatorTool(Tool):
    name = "calculator"
    description = "Safely evaluate basic arithmetic expressions."
    schema: Dict[str, Any] = {
        "type": "object",
        "properties": {"expression": {"type": "string"}},
        "required": ["expression"],
    }

    def run(self, expression: str, **_: Any) -> Any:
        # keep only a conservative subset
        expr = expression.strip()
        tree = ast.parse(expr, mode="eval")
        return _eval(tree.body)
