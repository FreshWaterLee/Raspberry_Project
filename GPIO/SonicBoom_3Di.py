import RPi.GPIO as GPIO
from time import sleep,time
import keyboard
GPIO.setmode(GPIO.BCM)
GPIO_TRI = 17
Jug_dis = 15 ## 한계 거리 조정 전역 변수로 사용해야 다른 함수에서 불러왔을때 한번만 설정 하면 됨 
GPIO_Di =[2,3,4] ## 초음파 센서 거리 입력 핀 (전,좌,우)
Di_LED= [18,23,24] ## 가능 거리에 따른 출력 핀 (전,좌,우)
distances = [0,0,0] ## 순서대로 정면, 왼쪽, 오른쪽 전역변수로 선언한 이유는 계속해서 변하기 때문
Dir=['F','L','R']## 터미널에서 거리 출력시 어느 방향인지를 위한 전역변수

#Echo 핀은 초음파가 물체와 부딪혔을때의 데이터를 받는 핀, TRIGER 핀은 초음파를 쏘는 핀
GPIO.setup(GPIO_TRI,GPIO.OUT)
GPIO.setup(Di_LED[0],GPIO.OUT)
GPIO.setup(Di_LED[1],GPIO.OUT)
GPIO.setup(Di_LED[2],GPIO.OUT)
GPIO.setup(GPIO_Di[0],GPIO.IN) #직진 판단 
GPIO.setup(GPIO_Di[1],GPIO.IN) #좌회전 판단 
GPIO.setup(GPIO_Di[2],GPIO.IN) #우회전 판단

## for문 내부에 입력하여 재귀함수로 이용
def Led_off(): ##LED를 오프 하기위해  모터를 이용하는 것까지 간다면 삭제 예정
    GPIO.output(Di_LED[0],GPIO.LOW)
    GPIO.output(Di_LED[1],GPIO.LOW)
    GPIO.output(Di_LED[2],GPIO.LOW)
    
def Detect_dir(i):
    GPIO.output(GPIO_TRI,True)
    sleep(0.1)
    GPIO.output(GPIO_TRI,False)
    Start_t = time()
    Stop_t = time()
    while GPIO.input(GPIO_Di[i]) == 0:
        Start_t = time()
    while GPIO.input(GPIO_Di[i]) == 1:
        Stop_t = time()
    TimeEla = Stop_t - Start_t
    distance = (TimeEla * 34300)/2
    distances[i] = distance ## 인덱스에 따라 방향 거리를 저장 
    sleep(0.2)
    
###
def Led_Jud():
    ### 직진 가능 여부부터 확인 (왜냐하면 좌로가든 우로 가든 직진은 해야하기때문 )
    print(distances)
    if(Jug_dis<distances[0]):
        print("직진!!!")
        GPIO.output(Di_LED[0],GPIO.HIGH)
    else:
        Led_off()
    lr_idx = 1 if distances[1]>distances[2] else 2 ## 비교적 여유로운 방향을 설정하기 위해
    print(lr_idx,"의 거리는 : ",distances[lr_idx])
    if(Jug_dis<distances[lr_idx] and distances[0]<distances[lr_idx]):
        ## 좌우에 공간 여유가 적다면 좌우 코너링은 안함(직진만), 또한 정면 공간보다 여유가 적다면 굳이 코너링을 할 필요는 없다
        print("좌우 회전!!")
        GPIO.output(Di_LED[lr_idx],GPIO.HIGH)
        GPIO.output(Di_LED[0],GPIO.HIGH)
    sleep(1)
        
try:
    while True:
        print("잠시만 기다려주세용!!")
        sleep(3)
        ## 하나의 센서의 데이터를 불러올때 사용 (센서 작동 유무 확인을 위해)
        i=2
        print("Detect  ",GPIO_Di[i])
        GPIO.output(GPIO_TRI,True)
        sleep(0.1)
        GPIO.output(GPIO_TRI,False)
        Start_t = time()
        Stop_t = time()
        while GPIO.input(GPIO_Di[i]) == 0:
            Start_t = time()
        while GPIO.input(GPIO_Di[i]) == 1:
            Stop_t = time()
        TimeEla = Stop_t - Start_t
        distance = (TimeEla * 34300)/2
        distances[i] = distance ## 인덱스에 따라 방향 거리를 저장 
        print(Dir[i],"distance: ",distance)
        sleep(0.2)
        Led_Jud()
except KeyboardInterrupt:
    print("LED_OFF")
    Led_off()
    print("Good Bye!!!")
    sleep(1)
    exit()
