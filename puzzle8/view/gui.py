# puzzle8/view/gui.py
from __future__ import annotations
import tkinter as tk
from tkinter import messagebox
from typing import Callable, Optional
from model.board import Tablero

Tile = list[list[tk.Label]]

class GUIView:
    def __init__(self, title="Puzzle 8"):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.resizable(False, False)

        # ====== LAYOUT ======
        self._frame = tk.Frame(self.root, padx=12, pady=12)
        self._frame.grid(row=0, column=0)

        # Panel tablero 3x3
        self.grid_frame = tk.Frame(self._frame, bd=2, relief="groove")
        self.grid_frame.grid(row=0, column=0, columnspan=4, pady=(0, 10))
        self.tiles: Tile = [[None]*3 for _ in range(3)]  # type: ignore

        self.moves_label = tk.Label(self._frame, text="Movimientos (A*): 0", anchor="w")
        self.moves_label.grid(row=2, column=0, columnspan=2, sticky="w", pady=(4, 0))

        for r in range(3):
            for c in range(3):
                lbl = tk.Label(self.grid_frame, text="",
                               width=4, height=2,
                               font=("Segoe UI", 20, "bold"),
                               bd=1, relief="ridge", padx=10, pady=10,
                               bg="#ffffff")
                lbl.grid(row=r, column=c, padx=4, pady=4, sticky="nsew")
                self.tiles[r][c] = lbl

        # Botones
        self.btn_shuffle = tk.Button(self._frame, text="Barajar", width=10, command=lambda: None)
        self.btn_solve   = tk.Button(self._frame, text="Resolver A*", width=12, command=lambda: None)
        self.btn_quit    = tk.Button(self._frame, text="Salir", width=10, command=self.root.destroy)
            
        self.btn_shuffle.grid(row=1, column=0, padx=4)
        self.btn_solve.grid(row=1, column=1, padx=4)
        self.btn_quit.grid(row=1, column=3, padx=4)

        # Status
        self.status = tk.Label(self._frame, text="Bienvenido!", anchor="w", fg="#333")
        self.status.grid(row=2, column=0, columnspan=4, sticky="we", pady=(10,0))

        # Callbacks (los inyecta el Controller)
        self._on_shuffle: Optional[Callable[[], None]] = None
        self._on_solve: Optional[Callable[[], None]] = None

    def bind_on_shuffle(self, fn: Callable[[], None]):
        self._on_shuffle = fn
        self.btn_shuffle.configure(command=fn)

    def bind_on_solve(self, fn: Callable[[], None]):
        self._on_solve = fn
        self.btn_solve.configure(command=fn)

    # ==== API que usa el Controller ====
    def render(self, board: Tablero, header: str | None = None, movs: int | None = None):
        if header: self.set_status(header)
        if movs is not None:
            self.moves_label.configure(text=f"Movimientos (A*): {movs}")
            self.moves_label.update_idletasks()

        st = board.state
        for r in range(3):
            for c in range(3):
                v = st[r*3 + c]
                lbl = self.tiles[r][c]
                if v == 0:
                    lbl.configure(text="", bg="#eaeaea")
                else:
                    lbl.configure(text=str(v), bg="#c95c5c")

    def set_status(self, msg: str):
        self.status.configure(text=msg)
        self.status.update_idletasks()

    def schedule(self, ms: int, fn: Callable[[], None]):
        self.root.after(ms, fn)

    def mainloop(self):
        self.root.mainloop()