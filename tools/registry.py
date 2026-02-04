from __future__ import annotations

from typing import Dict, List

from .base import Tool
from .calculator import CalculatorTool


_REGISTRY: Dict[str, Tool] = {
    CalculatorTool.name: CalculatorTool(),
}


def get_tool(name: str) -> Tool:
    if name not in _REGISTRY:
        raise KeyError(f"Unknown tool: {name}. Available: {', '.join(_REGISTRY)}")
    return _REGISTRY[name]


def list_tools() -> List[str]:
    return sorted(_REGISTRY.keys())
