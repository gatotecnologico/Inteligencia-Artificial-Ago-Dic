# Integrantes: Grande Espinoza Victor Ramon, Ana Jasmin Torres.
import pandas as pd
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import numpy as np

# --- 1. Descarga de recursos y configuración ---
nltk.download('punkt')
nltk.download('stopwords')
nltk.data.find('tokenizers/punkt')
nltk.data.find('corpora/stopwords')
    

# Definir las stopwords en español
SPANISH_STOPWORDS = set(stopwords.words('spanish'))

# --- 2. Método para el preprocesamiento de datos (Mejorado) ---
def limpiar_texto(texto):
    """Limpia, tokeniza y elimina stop words."""
    texto = texto.lower() 
    # Eliminar caracteres no alfanuméricos y reemplazarlos por espacio
    texto = re.sub(r'\W', ' ', texto) 
    tokens = word_tokenize(texto) 
    
    # Filtrar stop words y tokens de una sola letra
    tokens = [word for word in tokens if word not in SPANISH_STOPWORDS and len(word) > 1]
    return tokens

# --- 3. Datos de ejemplo y Preprocesamiento ---
data = {'email': ['Gana dinero fácil $$$ desde casa!!!',
                  'Reunión de trabajo a las 3 PM.',
                  'Gana dinero fácil $$$ desde casa!!!',
                  'Haz clic aquí para reclamar tu premio!',
                  'Tu trabajo te espera, aplica ahora',
                  'Recuerda la hora de la reunión'],
        'spam': [1, 0, 1, 1, 1, 0]}
df = pd.DataFrame(data)

# Eliminar correos electrónicos duplicados
df = df.drop_duplicates(subset=['email'])

# Aplicar limpieza y preprocesamiento
df['tokens'] = df['email'].apply(limpiar_texto)

# --- 4. Cálculo de Probabilidades Previas (P(Spam)) ---
num_spam = df['spam'].sum()
total_correos = len(df)
P_spam = num_spam / total_correos
P_no_spam = 1 - P_spam 

# Separar tokens
spam_tokens = [word for tokens in df[df['spam'] == 1]['tokens'] for word in tokens]
no_spam_tokens = [word for tokens in df[df['spam'] == 0]['tokens'] for word in tokens]

# Contar frecuencia de palabras
spam_counts = Counter(spam_tokens)
no_spam_counts = Counter(no_spam_tokens)

# Vocabulario total (para el suavizado de Laplace)
vocabulario_total = set(spam_tokens + no_spam_tokens)
V = len(vocabulario_total)

# Totales de palabras en cada clase
total_spam_words = len(spam_tokens)
total_no_spam_words = len(no_spam_tokens)

# --- 5. Cálculo de Log-Probabilidades (P(Palabra | Clase)) ---
# El suavizado de Laplace se implementa aquí: (Count + 1) / (Total_Words + V)

# Función auxiliar para obtener el Logaritmo de P(Palabra | Clase)
def get_log_prob(word, counts, total_words, V):
    """Calcula log(P(Palabra | Clase)) con suavizado de Laplace."""
    # Frecuencia de la palabra + 1 (suavizado)
    frecuencia = counts.get(word, 0) + 1 
    # Denominador (Total de palabras en la clase + tamaño del vocabulario)
    denominador = total_words + V 
    return np.log(frecuencia / denominador)

# Calcular las log-probabilidades para el vocabulario completo
log_prob_spam_words = {word: get_log_prob(word, spam_counts, total_spam_words, V) for word in vocabulario_total}
log_prob_no_spam_words = {word: get_log_prob(word, no_spam_counts, total_no_spam_words, V) for word in vocabulario_total}


# --- 6. Función de Clasificación (Usando Logaritmos) ---
def clasificar_correo(texto):
    """Clasifica el correo usando Log-Probabilidades para evitar underflow."""
    palabras = limpiar_texto(texto)
    
    # Inicializar el cálculo con el logaritmo de la probabilidad previa
    log_P_spam_score = np.log(P_spam) 
    log_P_no_spam_score = np.log(P_no_spam)
    
    # Log-Probabilidad para palabras no vistas (usando el suavizado de Laplace)
    # log(1 / (Total_Words + V))
    log_prob_desconocida_spam = np.log(1 / (total_spam_words + V))
    log_prob_desconocida_no_spam = np.log(1 / (total_no_spam_words + V))

    for word in palabras:
        # Sumamos los logaritmos de las probabilidades condicionales (P(palabra | Clase))
        log_P_spam_score += log_prob_spam_words.get(word, log_prob_desconocida_spam)
        log_P_no_spam_score += log_prob_no_spam_words.get(word, log_prob_desconocida_no_spam)
    
    # La clasificación se basa en qué score logarítmico es mayor.
    if log_P_spam_score > log_P_no_spam_score:
        return "Spam", log_P_spam_score, log_P_no_spam_score
    else:
        return "No Spam", log_P_spam_score, log_P_no_spam_score


# --- 7. Resultados y Evaluación ---

# Ejemplo de prueba:
nuevo_email = "Gana dinero ahora con esta increíble oferta"
resultado, log_spam, log_nospam = clasificar_correo(nuevo_email)

print(df[['email', 'spam', 'tokens']])
print("--------------------------------------------------")
print(f"Probabilidad previa de Spam (P(Spam)): {P_spam:.2f}")

print("\n--- Ejemplo de Clasificación (Log-Probabilidades) ---")
print(f"Nuevo Correo: '{nuevo_email}'")
print(f"Log Score (Spam): {log_spam:.4f}")
print(f"Log Score (No Spam): {log_nospam:.4f}")
print(f"➡ Clasificación: {resultado}")

# Para obtener la probabilidad real P(Spam | Características) se usa Softmax (o logsumexp)
# Esto es opcional, pero da un resultado más interpretable:
import scipy.special
prob_real_spam = np.exp(log_spam) / (np.exp(log_spam) + np.exp(log_nospam))
print(f"Probabilidad de que sea spam (Softmax): {prob_real_spam:.4f}")

# Evaluación (Nota: La precisión será alta en este pequeño set de entrenamiento)
clasificaciones_predichas = np.array([clasificar_correo(correo)[0] == 'Spam' for correo in df['email']])
etiquetas_reales = df['spam'].values.astype(bool)

from sklearn.metrics import accuracy_score, recall_score, precision_score

print("\n--- Métricas de Evaluación ---")
print(f"Accuracy (Precisión Total): {accuracy_score(etiquetas_reales, clasificaciones_predichas):.4f}")
print(f"Recall (Sensibilidad, detectando Spam): {recall_score(etiquetas_reales, clasificaciones_predichas):.4f}")