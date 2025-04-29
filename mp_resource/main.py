import device
from config import wifi_setup
from config.settings import INSTALLED_SENSORS
from mqtt.publisher import start_publishing
from sensor.smoke import get_full_result as get_smoke_full_result
from sensor.water import get_full_result as get_water_full_result
import mqtt.heartbeat as heartbeat
import ntptime


def main():
    if wifi_setup.connect_wifi():
        print('Starting Microdot server...')
        mqtt_client = device.initialize_mqtt_client()
        device.register_device(mqtt_client, INSTALLED_SENSORS)
        ntptime.settime()

        heartbeat.start_heartbeat(mqtt_client)

        start_publishing(mqtt_client, get_smoke_full_result, "smoke")
        start_publishing(mqtt_client, get_water_full_result, "water")


if __name__ == '__main__':
    main()
