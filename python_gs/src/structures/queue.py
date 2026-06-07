"""
Fila FIFO para processamento em lote de propriedades rurais.
Analista enfileira talhões; sistema processa na ordem de chegada.
"""

from __future__ import annotations
from typing import Any, Optional


class Queue:
    def __init__(self) -> None:
        self._data: list[Any] = []

    def enqueue(self, item: Any) -> None:
        """Adiciona item no final da fila (rear)."""
        self._data.append(item)

    def dequeue(self) -> Any:
        """Remove e retorna item do início (front). Raises IndexError se vazia."""
        if self.is_empty():
            raise IndexError("dequeue em fila vazia")
        return self._data.pop(0)

    def peek_front(self) -> Any:
        """Retorna próximo item sem remover. Raises IndexError se vazia."""
        if self.is_empty():
            raise IndexError("peek em fila vazia")
        return self._data[0]

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def size(self) -> int:
        return len(self._data)

    def to_list(self) -> list:
        """Retorna cópia da fila (front → rear)."""
        return list(self._data)

    def clear(self) -> None:
        self._data.clear()

    def __repr__(self) -> str:
        return f"Queue(size={len(self._data)})"
