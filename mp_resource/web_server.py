from lib.microdot import Microdot, Response
import json
import water_sensor

app = Microdot()

@app.route('/api/water-sensor')
def get_data(request):
    value = water_sensor.measure_water_level()

    data = {
        'water_level': value,
    }

    return Response(json.dumps(data), headers={'Content-Type': 'application/json'})
