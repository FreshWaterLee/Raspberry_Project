import RPi.GPIO as GPIO
from time import sleep,time
GPIO.setmode(GPIO.BCM)
GPIO_TRI = 17
GPIO_Ech = 18
#Echo 핀은 초음파가 물체와 부딪혔을때의 데이터를 받는 핀, TRIGER 핀은 초음파를 쏘는 핀
GPIO.setup(GPIO_TRI,GPIO.OUT)
GPIO.setup(GPIO_Ech,GPIO.IN)
try:
    while True:
        GPIO.output(GPIO_TRI,True)
        sleep(0.1)
        GPIO.output(GPIO_TRI,False)
        StartTime = time()
        StopTime = time()
        while GPIO.input(GPIO_Ech)==0:
            StartTime = time()
        while GPIO.input(GPIO_Ech)==1:
            StopTime = time()
        TimeElapsed = StopTime-StartTime
        distance = (TimeElapsed * 34300)/2
        print('Measured Distance =%.1f'%distance)
        sleep(1)
except KeyboardInterrupt:
    print("Good Bye!!!")
    sleep(1)
    exit()
