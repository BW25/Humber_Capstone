import time
import RPi.GPIO as GPIO


ledPin = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(ledPin, GPIO.OUT)

pwm = GPIO.PWM(ledPin, 100)
pwm.start(50)

time.sleep(1)
pwm.ChangeDutyCycle(100)
time.sleep(5)


pwm.stop()
GPIO.cleanup()
