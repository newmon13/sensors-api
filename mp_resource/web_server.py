from lib.microdot import Microdot, Response
import json
import water_sensor
import smoke_sensor

app = Microdot()

@app.route('/api/water-sensor')
def get_water_sensor_data(request):
    value = water_sensor.measure_water_level()

    data = {
        'water_level': value,
    }

    return Response(json.dumps(data), headers={'Content-Type': 'application/json'})

@app.route('/api/smoke-sensor')
def get_smoke_sensor_data(request):
    value = smoke_sensor.measure_smoke_level()
    return Response(json.dumps(value), headers={'Content-Type': 'application/json'})
