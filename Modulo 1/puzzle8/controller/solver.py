# puzzle8/controller/solver.py
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Tuple
import heapq
from model.board import Board
from model.heuristics import manhattan

Heuristic = Callable[[Board], int]

@dataclass(order=True)
class Prioritized:
    f: int
    cnt: int
    board: Board = field(compare=False)

# Reconstruye la secuencia de movimientos desde el objetivo hasta el inicio e invierte la lista para obtener 
# los movimientos en orden correcto.
def reconstruct_path(came_from: Dict[Board, Tuple[Optional[Board], Optional[str]]],
                     goal: Board) -> List[str]:
    moves: List[str] = []
    cur = goal
    while True:
        prev, move = came_from[cur]
        if prev is None:
            break
        moves.append(move)  # move que llevó de prev -> cur
        cur = prev
    moves.reverse()
    return moves

def astar(start: Board,
          heuristic: Heuristic = manhattan,
          max_expansions: int = 200000) -> Tuple[List[str], int]:
    """
    Devuelve (lista_de_movimientos, nodos_expandidos).
    Lanza ValueError si no hay solución o se excede max_expansions.
    """
    if not start.is_solvable():
        raise ValueError("El estado inicial NO es resoluble (paridad incorrecta).")

    g_score: Dict[Board, int] = {start: 0}
    came_from: Dict[Board, Tuple[Optional[Board], Optional[str]]] = {start: (None, None)}

    cnt = 0
    open_heap: List[Prioritized] = []
    heapq.heappush(open_heap, Prioritized(heuristic(start), cnt, start))
    visited: set[Board] = set()

    expansions = 0

    while open_heap:
        current = heapq.heappop(open_heap).board
        if current in visited:
            continue
        visited.add(current)

        if current.is_solved():
            return reconstruct_path(came_from, current), expansions

        expansions += 1
        if expansions > max_expansions:
            raise ValueError("Se excedió el límite de expansiones.")

        for move, nb in current.neighbors():
            if nb is None:
                continue
            tentative_g = g_score[current] + 1
            if tentative_g < g_score.get(nb, 1_000_000_000):
                g_score[nb] = tentative_g
                came_from[nb] = (current, move)
                cnt += 1
                f = tentative_g + heuristic(nb)
                heapq.heappush(open_heap, Prioritized(f, cnt, nb))

    raise ValueError("No se encontró solución (¿estado incorrecto?).")
