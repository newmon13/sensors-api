import network
import time
from config.settings import WIFI_CONFIG

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if establish_wifi_connection(wlan):
        print_connection_details(wlan)
    return wlan.isconnected()

def establish_wifi_connection(wlan: network.WLAN):
    print('Connecting to network...')
    wlan.connect(WIFI_CONFIG['ssid'], WIFI_CONFIG['password'])
    max_wait = 10
    while max_wait > 0:
        if wlan.isconnected():
            break
        max_wait -= 1
        print('Waiting for connection...')
        time.sleep(1)

    return wlan.isconnected()

def print_connection_details(wlan: network.WLAN):
    if wlan.isconnected():
        print('Connected to WiFi')
        print('Network config:', wlan.ifconfig())
