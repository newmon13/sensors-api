from lib.microdot import Microdot, Response
import json
from sensor import smoke, water

app = Microdot()

@app.route('/api/water-sensor')
def get_water_sensor_data(request):
    value = water_sensor.get_full_result()

    data = {
        'water_level': value,
    }

    return Response(json.dumps(data), headers={'Content-Type': 'application/json'})

@app.route('/api/smoke-sensor')
def get_smoke_sensor_data(request):
    value = smoke_sensor.get_full_result()
    return Response(json.dumps(value), headers={'Content-Type': 'application/json'})
