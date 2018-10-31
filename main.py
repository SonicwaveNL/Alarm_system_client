#!/usr/bin/python3

# Import libraries
from urllib.request import urlopen
from gpiozero import *
from time import sleep

# Server settings
hostname = "192.168.42.6:5000"

# Input presets
btn_switch = Button(2)
btn_alarm = Button(27)

# Ouput presets
led_Red = LED(3)
led_Yellow = LED(4)
led_Green = LED(17)
buzzer_alarm = Buzzer(22)

# Client settings
client = True
alarm = False
first_check = True


# Setup of the connection to the server
def httpconnect(action):
    url = 'http://{}/{}'.format(hostname, action)
    try:
        print(urlopen(url).read().decode())
    except:
        print("Couldn't connect to {}".format(url))
        exit()


# Sets the client to status: offline
def client_offline():
    global client
    global alarm

    client = False
    alarm = False
    switch_client(False)
    print("Client is offline\n")


# Sets the client to status: online
def client_online():
    global client
    global alarm

    client = True
    alarm = True
    switch_client(True)
    print("Client is on\n")


# Switches the client to the opposite status when activated
def switch_client(status):
    if status:
        print("Client alarm off...\n")
        sleep(1)
        led_Green.off()
        progress()
        sleep(1)
        led_Red.on()

    else:
        print("Turning client on...\n")
        sleep(1)
        led_Red.off()
        progress()
        sleep(1)
        led_Green.on()


# Alarm of the client
def switch_alarm():
    alarm_status = 0

    while alarm_status < 5:
        sleep(0.5)
        buzzer_alarm.on()
        led_Red.off()
        sleep(0.5)
        buzzer_alarm.off()
        led_Red.on()
        alarm_status += 1


# Sents a 'alarm: ON' state to the server
def alarm_on():
    global alarm

    switch_alarm()
    alarm = False
    httpconnect('alarm/on')


# Sents a 'alarm: OFF' state to the server
def alarm_off():
    global alarm

    alarm = True
    httpconnect('alarm/off')


def progress():
    blink = 0

    while blink < 3:
        sleep(0.5)
        led_Yellow.on()
        sleep(0.5)
        led_Yellow.off()
        blink += 1


client_offline()

# Begin main function
while True:

    # First connection to the server
    if first_check:
        httpconnect('')
        first_check = False

    # Execute when black button is pressed
    if btn_switch.is_pressed:

        print("Switching system!")

        if client:
            sleep(.5)
            client_offline()

        else:
            sleep(.5)
            client_online()

    # Execute when red button is pressed
    if btn_alarm.is_pressed:

        print("Switching alarm!")

        if alarm:
            sleep(.5)
            alarm_on()

        else:
            sleep(.5)
            alarm_off()
