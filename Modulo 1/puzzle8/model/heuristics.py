from __future__ import annotations
from typing import Tuple
from .board import Board, GOAL

Position = Tuple[int, int]

# Suma de distancias Manhattan de cada ficha a su posición objetivo
def manhattan(board: Board) -> int:
    dist = 0
    for v in range(1, 9):
        r1, c1 = board.index_of(v)
        idx_goal = GOAL.index(v)
        r2, c2 = idx_goal // 3, idx_goal % 3
        dist += abs(r1 - r2) + abs(c1 - c2)
    return dist