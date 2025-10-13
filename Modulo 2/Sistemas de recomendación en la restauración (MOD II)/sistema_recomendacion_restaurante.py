import pandas as pd
from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

class RecomendadorRestauranteBayesiano:
    # --- 1. CONOCIMIENTO DEL DOMINIO (Estructuras de Datos) ---

    PLATOS = {
        "Hamburguesa Clasica": {
            "ingredientes": ["Carne", "Pan", "Queso", "Lechuga"],
            "sabor": "Salado"
        },
        "Ensalada Vegana": {
            "ingredientes": ["Lechuga", "Garbanzos", "Aguacate"],
            "sabor": "Fresco"
        },
        "Tarta de Chocolate": {
            "ingredientes": ["Cacao", "Huevo", "Harina", "Crema"],
            "sabor": "Dulce"
        },
        "Ravioles de Queso": {
            "ingredientes": ["Pasta", "Queso", "Huevo", "Mantequilla"],
            "sabor": "Salado"
        },
        "Curry de Garbanzos": {
            "ingredientes": ["Garbanzos", "Arroz", "Especias_Curry"],
            "sabor": "Picante"
        }
    }

    RESTRICCIONES_DIETETICAS = {
        "Ninguna": [],
        "Vegetariano": ["Carne"],
        "Vegano": ["Carne", "Huevo", "Queso", "Crema", "Mantequilla"],
        "Alergia_Gluten": ["Pan", "Harina", "Pasta"],
        "Alergia_Lacteos": ["Queso", "Crema", "Mantequilla"]
    }

    # Estado de disponibilidad inicial (puede ser modificado dinámicamente)
    DISPONIBILIDAD = {
        "Carne": "Alto",
        "Pan": "Alto",
        "Queso": "Alto",
        "Garbanzos": "Alto",
        "Cacao": "Alto",
        "Huevo": "Alto",
        "Harina": "Alto",
        "Crema": "Alto",
        "Pasta": "Alto",
        "Mantequilla": "Alto",
        "Arroz": "Alto",
        "Especias_Curry": "Alto",
    }

    def __init__(self):
        self.modelo_bayesian = self._setup_bayesian_model()
        self.inferencia_engine = VariableElimination(self.modelo_bayesian)

    # --- 2. DISEÑO E IMPLEMENTACIÓN DEL SISTEMA (Red Bayesiana) ---

    def _setup_bayesian_model(self):        
        # Estados: 0 = No / Fallida; 1 = Sí / Cumplida (para todas las variables)
        
        modelo_bayesian = DiscreteBayesianNetwork([
            # La Probabilidad de Recomendación es influenciada por las 3 variables de entrada
            ('Restriccion_Cumplida', 'Probabilidad_Recomendacion'),
            ('Preferencia_Alineada', 'Probabilidad_Recomendacion'),
            ('Disponibilidad_Plato', 'Probabilidad_Recomendacion')
        ])

        # CPTs simples: Probabilidades a priori
        
        # P(Restriccion_Cumplida)
        cpd_r = TabularCPD(variable='Restriccion_Cumplida', variable_card=2, values=[[0.05], [0.95]], 
                           state_names={'Restriccion_Cumplida': [0, 1]})

        # P(Preferencia_Alineada)
        cpd_p = TabularCPD(variable='Preferencia_Alineada', variable_card=2, values=[[0.3], [0.7]], 
                           state_names={'Preferencia_Alineada': [0, 1]})

        # P(Disponibilidad_Plato)
        cpd_d = TabularCPD(variable='Disponibilidad_Plato', variable_card=2, values=[[0.2], [0.8]], 
                           state_names={'Disponibilidad_Plato': [0, 1]})

        # P(Recomendacion | R, P, D) - CPT Clave (2x2x2 = 8 combinaciones)
        # Orden de evidencia (columnas): [R=0, P=0, D=0], [R=1, P=0, D=0], ..., [R=1, P=1, D=1]
        
        cpd_rec = TabularCPD(
            variable='Probabilidad_Recomendacion', variable_card=2,
            values=[
                # P(Recomendacion = No)
                [0.95, 0.90, 0.80, 0.70,  # D=0 (Baja disponibilidad)
                 0.80, 0.60, 0.40, 0.10], # D=1 (Alta disponibilidad)
                # P(Recomendacion = Sí)
                [0.05, 0.10, 0.20, 0.30, 
                 0.20, 0.40, 0.60, 0.90]  
            ],
            evidence=['Restriccion_Cumplida', 'Preferencia_Alineada', 'Disponibilidad_Plato'],
            evidence_card=[2, 2, 2],
            state_names={'Probabilidad_Recomendacion': [0, 1], 'Restriccion_Cumplida': [0, 1],
                         'Preferencia_Alineada': [0, 1], 'Disponibilidad_Plato': [0, 1]}
        )

        modelo_bayesian.add_cpds(cpd_r, cpd_p, cpd_d, cpd_rec)
        
        if not modelo_bayesian.check_model():
            raise ValueError("El modelo Bayesiano es inválido. Revisar CPTs.")

        return modelo_bayesian

    def _evaluar_condiciones_plato(self, plato_nombre, restriccion_cliente):
        """
        Evalúa las condiciones deterministas para la Restricción (R) y Disponibilidad (D).
        """
        plato = self.PLATOS.get(plato_nombre)
        
        # 1. R (Restricción Cumplida): 1 = Sí (Seguro), 0 = No (Inseguro)
        es_seguro = 1 
        ingredientes_prohibidos = self.RESTRICCIONES_DIETETICAS.get(restriccion_cliente, [])
        for ingrediente in plato["ingredientes"]:
            if ingrediente in ingredientes_prohibidos:
                es_seguro = 0 
                break

        # 2. D (Disponibilidad Plato): 1 = Sí (Disponible), 0 = No (Agotado)
        es_disponible = 1 
        for ingrediente in plato["ingredientes"]:
            if self.DISPONIBILIDAD.get(ingrediente, "Alto") == "Bajo":
                es_disponible = 0 
                break
                
        return es_seguro, es_disponible

    def evaluar_plato_probabilistico(self, plato_nombre, restriccion_cliente, preferencia_cliente):

        plato = self.PLATOS.get(plato_nombre)
        if not plato:
            return 0.0, "Plato no encontrado."
            
        es_seguro, es_disponible = self._evaluar_condiciones_plato(plato_nombre, restriccion_cliente)

        # P (Preferencia Alineada): 1 = Sí (Coincide), 0 = No (No coincide)
        es_alineado = 1 if plato["sabor"] == preferencia_cliente else 0
        
        # Inferencia Probabilística (Variable Elimination)
        evidencia = {
            'Restriccion_Cumplida': es_seguro,
            'Preferencia_Alineada': es_alineado,
            'Disponibilidad_Plato': es_disponible
        }

        prob_recomendacion = self.inferencia_engine.query(
            variables=['Probabilidad_Recomendacion'],
            evidence=evidencia
        )
        
        # P(Recomendacion = Sí) es el valor asociado al estado 1
        prob_si = prob_recomendacion.values[1] 
        
        estado_detalle = f"R:{es_seguro}, P:{es_alineado}, D:{es_disponible}"
        return prob_si, estado_detalle

    def generar_top_recomendaciones(self, restriccion_cliente, preferencia_cliente, top_n=3):
        resultados = []
        
        for nombre_plato in self.PLATOS:
            prob, estado_detalle = self.evaluar_plato_probabilistico(
                nombre_plato, restriccion_cliente, preferencia_cliente
            )
            resultados.append({
                "Plato": nombre_plato,
                "Probabilidad": prob,
                "Detalle_Estado": estado_detalle
            })
            
        df_resultados = pd.DataFrame(resultados).sort_values(by="Probabilidad", ascending=False)
        return df_resultados.head(top_n)

    # --- 3. INCORPORAR RAZONAMIENTO NO MONÓTONO ---
    def actualizar_disponibilidad(self, ingrediente: str, estado: str):

        if estado not in ["Alto", "Bajo"]:
            print("ERROR: El estado debe ser 'Alto' o 'Bajo'.")
            return

        if ingrediente in self.DISPONIBILIDAD:
            self.DISPONIBILIDAD[ingrediente] = estado
            print(f"DEBUG: Disponibilidad de '{ingrediente}' actualizada a '{estado}'.")
        else:
            print(f"ADVERTENCIA: Ingrediente '{ingrediente}' no rastreado.")

