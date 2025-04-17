import wifi_setup

SSID = '_'
PASSWORD = '123zxcvbnm'


def main():
    if wifi_setup.connect_wifi(SSID, PASSWORD):
        print('Starting Microdot server...')

if __name__ == '__main__':
    main()