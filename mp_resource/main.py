import web_server
import wifi_setup
import config

def main():
    if wifi_setup.connect_wifi():
        print('Starting Microdot server...')
        try:
            web_server.app.run(port=config.SERVER_CONFIG.get("port"), debug=True)
        except KeyboardInterrupt:
            print('Server stopped')

if __name__ == '__main__':
    main()