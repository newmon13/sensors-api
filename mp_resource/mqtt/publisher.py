from collections import deque
from lib.simple import MQTTClient
from device import DEVICE_ID
import _thread
import utime
import json

BASE_TOPIC: str = f"devices/{DEVICE_ID}/sensors"
SENSOR_READ_VALUE_THRESHOLD = 50

lock = _thread.allocate_lock()


def start_publishing(mqtt_client: MQTTClient, get_measurement, topic):
    _thread.start_new_thread(publishing_thread_function, (mqtt_client, get_measurement, topic,))


def publishing_thread_function(mqtt_client: MQTTClient, get_measurement, topic: str):
    measurements = deque([], 4)
    while True:
        sensor_data = get_measurement()
        measurements.append(sensor_data.get("raw_value"))
        if exceeds_threshold(measurements, SENSOR_READ_VALUE_THRESHOLD):
            full_new_topic = f"{BASE_TOPIC}/{topic}".encode()
            lock.acquire()
            mqtt_client.publish(full_new_topic, json.dumps(sensor_data))
            lock.release()
        utime.sleep(2)


def exceeds_threshold(measurements: deque, threshold):
    if len(measurements) < 2:
        return False

    oldest_value = measurements[0]
    latest_value = measurements[-1]

    return abs(oldest_value - latest_value) > threshold
