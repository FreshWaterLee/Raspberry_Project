from Adafruit_Python_DHT import Adafruit_DHT
import time

sensor = Adafruit_DHT.DHT11
pin = 4

try:
    while True:
        h,t = Adafruit_DHT.read_retry(sensor,pin)
        if h is not None and t is not None:
            print("Temperature = {0:0.1f}*C Humidity = {1:0.1f}%".format(t,h))
        else:
            print('Read Error')
        time.sleep(1)
except KeyboardInterrupt:
    print("Terminated by Keyboard")
finally:
    print("End of Program")