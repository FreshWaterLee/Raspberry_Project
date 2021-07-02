import datetime
from Adafruit_CircuitPython_DHT import adafruit_dht as dht
import board
htd = dht.DHT11(board.D4)
h = htd.humidity
t = htd.temperature
sleep(2)

print(h)
print(t)
