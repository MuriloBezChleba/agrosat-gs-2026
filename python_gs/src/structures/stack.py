"""
Pilha LIFO para histórico de análises de risco.
Armazena últimas MAX_SIZE análises — a mais recente fica no topo.
"""

from __future__ import annotations
from typing import Any, Optional

MAX_SIZE = 20


class Stack:
    def __init__(self, max_size: int = MAX_SIZE) -> None:
        self._data: list[Any] = []
        self._max_size = max_size

    def push(self, item: Any) -> None:
        """Empilha item. Se atingir max_size, descarta o mais antigo (base)."""
        if len(self._data) >= self._max_size:
            self._data.pop(0)
        self._data.append(item)

    def pop(self) -> Any:
        """Desempilha e retorna topo. Raises IndexError se vazia."""
        if self.is_empty():
            raise IndexError("pop em pilha vazia")
        return self._data.pop()

    def peek(self) -> Any:
        """Retorna topo sem remover. Raises IndexError se vazia."""
        if self.is_empty():
            raise IndexError("peek em pilha vazia")
        return self._data[-1]

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def size(self) -> int:
        return len(self._data)

    def to_list(self) -> list:
        """Retorna cópia da pilha do mais antigo ao mais recente."""
        return list(self._data)

    def __repr__(self) -> str:
        return f"Stack(size={len(self._data)}, max={self._max_size})"
