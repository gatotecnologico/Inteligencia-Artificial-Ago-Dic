"""
Validaciones de datos del paciente
"""

class Validador:
    @staticmethod
    def validar_edad(edad):
        """Valida que la edad sea válida"""
        if not isinstance(edad, int):
            return False, "La edad debe ser un número entero"
        if edad < 0 or edad > 120:
            return False, "La edad debe estar entre 0 y 120 años"
        return True, ""
    
    @staticmethod
    def validar_paciente(paciente_dict):
        """Valida los datos completos del paciente"""
        errores = []
        
        # Validar edad
        valido, msg = Validador.validar_edad(paciente_dict.get('edad', 0))
        if not valido:
            errores.append(msg)
        
        # Validar que tenga al menos un síntoma
        sintomas = ['sibilancias', 'tos_nocturna', 'tos_productiva', 'tos_seca',
                   'disnea', 'fiebre', 'dolor_toracico', 'fatiga', 'perdida_olfato']
        tiene_sintoma = any(paciente_dict.get(s, False) for s in sintomas)
        
        if not tiene_sintoma:
            errores.append("Debe seleccionar al menos un síntoma")
        
        return len(errores) == 0, errores
