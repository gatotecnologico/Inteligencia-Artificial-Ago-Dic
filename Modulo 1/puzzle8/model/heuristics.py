from __future__ import annotations
from typing import Tuple
from .board import Tablero, solucion

# Position: representa una coordenada en el tablero (fila, columna).
Position = Tuple[int, int]

def manhattan(board: Tablero) -> int:
    """Calcula la heurística Manhattan para un tablero del puzzle 8.

    La distancia Manhattan de una ficha es el número de movimientos 
    verticales y horizontales que necesita para llegar a su posición 
    correcta en el estado objetivo. La heurística total es la suma 
    de estas distancias para todas las fichas.

    """
    dist = 0
    # Recorre fichas del 1 al 8 (el 0 es el espacio vacío, no se cuenta).
    for v in range(1, 9):
        # Posición actual de la ficha v
        r1, c1 = board.index(v)

        # Posición objetivo de la ficha v en el estado solución
        idx_solu = solucion.index(v)
        r2, c2 = idx_solu // 3, idx_solu % 3

        # Distancia Manhattan de la ficha actual a su meta
        dist += abs(r1 - r2) + abs(c1 - c2)

    return dist
