import _thread
import utime
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
            "heartbeat": "alive",
            "timestamp": utime.time()
        }
        lock.acquire()
        mqtt_client.publish(HEARTBEAT_TOPIC, json.dumps(heartbeat_data).encode())
        lock.release()
        utime.sleep(HEARTBEAT_INTERVAL_SECONDS)