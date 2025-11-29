from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Tuple
import heapq
from model.board import Tablero
from model.heuristics import manhattan

Heuristic = Callable[[Tablero], int]

@dataclass(order=True)
class Prioritized:
    f: int
    act: int
    board: Tablero = field(compare=False)
def trazar_ruta(raiz: Dict[Tablero, Tuple[Optional[Tablero], Optional[str]]],
                solution: Tablero) -> List[str]:
    movimientos: List[str] = []
    actual = solution 
    while True:
        prev, mov = raiz[actual]
        if prev is None:
            break
        movimientos.append(mov)  
        actual = prev
    movimientos.reverse()
    return movimientos

def astar(start: Tablero,
          heuristic: Heuristic = manhattan,
          max_expansions: int = 200000) -> Tuple[List[str], int]:
          
    if not start.es_resoluble():
        raise ValueError("El estado inicial NO es resoluble (paridad incorrecta).")

    costo_acumulado: Dict[Tablero, int] = {start: 0}
    raiz: Dict[Tablero, Tuple[Optional[Tablero], Optional[str]]] = {start: (None, None)}

    act = 0
    open_heap: List[Prioritized] = []
    heapq.heappush(open_heap, Prioritized(heuristic(start), act, start))
    visited: set[Tablero] = set()

    expansions = 0

    while open_heap:
        actual = heapq.heappop(open_heap).board
        if actual in visited:
            continue
        visited.add(actual)

        if actual.es_meta():
            return trazar_ruta(raiz, actual), expansions

        expansions += 1
        if expansions > max_expansions:
            raise ValueError("Se excedió el límite de expansiones.")

        for move, nb in actual.neighbors():
            if nb is None:
                continue
            tentative_g = costo_acumulado[actual] + 1
            if tentative_g < costo_acumulado.get(nb, 1_000_000_000):
                costo_acumulado[nb] = tentative_g
                raiz[nb] = (actual, move)
                act += 1
                f = tentative_g + heuristic(nb)
                heapq.heappush(open_heap, Prioritized(f, act, nb))

    raise ValueError("No se encontró solución (¿estado incorrecto?).")
