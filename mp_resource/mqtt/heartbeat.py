import _thread
import time
import json
from lib.simple import MQTTClient
import ubinascii
from machine import unique_id

DEVICE_ID = ubinascii.hexlify(unique_id()).decode('utf-8')
HEARTBEAT_TOPIC = f"devices/{DEVICE_ID}/heartbeat"
HEARTBEAT_INTERVAL_SECONDS = 10

lock = _thread.allocate_lock()

def start_heartbeat(mqtt_client: MQTTClient):
    _thread.start_new_thread(heartbeat_thread_function, (mqtt_client,))


def heartbeat_thread_function(mqtt_client: MQTTClient):
    while True:
        heartbeat_data = {
            "timestamp": get_unix_timestamp()
        }
        lock.acquire()
        mqtt_client.publish(HEARTBEAT_TOPIC, json.dumps(heartbeat_data).encode())
        lock.release()
        time.sleep(HEARTBEAT_INTERVAL_SECONDS)

def get_unix_timestamp():
    y2k_timestamp = time.time()
    unix_timestamp = y2k_timestamp + 946684800
    return int(unix_timestamp)