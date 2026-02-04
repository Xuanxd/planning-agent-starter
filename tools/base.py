from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict


class Tool(ABC):
    name: str
    description: str
    schema: Dict[str, Any]

    @abstractmethod
    def run(self, **kwargs: Any) -> Any:
        raise NotImplementedError
