# puzzle8/view/cli.py
from __future__ import annotations
from model.board import Board

class CLIView:
    def show_welcome(self):
        print("\n== 8-Puzzle MVC (CLI) ==")
        print("W/A/S/D para mover el hueco (0). Q para salir.\n")

    def render(self, board: Board, header: str | None = None):
        if header:
            print(header)
        print("+---+---+---+")
        st = board.state
        for r in range(3):
            row = st[r*3:(r+1)*3]
            def cell(x): return " " if x == 0 else str(x)
            print("| {} | {} | {} |".format(*(cell(x) for x in row)))
            print("+---+---+---+")
        print()

    def ask_move(self, legal_moves: list[str]) -> str:
        s = input("Movimiento (W/A/S/D, Q salir): ").strip()
        return s

    def show_solved(self):
        print("¡Resuelto! 🎉")

    def say(self, msg: str):
        print(msg)
