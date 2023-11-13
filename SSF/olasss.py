from gpiozero import InputDevice, OutputDevice
from time import sleep

pins = [4, 17, 27, 18]  # Reemplaza estos números con los pines que desees verificar

for pin_number in pins:
    pin = InputDevice(pin_number)  # Utiliza InputDevice para verificar el estado de entrada
    print(f"Pin {pin_number}: Estado = {pin.is_active}")
    sleep(1)  # Espera 1 segundo antes de verificar el siguiente pin
