from machine import I2C, Pin, Timer
from network import LoRa, WLAN
import time
import pycom
import socket
import machine


wlan = WLAN()
wlan.init(mode=WLAN.AP, ssid='TEST', auth=(WLAN.WPA2,'12345678'))
s_UDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s_UDP.setblocking(False)
IP_receive = "192.168.4.1"
IP_send = "192.128.4.2"
PORT = 5005

pycom.heartbeat(False)
lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)
s_LORA = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s_LORA.setblocking(False)
ack_time = Timer.Chrono()

def SEND_MYID(MYID):
    NAME = "N," + MYID
    NAME = bytes(NAME, 'utf-8')
    s.send(NAME)
def SEND_ACK(sender):
    ACK = "A," + sender +","+ MYID
    ACK= bytes(ACK, 'utf-8')
    s.send(ACK)
def ADDING(sender,neighbor_table):
    s = str(neighbor_table).split(',')
    l = len(s)
    for i in range(0,l):
        if sender == s[i]:
            checked = 0
        else:
            checked = 1
    if checked == 1:
        neighbor_table = neighbor_table +","+sender

    return neighbor_table
def TIME(min_wait):
    min_wait = min_wait + (machine.rng()/10000000)
    time.sleep(min_wait)

MYID = "1:4"
neighbor_table = ""
dead_time = 3
pycom.rgbled(0xFF0000)
time.sleep_ms(200)
pycom.rgbled(0)

ack_time.start()
while(True):
    ack_live = ack_time.read()
    if ack_live > dead_time:
        SEND_MYID(MYID)
        ack_time.reset()
    received_information_LORA = s_LORA.recv(128)
    received_information_UDP = s_UDP.recv(128)
    if(received_information_UDP):
        payload = received_information_UDP
        

    if (received_information_LORA):
        received_information_LORA = received_information.decode("utf-8")
        print(received_information_LORA)
        received_information_LORA = str(received_information_LORA).split(',')

        if received_information_LORA[0] == "N":
            pycom.rgbled(0x0000FF)
            time.sleep_ms(20)
            pycom.rgbled(0)
            sender = received_information[1]
            neighbor_table = ADDING(sender,neighbor_table)
            SEND_ACK(sender)

        if received_information_LORA[0] == "A" and received_information_LORA[2] == MYID:
            pycom.rgbled(0x00FF00)
            time.sleep_ms(20)
            pycom.rgbled(0)
            sender = received_information_LORA[1]
            neighbor_table = ADDING(sender,neighbor_table)
