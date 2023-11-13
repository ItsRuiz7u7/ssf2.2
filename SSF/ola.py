import cv2
import face_recognition
import mysql.connector
from mysql.connector import Error
import tkinter as tk
from gpiozero import AngularServo
from tkinter import simpledialog
import numpy as np

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

# Crear una ventana emergente para ingresar el nombre de usuario
root = tk.Tk()
root.withdraw()  # Ocultar la ventana principal

user_name = simpledialog.askstring("Ingresar Nombre", "Ingresa tu nombre:")
root.destroy()  # Cerrar la ventana emergente

# Captura una imagen de la cámara
cap = cv2.VideoCapture(0)
ret, frame = cap.read()

# Guarda la imagen capturada como 'captured_img.jpg'
if ret:
    cv2.imwrite('captured_img.jpg', frame)

    
# Lee la imagen capturada como bytes
with open('captured_img.jpg', 'rb') as img_file:
    image_data = img_file.read()

# Utiliza face_recognition para extraer características faciales
face_encodings = face_recognition.face_encodings(face_recognition.load_image_file('captured_img.jpg'))

if len(face_encodings) > 0:
    # Toma la primera característica facial (puedes manejar múltiples si lo deseas)
    face_encoding = face_encodings[0]

    # Inserta el nombre, la imagen y las características en la base de datos
    try:
        query = "INSERT INTO users (usuarios, imagen, face_encoding) VALUES (%s, %s, %s)"
        values = (user_name, image_data, np.array(face_encoding).tobytes())
        cursor.execute(query, values)
        db.commit()
        print("Datos insertados correctamente.")

    except Error as e:
        print("Error al insertar datos:", e)
        db.rollback()

else:
    print("No se detectaron rostros en la imagen.")

# Cierra la conexión a la base de datos
db.close()