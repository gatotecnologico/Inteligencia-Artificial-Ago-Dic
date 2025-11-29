import cv2
import os
from deepface import DeepFace
import numpy as np

# ====================
# CONFIGURACIÓN INICIAL
# ====================

print("🚀 Iniciando sistema de reconocimiento con DeepFace (100% Redes Neuronales)")
print("=" * 70)

# Ruta a la base de datos de rostros conocidos
dataPersonas = r'C:\Users\JoseA\OneDrive\Desktop\Archivos Uni\Inteligencia-Artificial-Ago-Dic\Modulo 4\Reconocimiento Emociones\data\personas'

# Traducción de emociones
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
# MODELOS DISPONIBLES EN DEEPFACE
# ====================
# VGG-Face, Facenet, Facenet512, OpenFace, DeepFace, DeepID, ArcFace, Dlib, SFace
# Facenet512 es excelente en precisión pero más lento
# VGG-Face es un buen balance

MODEL_NAME = "Facenet512"  # Puedes cambiar a: VGG-Face, Facenet, ArcFace, etc.

print(f"📦 Modelo de reconocimiento facial: {MODEL_NAME}")
print(f"📁 Base de datos: {dataPersonas}")

# ====================
# DETECCIÓN DE BACKEND
# ====================
# opencv, ssd, dlib, mtcnn, retinaface, mediapipe, yolov8, yunet, fastmtcnn
DETECTOR_BACKEND = "opencv"  # Más rápido

print(f"🔍 Detector de rostros: {DETECTOR_BACKEND}")
print("=" * 70)

# ====================
# INICIAR CÁMARA
# ====================

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
print("\n🎥 Cámara iniciada. Presiona ESC para salir.\n")

frame_count = 0
last_analysis = None
analysis_interval = 15  # Analizar cada 15 frames (para mejor rendimiento)

