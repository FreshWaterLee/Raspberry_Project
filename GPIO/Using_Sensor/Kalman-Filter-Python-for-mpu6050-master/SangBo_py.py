from Kalman import KalmanAngle
import smbus
#import SMBus module of I2C
import time
import math
import RPi.GPIO as GPIO

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

t_now = 0.0
t_prev = 0.0

gyro_x =0.0
gyro_y =0.0
gyro_z =0.0
bus = smbus.SMBus(1)

 
    
def MPU_Init():
    #write to sample rate register
    bus.write_byte_data(DeviceAddress, SMPLRT_DIV, 7)
    #Write to power management register
    bus.write_byte_data(DeviceAddress, PWR_MGMT_1, 1)
    #Write to Configuration register
    #Setting DLPF (last three bit of 0X1A to 6 i.e '110' It removes the noise due to vibration.) https://ulrichbuschbaum.wordpress.com/2015/01/18/using-the-mpu6050s-dlpf/
    bus.write_byte_data(DeviceAddress, CONFIG, int('0000110',2))
    #Write to Gyro configuration register
    bus.write_byte_data(DeviceAddress, GYRO_CONFIG, 24)
    #Write to interrupt enable register
    bus.write_byte_data(DeviceAddress, INT_ENABLE, 1)

def read_raw_data(addr):
    #Accelero and Gyro value are 16-bit
    high = bus.read_byte_data(DeviceAddress, addr)
    low = bus.read_byte_data(DeviceAddress, addr+1)
    #concatenate higher and lower value
    value = ((high << 8) | low)
    #to get signed value from mpu6050
    if(value > 32768):
            value = value - 65536
    return value

def calcDT():
    global t_prev
    t_now = time.time()
    dt = (t_now - t_prev)
    t_prev= t_now
    return dt

def read_all_data():
    AcX =read_raw_data(ACCEL_XOUT_H)
    AcY =read_raw_data(ACCEL_YOUT_H)
    AcZ =read_raw_data(ACCEL_ZOUT_H)
    GyX =read_raw_data(GYRO_XOUT_H)
    GyY =read_raw_data(GYRO_YOUT_H)
    GyZ =read_raw_data(GYRO_ZOUT_H)
    return AcX,AcY,AcZ,GyX,GyY,GyZ

def calibAccelGyro():
    sumAcX =0.0
    sumAcY =0.0
    sumAcZ =0.0
    sumGyX =0.0
    sumGyY =0.0
    sumGyZ =0.0
    for i in range(0,10):
        AcX,AcY,AcZ,GyX,GyY,GyZ = read_all_data()
        sumAcX += AcX
        sumAcY += AcY
        sumAcZ += AcZ
        sumGyX += GyX
        sumGyY += GyY
        sumGyZ += GyZ
        time.sleep(0.1)
    baseAcX = sumAcX/10
    baseAcY = sumAcY/10
    baseAcZ = sumAcZ/10
    baseGyX = sumGyX/10
    baseGyY = sumGyY/10
    baseGyZ = sumGyZ/10

def calcAccelYPR():
    accel_x =0.0
    accel_y =0.0
    accel_z =0.0
    RADIAN_TO_DEGREES = 180/3.14159
    
    accel_x = AcX-baseAcX
    accel_y = AcY-baseAcY
    accel_z = AcZ-baseAcZ
    
    accel_yz = math.sqrt(math.pow(accel_y,2)+math.pow(accel_z,2))
    accel_angle_y = math.atan(-accel_x /accel_yz)* RADIAN_TO_DEGREES
    
    accel_xz = math.sqrt(math.pow(accel_x,2)+math.pow(accel_z,2))
    accel_angle_x = math.atan(accel_y/accel_xz) *RADIAN_TO_DEGREES
    
    accel_angle_z = 0
def calcGyroYRP():
    global gyro_x
    global gyro_y
    global gyro_z
    GYRO_TO_DEGREE = 131
    gyro_x = (GyX-baseGyX) / GYRO_TO_DEGREE
    gyro_y = (GyY-baseGyY) / GYRO_TO_DEGREE
    gyro_z = (GyZ-baseGyZ) / GYRO_TO_DEGREE
    
try:
    while True:
        MPU_Init()
        dt = calcDT()
        #read_all_data()
        calibAccelGyro()
        print(dt)
except KeyboardInterrupt:
    print("Good Bye!!")