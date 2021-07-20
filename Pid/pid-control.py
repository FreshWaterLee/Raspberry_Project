import PID
import time
import os.path

targetT=35
P=10
I=1
D=1

pid = PID.PID(P,I,D)
pid.SetPoint = targetT
pid.setSampleTime(1)

def readConfig ():
    global targetT
    with open ('/tmp/pid.conf', 'r') as f:
        config = f.readline().split(',')
        pid.SetPoint = float(config[0])
        targetT = pid.SetPoint
        pid.setKp (float(config[1]))
        pid.setKi (float(config[2]))
        pid.setKd (float(config[3]))

def createConfig ():
    if not os.path.isfile('/tmp/pid.conf'):
        with open ('/tmp/pid.conf', 'w') as f:
            f.write('%s,%s,%s,%s'%(targetT,P,I,D))
            

createConfig()

while 1:
    readConfig()
    a0 = 25
    temperature = (a0 -0.5)*100
    
    pid.update(temperature)
    targetPWM = pid.output
    targetPWM = max(min(int(targetPWM), 100),0)
    
    print("Target : %.1f C | Current : %.1f C | PWM: %s %%"%(targetT, temperature, targetPWM))
    time.sleep(0.5)