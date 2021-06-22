import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)
##핀맵의 번호가 아닌 GPIO 핀넘버

while True:
    try:
        GPIO.output(18,False)
        print('OFF')
        time.sleep(2)
        GPIO.output(18,True)
        print('On')
        time.sleep(2)
    except KeyboardInterrupt:
        pass
        print('Exit with ^C. GoodBye!')
        GPIO.cleanup()
        exit()
