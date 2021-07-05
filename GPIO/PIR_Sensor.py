import os
import RPi.GPIO as GPIO
import time

pin = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.IN)

time.sleep(2)
print('Ready')

try:
    while True:
        if(GPIO.input(pin)==1):
            print('motion')
        else:
            print('nothing')
        time.sleep(1)
except KeyboardInterrupt:
    pass
    print("Exit with ^C. GoodBye")
    GPIO.cleanup()
    exit()