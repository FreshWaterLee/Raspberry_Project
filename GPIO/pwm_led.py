import RPi.GPIO as GPIO
import time

led = 18
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(led, GPIO.OUT)

pi_pwm = GPIO.PWM(LED,1000)
pi_pwm.start(0)

try:
    while 1:
        