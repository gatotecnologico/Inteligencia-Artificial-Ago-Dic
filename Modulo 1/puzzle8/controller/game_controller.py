from __future__ import annotations
from typing import Optional, List
from model.board import Tablero
from .solver import astar
import random

class PuzzleController:
    def __init__(actual, tablero: Tablero):
        actual.tablero = tablero
        actual._init = tablero
        actual.movimientos_jugador = 0

    def hacer_gui(actual, guiview):
        actual.view = guiview
        guiview.bind_on_shuffle(actual.barajear)
        guiview.bind_on_solve(actual.on_solve)
        actual.view.render(actual.tablero)
        if actual.tablero.es_meta():
            actual.view.set_status("¡Resuelto!")

            
    def barajear(actual, n: int = 40, semilla: int | None = None):
        random.seed(semilla)
        b = actual.tablero
        for _ in range(n):
            mv = random.choice(b.movimientos_legales())
            b = b.movimiento(mv)
        actual.tablero = b
        actual._init = b
        actual.movimientos_jugador = 0
        actual.view.render(actual.tablero, header=f"Barajado ({n} movimientos)")

    def on_solve(actual, animate: bool = True, delay_ms: int = 100):
        try:
            actual.view.set_status("Buscando solución con A* …")
           
            #Llama al algoritmo A* pasando el tablero actual.
            ruta, nodos_expandidos = astar(actual.tablero) 
            total = len(ruta) #Calcula el total de movimientos necesarios para resolver
            
            #Guarda estadísticas para usarlas al final de la animación
            actual.movimientos_solver = 0
            actual.solver_total = total
            actual.solver_nodos_expandidos = nodos_expandidos

                       
            actual._playback(
            ruta[:],
            delay_ms 
            )
    
        except ValueError as e:
            actual.view.set_status(str(e))


    def _playback(actual, raiz: List[str], delay_ms: int):
        # Si ya no hay movimientos, deja el mensaje final con ambas métricas
        if not raiz:
            total = getattr(actual, "solver_total", actual.movimientos_solver)
            exp = getattr(actual, "solver_nodos_expandidos", None)

            # Ajusta el contador por si faltó sincronizar
            actual.movimientos_solver = total

            if exp is not None:
                actual.view.set_status(
                    f"¡Resuelto por A* en {total} movimientos! "
                    f"Nodos expandidos: {exp}"
                )
            else:
                actual.view.set_status(f"¡Resuelto por A* en {total} movimientos!")
            return

        # Aplica el siguiente movimiento
        mv = raiz.pop(0)
        actual.tablero = actual.tablero.movimiento(mv)
        actual.movimientos_solver += 1

        # Progreso en vivo: paso X/Y
        paso = actual.movimientos_solver
        total = getattr(actual, "solver_total", paso)

        actual.view.render(
            actual.tablero,
            header=f"A* aplicando: {mv}  ·  Paso {paso}/{total}",
            movs=paso
        )

        # Programa el siguiente paso (usa el scheduler propio de tu vista)
        actual.view.schedule(delay_ms, lambda: actual._playback(raiz, delay_ms))