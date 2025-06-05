from dtbox.mqtt.shortcuts import mqtt_client, ensure_subscriptions
from dtbox.network.shortcuts import network
from dtbox.wsled.shortcuts import wsled
from random import randint


nodes = []
game_state = False #False is not playing and True is running game
nodes_to_click = 5
next_node = -1
pressed = True
MQTT_START, MQTT_REGISTER, MQTT_GAME, MQTT_PRESSED, MQTT_SIZE = "dtbox/start", "dtbox/register", "dtbox/game", "dtbox/next", "dtbox/size"
mqtt_client.set_callback(_handle_message)
ensure_subscriptions(network, mqtt_client, [MQTT_REGISTER, MQTT_GAME, MQTT_NEXT, MQTT_SIZE])


def _handle_message(topic, message):
    topic = topic.decode()
    message = message.decode()
    
    if topic == MQTT_START and message:
        chnge_game_state(bool(message))
        
    if !game_state:
        if topic == MQTT_REGISTER and message:
            add_node(message)
        elif topic == MQTT_SIZE and message:
            set_nodes_to_click(int(message))
    elif topic == MQTT_PRESSED and message:
        press(message)
    
        
def change_game_state(to_switch):
    global game_state
    game_state = to_switch
            
def add_node(MAC_adress):
    global nodes
    nodes.append(MAC_adress)
    
def set_nodes_to_click(x):
    global nodes_to_click
    nodes_to_click += x

def press(MAC):
    if MAC == nodes[next_node] and !pressed:
        pressed = !pressed
    
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
    
        
while True:
    mqtt_client.check_msg()
    if game_state and pressed:
        if get_next_node() is not None:
            mqtt_client.publish(MQTT_NEXT, nodes[next_node])

    
        
        
        