from machine import Pin, ADC

DIGITAL_SIGNAL_PIN = 15
ANALOG_SIGNAL_PIN = 39

digital_pin = Pin(DIGITAL_SIGNAL_PIN, Pin.IN)
analog_pin = Pin(ANALOG_SIGNAL_PIN, Pin.IN)

signal = ADC(analog_pin)
signal.width(ADC.WIDTH_12BIT)
signal.atten(ADC.ATTN_11DB)

SMOKE_THRESHOLD_LOW = 600
SMOKE_THRESHOLD_MEDIUM = 900
SMOKE_THRESHOLD_HIGH = 1300

def measure_smoke_level():
    analog_result = signal.read()
    digital_result = digital_pin.value()

    normalized_value = normalize_smoke_level(analog_result)
    severity = get_smoke_level_severity(analog_result)

    return {
        "raw_value": analog_result,
        "smoke_presence": not digital_result,
        "normalized_value": normalized_value,
        "severity": severity
    }

def normalize_smoke_level(value: int):
    if value <= SMOKE_THRESHOLD_LOW:
        normalized_level = 0
    elif value >= SMOKE_THRESHOLD_HIGH:
        normalized_level = 100
    else:
        normalized_level = ((value - SMOKE_THRESHOLD_LOW) / (SMOKE_THRESHOLD_HIGH - SMOKE_THRESHOLD_LOW)) * 100

    return normalized_level

def get_smoke_level_severity(level: float):
    severity = "None"
    if level > SMOKE_THRESHOLD_HIGH:
        severity = "High"
    elif level > SMOKE_THRESHOLD_MEDIUM:
        severity = "Medium"
    elif level > SMOKE_THRESHOLD_LOW:
        severity = "Low"

    return severity

if __name__ == '__main__':
    import time
    while True:
        result = measure_smoke_level()
        print(result)
        time.sleep(1)