import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox

# --- 1. DATOS AMPLIADOS ---

def setup_recommender():
    """Prepara los datos y calcula la matriz de similitud de ítems."""
    data_super_ampliada = {
        'Usuario': ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank', 'Grace', 'Heidi'],
        'Star Wars': [5, 4, np.nan, 4, 3, 5, 4, 3],
        'Pulp Fiction': [4, 5, 5, np.nan, 4, 4, 5, 5],
        'Inception': [4, np.nan, 4, 5, 5, 3, np.nan, 4],
        'Titanic': [1, 2, 1, 3, np.nan, 2, 1, 2],
        'The Matrix': [5, 4, 5, 3, 5, 4, 5, 3],
        'Amelie': [np.nan, 3, 5, 1, 2, 5, 4, np.nan],
        'Avatar': [3, 4, np.nan, 5, 4, 3, 5, 4],
        'Parasite': [5, 5, 4, 3, 5, 4, 5, 5],
        'Forrest Gump': [5, np.nan, 4, 4, 5, 5, 4, 4],
        'The Lion King': [2, 3, np.nan, 2, 1, 3, np.nan, 3],
        'Interstellar': [4, 5, 5, 4, 5, 4, 5, 4],
        'Spirited Away': [5, 4, 5, np.nan, 3, np.nan, 4, 5],
        'Toy Story': [3, 3, 4, 3, 2, 4, 3, np.nan],
        'Gladiator': [5, 4, np.nan, 5, 4, 5, 4, 5],
        'La La Land': [3, np.nan, 4, 2, 3, 3, np.nan, 4]
    }

    df_ratings = pd.DataFrame(data_super_ampliada).set_index('Usuario')
    
    # Transponer y preparar para similitud de ítems
    df_ratings_T = df_ratings.T
    item_ratings = df_ratings_T.fillna(0)
    
    # Calcular la Matriz de Similitud del Coseno entre Películas
    item_similarity = cosine_similarity(item_ratings)
    df_item_similarity = pd.DataFrame(item_similarity, 
                                      index=df_ratings_T.index, 
                                      columns=df_ratings_T.index)
    
    return df_ratings, df_item_similarity, list(df_ratings.index)

def recomendar_por_items(usuario_target, df_ratings, df_item_similarity, top_n=3):
    """Lógica de recomendación basada en la similitud de ítems."""
    ratings_del_usuario = df_ratings.loc[usuario_target].dropna()
    predicciones = {}
    peliculas_no_vistas = df_ratings.columns[df_ratings.loc[usuario_target].isna()]
    
    for pelicula_no_vista in peliculas_no_vistas:
        # Solo consideramos películas que el usuario ha valorado
        # para calcular la similitud con la película no vista.
        
        # Filtramos similitudes para incluir solo películas que el usuario ha calificado
        similitudes_con_vistas = df_item_similarity[pelicula_no_vista].loc[ratings_del_usuario.index]
        
        # Eliminamos cualquier similitud que sea NaN (si una película vista no tuviera similitud con la no vista, aunque no debería pasar con fillna(0))
        similitudes_con_vistas = similitudes_con_vistas.dropna()
        
        if not similitudes_con_vistas.empty:
            # Numerador: Suma de (Similitud * Puntuación del Usuario)
            numerador = np.sum(similitudes_con_vistas * ratings_del_usuario[similitudes_con_vistas.index])
            
            # Denominador: Suma de las Similitudes (solo las positivas para evitar división por cero o sumar similitudes negativas que no tienen sentido aquí)
            denominador = np.sum(np.abs(similitudes_con_vistas)) # Usamos abs para considerar el 'peso' de la similitud
            
            if denominador > 0:
                prediccion = numerador / denominador
                predicciones[pelicula_no_vista] = prediccion
            
    df_predicciones = pd.Series(predicciones).sort_values(ascending=False).head(top_n)
    return df_predicciones

# Inicializar los datos del recomendador
df_ratings, df_item_similarity, lista_usuarios = setup_recommender()


# --- 2. INTERFAZ GRÁFICA (TKINTER) ---

def mostrar_recomendaciones():
    """Función que se llama al presionar el botón."""
    usuario_seleccionado = user_var.get()
    
    if not usuario_seleccionado:
        messagebox.showerror("Error", "Por favor, selecciona un usuario.")
        return

    # Ejecutar la lógica de recomendación
    recomendaciones = recomendar_por_items(usuario_seleccionado, df_ratings, df_item_similarity, top_n=3)
    
    # Limpiar el área de resultados anterior
    results_text.set("")
    
    if recomendaciones.empty:
        results_text.set(f"No hay suficientes datos para {usuario_seleccionado} o no hay películas no vistas que recomendar.")
    else:
        # Formatear el resultado
        resultado_str = f"Recomendaciones para {usuario_seleccionado}:\n"
        for pelicula, score in recomendaciones.items():
            resultado_str += f"- {pelicula} (Score predicho: {score:.2f})\n"
        
        results_text.set(resultado_str)

# Configuración principal de la ventana
root = tk.Tk()
root.title("🎬 Sistema de Recomendación de Películas")
root.geometry("500x350") # Ajustado el tamaño de la ventana
root.resizable(False, False)

# Variables de control
user_var = tk.StringVar(root)
results_text = tk.StringVar(root)

# 1. Título y Etiqueta
ttk.Label(root, text="Selecciona un Usuario:", font=('Helvetica', 12, 'bold')).pack(pady=10)

# 2. Desplegable (ComboBox) de Usuarios
user_dropdown = ttk.Combobox(root, textvariable=user_var, values=lista_usuarios, state='readonly')
user_dropdown.pack(pady=5)
user_dropdown.current(0) # Selecciona el primer usuario por defecto

# 3. Botón para generar recomendaciones
ttk.Button(root, text="Generar Recomendaciones", command=mostrar_recomendaciones).pack(pady=15)

# 4. Área de Resultados
ttk.Label(root, text="--- Resultados ---", font=('Helvetica', 10)).pack()
ttk.Label(root, textvariable=results_text, justify=tk.LEFT, font=('Courier', 10)).pack(padx=20, pady=10)

# Iniciar el bucle principal de la GUI
root.mainloop()