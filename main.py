"""
DT-Box main.py

Put your own code in this file.
It will be executed after device boot.
"""

show_version()

#from demos import led
#from demos import wsled
#from demos import wsled_matrix
#from demos import display_animate
#from demos import temperature_display
#from demos import temperature_display_cloud
#from demos import distance_display
#from demos import buzzer_melody
#from demos import mqtt_alarm
#from demos import servo

#test(display_steps=False)



from dtbox.mqtt.shortcuts import mqtt_client, ensure_subscriptions
from dtbox.network.shortcuts import network
from dtbox.wsled.shortcuts import wsled
from random import randint
from time import sleep
from dtbox.button.shortcuts import button_o
from dtbox.display.shortcuts import display
from dtbox.led.shortcuts import led_amber, led_green


nodes = []
game_state = False #False is not playing and True is running game
nodes_to_click = 10
next_node = -1
pressed = True
MQTT_START, MQTT_REGISTER, MQTT_GAME, MQTT_PRESSED, MQTT_SIZE = "dtbox/start", "dtbox/register", "dtbox/game", "dtbox/next", "dtbox/size"

def _handle_message(topic, message):
    topic = topic.decode()
    message = message.decode()
    
    if topic == MQTT_START and message:
        change_game_state(bool(message))
        
    if not game_state:
        if topic == MQTT_REGISTER and message:
            add_node(message)
        elif topic == MQTT_SIZE and message:
            set_nodes_to_click(int(message))
    elif topic == MQTT_PRESSED and message:
        press(message)



mqtt_client.set_callback(_handle_message)
ensure_subscriptions(network, mqtt_client, [MQTT_START, MQTT_REGISTER, MQTT_GAME, MQTT_PRESSED, MQTT_SIZE])
        
def change_game_state(to_switch): 
    global game_state
    print(to_switch, "to swtch")
    game_state = to_switch
            
def add_node(MAC_adress):
    global nodes
    print(MAC_adress, "MAC adress")
    nodes.append(MAC_adress)
    
def set_nodes_to_click(x):
    global nodes_to_click
    print(x, "num")
    nodes_to_click = x

def press(MAC):
    print(MAC, "MAC")
    if len(nodes) <= 1:
        change_game_state(False)
    if MAC == nodes[next_node] and not pressed:
        pressed = not pressed
    
def get_next_node():
    global next_node
    if len(nodes) <= 1:
        change_game_state(False)
        return None
    try_next_node = randint(0, len(nodes))
    while try_next_node != next_node:
        try_next_node = randint(0, len(nodes))
    next_node = try_next_node
    return next_node
   
running = True

def leave():
    global running
    running = False
    
button_o.on_press(leave)
        
while running:
    try:
        mqtt_client.check_msg()
        if game_state and pressed:
            if get_next_node() is not None:
                mqtt_client.publish(MQTT_GAME, nodes[next_node])
        sleep(0.1)
    except Exception as e:
        print("Chyba při MQTT:", e)
        display.show("ERROR")
        

        
        

