#!/usr/bin/python3

from urllib.request import urlopen


hostname = "192.168.42.6:5000"


def httpconnect(action):
    url = 'http://{}/{}'.format(hostname, action)
    try:
        print(urlopen(url).read().decode())
    except:
        print("Couldn't connect to {}".format(url))
        exit()

httpconnect('')