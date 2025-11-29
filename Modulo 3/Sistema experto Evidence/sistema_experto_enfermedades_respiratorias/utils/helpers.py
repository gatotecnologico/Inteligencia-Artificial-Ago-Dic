# ==================== ARCHIVO: utils/helpers.py ====================
"""
Funciones auxiliares
"""

def obtener_nivel_certeza(porcentaje):
    """Retorna el nivel de certeza según el porcentaje"""
    if porcentaje >= 75:
        return "Alta confianza", "#28a745"
    elif porcentaje >= 50:
        return "Confianza moderada", "#ffc107"
    else:
        return "Baja confianza", "#dc3545"

def formatear_porcentaje(certeza):
    """Formatea el factor de certeza a porcentaje"""
    return round(certeza * 100)
