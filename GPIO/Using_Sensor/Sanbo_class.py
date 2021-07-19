import smbus
#import SMBus module of I2C
import time
import math
import RPi.GPIO as GPIO

class Sangbo:
    ## 클래스에서 함수에 사용할 변수 선언 
    bus = smbus.SMBus(1)
    DeviceAddress = 0x68
    PWR_MGMT_1   = 0x6B
    SMPLRT_DIV   = 0x19
    CONFIG       = 0x1A
    GYRO_CONFIG  = 0x1B
    INT_ENABLE   = 0x38
    ACCEL_XOUT_H = 0x3B
    ACCEL_YOUT_H = 0x3D
    ACCEL_ZOUT_H = 0x3F
    GYRO_XOUT_H  = 0x43
    GYRO_YOUT_H  = 0x45
    GYRO_ZOUT_H  = 0x47

    AcX =0.0
    AcY =0.0
    AcZ =0.0
    Tmp =0.0
    GyX =0.0
    GyY =0.0
    GyZ =0.0
    dt = 0.0

    accel_angle_x = 0.0
    accel_angle_y = 0.0
    accel_angle_z = 0.0

    gyro_angle_x = 0.0
    gyro_angle_y = 0.0
    gyro_angle_z = 0.0

    fil_angle_x = 0.0
    fil_angle_y = 0.0
    fil_angle_z = 0.0

    baseAcX = 0.0
    baseAcY = 0.0
    baseAcZ = 0.0

    baseGyX = 0.0
    baseGyY = 0.0
    baseGyZ = 0.0
    
    dt = 0.0
    t_now = 0.0
    t_prev = 0.0

    gyro_x =0.0
    gyro_y =0.0
    gyro_z =0.0
    ## 데이터 확인을 위한
    def print_data(self):
        print(self.AcX,self.AcY)
    
    ## 생성시 설정할 기본값(시간, Bus연결)
    def __init__(self):
        ## bus설정
        self.bus.write_byte_data(self.DeviceAddress, self.SMPLRT_DIV, 7)
        self.bus.write_byte_data(self.DeviceAddress, self.PWR_MGMT_1, 1)
        self.bus.write_byte_data(self.DeviceAddress, self.CONFIG, int('0000110',2))
        self.bus.write_byte_data(self.DeviceAddress, self.GYRO_CONFIG, 24)
        self.bus.write_byte_data(self.DeviceAddress, self.INT_ENABLE, 1)
        self.t_prev = time.time()
        
    ## 센서값 전처리 함수
    def read_data(self,addr):
        high = self.bus.read_byte_data(self.DeviceAddress, addr)
        low = self.bus.read_byte_data(self.DeviceAddress, addr+1)
        #concatenate higher and lower value
        value = ((high << 8) | low)
        #to get signed value from mpu6050
        if(value > 32768):
                value = value - 65536
        return value
    
    ## 센서값 획득 함수
    def readAccelGyro(self):
        self.AcX = self.read_data(addr=self.ACCEL_XOUT_H)
        self.AcY = self.read_data(addr=self.ACCEL_YOUT_H)
        self.AcZ = self.read_data(addr=self.ACCEL_ZOUT_H)
        self.GyX = self.read_data(addr=self.GYRO_XOUT_H)
        self.GyY = self.read_data(addr=self.GYRO_YOUT_H)
        self.GyZ = self.read_data(addr=self.GYRO_ZOUT_H)
    
    ## 시간 변화량 획득(상보 필터 및 PID에서 사용하기 위해)
    def calDT(self):
        self.t_now = time.time()
        self.dt = (self.t_now - self.t_prev)/1000000.0
        self.t_prev = self.t_now
    
    ## 데이터 칼리브레이션 함수
    def calibAccelData(self):
        sumAcX =0.0
        sumAcY =0.0
        sumAcZ =0.0
        sumGyX =0.0
        sumGyY =0.0
        sumGyZ =0.0
        self.readAccelGyro()
        for i in range(0,10):
            self.readAccelGyro()
            sumAcX += self.AcX
            sumAcY += self.AcY
            sumAcZ += self.AcZ
            sumGyX += self.GyX
            sumGyY += self.GyY
            sumGyZ += self.GyZ
            time.sleep(0.1)
        self.baseAcX = sumAcX/10
        self.baseAcY = sumAcY/10
        self.baseAcZ = sumAcZ/10
        self.baseGyX = sumGyX/10
        self.baseGyY = sumGyY/10
        self.baseGyZ = sumGyZ/10
        self.print_data()
        
    ## 가속도값 계산 함수
    def calcAccelYPR(self):
        RADIAN_2_Degree = 180/3.14159
        accel_x = self.AcX - self.baseAcX
        accel_y = self.AcY - self.baseAcY
        accel_z = self.AcZ + (16384-self.baseAcZ)
        
        accel_yz = math.sqrt(math.pow(accel_y,2) + math.pow(accel_z,2))
        self.accel_angle_y = math.atan(-accel_x / accel_yz)* RADIAN_2_Degree
        
        accel_xz = math.sqrt(math.pow(accel_x,2) + math.pow(accel_z,2))

        self.accel_angle_x = math.atan(accel_y/accel_xz) * RADIAN_2_Degree
        self.accel_angle_z = 0
    
    ## 자이로값 계산 함수
    def calcGyroYPR(self):
        GYRO_2_Degree_Per_Sec = 131.0
        self.gyro_x = (self.GyX-self.baseGyX) / GYRO_2_Degree_Per_Sec
        self.gyro_y = (self.GyY-self.baseGyY) / GYRO_2_Degree_Per_Sec
        self.gyro_z = (self.GyZ-self.baseGyZ) / GYRO_2_Degree_Per_Sec
    
    ## 필터 적용
    def calcFilterYPR(self):
        gz_th1 = 0.2
        gz_th2 = 1.0
        ALPHA = 0.96
        tmp_angle_x = self.fil_angle_x + self.gyro_x * self.dt
        tmp_angle_y = self.fil_angle_y + self.gyro_y * self.dt

        if(self.gyro_z < gz_th1 and self.gyro_z > -gz_th2):
            self.gyro_z = 0
        tmp_angle_z = self.fil_angle_z + self.gyro_z * self.dt
        
        self.fil_angle_x = ALPHA * tmp_angle_x + (1.0-ALPHA)* self.accel_angle_x
        self.fil_angle_y = ALPHA * tmp_angle_y + (1.0-ALPHA)* self.accel_angle_y
        self.fil_angle_z = tmp_angle_z
        #self.fil_angle_z = ALPHA * tmp_angle_z + (1.0-ALPHA)* self.accel_angle_z
        
if __name__ == '__main__':
    ## 작성한 클래스 객체 생성
    sang = Sangbo()
    while True:
        try: ## 굳이 키보드값을 받을 필요를 느끼지 않기에 try~except을 사용
            sang.readAccelGyro()
            sang.calDT()
            sang.calcAccelYPR()
            sang.calcGyroYPR()
            sang.calcFilterYPR()
            #print("상보필터 적용 결과")
            #print("X축은 : ",str(sang.fil_angle_x)," Y축은 : ",str(sang.fil_angle_y))
            print("Z축은 : ",str(sang.fil_angle_z))
        except KeyboardInterrupt: ## 센서값 취득 종료를 위한 예외 설정
            break
    print("테스트 종료")