# --- 4. PRUEBAS FUNCIONALES ---

if __name__ == "__main__":
    # 1. Inicializar el sistema
    recomendador = RecomendadorRestauranteBayesiano()

    print("====================================================")
    print("SISTEMA DE RECOMENDACIÓN EN RESTAURACIÓN (MOD II)")
    print("====================================================")
    
    # ----------------------------------------------------
    # PRUEBA A: ESCENARIO IDEAL (Referencia)
    # ----------------------------------------------------
    print("\n--- PRUEBA A: Cliente Sin Restricciones, Preferencia SALADO ---")
    
    restriccion_A = "Ninguna"
    preferencia_A = "Salado"
    
    top_rec_A = recomendador.generar_top_recomendaciones(restriccion_A, preferencia_A, top_n=3)
    print(f"Restricción: '{restriccion_A}', Preferencia: '{preferencia_A}'")
    print(top_rec_A.to_string(index=False))
    # Expectativa: Ravioles y Hamburguesa deben tener alta probabilidad (R=1, P=1, D=1 => ~0.90)

    # ----------------------------------------------------
    # PRUEBA B: RAZONAMIENTO MONÓTONO (Restricción Falla)
    # ----------------------------------------------------
    print("\n--- PRUEBA B: Cliente VEGANO, Preferencia FRESCO ---")
    restriccion_B = "Vegano"
    preferencia_B = "Fresco"
    
    top_rec_B = recomendador.generar_top_recomendaciones(restriccion_B, preferencia_B, top_n=3)
    print(f"Restricción: '{restriccion_B}', Preferencia: '{preferencia_B}'")
    print(top_rec_B.to_string(index=False))
    # Expectativa: Hamburguesa, Ravioles y Tarta caen a baja probabilidad (R=0).
    # Ensalada Vegana (R=1, P=1, D=1) sube al primer lugar (~0.90).

    # ----------------------------------------------------
    # PRUEBA C: RAZONAMIENTO NO MONÓTONO (Disponibilidad Dinámica)
    # ----------------------------------------------------
    print("\n--- PRUEBA C: DEMOSTRACIÓN NO MONÓTONA (Mantequilla Agotada) ---")

    # 1. Estado inicial de Ravioles (Debería ser alto: ~0.90)
    prob_inicial, _ = recomendador.evaluar_plato_probabilistico("Ravioles de Queso", restriccion_A, preferencia_A)
    print(f"Prob. inicial de Ravioles (antes de agotarse): {prob_inicial:.4f}")
    
    # 2. **CAMBIO DINÁMICO (NO MONÓTONO)**: La mantequilla se agota.
    recomendador.actualizar_disponibilidad("Mantequilla", "Bajo")
    
    # 3. Nuevo cálculo para el mismo cliente A
    print("\nVolviendo a recomendar para el cliente A ('Ninguna', 'Salado'):")
    top_rec_C = recomendador.generar_top_recomendaciones(restriccion_A, preferencia_A, top_n=3)
    print(f"Restricción: '{restriccion_A}', Preferencia: '{preferencia_A}' (¡Mantequilla agotada!)")
    print(top_rec_C.to_string(index=False))

    # El plato "Ravioles de Queso" ahora tiene D=0, lo que provoca que su probabilidad caiga de 0.90 a 0.30/0.40,
    # siendo superado por platos que sí están 100% disponibles. **El sistema ha revisado su creencia (probabilidad)**
    # debido a la nueva evidencia (falta de mantequilla).