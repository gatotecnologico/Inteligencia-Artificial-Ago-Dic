from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable, List, Optional, Tuple

Coord = Tuple[int, int]
estado = Tuple[int, ...]  # tupla de 9, 0 = hueco

solucion: estado = (1, 2, 3, 4, 5, 6, 7, 8, 0)

MOVIMIENTOS = {
    'U': (-1, 0),  # mover el hueco hacia arriba (el hueco sube)
    'D': (1, 0),
    'L': (0, -1),
    'R': (0, 1),
}

@dataclass(frozen=True)
class Tablero:
    """Representa un estado del 8-puzzle como tupla inmutable."""
    state: estado

    @staticmethod
    def from_list(vals: Iterable[int]) -> "Tablero":
        t = tuple(vals)
        if len(t) != 9 or set(t) != set(range(9)):
            raise ValueError("El estado debe contener los números 0..8 exactamente una vez.")
        return Tablero(t)
###

# --- META: ¿ya está resuelto exactamente? ---
    def es_meta(self) -> bool:
        return self.state == solucion

    # --- RESOLUBILIDAD: ¿tiene solución (paridad de inversiones)? ---
    def es_resoluble(self) -> bool:
        arr = [x for x in self.state if x != 0]
        inv = 0
        for i in range(len(arr)):
            for j in range(i + 1, len(arr)):
                if arr[i] > arr[j]:
                    inv += 1
        return inv % 2 == 0  # 3x3: par = resoluble
    

    def index(self, value: int) -> Coord:
        i = self.state.index(value)
        return (i // 3, i % 3)

    def movimientos_legales(self) -> List[str]:
        fila, columna = self.index(0)
        moves = []
        for move, (df, dc) in MOVIMIENTOS.items():
            newf, newc = fila + df, columna + dc
            if 0 <= newf < 3 and 0 <= newc < 3:
                moves.append(move)
        return moves

    def movimiento(self, m: str) -> Optional["Tablero"]:
        """Devuelve un nuevo Board aplicando el movimiento, o None si no es legal."""
        if m not in MOVIMIENTOS:
            return None
        r, c = self.index(0)
        dr, dc = MOVIMIENTOS[m]
        nr, nc = r + dr, c + dc
        if not (0 <= nr < 3 and 0 <= nc < 3):
            return None

        idx0 = r * 3 + c
        idx1 = nr * 3 + nc
        lst = list(self.state)
        lst[idx0], lst[idx1] = lst[idx1], lst[idx0]
        return Tablero(tuple(lst))

    def neighbors(self) -> List[Tuple[str, "Tablero"]]:
        return [(m, self.movimiento(m)) for m in self.movimientos_legales()]

    def is_solved(self) -> bool:
        """Para 3x3, es resoluble si el número de inversiones es par."""
        arr = [x for x in self.state if x != 0]
        inv = 0
        for i in range(len(arr)):
            for j in range(i + 1, len(arr)):
                if arr[i] > arr[j]:
                    inv += 1
        return inv % 2 == 0


