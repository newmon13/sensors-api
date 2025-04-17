import network
import time
from lib.microdot import Microdot, Response
import json
import water_sensor
import web_server
import wifi_setup

SSID = 'UPC1117673'
PASSWORD = 'zvzukx7sswpmuweV'


def main():

    if wifi_setup.connect_wifi(SSID, PASSWORD):

        print('Starting Microdot server...')
        try:
            web_server.app.run(port=8081, debug=True)
        except KeyboardInterrupt:
            print('Server stopped')


if __name__ == '__main__':
    main()