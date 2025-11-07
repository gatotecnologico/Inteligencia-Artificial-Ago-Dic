# ==================== ARCHIVO: main.py ====================
"""
Archivo principal - Ejecutar este para iniciar la aplicación
"""

import tkinter as tk
from modelos.base_conocimientos import BaseConocimientos
from logica.motor_inferencia import MotorInferencia
from interfaz.gui_tkinter import SistemaExpertoGUI

def main():
    """Función principal"""
    # Crear ventana principal
    root = tk.Tk()
    
    # Inicializar componentes
    bc = BaseConocimientos()
    motor = MotorInferencia(bc)
    
    # Crear interfaz
    app = SistemaExpertoGUI(root, bc, motor)
    
    # Iniciar aplicación
    root.mainloop()

if __name__ == "__main__":
    main()

