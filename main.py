import argparse
import json
import sys
from datetime import datetime

from PyQt6.QtCore import QTimer, QTime, Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel


class Window(QWidget):
    def __init__(self):
        super().__init__()
        # creating a vertical layout
        layout = QVBoxLayout()
        # changing the background color to yellow
        self.setStyleSheet("color: #ffd369; background-color: #222831;")
        self.setFixedSize(800, 480)
        font_date = QFont('Roboto', 45)
        font_date.setBold(True)
        font_time = QFont('Roboto', 130)
        font_time.setBold(True)
        self.date_label = QLabel()
        self.date_label.setFont(font_date)
        layout.addWidget(self.date_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.time_label = QLabel()
        self.time_label.setFont(font_time)

        if args.temp:
            font_temp = QFont('Roboto', 50)
            font_temp.setBold(True)
            self.container = QHBoxLayout()
            self.temp_label = QLabel()
            self.temp_label.setFont(font_temp)
            self.container.addWidget(self.temp_label, alignment=Qt.AlignmentFlag.AlignCenter)
            self.humidity_label = QLabel()
            self.humidity_label.setFont(font_temp)
            self.container.addWidget(self.humidity_label, alignment=Qt.AlignmentFlag.AlignCenter)
            alignment_time = Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom
        else:
            alignment_time = Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop
        layout.addWidget(self.time_label, alignment=alignment_time)

        if args.temp:
            layout.addLayout(self.container)

        self.setLayout(layout)
        self.timer = QTimer()
        self.timer.timeout.connect(self.show_time)
        self.timer.start(5000)

        if args.temp:
            self.timer_slow = QTimer(self)
            self.timer_slow.timeout.connect(self.show_temperature)
            self.timer_slow.start(5000)

    # method called by timer
    def show_time(self):
        current_time = QTime.currentTime()
        label_time = current_time.toString('hh:mm')
        label_date = datetime.now().strftime("%A, %d.%m.%Y")
        self.time_label.setText(label_time)
        self.date_label.setText(label_date)

    def show_temperature(self):
        temperature, humidity = get_temp()
        if temperature is not None:
            self.temp_label.setText(temperature + "°C")
        if humidity is not None:
            self.humidity_label.setText(humidity + "%")


def send_message(temperature, humidity):
    message = {
        "temperature": temperature,
        "humidity": humidity
    }
    publish.single(topic="home/office/clock", hostname=mqtt_hostname, auth=mqtt_auth, payload=json.dumps(message))


def get_temp():
    try:
        temperature = dhtDevice.temperature
        humidity = dhtDevice.humidity
        temperature = str(round(temperature, 2))
        humidity = str(round(humidity, 2))
        if args.mqtt:
            send_message(temperature, humidity)
        return temperature, humidity
    except RuntimeError:
        return None, None


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

# create pyqt5 app
App = QApplication(sys.argv)
window = Window()
window.show()
App.exit(App.exec())
