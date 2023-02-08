import argparse
import json
import logging
import os
from guizero import App, Text
from datetime import datetime


def send_message(message):
    publish.single(topic=mqtt_topic, hostname=mqtt_hostname, port=1883, auth=mqtt_auth, payload=message)
    logging.info(f'Message sent to topic ({mqtt_topic}): {message}')


def update_temperature():
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
        temp.value = f"{temperature}°C  -  {humidity}%"
    except RuntimeError as e:
        logging.error(f'Could not get data from sensor with error: {e}')


def update_time():
    time.value = datetime.now().strftime("%H:%M")


def update_date():
    date.value = datetime.now().strftime("%a, %d.%m")


app = App(title="Simple Desk-Clock", bg="#262A39")
app.full_screen = True
date = Text(app, text=datetime.now().strftime("%a, %d.%m."), size=62, color="#91ff0f")
date.repeat(10000, update_date)
dummy_1 = Text(app, text=" ", size=12)
time = Text(app, text=datetime.now().strftime("%H:%M"), size=168, color="#91ff0f")
time.repeat(2000, update_time)

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

    dummy_2 = Text(app, text=" ", size=2)
    temp = Text(app, text="Temperature", size=62, color="#91ff0f")
    temp.repeat(30000, update_temperature)

if args.mqtt:
    import paho.mqtt.publish as publish

    mqtt_topic = args.mqtt[0]
    mqtt_hostname = args.mqtt[1]
    mqtt_auth = {
        "username": args.mqtt[2],
        "password": args.mqtt[3]
    }


if __name__ == '__main__':
    script_path = os.path.dirname(os.path.realpath(__file__))
    logging.basicConfig(filename=f'{script_path}/desk_clock.log',
                        filemode='a', format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S', level=logging.INFO)
    logging.info(f"Starting app with temp {'enabled' if args.temp else 'disabled'} "
                 f"and mqtt {'enabled' if args.mqtt else 'disabled'}.")
    app.display()
