from machine import Pin, ADC
import time

POWER_PIN = 25  # GPIO25 connected to the VCC pin of water sensor
SIGNAL_PIN = 36  # ESP32 pin GPIO36 (ADC0) connected to the S pin

SENSOR_MIN = 100  # Value when sensor is dry
SENSOR_MAX = 360  # Value when sensor is fully submerged

power = Pin(POWER_PIN, Pin.OUT)
power.value(0)

signal = ADC(Pin(SIGNAL_PIN))
signal.width(ADC.WIDTH_12BIT)
signal.atten(ADC.ATTN_11DB)

def measure_water_level():
    power.value(1)
    time.sleep_ms(10)

    value = get_avg_measurement()

    power.value(0)
    time.sleep(0.2)

    value = max(value, SENSOR_MIN)

    linear_percentage = map_value(value, SENSOR_MIN, SENSOR_MAX, 0, 100)
    linear_percentage = max(0, min(100, linear_percentage))
    curved_percentage = apply_curve(linear_percentage)

    return curved_percentage

def get_avg_measurement():
    readings = []
    for _ in range(3):
        readings.append(signal.read())
        time.sleep_ms(5)

    return sum(readings) // len(readings)

def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

def apply_curve(percentage):
    """Apply a curve to make the sensor response more gradual
    This will reduce the sudden jump at the beginning (sensor does not measure in linear way)"""
    return int((percentage / 100) ** 2 * 100)


if __name__ == '__main__':
    while True:
        result = measure_water_level()
        print("Water level: " + str(result) + "%")