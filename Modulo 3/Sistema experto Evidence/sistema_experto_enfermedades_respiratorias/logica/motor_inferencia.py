"""
Motor de Inferencia - Reglas y lógica de diagnóstico
"""

from typing import Dict, List

class MotorInferencia:
    def __init__(self, base_conocimientos):
        self.bc = base_conocimientos
    
    def combinar_fc(self, fc1: float, fc2: float) -> float:
        """
        Combina factores de certeza usando la fórmula:
        FC = FC1 + FC2 × (1 - FC1)

                """
        return fc1 + fc2 * (1 - fc1)
    
    def regla_asma(self, paciente: Dict) -> Dict:
        """REGLA 1: Diagnóstico de Asma"""
        fc = 0
        reglas = []
        
        # directa 
        if (paciente.get('sibilancias') and 
            paciente.get('tos_nocturna') and 
            paciente.get('alergias')):
            fc = 0.90
            reglas.append("Regla 1: Sibilancias + Tos nocturna + Antecedentes alergia (FC: 0.90)")
        
        # por asociación
        if paciente.get('sibilancias'):
            fc = self.combinar_fc(fc, 0.70)
            reglas.append(" Regla 6: Presencia de sibilancias (FC: 0.70)")
        
        if paciente.get('disnea_ejercicio'):
            fc = self.combinar_fc(fc, 0.60)
            reglas.append(" Regla 6: Disnea con ejercicio (FC: 0.60)")
        
        recomendaciones = [
            "- Realizar espirometría",
            "- Pruebas de alergia",
            "- Considerar tratamiento con broncodilatadores",
            "- Prueba de función pulmonar"
        ]
        
        return {'fc': fc, 'reglas': reglas, 'recomendaciones': recomendaciones}
    
    def regla_neumonia(self, paciente: Dict) -> Dict:
        """REGLA 2: Diagnóstico de Neumonía"""
        fc = 0
        reglas = []
        
        if (paciente.get('fiebre') and 
            paciente.get('tos_productiva') and 
            paciente.get('crepitantes') and 
            paciente.get('disnea')):
            fc = 0.85
            reglas.append(" Regla 2: Fiebre + Tos productiva + Crepitantes + Disnea (FC: 0.85)")
        
        if paciente.get('fiebre'):
            fc = self.combinar_fc(fc, 0.60)
            reglas.append(" Regla 7: Fiebre alta presente (FC: 0.60)")
        
        if paciente.get('dolor_toracico'):
            fc = self.combinar_fc(fc, 0.70)
            reglas.append(" Regla 7: Dolor torácico al respirar (FC: 0.70)")
        
        if paciente.get('sat_baja'):
            fc = self.combinar_fc(fc, 0.80)
            reglas.append(" Regla 7: Saturación de oxígeno baja (FC: 0.80)")
        
        recomendaciones = [
            "- Radiografía de tórax URGENTE",
            "- Análisis de sangre (leucocitos, PCR)",
            "- Cultivo de esputo",
            "- Considerar hospitalización si severidad alta",
            "- Antibióticos empíricos según guías clínicas"
        ]
        
        return {'fc': fc, 'reglas': reglas, 'recomendaciones': recomendaciones}
    
    def regla_bronquitis(self, paciente: Dict) -> Dict:
        """REGLA 3: Diagnóstico de Bronquitis Aguda"""
        fc = 0
        reglas = []
        
        if ((paciente.get('tos_productiva') or paciente.get('tos_seca')) and
            paciente.get('infeccion_previa') and
            not paciente.get('sintomas_cronicos') and
            not paciente.get('consolidacion')):
            fc = 0.75
            reglas.append(" Regla 3: Tos + Infección previa + Síntomas < 3 semanas (FC: 0.75)")
        
        recomendaciones = [
            "- Manejo sintomático",
            "- Hidratación abundante",
            "- Reposo relativo",
            "- Control en 7-10 días"
        ]
        
        return {'fc': fc, 'reglas': reglas, 'recomendaciones': recomendaciones}
    
    def regla_epoc(self, paciente: Dict) -> Dict:
        """REGLA 4: Diagnóstico de EPOC"""
        fc = 0
        reglas = []
        
        if (paciente.get('disnea') and 
            paciente.get('tabaquismo') and
            (paciente.get('tos_productiva') or paciente.get('sintomas_cronicos')) and
            paciente.get('edad', 0) > 40):
            fc = 0.88
            reglas.append(" Regla 4: Disnea + Tabaquismo + Tos crónica + Edad>40 (FC: 0.88)")
        
        if paciente.get('tabaquismo') and paciente.get('sintomas_cronicos'):
            fc = self.combinar_fc(fc, 0.70)
            reglas.append(" Regla 8,13: Tabaquismo + Síntomas crónicos (FC: 0.70)")
        
        recomendaciones = [
            "- Espirometría con broncodilatador",
            "- Radiografía de tórax",
            "- Cesación tabáquica URGENTE",
            "- Tratamiento con broncodilatadores"
        ]
        
        return {'fc': fc, 'reglas': reglas, 'recomendaciones': recomendaciones}
    
    def regla_covid(self, paciente: Dict) -> Dict:
        """REGLA 5: Diagnóstico de COVID-19"""
        fc = 0
        reglas = []
        
        if (paciente.get('fiebre') and 
            paciente.get('tos_seca') and
            paciente.get('perdida_olfato') and 
            paciente.get('fatiga')):
            fc = 0.82
            reglas.append(" Regla 5: Fiebre + Tos seca + Pérdida olfato + Fatiga (FC: 0.82)")
        
        recomendaciones = [
            "- Test PCR o antígeno para SARS-CoV-2",
            "- Aislamiento inmediato",
            "- Monitoreo de saturación de oxígeno"
        ]
        
        return {'fc': fc, 'reglas': reglas, 'recomendaciones': recomendaciones}
    
    def aplicar_regla_exclusion(self, diagnosticos: List[Dict], paciente: Dict):
        """REGLA 9: Exclusión de neumonía sin fiebre ni crepitantes"""
        if not paciente.get('fiebre') and not paciente.get('crepitantes'):
            for d in diagnosticos:
                if d['enfermedad'] == 'neumonia':
                    d['certeza'] *= 0.3
                    d['reglas'].append("Regla 9: Certeza reducida (sin fiebre/crepitantes)")
    
    def diagnosticar(self, paciente: Dict) -> List[Dict]:
        """
        Ejecuta el motor de inferencia con encadenamiento hacia adelante
        """
        diagnosticos = []
        
        # aplicar todas las reglas
        reglas_a_aplicar = [
            ('asma', self.regla_asma),
            ('neumonia', self.regla_neumonia),
            ('bronquitis', self.regla_bronquitis),
            ('epoc', self.regla_epoc),
            ('covid', self.regla_covid)
        ]
        
        for enfermedad, regla_func in reglas_a_aplicar:
            resultado = regla_func(paciente)
            if resultado['fc'] > 0:
                diagnosticos.append({
                    'enfermedad': enfermedad,
                    'certeza': resultado['fc'],
                    'reglas': resultado['reglas'],
                    'recomendaciones': resultado['recomendaciones']
                })
        
        # aplicar reglas de exclusión
        self.aplicar_regla_exclusion(diagnosticos, paciente)
        
        # ordenar por certeza descendente
        diagnosticos.sort(key=lambda x: x['certeza'], reverse=True)
        
        return diagnosticos