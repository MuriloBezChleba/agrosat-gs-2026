"""
Lista duplamente ligada para armazenar observações satelitais de um talhão em
ordem cronológica. Permite percorrer do mais antigo ao mais recente e vice-versa.
"""

from __future__ import annotations
from typing import Any, Iterator, Optional


class Node:
    def __init__(self, data: Any) -> None:
        self.data = data
        self.prev: Optional[Node] = None
        self.next: Optional[Node] = None


class DoublyLinkedList:
    def __init__(self) -> None:
        self._head: Optional[Node] = None
        self._tail: Optional[Node] = None
        self._size: int = 0

    def append(self, data: Any) -> None:
        """Insere no final (observação mais recente)."""
        node = Node(data)
        if self._tail is None:
            self._head = self._tail = node
        else:
            node.prev = self._tail
            self._tail.next = node
            self._tail = node
        self._size += 1

    def prepend(self, data: Any) -> None:
        """Insere no início (observação mais antiga)."""
        node = Node(data)
        if self._head is None:
            self._head = self._tail = node
        else:
            node.next = self._head
            self._head.prev = node
            self._head = node
        self._size += 1

    def remove(self, data: Any) -> bool:
        """Remove primeiro nó com data == data. Retorna True se removeu."""
        current = self._head
        while current:
            if current.data == data:
                if current.prev:
                    current.prev.next = current.next
                else:
                    self._head = current.next
                if current.next:
                    current.next.prev = current.prev
                else:
                    self._tail = current.prev
                self._size -= 1
                return True
            current = current.next
        return False

    def find(self, predicate) -> Optional[Any]:
        """Retorna primeiro elemento onde predicate(data) é True."""
        current = self._head
        while current:
            if predicate(current.data):
                return current.data
            current = current.next
        return None

    def to_list(self) -> list:
        """Converte para list Python (head → tail)."""
        result = []
        current = self._head
        while current:
            result.append(current.data)
            current = current.next
        return result

    def to_list_reversed(self) -> list:
        """Converte para list Python (tail → head)."""
        result = []
        current = self._tail
        while current:
            result.append(current.data)
            current = current.prev
        return result

    def is_empty(self) -> bool:
        return self._size == 0

    def size(self) -> int:
        return self._size

    def __iter__(self) -> Iterator:
        current = self._head
        while current:
            yield current.data
            current = current.next

    def __len__(self) -> int:
        return self._size

    def __repr__(self) -> str:
        return f"DoublyLinkedList(size={self._size})"
