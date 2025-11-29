import cv2
import os
from deepface import DeepFace
import numpy as np

# ====================
# CONFIGURACIÓN INICIAL
# ====================

# Rutas a los datos y modelos
dataPersonas = r'C:\Users\JoseA\OneDrive\Desktop\Archivos Uni\Inteligencia-Artificial-Ago-Dic\Modulo 4\Reconocimiento Emociones\data\personas'

# Cargar nombres de personas desde las carpetas
personNames = os.listdir(dataPersonas)
print(f"Personas detectadas: {personNames}")

# Cargar modelo LBPH para reconocimiento de personas (tu modelo entrenado)
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.read('modeloPersonasLBPH.xml')

# Detector de rostros Haar Cascade
faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# ====================
# CONFIGURACIÓN DE DEEPFACE
# ====================

# DeepFace usa modelos pre-entrenados:
# - Emociones: 'angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral'
# Modelos disponibles: VGG-Face, Facenet, OpenFace, DeepFace, DeepID, ArcFace

# Traducción de emociones al español
emotion_translation = {
    'angry': 'Enojado',
    'disgust': 'Disgusto',
    'fear': 'Miedo',
    'happy': 'Feliz',
    'sad': 'Triste',
    'surprise': 'Sorpresa',
    'neutral': 'Neutral'
}

# ====================
# INICIAR CÁMARA
# ====================

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
print("\n🎥 Cámara iniciada. Presiona ESC para salir.\n")

frame_count = 0
emotion_result = None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convertir a escala de grises para el detector Haar
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detectar rostros
    faces = faceClassif.detectMultiScale(gray, 1.3, 5)

    # Procesar cada rostro detectado
    for (x, y, w, h) in faces:
        
        # ===========================
        # RECONOCIMIENTO DE PERSONA (LBPH)
        # ===========================
        rostro = gray[y:y+h, x:x+w]
        rostro_resized = cv2.resize(rostro, (150, 150), interpolation=cv2.INTER_CUBIC)
        
        # Predecir persona
        label_p, confidence_p = face_recognizer.predict(rostro_resized)
        persona = personNames[label_p] if confidence_p < 80 else "Desconocido"
        
        # ===========================
        # RECONOCIMIENTO DE EMOCIÓN (DeepFace)
        # ===========================
        # DeepFace analiza cada 10 frames para no ralentizar el video
        if frame_count % 10 == 0:
            try:
                # Recortar el rostro del frame original (BGR)
                face_roi = frame[y:y+h, x:x+w]
                
                # Analizar emoción con DeepFace
                # enforce_detection=False evita errores si no detecta rostro perfectamente
                result = DeepFace.analyze(face_roi, 
                                        actions=['emotion'],
                                        enforce_detection=False,
                                        silent=True)
                
                # Obtener la emoción dominante
                if isinstance(result, list):
                    result = result[0]
                
                dominant_emotion = result['dominant_emotion']
                emotion_scores = result['emotion']
                
                # Guardar resultado para mostrar en frames siguientes
                emotion_result = {
                    'emotion': emotion_translation.get(dominant_emotion, dominant_emotion),
                    'scores': emotion_scores,
                    'confidence': emotion_scores[dominant_emotion]
                }
                
            except Exception as e:
                # Si DeepFace falla, mantener la última emoción detectada
                if emotion_result is None:
                    emotion_result = {'emotion': '???', 'confidence': 0}
        
        # ===========================
        # VISUALIZACIÓN
        # ===========================
        
        # Obtener emoción actual
        emocion = emotion_result['emotion'] if emotion_result else '???'
        conf_emotion = emotion_result['confidence'] if emotion_result else 0
        
        # Texto principal: Persona - Emoción
        texto_principal = f'{persona} - {emocion}'
        
        # Color del rectángulo según emoción
        color = (0, 255, 0)  # Verde por defecto
        if emocion == 'Feliz':
            color = (0, 255, 255)  # Amarillo
        elif emocion == 'Enojado':
            color = (0, 0, 255)  # Rojo
        elif emocion == 'Triste':
            color = (255, 0, 0)  # Azul
        
        # Dibujar rectángulo alrededor del rostro
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        
        # Fondo semitransparente para el texto
        overlay = frame.copy()
        cv2.rectangle(overlay, (x, y-40), (x+w, y), color, -1)
        frame = cv2.addWeighted(overlay, 0.4, frame, 0.6, 0)
        
        # Texto principal
        cv2.putText(frame, texto_principal, (x+5, y-10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)
        
        # Mostrar confianza de la emoción
        texto_conf = f'Conf: {conf_emotion:.1f}%'
        cv2.putText(frame, texto_conf, (x+5, y+h+20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
    
    # ===========================
    # INFO EN PANTALLA
    # ===========================
    
    # Mostrar instrucciones
    cv2.putText(frame, 'Presiona ESC para salir', (10, 30),
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2, cv2.LINE_AA)
    
    # Mostrar FPS aproximado
    cv2.putText(frame, f'Usando: DeepFace + LBPH', (10, frame.shape[0] - 10),
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 1, cv2.LINE_AA)
    
    # Mostrar ventana
    cv2.imshow('Reconocimiento con DeepFace (Red Neuronal)', frame)
    
    # Incrementar contador de frames
    frame_count += 1
    
    # Salir con ESC
    if cv2.waitKey(1) == 27:
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()

print("\n✅ Programa finalizado correctamente.")

