from machine import I2C, Pin, Timer, rng
from network import LoRa, WLAN
import time
import pycom
import socket

MYID = "1:1"
IP_receive = "192.168.4.1"
IP_send = "192.128.4.2"
PORT = 5005
dead_time = 1

wlan = WLAN()
wlan.init(mode=WLAN.AP, ssid='TEST ' + MYID, auth=(WLAN.WPA2, '12345678'))

s_UDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s_UDP.setblocking(False)

lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868) # Do we need this???
s_LORA = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s_LORA.setblocking(False)

s_UDP.bind((IP_receive, PORT)) # A problem may occur - if so try writing manually the IP_receive and PORT

def RGB_LED(color, delay):
    pycom.rgbled(color) # set led to <color>
    time.sleep_ms(delay) # for <time> time
    pycom.rgbled(0) # reset led to none

pycom.heartbeat(False)
RGB_LED(0xFF00FF, 200)

life = Timer.Chrono()
valid = Timer.Chrono()

def TIME(min_wait):
    min_wait = min_wait + (rng()/10000000) # if problem occurs try to import machine and use ... + (machine.rng/10000000)
    time.sleep(min_wait)

life.start()
while(True):
    life_time = life.read()
    if life_time > dead_time:
        MyIDsenD = "V,"+ MYID
        bID = bytes(MyIDsenD, 'utf-8')
        s_LORA.send(bID)
        valid.start()
        life.reset()
    recv_info_LORA = s_LORA.recv(128)
    recv_info_UDP = s_UDP.recv(128)
    valid_time = valid.read()
    if (recv_info_LORA):
        recv_info_LORA = str(recv_info_LORA.decode("utf-8")).split(',')

        if valid_time < 5 and recv_info_LORA[0] == "V":
            RGB_LED(0xFF00FF, 20)
            auth = 1
        else:
            valid.reset()

        if recv_info_LORA[0] == "M":
            toID, msg = recv_info_LORA[1].split("|")
            if toID == MYID:
                try:
                    s_UDP.sendto(msg, (IP_send,PORT))
                except OSError as err:
                    print(err)
            else:
                s_LORA.send("M,{}".format(recv_info_LORA[2]).encode("utf-8"))

    if(recv_info_UDP):
        if auth:
            try:
                toID, msg = recv_info_UDP.decode("utf-8").split("|")
                s_LORA.send("M,{}".format(msg).encode("utf-8"))
                RGB_LED(0xFFFFFF, 20)
            except ValueError:
                print("Wrong syntax")
                pass
        else:
            print("No connection")
