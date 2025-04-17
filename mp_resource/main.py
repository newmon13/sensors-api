import web_server
import wifi_setup

def main():

    if wifi_setup.connect_wifi():
        print('Starting Microdot server...')
        try:
            web_server.app.run(port=8081, debug=True)
        except KeyboardInterrupt:
            print('Server stopped')


if __name__ == '__main__':
    main()