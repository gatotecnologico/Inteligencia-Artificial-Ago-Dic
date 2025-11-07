# ==================== ARCHIVO: modelos/paciente.py ====================
"""
Modelo de datos del paciente
"""

class Paciente:
    def __init__(self):
        self.edad = 0
        self.sexo = ""
        
        # Síntomas
        self.sibilancias = False
        self.tos_nocturna = False
        self.tos_productiva = False
        self.tos_seca = False
        self.disnea = False
        self.disnea_ejercicio = False
        self.fiebre = False
        self.dolor_toracico = False
        self.fatiga = False
        self.perdida_olfato = False
        
        # Hallazgos físicos
        self.crepitantes = False
        self.ronquidos = False
        self.sat_baja = False
        self.consolidacion = False
        
        # Factores de riesgo
        self.tabaquismo = False
        self.alergias = False
        self.contaminantes = False
        self.infeccion_previa = False
        self.sintomas_cronicos = False
    
    def to_dict(self):
        """Convierte el paciente a diccionario"""
        return {
            'edad': self.edad,
            'sexo': self.sexo,
            'sibilancias': self.sibilancias,
            'tos_nocturna': self.tos_nocturna,
            'tos_productiva': self.tos_productiva,
            'tos_seca': self.tos_seca,
            'disnea': self.disnea,
            'disnea_ejercicio': self.disnea_ejercicio,
            'fiebre': self.fiebre,
            'dolor_toracico': self.dolor_toracico,
            'fatiga': self.fatiga,
            'perdida_olfato': self.perdida_olfato,
            'crepitantes': self.crepitantes,
            'ronquidos': self.ronquidos,
            'sat_baja': self.sat_baja,
            'consolidacion': self.consolidacion,
            'tabaquismo': self.tabaquismo,
            'alergias': self.alergias,
            'contaminantes': self.contaminantes,
            'infeccion_previa': self.infeccion_previa,
            'sintomas_cronicos': self.sintomas_cronicos
        }
    
    def from_dict(self, datos):
        """Carga datos desde un diccionario"""
        for key, value in datos.items():
            if hasattr(self, key):
                setattr(self, key, value)
