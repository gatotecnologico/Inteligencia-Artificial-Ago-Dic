

# puzzle8/main.py  (reemplaza por esta versión)
from __future__ import annotations
import argparse, random
from typing import List
from .model.board import Board, GOAL
from .controller.game_controller import GameController

def parse_args():
    p = argparse.ArgumentParser(description="8-Puzzle MVC")
    p.add_argument("--start", type=str,
                   help='Estado inicial como 9 números separados por espacios. Ej: "1 2 3 4 5 6 7 0 8"')
    p.add_argument("--random", type=int, default=0,
                   help="Aplicar N barajadas aleatorias desde el objetivo.")
    p.add_argument("--seed", type=int, default=None, help="Semilla RNG para reproducibilidad.")
    p.add_argument("--solve", action="store_true", help="Resolver con A* y mostrar la animación (CLI).")
    p.add_argument("--gui", action="store_true", help="Lanzar interfaz gráfica Tkinter.")
    return p.parse_args()

def random_board(shuffles: int, seed: int | None) -> Board:
    random.seed(seed)
    b = Board(GOAL)
    for _ in range(shuffles):
        mv = random.choice(b.legal_moves())
        b = b.move(mv)
    return b

def main():
    args = parse_args()

    if args.start:
        vals = [int(x) for x in args.start.split()]
        board = Board.from_list(vals)
    elif args.random and args.random > 0:
        board = random_board(args.random, args.seed)
    else:
        board = Board.from_list((1, 2, 3, 4, 5, 6, 0, 7, 8))

    if not board.is_solvable():
        raise SystemExit("El estado inicial no es resoluble. Intenta otra semilla o barajado.")

    ctrl = GameController(board)

    if args.gui:
        from .view.gui import GUIView
        gv = GUIView()
        ctrl.bind_gui(gv)
        gv.mainloop()
        return

    # CLI
    if args.solve:
        ctrl.solve_and_playback(animate=True)
    else:
        ctrl.loop()

if __name__ == "__main__":
    main()
