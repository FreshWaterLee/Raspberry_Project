## 좌우 방향으로 경로 설정
## 2개다 제한 거리에 여유가 있다면 직진
## 한쪽이 제한거리에 여유가 없다면 여유로운 방향으로 이동
import RPi.GPIO as GPIO
from time import sleep,time
import keyboard
GPIO.setmode(GPIO.BCM)
Front = 18
GPIO_TRI = 17
Jug_dis = 15 ## 한계 거리 조정 전역 변수로 사용해야 다른 함수에서 불러왔을때 한번만 설정 하면 됨 
GPIO_Di =[27,22] ## 초음파 센서 거리 입력 핀 (전,좌,우)
Di_LED= [23,24] ## 가능 거리에 따른 출력 핀 (전,좌,우)
distances = [0,0] ## 순서대로 정면, 왼쪽, 오른쪽 전역변수로 선언한 이유는 계속해서 변하기 때문
Dir=['L','R']## 터미널에서 거리 출력시 어느 방향인지를 위한 전역변수

#Echo 핀은 초음파가 물체와 부딪혔을때의 데이터를 받는 핀, TRIGER 핀은 초음파를 쏘는 핀
GPIO.setup(GPIO_TRI,GPIO.OUT)
GPIO.setup(Front,GPIO.OUT)
GPIO.setup(Di_LED[0],GPIO.OUT)
GPIO.setup(Di_LED[1],GPIO.OUT)
GPIO.setup(GPIO_Di[0],GPIO.IN) #좌회전 판단 
GPIO.setup(GPIO_Di[1],GPIO.IN) #우회전 판단 

## for문 내부에 입력하여 재귀함수로 이용
def Led_off(): ##LED를 오프 하기위해  모터를 이용하는 것까지 간다면 삭제 예정
    GPIO.output(Front,GPIO.LOW)
    GPIO.output(Di_LED[0],GPIO.LOW)
    GPIO.output(Di_LED[1],GPIO.LOW)
    
def Detect_dir(i):
    idx = GPIO_Di.index(i)
    GPIO.output(GPIO_TRI,True)
    sleep(0.1)
    GPIO.output(GPIO_TRI,False)
    Start_t = time()
    Stop_t = time()
    while GPIO.input(i) == 0:
        Start_t = time()
    while GPIO.input(i) == 1:
        Stop_t = time()
    TimeEla = Stop_t - Start_t
    distance = (TimeEla * 34300)/2
    distances[idx] = distance ## 인덱스에 따라 방향 거리를 저장
    print(Dir[idx],'의 거리는 : ',distance)
    sleep(0.1)
    
###
def Led_Jud():
    Led_off()
    ### 좌우 거리 값을 제한 거리와 비교
    Jug_lr = [False,False]
    ### 좌우 회전 확인 여부 둘다 참일 경우 직진 둘다 거짓일 경우 후진
    for i in range(len(distances)):
        if (distances[i] >Jug_dis):
            Jug_lr[i] = True
            ## 제한 거리 이상일경우 참 값을 입력
    try:
        if(Jug_lr.count(True)>1): ## True 값이 한방향이 아닐경우 직진으로 판단
            print('직진!!!')
            GPIO.output(Front,GPIO.HIGH)
        else:
            lr = Jug_lr.index(True)
            if (lr == 0): ## 좌회전
                print('좌회전')
                GPIO.output(Di_LED[lr],GPIO.HIGH)
            else: ## 우회전
                print('우회전')
                GPIO.output(Di_LED[lr],GPIO.HIGH)
    except ValueError: ## 좌우 둘 다 제한거리보다 짧을경우 
        print('후진!!')
    sleep(0.2)
        
try:
    while True:
        print("잠시만 기다려주세용!!")
        sleep(1)
        ## 하나의 센서의 데이터를 불러올때 사용 (센서 작동 유무 확인을 위해)
        for i in GPIO_Di:
            Detect_dir(i)
        Led_Jud()
except KeyboardInterrupt:
    print("LED_OFF")
    Led_off()
    print("Good Bye!!!")
    sleep(1)
    exit()