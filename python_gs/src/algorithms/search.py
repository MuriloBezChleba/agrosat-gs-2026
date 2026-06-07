"""
Algoritmos de busca aplicados ao dataset de propriedades rurais.
"""

from __future__ import annotations
from typing import Any, Callable, Optional


def linear_search(items: list, predicate: Callable[[Any], bool]) -> list:
    """
    Busca linear — percorre toda a lista aplicando predicate.
    O(n). Usa para busca por município, cultura ou estado.

    Retorna lista com todos os elementos que satisfazem predicate.
    """
    result = []
    for item in items:
        if predicate(item):
            result.append(item)
    return result


def binary_search(sorted_items: list, target: Any, key: Callable[[Any], Any]) -> Optional[Any]:
    """
    Busca binária em lista ordenada pela função key.
    O(log n). Usa para busca por property_id após quick_sort.

    Retorna o elemento encontrado ou None.
    """
    low = 0
    high = len(sorted_items) - 1

    while low <= high:
        mid = (low + high) // 2
        mid_val = key(sorted_items[mid])

        if mid_val == target:
            return sorted_items[mid]
        elif mid_val < target:
            low = mid + 1
        else:
            high = mid - 1

    return None
