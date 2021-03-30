from time import sleep

import RPi.GPIO as GPIO
import paho.mqtt.client as paho
import smbus
from apds9960 import APDS9960

port = 1
bus = smbus.SMBus(port)
apds = APDS9960(bus)

# hostname
broker = "192.168.2.1"
# port
port = 1883


def on_publish(client, userdata, result):
    print("Device 1 : Data published.")
    pass


client = paho.Client("admin")
client.on_publish = on_publish
client.connect(broker, port)


def intH(channel):
    print("INTERRUPT")


GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN)
try:
    # Interrupt-Event hinzufuegen, steigende Flanke
    GPIO.add_event_detect(7, GPIO.FALLING, callback=intH)

    apds.setProximityIntLowThreshold(50)

    print("Proximity Sensor Test")
    print("=====================")
    apds.enableProximitySensor()
    oval = -1
    while True:
        sleep(0.25)
        val = apds.readProximity()
        if val != oval:
            print("proximity={}".format(val))
            oval = val

            if val > 200:
                ret = client.publish("/data", "Nearby val=" + val)

finally:
    GPIO.cleanup()
    print("Bye")
