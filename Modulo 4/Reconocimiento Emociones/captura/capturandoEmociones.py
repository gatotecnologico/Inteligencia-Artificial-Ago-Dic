import cv2
import os
import imutils


# Nombre de la emoción que se capturará en esta sesión.
# Cambiar este valor manualmente para capturar cada clase.
emotionName = 'Tristeza'

# Ruta donde se guardarán las imágenes capturadas
dataPath = 'C:/Users/Jazva/OneDrive/Escritorio/Inteligencia-Artificial-Ago-Dic/Modulo 4/Reconocimiento Emociones/data/emociones'
emotionsPath = os.path.join(dataPath, emotionName)

# Si la carpeta de esta emoción no existe, se crea
if not os.path.exists(emotionsPath):
    os.makedirs(emotionsPath)
    print('Carpeta creada:', emotionsPath)



# Activamos la webcam (CAP_DSHOW corrige problemas con algunas cámaras en Windows)
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Cargamos el clasificador Haar Cascade para detectar rostros
faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Contador de imágenes capturadas
count = 0
max_images = 300   # Número total de imágenes a capturar por emoción


while True:
    ret, frame = cap.read()
    if not ret:
        break  # Si no se obtiene imagen, salir del bucle
    
    # Redimensionamos el fotograma para mejorar velocidad en tiempo real
    frame = imutils.resize(frame, width=640)

    # Convertimos a escala de grises porque Haar y LBPH trabajan en gris
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    auxFrame = gray.copy()

    # Detección de rostros en el fotograma
    faces = faceClassif.detectMultiScale(gray, 1.1, 4)

    # Procesar cada rostro detectado
    for (x, y, w, h) in faces:

        # Dibujar un rectángulo para visualizar la detección
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Recortar el rostro detectado
        rostro = auxFrame[y:y+h, x:x+w]

        # Redimensionar a 150x150 (tamaño estándar para LBPH)
        rostro = cv2.resize(rostro, (150, 150), interpolation=cv2.INTER_CUBIC)

        # Guardar la imagen en la carpeta correspondiente
        file_path = os.path.join(emotionsPath, f'{emotionName}_{count}.jpg')
        cv2.imwrite(file_path, rostro)
        count += 1

        # Mostrar texto de progreso en pantalla
        cv2.putText(frame,
                    f'Emocion en curso: {emotionName} - Capturando: {count}/{max_images}',
                    (10, 30), 2, 0.7, (255, 255, 0), 1, cv2.LINE_AA)

    # Mostrar la ventana con la cámara
    cv2.imshow('frame', frame)

    # Salir si se presiona ESC o si ya capturamos todas las imágenes
    k = cv2.waitKey(1)
    if k == 27 or count >= max_images:
        break


cap.release()
cv2.destroyAllWindows()

print(f"Captura finalizada: {count} imágenes guardadas en {emotionsPath}")
