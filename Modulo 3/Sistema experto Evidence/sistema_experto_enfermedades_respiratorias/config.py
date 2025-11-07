# ==================== ARCHIVO: config.py ====================
"""
Configuraciones globales del sistema
"""

NOMBRE_SISTEMA = "Sistema Experto - Diagnóstico Respiratorio"
VERSION = "1.0.0"

# Colores de la interfaz
COLORES = {
    'primario': '#667eea',
    'secundario': '#764ba2',
    'fondo': '#f0f0f0',
    'blanco': 'white',
    'advertencia': '#fff3cd',
    'texto_advertencia': '#856404'
}

# Configuración de ventana
VENTANA = {
    'ancho': 1200,
    'alto': 800,
    'titulo': NOMBRE_SISTEMA
}

# Umbrales de certeza
UMBRALES_CERTEZA = {
    'alta': 0.75,
    'media': 0.50
}
