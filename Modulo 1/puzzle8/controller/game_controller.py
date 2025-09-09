
# puzzle8/controller/game_controller.py  (añadir/editar)
from __future__ import annotations
from typing import Optional, List
from model.board import Board
from .solver import astar
import random

class GameController:
    # Guarda el estado actual del tablero y el estado inicial.
    def __init__(self, board: Board):
        self.board = board
        self._initial = board

    def bind_gui(self, guiview):
        self.view = guiview
        guiview.bind_on_shuffle(self.on_shuffle)
        guiview.bind_on_solve(self.on_solve)
        self.view.render(self.board)
        if self.board.is_solved():
            self.view.set_status("¡Resuelto!")

    # Mezcla el tablero con movimientos aleatorios y garantiza que el resultado sea resoluble con movimientos legales
    def on_shuffle(self, n: int = 40, seed: int | None = None):
        random.seed(seed)
        b = self.board
        for _ in range(n):
            mv = random.choice(b.legal_moves())
            b = b.move(mv)
        self.board = b
        self._initial = b
        self.view.render(self.board, header=f"Barajado ({n} movimientos)")

    # Usa el algoritmo A* para encontrar la solución óptima y muestra cuántos movimientos necesita
    def on_solve(self, animate: bool = True, delay_ms: int = 200):
        try:
            self.view.set_status("Buscando solución con A* …")
            path, expanded = astar(self.board)
            self.view.set_status(f"Solución en {len(path)} movs. Expandidos: {expanded}")
            if not animate:
                return
            self._playback(path, delay_ms)
        except ValueError as e:
            self.view.set_status(str(e))

    # Muestra cada movimiento en la interfaz
    def _playback(self, path: List[str], delay_ms: int):
        if not path:
            self.view.set_status("¡Resuelto! 🎉")
            return
        mv = path.pop(0)
        self.board = self.board.move(mv)
        self.view.render(self.board, header=f"Aplicando: {mv}")
        self.view.schedule(delay_ms, lambda: self._playback(path, delay_ms))
