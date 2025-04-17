import network
import time
import config

WIFI_SSID = config.WIFI_CONFIG.get("ssid")
WIFI_PASSWORD = config.WIFI_CONFIG.get("password")

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to network...')
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        max_wait = 10
        while max_wait > 0:
            if wlan.isconnected():
                break
            max_wait -= 1
            print('Waiting for connection...')
            time.sleep(1)

    if wlan.isconnected():
        print('Connected to WiFi')
        print('Network config:', wlan.ifconfig())
        return True
    else:
        print('Could not connect to WiFi')
        return False