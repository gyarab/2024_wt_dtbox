from dtbox.display.shortcuts import display
from dtbox.button.shortcuts import button_o, button_x
from dtbox.network.shortcuts import network
from dtbox.mqtt.shortcuts import mqtt_client, ensure_subscriptions
from dtbox.pinout import PIN_LED_RED, PIN_LED_AMBER, PIN_LED_GREEN
from machine import Pin
from time import sleep
red = Pin(PIN_LED_RED, Pin.OUT)
yellow = Pin(PIN_LED_AMBER, Pin.OUT)
green = Pin(PIN_LED_GREEN, Pin.OUT)

MQTT_TOPIC = "dtbox/game"
delka = 10
display.show("....")

def do_nothing(a, b):
    pass

def zprava(topic, message):
    if topic == MQTT_TOPIC and message == hostname:
        mqtt_client.set_callback(do_nothing)
        button_o.on_press(zhasni)
        button_x.on_press(zhasni)
        red.on()
        yellow.on()
        green.on()
        display.show("8888")

def zhasni():
    mqtt_client.publish("dtbox/pressed", "")
    mqtt_client.set_callback(zprava)
    button_o._on_press_callbacks.clear()
    button_x._on_press_callbacks.clear()
    red.off()
    yellow.off()
    green.off()
    display.show("    ")

mqtt_client.set_callback(zprava)
ensure_subscriptions(network, mqtt_client, [MQTT_TOPIC])
mqtt_client.publish("dtbox/register", hostname)

display.show("    ")

while True:
    sleep(5)
    ensure_subscriptions(network, mqtt_client, [MQTT_TOPIC])
