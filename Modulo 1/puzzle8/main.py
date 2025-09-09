#python main.py
from __future__ import annotations
from typing import List
from model.board import Board, GOAL
from controller.game_controller import GameController

def main():
    board = Board.from_list((1, 2, 3, 4, 5, 6, 0, 7, 8))

    if not board.is_solvable():
        raise SystemExit("El estado inicial no es resoluble. Intenta otra semilla o barajado.")

    ctrl = GameController(board)

    from view.gui import GUIView
    gv = GUIView()
    ctrl.bind_gui(gv)
    gv.mainloop()
    return

if __name__ == "__main__":
    main()
