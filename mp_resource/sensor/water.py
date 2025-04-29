from machine import Pin, ADC
import time

POWER_PIN = 25
SIGNAL_PIN = 36

SENSOR_MIN = 100
SENSOR_MAX = 360

power = Pin(POWER_PIN, Pin.OUT)
power.value(0)

signal = ADC(Pin(SIGNAL_PIN))
signal.width(ADC.WIDTH_12BIT)
signal.atten(ADC.ATTN_11DB)


def get_full_result():
    power.value(1)
    time.sleep_ms(10)
    raw_value = signal.read()
    power.value(0)

    value = max(raw_value, SENSOR_MIN)

    linear_percentage = map_value(value, SENSOR_MIN, SENSOR_MAX, 0, 100)
    linear_percentage = max(0, min(100, linear_percentage))
    curved_percentage = apply_curve(linear_percentage)

    return {
        "raw_value": raw_value,
        "normalized_value": curved_percentage,
        "severity": "NONE"
    }


def get_raw_result():
    return signal.read()


def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min


def apply_curve(percentage):
    return int((percentage / 100) ** 2 * 100)

