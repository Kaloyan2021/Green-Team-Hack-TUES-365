from machine import I2C, Pin, Timer, rng
from network import LoRa, WLAN
import time
import pycom
import socket
<<<<<<< HEAD

MYID = "1:1"
IP_receive = "192.168.4.1"
IP_send = "192.128.4.2"
PORT = 5005

wlan = WLAN()
wlan.init(mode=WLAN.AP, ssid='TEST ' + MYID, auth=(WLAN.WPA2, '12345678'))

s_UDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s_UDP.setblocking(False)

=======
# import machine

wlan = WLAN()
wlan.init(mode=WLAN.AP, ssid='TEST ' + MYID, auth=(WLAN.WPA2, '12345678'))

s_UDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s_UDP.setblocking(False)

>>>>>>> f4a6e0298e74872b3880ce2e43fded4baefc8745
lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868) # Do we need this???
s_LORA = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s_LORA.setblocking(False)

<<<<<<< HEAD
s_UDP.bind((IP_receive, PORT)) # A problem may occur - if so try writing manually the IP_receive and PORT

def RGB_LED(color, delay):
    pycom.rgbled(color) # set led to <color>
    time.sleep_ms(delay) # for <time> time
    pycom.rgbled(0) # reset led to none

pycom.heartbeat(False)
RGB_LED(0xFF00FF, 200)

def SEND_MESSAGE(sender, payload):
    s_LORA.send("M,{},{}".format(sender, payload).encode("utf-8")) # if there is a problem - split the argument
=======
global MYID = "1:1"
global IP_receive = "192.168.4.1"
global IP_send = "192.128.4.2"
global PORT = 5005

s_UDP.bind((IP_receive, PORT)) # A problem may occur - if so try writing manually the IP_receive and PORT

def RGB_LED(color, time):
    pycom.rgbled(color) # set led to <color>
    time.sleep_ms(time) # for <time> time
    pycom.rgbled(0) # reset led to none

pycom.heartbeat(False)
ack_time = Timer.Chrono()
ack_time.start()
neighbour_table = ["NT"]
dead_time = 3
RGB_LED(0xFF00FF, 200)

def SEND_MYID(MYID):
    NAME = bytes("N,{}".format(MYID), "utf-8") # if there is a problem - split the actions
    s_LORA.send(NAME)

def SEND_ACK(sender):
    ACK = bytes("A,{},{}".format(sender, MYID)) # if there is a problem - split the actions
    s_LORA.send(ACK)

def SEND_MESSAGE(sender, payload):
    s_LORA.send("M,{},{},{},".format(MYID, sender, payload).encode("utf-8")) # if there is a problem - split the argument

def ADDING(sender, neighbour_table): # Checks the neighbour_table and if sender (id) is not in it - adds it
    for i in range(len(neighbour_table)):
        if sender == neighbour_table[i] and sender != MYID:
            return neighbour_table # sender is in neighbour_table -> no need to add again
    neighbour_table.append(sender)
    return neighbour_table
>>>>>>> f4a6e0298e74872b3880ce2e43fded4baefc8745

def TIME(min_wait):
    min_wait = min_wait + (rng()/10000000) # if problem occurs try to import machine and use ... + (machine.rng/10000000)
    time.sleep(min_wait)

while(True):
<<<<<<< HEAD
    recv_info_LORA = s_LORA.recv(128)
    recv_info_UDP = s_UDP.recv(128)
    if (recv_info_LORA):
        RGB_LED(0x03FCAB, 20)
        recv_info_LORA = str(recv_info_LORA.decode("utf-8")).split(',')
        if recv_info_LORA[0] == "M":
            toID, msg = recv_info_LORA[2].split("|")
            if toID == MYID:
                try:
                    s_UDP.sendto(msg, (IP_send,PORT))
                    print(msg)
                except OSError as err:
                    print(err)
            else:
                s_LORA.send("M,{}{}".format(recv_info_LORA[1],recv_info_LORA[2]).encode("utf-8"))

    if(recv_info_UDP):
        toID, msg = recv_info_UDP.decode("utf-8").split("|")
        SEND_MESSAGE(toID, recv_info_UDP.decode("utf-8"))
        RGB_LED(0xFFFFFF, 20)
=======
    ack_live = ack_time.read()
    if ack_live > dead_time:
        SEND_MYID(MYID)
        ack_time.reset()

    recv_info_LORA = s_LORA.recv(128)
    recv_info_UDP = s_UDP.recv(128)

    if (recv_info_LORA):
        recv_info_LORA = str(recv_info_LORA.decode("utf-8")).split(',')
        if recv_info_LORA[0] == "N":
            neighbour_table = ADDING(recv_info_LORA[1], neighbour_table)
            SEND_ACK(recv_info_LORA[1])
            RGB_LED(0x0000FF, 20)

        if recv_info_LORA[0] == "A" and recv_info_LORA[2] == MYID:
            neighbour_table = ADDING(recv_info_LORA[1], neighbour_table)
            RGB_LED(0x00FF00, 20)

        if recv_info_LORA[0] == "M" and recv_info_LORA[2] == MYID:
            s_UDP.sendto(recv_info_LORA[3], (IP_send,PORT))
            RGB_LED(0xFFFF00, 20)

    if(recv_info_UDP):
        try:
            SEND_MESSAGE(neighbour_table[1], recv_info_UDP.decode("utf-8"))
            RGB_LED(0xFFFFFF, 20)

        except IndexError as err:
            print(err)
            continue
>>>>>>> f4a6e0298e74872b3880ce2e43fded4baefc8745
