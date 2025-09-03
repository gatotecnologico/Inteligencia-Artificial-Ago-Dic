

# puzzle8/view/gui.py
from __future__ import annotations
import tkinter as tk
from tkinter import messagebox
from typing import Callable, Optional
from ..model.board import Board

Tile = list[list[tk.Label]]

class GUIView:
    """Vista Tkinter para 8-puzzle. No contiene lógica del juego."""
    def __init__(self, title="8-Puzzle"):
        self.root = tk.Tk()
        self.root.title(title)                 # ← título de la ventana
        self.root.resizable(False, False)

        # ====== MENÚ ======
        self.menubar = tk.Menu(self.root)
        # Menú Juego
        self.menu_game = tk.Menu(self.menubar, tearoff=0)
        self.menu_game.add_command(label="Barajar\tCtrl+N", command=lambda: None)
        self.menu_game.add_command(label="Resolver A*\tCtrl+Enter", command=lambda: None)
        self.menu_game.add_command(label="Reset\tCtrl+R", command=lambda: None)
        self.menu_game.add_separator()
        self.menu_game.add_command(label="Salir\tCtrl+Q", command=self.root.destroy)
        self.menubar.add_cascade(label="Juego", menu=self.menu_game)

        # Menú Ayuda
        self.menu_help = tk.Menu(self.menubar, tearoff=0)
        self.menu_help.add_command(label="Controles…\tF1", command=self._show_controls)
        self.menu_help.add_command(label="Acerca de…", command=self._show_about)
        self.menubar.add_cascade(label="Ayuda", menu=self.menu_help)

        self.root.config(menu=self.menubar)

        # ====== ATALHOS (accelerators) ======
        self.root.bind("<Control-n>", lambda e: self._on_shuffle() if self._on_shuffle else None)
        self.root.bind("<Control-Return>", lambda e: self._on_solve() if self._on_solve else None)
        self.root.bind("<Control-r>", lambda e: self._on_reset() if self._on_reset else None)
        self.root.bind("<Control-q>", lambda e: self.root.destroy())
        self.root.bind("<F1>", lambda e: self._show_controls())

        # ====== LAYOUT ======
        self._frame = tk.Frame(self.root, padx=12, pady=12)
        self._frame.grid(row=0, column=0)

        # Panel tablero 3x3
        self.grid_frame = tk.Frame(self._frame, bd=2, relief="groove")
        self.grid_frame.grid(row=0, column=0, columnspan=4, pady=(0, 10))
        self.tiles: Tile = [[None]*3 for _ in range(3)]  # type: ignore

        for r in range(3):
            for c in range(3):
                lbl = tk.Label(self.grid_frame, text="",
                               width=4, height=2,
                               font=("Segoe UI", 20, "bold"),
                               bd=1, relief="ridge", padx=10, pady=10,
                               bg="#ffffff")
                lbl.grid(row=r, column=c, padx=4, pady=4, sticky="nsew")
                self.tiles[r][c] = lbl

        # Botones (opcional mantenerlos)
        self.btn_shuffle = tk.Button(self._frame, text="Barajar", width=10, command=lambda: None)
        self.btn_solve   = tk.Button(self._frame, text="Resolver A*", width=12, command=lambda: None)
        # self.btn_reset   = tk.Button(self._frame, text="Reset", width=10, command=lambda: None)
        self.btn_quit    = tk.Button(self._frame, text="Salir", width=10, command=self.root.destroy)
            
        self.btn_shuffle.grid(row=1, column=0, padx=4)
        self.btn_solve.grid(row=1, column=1, padx=4)
        # self.btn_reset.grid(row=1, column=2, padx=4)
        self.btn_quit.grid(row=1, column=3, padx=4)

        # Status
        self.status = tk.Label(self._frame, text="Listo. Usa WASD o flechas.  (F1: Ayuda)",
                               anchor="w", fg="#333")
        self.status.grid(row=2, column=0, columnspan=4, sticky="we", pady=(10,0))

        # Callbacks (los inyecta el Controller)
        self._on_key: Optional[Callable[[str], None]] = None
        self._on_shuffle: Optional[Callable[[], None]] = None
        self._on_solve: Optional[Callable[[], None]] = None
        # self._on_reset: Optional[Callable[[], None]] = None

        # Bind teclas (WASD + flechas)
        for k in ["w","a","s","d","W","A","S","D","Up","Down","Left","Right"]:
            # Nota: las flechas necesitan los <>
            self.root.bind(f"<{k}>" if k[0].isupper() else k, self._key_event)

    # ==== Enlaces que hace el Controller ====
    def bind_on_key(self, fn: Callable[[str], None]): self._on_key = fn

    def bind_on_shuffle(self, fn: Callable[[], None]):
        self._on_shuffle = fn
        self.btn_shuffle.configure(command=fn)
        # también conectar menú
        self.menu_game.entryconfig(0, command=fn)

    def bind_on_solve(self, fn: Callable[[], None]):
        self._on_solve = fn
        self.btn_solve.configure(command=fn)
        self.menu_game.entryconfig(1, command=fn)

    def bind_on_reset(self, fn: Callable[[], None]):
        self._on_reset = fn
        # self.btn_reset.configure(command=fn)
        self.menu_game.entryconfig(2, command=fn)

    # ==== API que usa el Controller ====
    def render(self, board: Board, header: str | None = None):
        if header: self.set_status(header)
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

    # ==== Interno ====
    def _key_event(self, ev):
        if not self._on_key: return
        # keysym: "w", "a", "s", "d", "Up", "Down", "Left", "Right"
        self._on_key(ev.keysym.lower())

    def _show_controls(self):
        messagebox.showinfo(
            "Controles",
            "Mover: WASD o Flechas ↑ ↓ ← →\n"
            "Barajar: Ctrl+N\n"
            "Resolver A*: Ctrl+Enter\n"
            "Salir: Ctrl+Q"
        )

    def _show_about(self):
        messagebox.showinfo(
            "Acerca de",
            "8-Puzzle en Python Y Tkinter\n"
            "Algoritmo de búsqueda: A* con heurística Manhattan"
        )
