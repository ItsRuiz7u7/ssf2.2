import cv2
import face_recognition
import mediapipe as mp
import mysql.connector
from mysql.connector import Error
import numpy as np
import matplotlib.pyplot as plt

# Conéctate a la base de datos en phpMyAdmin
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="J0n4than1234",
        database="ayuda"
    )

    cursor = db.cursor()

except Error as e:
    print("Error al conectar a la base de datos:", e)
    exit()

# Carga las características faciales y nombres de la base de datos
cursor.execute("SELECT usuarios, imagen, face_encoding FROM users")
db_data = cursor.fetchall()

known_names = []
known_face_encodings = []

for name, image_data, encoding_data in db_data:
    known_names.append(name)
    
    # Utiliza numpy para decodificar los datos de imagen
    nparr = np.frombuffer(image_data, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Decodifica los datos de características faciales almacenados en la base de datos
    encoding_array = np.frombuffer(encoding_data, dtype=np.float64)
    face_encoding = encoding_array.reshape((128,))

    known_face_encodings.append(face_encoding)

# Inicia la cámara
cap = cv2.VideoCapture(0)

# Crea un objeto de detección de rostros de Mediapipe
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

# ...

with mp_face_detection.FaceDetection(min_detection_confidence=0.5) as face_detection:
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detecta los rostros en tiempo real utilizando Mediapipe
        results = face_detection.process(frame)
        if results.detections:
            for detection in results.detections:
                # Verifica si hay detecciones de rostros
                if detection.location_data:
                    bboxC = detection.location_data.relative_bounding_box
                    ih, iw, _ = frame.shape
                    x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)
                    face_image = frame[y:y+h, x:x+w]
                    
                    # Calcula las características faciales para la imagen de rostro actual
                    face_encodings = face_recognition.face_encodings(face_image)

                    if len(face_encodings) > 0:
                        face_encoding = face_encodings[0]
                    
                        # Compara las características faciales con las de la base de datos
                        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                        
                        name = "Desconocido"
                        if True in matches:
                            matched_index = matches.index(True)
                            name = known_names[matched_index]
                        
                        # Dibuja un rectángulo y muestra el nombre del usuario en la imagen
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        cv2.putText(frame, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # Muestra la imagen con los rostros detectados utilizando Matplotlib
        plt.imshow(frame)
        plt.show()

        # Sal del script si se presiona la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Libera los recursos utilizados por Mediapipe y OpenCV
cap.release()
cv2.destroyAllWindows()