from dtbox.display.shortcuts import display
from dtbox.button.shortcuts import button_o, button_x
from dtbox.network.shortcuts import network
from hra.mqtt.shortcuts import mqtt_client, ensure_subscriptions
from dtbox.wsled.shortcuts import wsled
from dtbox.pinout import PIN_LED_RED, PIN_LED_AMBER, PIN_LED_GREEN
from dtbox.led import *
from dtbox.boot import *
from dtbox.colors import *
from machine import Pin
from time import sleep

hostname_str = hostname()

red = Pin(PIN_LED_RED, Pin.OUT)
yellow = Pin(PIN_LED_AMBER, Pin.OUT)
green = Pin(PIN_LED_GREEN, Pin.OUT)

MQTT_TOPIC = "dtbox/game"
display.show("....")

def zprava(topic, message):
    if topic.decode() == MQTT_TOPIC and message.decode() == hostname_str:
        nastav_barvu(PURPLE)
        print(f"MQTT zpráva: {topic}: {message}")
        red.on()
        yellow.on()
        green.on()
        display.show("8.8.8.8.")

def zhasni():
    mqtt_client.publish("dtbox/pressed", hostname_str)
    nastav_barvu(BLACK)
    red.off()
    yellow.off()
    green.off()
    display.show("    ")

def nastav_barvu(barva):
    wsled.color(barva)

mqtt_client.set_callback(zprava)
ensure_subscriptions(network, mqtt_client, [MQTT_TOPIC])
mqtt_client.publish("dtbox/register", hostname_str)

button_o.on_press(zhasni)
button_x.on_press(zhasni)

display.show("    ")

while True:
    sleep(0.1)
    mqtt_client.check_msg()

