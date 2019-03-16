import time
from machine import I2C

i2c = I2C(0, I2C.MASTER, baudrate=100000, pins=('P22', 'P21'))
address = const(0x10)

while(True):
    sensor = i2c.readfrom(address, 200)
    # sensor = sensor.decode("ust-8")
    time.sleep(1)
    # print(sensor)
    print(sensor.decode('UTF-8'))

def encho(age):
    if(age > 15):
        print(age)

age = 18
encho(age)
