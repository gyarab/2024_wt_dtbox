from . import MQTTClient



mqtt_client = MQTTClient.from_config()


def ensure_subscriptions(network, client, subscriptions=[]):
    wifi_connected = False
    broker_connected = False
    while not (wifi_connected and broker_connected):
        try:
            if not wifi_connected:
                print("w", end="")
                wifi_connected = network.connect()
            if not broker_connected:
                print("b", end="")
                client.connect()
                broker_connected = True
                for subscription in subscriptions:
                    client.subscribe(subscription)
        except (OSError, IndexError):
            print(".", end="")
            pass
    print()


