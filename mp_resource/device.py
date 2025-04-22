from machine import unique_id
from umqtt.simple import MQTTClient
from config.settings import BROKER_CONFIG
import ubinascii
import ujson as json
import network
import utime

DEVICE_ID = ubinascii.hexlify(unique_id()).decode('utf-8')
DISCOVERY_TOPIC = "system/discovery".encode()
STATUS_TOPIC = f"devices/{DEVICE_ID}/status".encode()
HEARTBEAT_TOPIC = f"devices/{DEVICE_ID}/heartbeat".encode()

STATUS_ONLINE = "online"
STATUS_OFFLINE = "offline"


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

    status_data = prepare_status_data(STATUS_OFFLINE)
    client.set_last_will(
        STATUS_TOPIC,
        status_data,
        retain=True
    )

    client.connect()
    print(f"Connected to MQTT broker at {BROKER_CONFIG['host']}:{BROKER_CONFIG['port']}")

    status_data = prepare_status_data(STATUS_ONLINE)
    client.publish(STATUS_TOPIC, status_data, retain=True)

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

    status_data = prepare_status_data(STATUS_ONLINE)
    mqtt_client.publish(
        STATUS_TOPIC,
        status_data,
        retain=True
    )


def prepare_status_data(status_str: str):
    status_data = {
        "device_id": DEVICE_ID,
        "status": status_str,
        "timestamp": utime.time()
    }

    return json.dumps(status_data).encode()
