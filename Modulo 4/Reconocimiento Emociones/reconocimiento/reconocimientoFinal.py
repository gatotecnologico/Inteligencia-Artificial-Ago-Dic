import cv2
import os

# Rutas
dataPersonas = 'C:/Users/Jazva/OneDrive/Escritorio/Inteligencia-Artificial-Ago-Dic/Modulo 4/Reconocimiento Emociones/data/personas'
dataEmociones = 'C:/Users/Jazva/OneDrive/Escritorio/Inteligencia-Artificial-Ago-Dic/Modulo 4/Reconocimiento Emociones/data/emociones'

# Listas
personNames = os.listdir(dataPersonas)
emotionNames = os.listdir(dataEmociones)

# Modelos
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.read('modeloPersonasLBPH.xml')

emotion_recognizer = cv2.face.LBPHFaceRecognizer_create()
emotion_recognizer.read('modeloLBPH.xml')

# Detector
faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    ret, frame = cap.read()
    if not ret: break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceClassif.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        rostro = gray[y:y+h, x:x+w]
        rostro = cv2.resize(rostro, (150,150), interpolation=cv2.INTER_CUBIC)

        # RECONOCER PERSONA
        label_p, conf_p = face_recognizer.predict(rostro)
        persona = personNames[label_p] if conf_p < 80 else "Desconocido"

        # RECONOCER EMOCIÓN
        label_e, conf_e = emotion_recognizer.predict(rostro)
        emocion = emotionNames[label_e] if conf_e < 90 else "???"

        # MOSTRAR RESULTADO
        texto = f'{persona} - {emocion}'
        cv2.putText(frame, texto, (x, y - 10), 2, 0.7, (0,255,0), 2, cv2.LINE_AA)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)

    cv2.imshow('Reconocimiento Persona + Emoción', frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
