import time
import board
import adafruit_dht

dhtDevice = adafruit_dht.DHT11(board.D18)
while True:
    try:
        temper_c = dhtDevice.temperature
        temper_f = temper_c * (9/5)+32
        humidty = dhtDevice.humidity
        print("Temp:{:.1f} F/ {:.1f} C Humidty: {} %".format(
                temper_f,temper_c,humidty))
        time.sleep(2.0)
    except KeyboardInterrupt:
        pass
        print('Exit with ^C. Good Bye')
        exit()