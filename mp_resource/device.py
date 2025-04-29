from machine import unique_id
from umqtt.simple import MQTTClient
from config.settings import BROKER_CONFIG
import ubinascii
import ujson as json
import network

DEVICE_ID = ubinascii.hexlify(unique_id()).decode('utf-8')
DISCOVERY_TOPIC = "system/discovery".encode()
HEARTBEAT_TOPIC = f"devices/{DEVICE_ID}/heartbeat".encode()

def get_ip_address():
    wlan = network.WLAN(network.STA_IF)
    if wlan.isconnected():
        return wlan.ifconfig()[0]
    return None


def initialize_mqtt_client():
    client_id = f"{DEVICE_ID}".encode()

    client = MQTTClient(
        client_id,
        BROKER_CONFIG['host'],
        BROKER_CONFIG['port'],
        keepalive=60
    )

    client.connect()
    print(f"Connected to MQTT broker at {BROKER_CONFIG['host']}:{BROKER_CONFIG['port']}")
    return client


def register_device(mqtt_client: MQTTClient, sensors: list):
    ip_address = get_ip_address()

    device_details = {
        "device_id": DEVICE_ID,
        "ip_address": ip_address,
        "sensors": sensors,
    }

    mqtt_client.publish(
        DISCOVERY_TOPIC,
        json.dumps(device_details).encode()
    )
    print(f"Device {DEVICE_ID} registered with discovery service")
    if ip_address:
        print(f"Device IP: {ip_address}")
