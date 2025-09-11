from __future__ import annotations
import random 
from typing import List
from model.board import Tablero, solucion
from controller.game_controller import PuzzleController


def random_tablero(barajadas: int, semilla: int | None) -> Tablero: 
    """Genera un tablero aleatorio pero siempre resoluble.
    
    Parte de la solución final y aplica una cantidad de movimientos legales 
    aleatorios para "barajar" el puzzle. De esta forma se garantiza que 
    el tablero resultante sea alcanzable desde el estado meta.

    Args:
        barajadas (int): Número de movimientos aleatorios a aplicar.
        semilla (int | None): Semilla para el generador aleatorio (opcional).
    
    Returns:
        Tablero: Estado inicial del puzzle después de los movimientos.
    """
    random.seed(semilla)
    b = Tablero(solucion) 
    for _ in range(barajadas):
        mv = random.choice(b.movimientos_legales())
        b = b.movimiento(mv)
    return b


def main():
    """Punto de entrada del programa.

    - Define un tablero inicial (puede ser fijo o aleatorio).
    - Verifica que el tablero tenga solución.
    - Crea el controlador principal (`PuzzleController`).
    - Inicializa la interfaz gráfica y lanza el bucle principal.
    """
    board = Tablero.from_list((4, 0, 1, 3, 5, 6, 2, 7, 8))

    if not board.es_resoluble():
        raise SystemExit("El estado inicial no es resoluble. Intenta otra barajado.")

    ctrl = PuzzleController(board)

    from view.gui import GUIView
    ventana = GUIView()
    ctrl.hacer_gui(ventana)
    ventana.mainloop()
    return


if __name__ == "__main__":
    main()