# Detector de rostros Haar para preview rápido
faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceClassif.detectMultiScale(gray, 1.3, 5)

    # ===========================
    # ANÁLISIS CON DEEPFACE
    # ===========================
    
    # Analizar cada cierto número de frames
    if frame_count % analysis_interval == 0 and len(faces) > 0:
        try:
            print(f"📊 Analizando frame {frame_count}...")
            
            # ===========================
            # RECONOCIMIENTO FACIAL + EMOCIÓN EN UNA SOLA LLAMADA
            # ===========================
            
            results = DeepFace.analyze(frame, 
                                      actions=['emotion', 'age', 'gender'],
                                      enforce_detection=False,
                                      detector_backend=DETECTOR_BACKEND,
                                      silent=True)
            
            # Si hay múltiples rostros, tomar el primero
            if isinstance(results, list):
                results = results[0] if len(results) > 0 else None
            
            if results:
                # Extraer información de emoción
                dominant_emotion = results['dominant_emotion']
                emotion_scores = results['emotion']
                
                # Extraer información demográfica
                age = results.get('age', 'N/A')
                gender = results.get('dominant_gender', 'N/A')
                
                # ===========================
                # VERIFICACIÓN DE IDENTIDAD
                # ===========================
                
                # Intentar reconocer la persona comparando con la base de datos
                persona_identificada = "Desconocido"
                max_similarity = 0
                
                try:
                    # DeepFace.find busca rostros similares en la base de datos
                    # Esto puede ser lento, así que lo hacemos solo cada cierto tiempo
                    if frame_count % (analysis_interval * 3) == 0:
                        df = DeepFace.find(img_path=frame,
                                          db_path=dataPersonas,
                                          model_name=MODEL_NAME,
                                          enforce_detection=False,
                                          silent=True)
                        
                        if isinstance(df, list) and len(df) > 0:
                            df = df[0]
                        
                        if not df.empty:
                            # Obtener el mejor match
                            best_match = df.iloc[0]
                            identity_path = best_match['identity']
                            
                            # Extraer nombre de la carpeta
                            persona_identificada = os.path.basename(os.path.dirname(identity_path))
                            
                            # Distancia (menor = más similar)
                            distance = best_match.get('distance', 1.0)
                            max_similarity = max(0, (1 - distance) * 100)
                            
                            print(f"✅ Persona identificada: {persona_identificada} (similaridad: {max_similarity:.1f}%)")
                        else:
                            persona_identificada = "Desconocido"
                            
                except Exception as e:
                    # Si falla el reconocimiento, mantener como desconocido
                    persona_identificada = "Desconocido"
                    print(f"⚠️  No se pudo identificar: {str(e)[:50]}")
                
                # Guardar análisis
                last_analysis = {
                    'persona': persona_identificada,
                    'emotion': emotion_translation.get(dominant_emotion, dominant_emotion),
                    'emotion_raw': dominant_emotion,
                    'confidence': emotion_scores[dominant_emotion],
                    'age': age,
                    'gender': gender,
                    'similarity': max_similarity,
                    'region': results.get('region', faces[0] if len(faces) > 0 else None)
                }
                
        except Exception as e:
            print(f"❌ Error en análisis: {str(e)[:100]}")
            # Mantener último análisis válido
    
    # ===========================
    # VISUALIZACIÓN
    # ===========================
    
    if last_analysis:
        # Usar región detectada por DeepFace o Haar
        if last_analysis['region']:
            if isinstance(last_analysis['region'], dict):
                x = last_analysis['region'].get('x', faces[0][0] if len(faces) > 0 else 0)
                y = last_analysis['region'].get('y', faces[0][1] if len(faces) > 0 else 0)
                w = last_analysis['region'].get('w', faces[0][2] if len(faces) > 0 else 100)
                h = last_analysis['region'].get('h', faces[0][3] if len(faces) > 0 else 100)
            else:
                x, y, w, h = faces[0] if len(faces) > 0 else (50, 50, 100, 100)
        else:
            x, y, w, h = faces[0] if len(faces) > 0 else (50, 50, 100, 100)
        
        # Información a mostrar
        persona = last_analysis['persona']
        emocion = last_analysis['emotion']
        confidence = last_analysis['confidence']
        age = last_analysis['age']
        gender = last_analysis['gender']
        
        # Color según emoción
        color_map = {
            'Feliz': (0, 255, 255),
            'Enojado': (0, 0, 255),
            'Triste': (255, 0, 0),
            'Neutral': (0, 255, 0),
            'Sorpresa': (255, 255, 0),
            'Miedo': (128, 0, 128),
            'Disgusto': (0, 128, 128)
        }
        color = color_map.get(emocion, (0, 255, 0))
        
        # Dibujar rectángulo
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 3)
        
        # Panel de información
        panel_height = 120
        panel_y = max(0, y - panel_height)
        
        # Fondo del panel
        overlay = frame.copy()
        cv2.rectangle(overlay, (x, panel_y), (x+w, y), (0, 0, 0), -1)
        frame = cv2.addWeighted(overlay, 0.6, frame, 0.4, 0)
        
        # Textos en el panel
        text_y = panel_y + 20
        cv2.putText(frame, f'Persona: {persona}', (x+5, text_y),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        
        text_y += 25
        cv2.putText(frame, f'Emocion: {emocion} ({confidence:.0f}%)', (x+5, text_y),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2, cv2.LINE_AA)
        
        text_y += 25
        cv2.putText(frame, f'Edad: ~{age} años', (x+5, text_y),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1, cv2.LINE_AA)
        
        text_y += 25
        cv2.putText(frame, f'Genero: {gender}', (x+5, text_y),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1, cv2.LINE_AA)
    
    # Info general
    cv2.putText(frame, f'DeepFace - Modelo: {MODEL_NAME}', (10, 30),
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2, cv2.LINE_AA)
    
    cv2.putText(frame, 'ESC = Salir', (10, frame.shape[0] - 10),
               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
    
    # Mostrar ventana
    cv2.imshow('Reconocimiento Avanzado - DeepFace (CNN)', frame)
    
    frame_count += 1
    
    # Salir
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()

print("\n✅ Sistema finalizado correctamente.")
print("=" * 70)

