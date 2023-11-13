import tkinter as tk
import RPi.GPIO as GPIO
from PIL import Image, ImageTk
import mysql.connector
import subprocess
import time
from tkinter import messagebox

# Función para abrir el script "ola.py"
def abrir_script():
    subprocess.Popen(["python", "ola.py"])
    

# Función para mostrar los usuarios y abrir la ventana de eliminación
def mostrar_usuarios():
    global ventana_usuarios  # Hacer que ventana_usuarios sea global para que sea referenciable
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="J0n4than1234",
        database="ayuda"
    )

    cursor = conexion.cursor()
    consulta = "SELECT usuarios FROM users"
    cursor.execute(consulta)

    usuarios = [fila[0] for fila in cursor.fetchall()]

    ventana_usuarios = tk.Toplevel(ventana)
    ventana_usuarios.title("Usuarios")
    ventana_usuarios.configure(bg="LightSlateGray")

    ventana_usuarios.geometry("450x600")  # Cambio de tamaño

    lista_usuarios = tk.Listbox(ventana_usuarios)
    lista_usuarios.pack(padx=20, pady=10)

    for usuario in usuarios:
        lista_usuarios.insert(tk.END, usuario)

    cursor.close()
    conexion.close()

    def actualizar_lista():
        if 'ventana_usuarios' in globals():  # Comprobar si la variable existe antes de destruir la ventana
            ventana_usuarios.destroy()
        mostrar_usuarios()  # Mostrar la lista actualizada

    boton_actualizar = tk.Button(ventana_usuarios, text="Actualizar Lista", command=actualizar_lista)
    boton_actualizar.pack(pady=5)

    def abrir_agregar_usuario():
        ventana_usuarios.withdraw()  # Ocultar la ventana de usuarios antes de abrir la ventana de agregar usuario
        abrir_script()

    boton_abrir_script = tk.Button(ventana_usuarios, text="Agregar Usuario", command=abrir_agregar_usuario)
    boton_abrir_script.pack(pady=5)

    def borrar_usuario_seleccionado():
        seleccionado = lista_usuarios.curselection()
        if seleccionado:
            usuario = lista_usuarios.get(seleccionado[0])
            mostrar_ventana_borrar(usuario)

    boton_borrar_usuario = tk.Button(ventana_usuarios, text="Borrar Usuario", command=borrar_usuario_seleccionado)
    boton_borrar_usuario.pack(pady=5)

# Función para mostrar la ventana de eliminación
def mostrar_ventana_borrar(usuario):
    ventana_borrar = tk.Toplevel(ventana)
    ventana_borrar.title("Borrar Usuario")

    mensaje_label = tk.Label(ventana_borrar, text=f"¿Deseas borrar al usuario '{usuario}'?")
    mensaje_label.pack(padx=20, pady=10)

    def borrar_y_cerrar():
        borrar_usuario(usuario)
        ventana_borrar.destroy()
        if 'ventana_usuarios' in globals():  # Comprobar si la variable existe antes de destruir la ventana
            ventana_usuarios.destroy()

    boton_confirmar = tk.Button(ventana_borrar, text="Confirmar", command=borrar_y_cerrar)
    boton_confirmar.pack(padx=20, pady=5)

    boton_cancelar = tk.Button(ventana_borrar, text="Cancelar", command=ventana_borrar.destroy)
    boton_cancelar.pack(padx=20, pady=5)

# Función para borrar el usuario seleccionado
def borrar_usuario(usuario):
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="J0n4than1234",
        database="ayuda"
    )

    cursor = conexion.cursor()
    consulta = f"DELETE FROM users WHERE usuarios = '{usuario}'"
    cursor.execute(consulta)
    conexion.commit()

    cursor.close()
    conexion.close()

    if 'ventana_usuarios' in globals():  # Comprobar si la variable existe antes de destruir la ventana
        ventana_usuarios.destroy()
        mostrar_usuarios()

# Funcion para el servo motor 
def abrirs():
    SERVO_MIN_PULSE = 500
    SERVO_MAX_PULSE = 2500
    Servo = 18

    def map(value, inMin, inMax, outMin, outMax):
        return (outMax - outMin) * (value - inMin) / (inMax - inMin) + outMin

    def setup():
        global p
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(Servo, GPIO.OUT)
        GPIO.output(Servo, GPIO.LOW)
        p = GPIO.PWM(Servo, 50)
        p.start(0)

    def setAngle(angle):
        angle = max(0, min(180, angle))
        pulse_width = map(angle, 0, 180, SERVO_MIN_PULSE, SERVO_MAX_PULSE)
        pwm = map(pulse_width, 0, 20000, 0, 100)
        p.ChangeDutyCycle(pwm)

    def loop():
        while True:
            for i in range(0, 181, 5):
                setAngle(i)
                time.sleep(0.002)
            time.sleep(5)
            for i in range(180, -1, -5):
                setAngle(i)
                time.sleep(0.002)
            time.sleep(5)

    def destroy():
        p.stop()
        GPIO.cleanup()

    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("SSF")

# Cambiar el color de fondo de la ventana principal
ventana.configure(bg="LightSlateGray")

# Definir el tamaño de la ventana a 450x600 píxeles
ventana.geometry("450x600")

# Agregar una imagen a la ventana principal
imagen = Image.open("logo_ssf.jpg")  # Cambia "ruta_de_la_imagen.jpg" por la ruta de tu imagen
##imagen = imagen.resize((200, 200), Image.ANTIALIAS)# Cambia el tamaño de la imagen si es necesario
imagen = ImageTk.PhotoImage(imagen)  # Usar ImageTk.PhotoImage para cargar la imagen
imagen_label = tk.Label(ventana, image=imagen)
imagen_label.pack(pady=20)

# Crear botones debajo de la imagen
boton_mostrar_usuarios = tk.Button(ventana, text="Mostrar Usuarios", command=mostrar_usuarios, bg="black", fg="white")
boton_mostrar_usuarios.pack(pady=10)

boton_abrir = tk.Button(ventana, text="Abrir", command=abrirs, bg="black", fg="white")
boton_abrir.pack(pady=5)

boton_camara = tk.Button(ventana, text="Camara", bg="black", fg="white")
boton_camara.pack(pady=5)

# Iniciar el bucle principal de la interfaz
ventana.mainloop()
