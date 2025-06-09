import time
import ujson
import machine
from machine import Pin
import network

from dtbox.button.shortcuts import button_o, button_x
from dtbox.network.shortcuts import network as dtbox_network
from dtbox.mqtt.shortcuts import mqtt_client, ensure_subscriptions     
from dtbox import colors  # definice barev v /lib > RED, GREEN, BLUE, ORANGE, BLACK (nesvítí)
from dtbox.wsled.shortcuts import wsled

MQTT_TOPIC_GAME = "dtbox/game"
MQTT_TOPIC_PRESSED = "dtbox/pressed"
alarm_trigger = False

def handle_mqtt_message(topic, message):
    global alarm_trigger

    topic_str = topic.decode()
    message_str = message.decode()

    print("MQTT zpráva:", topic_str, message_str)

    if topic_str == MQTT_TOPIC_GAME and message_str == hostname():
        wsled.color(colors.PURPLE)

def on_button_press():
    mqtt_client.publish(MQTT_TOPIC_PRESSED, hostname()) 
    wsled.color(colors.BLACK)

mqtt_client.set_callback(handle_mqtt_message)

ensure_subscriptions(dtbox_network, mqtt_client, [MQTT_TOPIC_GAME])
mqtt_client.publish("dtbox/register", hostname())

button_o.on_press(on_button_press)
button_x.on_press(on_button_press)

while True:
    mqtt_client.check_msg()
    time.sleep_ms(5)
