import argparse
import json
import logging
import os

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/getMetrics')
def get_metrics():
    return get_temp()


def send_message(message):
    publish.single(topic="office/sensor1", hostname=mqtt_hostname, port=1883, auth=mqtt_auth, payload=message)
    logging.info(f'Message sent: {message}')


def get_temp():
    try:
        temperature = dhtDevice.temperature
        humidity = dhtDevice.humidity
        temperature = str(round(temperature, 2))
        humidity = str(round(humidity, 2))
        message = json.dumps({
            "temperature": temperature,
            "humidity": humidity
        })
        if args.mqtt:
            send_message(message)
        return message
    except RuntimeError:
        return json.dumps({"Error": "No data"}), 204


parser = argparse.ArgumentParser(description='Simple Desk-Clock (TME).')
parser.add_argument('--temp', dest='temp', action='store_true',
                    help='Activate temperature sensor.')
parser.add_argument('--mqtt', nargs='+', dest='mqtt', action='store',
                    help='Activate mqtt output (connection string).')
args = parser.parse_args()

if args.temp:
    import adafruit_dht
    import board

    # initial device
    dhtDevice = adafruit_dht.DHT22(board.D2)

if args.mqtt:
    import paho.mqtt.publish as publish

    mqtt_hostname = args.mqtt[0]
    mqtt_auth = {
        "username": args.mqtt[1],
        "password": args.mqtt[2]
    }

if __name__ == '__main__':
    script_path = os.path.dirname(os.path.realpath(__file__))
    logging.basicConfig(filename=f'{script_path}/metrics_sender.log',
                        filemode='a', format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S', level=logging.INFO)
    app.run('0.0.0.0', 8080)
