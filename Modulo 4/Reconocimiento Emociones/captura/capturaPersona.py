import cv2
import os
import imutils

# Configuración inicial
# Nombre de la persona a capturar.
# Se debe cambiar cada vez que se registran nuevos individuos.
personName = 'Jasmin'

# Ruta donde se almacenarán las imágenes de esta persona
dataPath = 'C:/Users/Jazva/OneDrive/Escritorio/Inteligencia-Artificial-Ago-Dic/Modulo 4/Reconocimiento Emociones/data/personas'
personPath = os.path.join(dataPath, personName)

# Crear carpeta si no existe (una carpeta por persona)
if not os.path.exists(personPath):
    os.makedirs(personPath)
    print('Carpeta creada:', personPath)


# Inicialización de la cámara y del detector
# Activamos la webcam. CAP_DSHOW mejora compatibilidad en Windows.
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Cargamos el clasificador Haar Cascade para detectar rostros.
faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

count = 0                     # Contador de imágenes capturadas
max_images = 200              # Número de imágenes a capturar por persona


# Bucle principal de captura
while True:
    ret, frame = cap.read()
    if not ret:
        break   # Si no se puede leer la cámara, se termina el ciclo

    # Redimensionar para mejorar velocidad y estabilidad
    frame = imutils.resize(frame, width=640)

    # Convertir a escala de grises (Haar y LBPH trabajan en gris)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detección de rostros
    faces = faceClassif.detectMultiScale(gray, 1.3, 5)

    # Procesar cada rostro detectado
    for (x, y, w, h) in faces:

        # Dibujar un rectángulo para visualización
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Recortar el rostro de la imagen gris
        rostro = gray[y:y+h, x:x+w]

        # Normalizar el tamaño para el modelo de reconocimiento
        rostro = cv2.resize(rostro, (150,150), interpolation=cv2.INTER_CUBIC)

        # Guardar la imagen recortada en la carpeta de la persona
        cv2.imwrite(os.path.join(personPath, f'{personName}_{count}.jpg'), rostro)
        count += 1

        # Mostrar progreso en pantalla
        cv2.putText(frame, f'Fotos: {count}/{max_images}', (10, 20),
                    2, 0.7, (255,255,0), 1, cv2.LINE_AA)

    # Mostrar el video con la detección
    cv2.imshow('Captura Persona', frame)

    # Salir si se presiona ESC (27) o si se llega al total de imágenes
    k = cv2.waitKey(1)
    if k == 27 or count >= max_images:
        break


cap.release()
cv2.destroyAllWindows()
print(f'Captura finalizada: {count} imágenes guardadas en {personPath}')
