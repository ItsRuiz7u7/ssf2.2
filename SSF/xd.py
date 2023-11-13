import RPi.GPIO as GPIO
import time

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
    angle = max(0, min(90, angle))  # Cambiar el rango a 0-90 grados
    pulse_width = map(angle, 0, 90, SERVO_MIN_PULSE, SERVO_MAX_PULSE)
    pwm = map(pulse_width, 0, 20000, 0, 100)
    p.ChangeDutyCycle(pwm)

def loop():
    while True:
        setAngle(90)  # Mover el servo a 90 grados
        time.sleep(10)
        setAngle(0)  # Mover el servo de regreso a 0 grados
        time.sleep(1)  # Esperar 1 segundo antes de apagar el servo

def destroy():
    p.stop()
    GPIO.cleanup()

if __name__ == '__main':
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
