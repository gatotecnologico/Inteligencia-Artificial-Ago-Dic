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
    'U': (-1, 0),  # mover el hueco hacia arriba (el hueco sube)
    'D': (1, 0),
    'L': (0, -1),
    'R': (0, 1),
}

@dataclass(frozen=True)
class Board:
    """Representa un estado del 8-puzzle como tupla inmutable."""
    state: State

    @staticmethod
    def from_list(vals: Iterable[int]) -> "Board":
        t = tuple(vals)
        if len(t) != 9 or set(t) != set(range(9)):
            raise ValueError("El estado debe contener los números 0..8 exactamente una vez.")
        return Board(t)

    @staticmethod
    def goal() -> "Board":
        return Board(GOAL)

    def index_of(self, value: int) -> Coord:
        i = self.state.index(value)
        return (i // 3, i % 3)

    def is_solved(self) -> bool:
        return self.state == GOAL

    def legal_moves(self) -> List[str]:
        r, c = self.index_of(0)
        moves = []
        for m, (dr, dc) in MOVES.items():
            nr, nc = r + dr, c + dc
            if 0 <= nr < 3 and 0 <= nc < 3:
                moves.append(m)
        return moves

    def move(self, m: str) -> Optional["Board"]:
        """Devuelve un nuevo Board aplicando el movimiento, o None si no es legal."""
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

    def is_solvable(self) -> bool:
        """Para 3x3, es resoluble si el número de inversiones es par."""
        arr = [x for x in self.state if x != 0]
        inv = 0
        for i in range(len(arr)):
            for j in range(i + 1, len(arr)):
                if arr[i] > arr[j]:
                    inv += 1
        return inv % 2 == 0

    def __str__(self) -> str:
        rows = [self.state[0:3], self.state[3:6], self.state[6:9]]
        def fmt(x): return " " if x == 0 else str(x)
        return "\n".join(" | ".join(fmt(x) for x in row) for row in rows)
