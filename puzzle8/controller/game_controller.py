
# puzzle8/controller/game_controller.py  (añadir/editar)
from __future__ import annotations
from typing import Optional, List
from ..model.board import Board
from ..view.cli import CLIView
from .solver import astar
import random

INPUT_TO_MOVE = {
    'w': 'U', #(Up)
    's': 'D', #(Down)
    'a': 'L', #(Left)
    'd': 'R', #(Rigth)

     # Flechas
    'up': 'U',
    'down': 'D',
    'left': 'L',
    'right': 'R',
}

class GameController:
    def __init__(self, board: Board, view: Optional[CLIView] = None):
        self.board = board
        self.view = view or CLIView()
        self._initial = board

    # ====== CLI loop (ya existía) ======
    def loop(self):
        self.view.show_welcome()
        while True:
            self.view.render(self.board)
            if self.board.is_solved():
                self.view.show_solved()
                break

            cmd = self.view.ask_move(self.board.legal_moves())
            if cmd == 'q':
                self.view.say("Saliendo…")
                break
            move = INPUT_TO_MOVE.get(cmd.lower())
            if move is None:
                self.view.say("Comando inválido. Usa WASD o Q para salir.")
                continue

            newb = self.board.move(move)
            if newb is None:
                self.view.say("Movimiento ilegal.")
                continue
            self.board = newb

    # ====== API para GUI ======
    def bind_gui(self, guiview):
        """Conecta handlers GUI -> Controller y hace primer render."""
        self.view = guiview
        guiview.bind_on_key(self.on_key)
        guiview.bind_on_shuffle(self.on_shuffle)
        guiview.bind_on_solve(self.on_solve)
        guiview.bind_on_reset(self.on_reset)
        self.view.render(self.board, header="Usa A/W/S/D o botones.")
        if self.board.is_solved():
            self.view.set_status("¡Resuelto!")

    def on_key(self, key: str):
        mv = INPUT_TO_MOVE.get(key)
        if not mv: return
        nb = self.board.move(mv)
        if nb:
            self.board = nb
            self.view.render(self.board)
            if self.board.is_solved():
                self.view.set_status("¡Resuelto! 🎉")

    def on_shuffle(self, n: int = 40, seed: int | None = None):
        random.seed(seed)
        b = self.board
        for _ in range(n):
            mv = random.choice(b.legal_moves())
            b = b.move(mv)
        self.board = b
        self._initial = b
        self.view.render(self.board, header=f"Barajado ({n} movimientos)")

    def on_reset(self):
        self.board = self._initial
        self.view.render(self.board, header="Reset al estado barajado")

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

    def _playback(self, path: List[str], delay_ms: int):
        if not path:
            self.view.set_status("¡Resuelto! 🎉")
            return
        mv = path.pop(0)
        self.board = self.board.move(mv)
        self.view.render(self.board, header=f"Aplicando: {mv}")
        # Programar siguiente paso
        self.view.schedule(delay_ms, lambda: self._playback(path, delay_ms))
