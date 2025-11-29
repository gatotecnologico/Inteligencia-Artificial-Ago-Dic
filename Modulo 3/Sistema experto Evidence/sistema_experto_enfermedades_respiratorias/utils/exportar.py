
# ==================== ARCHIVO: utils/exportar.py ====================
"""
Exportar resultados a diferentes formatos
"""
from datetime import datetime

def exportar_a_texto(diagnosticos, paciente_info):
    """Exporta los diagnósticos a un archivo de texto"""
    contenido = []
    contenido.append("=" * 70)
    contenido.append("SISTEMA EXPERTO - DIAGNÓSTICO RESPIRATORIO")
    contenido.append(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    contenido.append("=" * 70)
    contenido.append(f"\nPaciente: Edad {paciente_info.get('edad')} años")
    contenido.append("\n" + "=" * 70)
    
    for i, d in enumerate(diagnosticos, 1):
        contenido.append(f"\nDIAGNÓSTICO #{i}")
        contenido.append(f"Certeza: {round(d['certeza']*100)}%")
        contenido.append("\nReglas activadas:")
        for regla in d['reglas']:
            contenido.append(f"  {regla}")
        contenido.append("\nRecomendaciones:")
        for rec in d['recomendaciones']:
            contenido.append(f"  {rec}")
        contenido.append("\n" + "-" * 70)
    
    return "\n".join(contenido)
