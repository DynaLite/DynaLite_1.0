#http://lan.developer.lifx.com/docs/device-messages
#https://github.com/mclarkk/lifxlan

from lifxlan import *
import settings

devices = None

def connect():
    print("Discovering lights....")
    lifx = LifxLAN(settings.NUM_LIGHTS)
    #get devices
    global devices
    devices = lifx.get_lights()
    for i,v in enumerate(devices):
        v.set_label("Light" + str(i))


def setLighting(targetName,color):
    for device in devices:
        if device.get_label() == targetName:
            device.set_color(color,rapid = True)


def power(state):
    for device in devices:
        device.set_power(state,True)






