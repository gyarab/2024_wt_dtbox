import time
import ujson
import machine
from machine import Pin
import network

from dtbox.display.shortcuts import display
from dtbox.button.shortcuts import button_o, button_x
from dtbox.network.shortcuts import network as dtbox_network
from dtbox.mqtt.shortcuts import mqtt_client


WIFI_SSID = b"[vs-uk]"       
WIFI_PASSWORD = b"[7uvtqZn4xa]"

MQTT_TOPIC = b"dtbox/pressed"
alarm_trigger = False

def run_light_animation():
    display.show("Animation", 500)

def ensure_connected(network_module, client_instance, subscriptions=[]):
    wifi_ok = False
    broker_ok = False
    
    while not (wifi_ok and broker_ok):
        try:
            if not wifi_ok:
                print("w", end="")
                wifi_ok = network_module.connect() 
                if not wifi_ok: 
                    raise OSError("WiFi connection failed") 

            if wifi_ok and not broker_ok: 
                print("b", end="")
                client_instance.server = MQTT_BROKER_ADDRESS
                client_instance.port = MQTT_BROKER_PORT
                client_instance.connect() 
                broker_ok = True 
                for sub in subscriptions:
                    client_instance.subscribe(sub)
                    print(f"Subscribed to: {sub.decode()}")
                
        except (OSError, IndexError) as e:
            print(f". (Error: {e})", end="")
            wifi_ok = False   
            broker_ok = False 
            time.sleep(2) 
            display.show("CONN ERR", scroll=True)

    print("\nConnected to Wi-Fi and MQTT broker.")
    display.show("Connected", scroll=True)

def handle_mqtt_message(topic, message):
    global alarm_trigger

    topic_str = topic.decode()
    message_str = message.decode()

    print("MQTT zpráva:", topic_str, message_str)

    if topic == MQTT_TOPIC and message_str:
        if message_str == "0":
            alarm_trigger = False
            print("Alarm deactivated")
            display.show("ALARM OFF", 1000)
        else:
            alarm_trigger = True
            print("Alarm activated")
            display.show("ALARM ON", 1000)
            run_light_animation()

def on_button_press(pin=None):
    connected = dtbox_network.connect() 
    
    if connected:
        try:
            wlan_if = network.WLAN(network.STA_IF) 
            mac = wlan_if.config('mac') 

            mac_str = ':'.join('{:02X}'.format(b) for b in mac)
            print("MAC:", mac_str)

            display.show("MQTT...", scroll=True)
            mqtt_client.publish(MQTT_TOPIC, mac_str) 

            display.show("OK", scroll=True)

        except Exception as e:
            print("Chyba při MQTT:", e)
            display.show("ERROR", scroll=True)
    else:
        print("Failed to connect to Wi-Fi.")
        display.show("NO WIFI", scroll=True)

mqtt_client.set_callback(handle_mqtt_message)

ensure_connected(dtbox_network, mqtt_client, [MQTT_TOPIC])

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
    machine.reset()
