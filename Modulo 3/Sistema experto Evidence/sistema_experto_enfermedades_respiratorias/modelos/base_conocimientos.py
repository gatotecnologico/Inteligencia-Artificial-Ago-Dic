
# ==================== ARCHIVO: modelos/base_conocimientos.py ====================
"""
Base de Conocimientos - Enfermedades y sus características
"""

class BaseConocimientos:
    def __init__(self):
        self.enfermedades = {
            'asma': {
                'nombre': 'Asma',
                'descripcion': 'Enfermedad inflamatoria crónica de las vías respiratorias',
                'color': '#667eea'
            },
            'neumonia': {
                'nombre': 'Neumonía',
                'descripcion': 'Infección aguda del parénquima pulmonar',
                'color': '#e74c3c'
            },
            'bronquitis': {
                'nombre': 'Bronquitis Aguda',
                'descripcion': 'Inflamación de los bronquios de corta duración',
                'color': '#f39c12'
            },
            'epoc': {
                'nombre': 'EPOC',
                'descripcion': 'Enfermedad Pulmonar Obstructiva Crónica',
                'color': '#95a5a6'
            },
            'covid': {
                'nombre': 'COVID-19',
                'descripcion': 'Infección por SARS-CoV-2',
                'color': '#9b59b6'
            }
        }
    
    def obtener_enfermedad(self, codigo):
        """Obtiene información de una enfermedad por su código"""
        return self.enfermedades.get(codigo, None)
    
    def listar_enfermedades(self):
        """Lista todas las enfermedades disponibles"""
        return list(self.enfermedades.keys())
