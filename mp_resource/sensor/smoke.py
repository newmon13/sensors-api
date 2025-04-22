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


def get_full_result():
    analog_result = signal.read()
    digital_result = digital_pin.value()

    normalized_value = normalize(analog_result)
    severity = get_severity(analog_result)

    return {
        "raw_value": analog_result,
        "normalized_value": normalized_value,
        "smoke_presence": not digital_result,
        "severity": severity
    }


def get_raw_result():
    return signal.read()


def normalize(value: int):
    if value <= SMOKE_THRESHOLD_LOW:
        normalized_level = 0
    elif value >= SMOKE_THRESHOLD_HIGH:
        normalized_level = 100
    else:
        normalized_level = ((value - SMOKE_THRESHOLD_LOW) / (SMOKE_THRESHOLD_HIGH - SMOKE_THRESHOLD_LOW)) * 100

    return normalized_level


def get_severity(level: float):
    severity = "NONE"
    if level > SMOKE_THRESHOLD_HIGH:
        severity = "HIGH"
    elif level > SMOKE_THRESHOLD_MEDIUM:
        severity = "MEDIUM"
    elif level > SMOKE_THRESHOLD_LOW:
        severity = "LOW"

    return severity
