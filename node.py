import time
import machine
import ujson

from dtbox.display.shortcuts import display
from dtbox.button.shortcuts import button_o, button_x
from dtbox.led.shortcuts import led
from dtbox.network.shortcuts import connect 
from dtbox.mqtt.shortcuts import connect_mqtt 

MQTT_TOPIC = b"dtbox/pressed"
alarm_trigger = False

def ensure_subscriptions(network_module, client, subscriptions=[]):
    wifi_connected = False
    broker_connected = False
    while not (wifi_connected and broker_connected):
        try:
            if not wifi_connected:
                print("w", end="")
                wifi_connected = network_module.connect()
            if not broker_connected:
                print("b", end="")
                client.connect()
                broker_connected = True
                for subscription in subscriptions:
                    client.subscribe(subscription)
        except (OSError, IndexError):
            print(".", end="")
            time.sleep(0.5)
    print()

def handle_message(topic, message):
    global alarm_trigger

    topic_str = topic.decode()
    message_str = message.decode()

    print("MQTT zpráva:", topic_str, message_str)

    if topic == MQTT_TOPIC and message_str:
        if message_str == "0":
            alarm_trigger = False
            print("Alarm deaktivován")
        else:
            alarm_trigger = True
            print("Alarm aktivován")
            run_light_animation()

def run_light_animation():
    led.set_lights(True, False, False, "CERVENA", 1000)
    led.set_lights(True, True, False, "PRIPRAV SE", 1000)
    led.set_lights(False, False, True, "JEĎ", 1000)
    display.show("LIGHTS!")

def send_mac_over_mqtt(pin=None):
    wlan = connect()
    mac = wlan.config('mac')
    mac_str = ':'.join('{:02X}'.format(b) for b in mac)
    print("MAC:", mac_str)

    try:
        display.show("MQTT...")
        client.publish(MQTT_TOPIC, mac_str)

        light_command = ujson.dumps({
            "command": "lights",
            "sequence": "go"
        })
        client.publish(MQTT_TOPIC, light_command)

        display.show("OK")

    except Exception as e:
        print("Chyba při MQTT:", e)
        display.show("ERROR")


client = connect_mqtt(callback=handle_message)
ensure_subscriptions(connect, client, [MQTT_TOPIC])

button_o.on_press(send_mac_over_mqtt)
button_x.on_press(send_mac_over_mqtt)

try:
    display.show("Ready")

    while True:
        client.check_msg()
        time.sleep(0.1)

except Exception as e:
    print("Chyba v hlavní smyčce:", e)
    display.show("ERROR")
    time.sleep(5)
    machine.reset()
