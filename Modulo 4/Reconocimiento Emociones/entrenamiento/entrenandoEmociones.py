import cv2
import os
import numpy as np

# Carga del dataset
# Ruta donde están almacenadas las carpetas de emociones.
# Cada carpeta representa una clase (feliz, triste, enojado, neutral, etc.)
dataPath = 'C:/Users/Jazva/OneDrive/Escritorio/Inteligencia-Artificial-Ago-Dic/Modulo 4/Reconocimiento Emociones/data/emociones'  

# Lista de carpetas (clases) existentes dentro del dataset
EmotionsList = os.listdir(dataPath)
print('Lista de emociones:', EmotionsList)

# Arreglos donde se almacenarán las imágenes y sus etiquetas
labels = []       # Etiqueta numérica por emoción
facesData = []    # Imágenes procesadas
label = 0         # Etiqueta inicial

# Lectura y preprocesamiento de cada imagen del dataset

for nameDir in EmotionsList:
    personPath = dataPath + '/' + nameDir
    print('Leyendo las imágenes de:', personPath)

    # Recorrer todos los archivos dentro de la carpeta de una emoción
    for fileName in os.listdir(personPath):

        # Cargar la imagen directamente en escala de grises
        img = cv2.imread(personPath + '/' + fileName, 0)

        # Redimensionar a 150x150 para estandarizar el tamaño
        img = cv2.resize(img, (150,150))

        # Guardar imagen y etiqueta asociada
        facesData.append(img)
        labels.append(label)

    # Incrementamos la etiqueta para la siguiente emoción
    label += 1

# Convertimos las etiquetas a arreglo NumPy para el entrenamiento
labels = np.array(labels)

# Creación y entrenamiento del modelo LBPH
# Crear el reconocedor LBPH (Local Binary Patterns Histograms)
emotion_recognizer = cv2.face.LBPHFaceRecognizer_create()

print("Entrenando modelo LBPH...")

# Entrenar el modelo con las imágenes preprocesadas y sus etiquetas
emotion_recognizer.train(facesData, labels)

# Guardar el modelo entrenado en un archivo XML
emotion_recognizer.write('modeloLBPH.xml')

print("Modelo guardado: modeloLBPH.xml")
