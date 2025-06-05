from dtbox.display.shortcuts import display
from dtbox.button.shortcuts import button_o, button_x
from dtbox.network.shortcuts import network, ensure_wifi
from dtbox.mqtt.shortcuts import mqtt_client, ensure_subscriptions
from time import sleep

MQTT_TOPIC = "dtbox/size"
delka = 10
display.show("....")

def do_nothing(a, b):
    pass

def plus():
    global delka
    ensure_wifi()
    delka += 1
    strdelka = str(delka)
    mqtt_client.publish(MQTT_TOPIC, strdelka)
    display.show(strdelka)

def minus():
    global delka
    if delka == 1: return
    ensure_wifi()
    delka -= 1
    strdelka = str(delka)
    mqtt_client.publish(MQTT_TOPIC, strdelka)
    display.show(strdelka)

button_o.on_press(plus)
button_x.on_press(minus)

display.show(delka)

mqtt_client.set_callback(do_nothing)
ensure_subscriptions(network, mqtt_client, [MQTT_TOPIC])

while True:
    sleep(10)

