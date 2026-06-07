"""
Algoritmos de ordenação aplicados ao dataset de propriedades rurais.
"""

from __future__ import annotations
from typing import Any, Callable


def quick_sort(items: list, key: Callable[[Any], Any], low: int = 0, high: int = -1) -> list:
    """
    Quick sort in-place usando pivô no elemento do meio.
    O(n log n) médio. Usa para ordenar propriedades por NDVI ou score de risco.

    Retorna a própria lista ordenada (in-place).
    """
    if high == -1:
        high = len(items) - 1

    if low < high:
        pivot_idx = _partition(items, key, low, high)
        quick_sort(items, key, low, pivot_idx - 1)
        quick_sort(items, key, pivot_idx + 1, high)

    return items


def _partition(items: list, key: Callable, low: int, high: int) -> int:
    pivot = key(items[(low + high) // 2])
    left = low
    right = high

    while True:
        while key(items[left]) < pivot:
            left += 1
        while key(items[right]) > pivot:
            right -= 1
        if left >= right:
            return right
        items[left], items[right] = items[right], items[left]
        left += 1
        right -= 1


def merge_sort(items: list, key: Callable[[Any], Any]) -> list:
    """
    Merge sort — cria nova lista ordenada.
    O(n log n) garantido. Usa para ordenar observações por data dentro de um talhão.

    Retorna nova lista ordenada (não modifica original).
    """
    if len(items) <= 1:
        return list(items)

    mid = len(items) // 2
    left = merge_sort(items[:mid], key)
    right = merge_sort(items[mid:], key)

    return _merge(left, right, key)


def _merge(left: list, right: list, key: Callable) -> list:
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result
