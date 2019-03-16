from machine import I2C, Pin, Timer
from network import LoRa, WLAN
import time
import pycom
import socket
import machine

MYID = "1:4"
wlan = WLAN()
wlan.init(mode=WLAN.AP, ssid='TEST '+MYID, auth=(WLAN.WPA2,'12345678'))
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
s_UDP.bind(("192.168.4.1", 5005))
ack_time.start()
neighbor_table = ["NT"]
dead_time = 3
pycom.rgbled(0xFF00FF)
time.sleep_ms(1000)
pycom.rgbled(0)



def SEND_MYID(MYID):
    NAME = "N," + MYID
    NAME = bytes(NAME, 'utf-8')
    s_LORA.send(NAME)
def SEND_ACK(sender):
    ACK = "A," + sender +","+ MYID
    ACK= bytes(ACK, 'utf-8')
    s_LORA.send(ACK)
def SEND_MESSAGE(sender, payload):
    Message = "M,{},{},{},".format(MYID, sender, payload)
    Message = Message.encode("utf-8")
    print(Message)
    s_LORA.send(Message)
def ADDING(sender,neighbor_table):
    print(neighbor_table)
    l = len(neighbor_table)
    for i in range(0,l):
        if sender == neighbor_table[i] and sender != MYID:
            checked = 0
        else:
            checked = 1
    if checked == 1:
        neighbor_table.append(sender)
    else:
        pass
    return neighbor_table
def TIME(min_wait):
    min_wait = min_wait + (machine.rng()/10000000)
    time.sleep(min_wait)

while(True):
    ack_live = ack_time.read()
    if ack_live > dead_time:
        SEND_MYID(MYID)
        ack_time.reset()

    received_information_LORA = s_LORA.recv(128)
    received_information_UDP = s_UDP.recv(128)


    if (received_information_LORA):
        received_information_LORA = received_information_LORA.decode("utf-8")
        received_information_LORA = str(received_information_LORA).split(',')

        if received_information_LORA[0] == "N":
            sender = received_information_LORA[1]
            neighbor_table = ADDING(sender,neighbor_table)
            print(neighbor_table)
            SEND_ACK(sender)
            pycom.rgbled(0x0000FF)
            time.sleep_ms(10)
            pycom.rgbled(0)

        if received_information_LORA[0] == "A" and received_information_LORA[2] == MYID:
            sender = received_information_LORA[1]
            neighbor_table = ADDING(sender,neighbor_table)
            pycom.rgbled(0x00FF00)
            time.sleep_ms(10)
            pycom.rgbled(0)

        if received_information_LORA[0] == "M" and received_information_LORA[2] == MYID:
            pycom.rgbled(0xFFFF00)
            time.sleep_ms(10)
            pycom.rgbled(0)
            end_message = received_information_LORA[3]
            print(end_message)
            s_UDP.sendto(end_message,("192.168.4.2",5005))

    if(received_information_UDP):
        payload = received_information_UDP
        print(payload)
        try:
            sender = neighbor_table[1]
            SEND_MESSAGE(sender,payload.decode("utf-8"))
            pycom.rgbled(0xFFFFFF)
            time.sleep_ms(10)
            pycom.rgbled(0)
        except IndexError as err:
            continue
