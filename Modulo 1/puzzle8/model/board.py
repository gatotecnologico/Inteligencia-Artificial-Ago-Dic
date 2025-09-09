# puzzle8/model/board.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable, List, Optional, Tuple

Coord = Tuple[int, int]
State = Tuple[int, ...]  # tupla de 9, 0 = hueco

GOAL: State = (1, 2, 3,
               4, 5, 6,
               7, 8, 0)

MOVES = {
    'U': (-1, 0),
    'D': (1, 0),
    'L': (0, -1),
    'R': (0, 1),
}

@dataclass(frozen=True)
class Board:
    # "Representa un estado del 8-puzzle como tupla inmutable."
    state: State

    @staticmethod
    def from_list(vals: Iterable[int]) -> "Board":
        t = tuple(vals)
        if len(t) != 9 or set(t) != set(range(9)):
            raise ValueError("El estado debe contener los números 0..8 exactamente.")
        return Board(t)

    # Devuelve el estado objetivo
    @staticmethod
    def goal() -> "Board":
        return Board(GOAL)

    def index_of(self, value: int) -> Coord:
        i = self.state.index(value)
        return (i // 3, i % 3)

    # Verifica si se alcanzó el estado objetivo
    def is_solved(self) -> bool:
        return self.state == GOAL

    # Devuelve movimientos válidos desde la posición del hueco
    def legal_moves(self) -> List[str]:
        r, c = self.index_of(0)
        moves = []
        for m, (dr, dc) in MOVES.items():
            nr, nc = r + dr, c + dc
            if 0 <= nr < 3 and 0 <= nc < 3:
                moves.append(m)
        return moves

    # Devuelve un nuevo tablero (Board) aplicando el movimiento, o None si no es legal
    def move(self, m: str) -> Optional["Board"]:
        if m not in MOVES:
            return None
        r, c = self.index_of(0)
        dr, dc = MOVES[m]
        nr, nc = r + dr, c + dc
        if not (0 <= nr < 3 and 0 <= nc < 3):
            return None

        idx0 = r * 3 + c
        idx1 = nr * 3 + nc
        lst = list(self.state)
        lst[idx0], lst[idx1] = lst[idx1], lst[idx0]
        return Board(tuple(lst))

    def neighbors(self) -> List[Tuple[str, "Board"]]:
        return [(m, self.move(m)) for m in self.legal_moves()]

    # Verifica si el juego es resoluble
    def is_solvable(self) -> bool:
        arr = [x for x in self.state if x != 0]
        inv = 0
        for i in range(len(arr)):
            for j in range(i + 1, len(arr)):
                if arr[i] > arr[j]:
                    inv += 1
        return inv % 2 == 0