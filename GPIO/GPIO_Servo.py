## 별도의 5V 전원을 서보에 공급하길 추천한다. 
## 서보에서 부하가 걸리면 라즈베리 파이 보드에 대미지를 먹을 수 있기 때문이다.
## 이러한 이유로 모터 전원은 보드가 아닌 건전지 혹은 배터리로 모터에 전력을 공급 한다.
## 보드에서 주는 값은 PWM값일뿐

import RPi.GPIO as GPIO
from time import sleep

servoPin = 12
SERVO_MAX = 12
SERVO_MIN = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPin,GPIO.OUT)
servo = GPIO.PWM(servoPin,50)
servo.start(0)

def setServoPos(degree):
    if degree> 180:
        degree = 180
    duty = SERVO_MIN+(degree*(SERVO_MAX-SERVO_MIN)/180.0)
    print("Degree: {} to {}(Duty)".format(degree,duty))
    servo.ChangeDutyCycle(duty)

if __name__ =="__main__":
    setServoPos(0)
    sleep(2)
    #setServoPos(90)
    #sleep(1)
    setServoPos(180)
    sleep(2)
    setServoPos(0)
    sleep(2)
    servo.stop()
    GPIO.cleanup()