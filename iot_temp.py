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

from dtbox.influxdb.shortcuts import influxdb
from dtbox.thermometer.shortcuts import thermometer
from dtbox.display.shortcuts import display
from dtbox.network.shortcuts import network
from dtbox.led.shortcuts import led_amber, led_green
from time import sleep


def ensure_wifi(network=network):
    global led_amber
    global led_green

    wifi_connected = False
    while not wifi_connected:
        led_amber.value(0)
        led_green.value(0)
        print("Ensuring WiFi: ", end="")
        try:
            if not wifi_connected:
                print("x", end="")
                wifi_connected = network.connect()
        except (OSError, IndexError):
            print(".", end="")
            pass
        if wifi_connected:
            print("C")
            led_amber.value(0)
            led_green.value(1)
        else:
            led_green.value(0)
            led_amber.value(1)


print("DEMO thermometer_display_cloud")


ensure_wifi()
influxdb.check_server()

while True:
    try:
        temp = thermometer.get_temp()
        print("Temperature {}".format(temp))

        display.show(temp, align_right=True)

        ensure_wifi()
        print("InfluxDB write")
        influxdb.write(value=temp)

    except Exception as exc:
        print(exc)
    print('...')
    sleep(5)



