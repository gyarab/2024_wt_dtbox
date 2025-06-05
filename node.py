import time
import ujson
import machine
from machine import Pin
import network

from dtbox.display.shortcuts import display
from dtbox.button.shortcuts import button_o, button_x
from dtbox.network.shortcuts import network as dtbox_network
from dtbox.mqtt.shortcuts import mqtt_client, ensure_subscriptions     

MQTT_TOPIC_GAME = "dtbox/game"
MQTT_TOPIC_PRESSED = "dtbox/pressed"
alarm_trigger = False

def run_light_animation():
    display.show("Animation", 500)

def handle_mqtt_message(topic, message):
    global alarm_trigger

    topic_str = topic.decode()
    message_str = message.decode()

    print("MQTT zpráva:", topic_str, message_str)

    if topic_str == MQTT_TOPIC_GAME and message_str:
        if message_str == hostname():
            display.show("here")

def on_button_press(pin=None):
    mqtt_client.publish(MQTT_TOPIC_PRESSED, hostname()) 
    display.show(".")

mqtt_client.set_callback(handle_mqtt_message)

ensure_subscriptions(dtbox_network, mqtt_client, [MQTT_TOPIC_GAME])

mqtt_client.publish("dtbox/register", hostname())

button_o.on_press(on_button_press)
button_x.on_press(on_button_press)

try:
    display.show("Ready", scroll=True)

    while True:
        mqtt_client.check_msg()
        time.sleep(0.1)

except Exception as e:
    print("Chyba v hlavní smyčce:", e)
    display.show("FATAL ERR", scroll=True)
    time.sleep(5)
    # machine.reset()
