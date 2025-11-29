import cv2
import os
import numpy as np

# Carga del dataset de personas

# Ruta donde se encuentran las carpetas de cada persona.
# Cada carpeta representa una clase distinta (un individuo).
dataPath = 'C:/Users/Jazva/OneDrive/Escritorio/Inteligencia-Artificial-Ago-Dic/Modulo 4/Reconocimiento Emociones/data/personas'

# Listamos todas las carpetas detectadas dentro del dataset
personsList = os.listdir(dataPath)
print('Personas detectadas:', personsList)

# Listas donde se almacenarán imágenes y etiquetas
labels = []       # Etiquetas numéricas para cada persona
facesData = []    # Imágenes de rostros preprocesados
label = 0         # Etiqueta inicial

# Lectura y preprocesamiento de imágenes

for nameDir in personsList:
    personPath = os.path.join(dataPath, nameDir)
    print('Leyendo imágenes de:', personPath)

    # Recorrer todas las imágenes dentro de la carpeta de la persona
    for fileName in os.listdir(personPath):
        imgPath = os.path.join(personPath, fileName)

        # Cargar la imagen en escala de grises
        img = cv2.imread(imgPath, 0)

        # Redimensionar a tamaño estándar para el modelo LBPH
        img = cv2.resize(img, (150,150))

        # Guardar imagen preprocesada y etiqueta asociada
        facesData.append(img)
        labels.append(label)

    # Se incrementa la etiqueta para la siguiente persona (siguiente clase)
    label += 1

# Convertimos las etiquetas a un arreglo NumPy
labels = np.array(labels)

# Entrenamiento del modelo LBPH

print("Entrenando modelo facial LBPH...")

# Crear el reconocedor LBPH para identificar personas
face_recognizer = cv2.face.LBPHFaceRecognizer_create()

# Entrenar el modelo con las imágenes y etiquetas cargadas
face_recognizer.train(facesData, labels)

# Guardar el modelo entrenado en un archivo XML
face_recognizer.write('modeloPersonasLBPH.xml')

print("Modelo guardado: modeloPersonasLBPH.xml")
