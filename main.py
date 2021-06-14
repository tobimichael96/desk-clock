import argparse
import sys
from datetime import datetime

from PyQt5.QtCore import QTimer, QTime, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel


class Window(QWidget):

    def __init__(self):
        super().__init__()
        # creating a vertical layout
        layout = QVBoxLayout()
        # changing the background color to yellow
        self.setStyleSheet("color: #ffd369; background-color: #222831;")
        self.setFixedSize(800, 480)

        font_day = QFont('Roboto', 50, QFont.Bold)
        font_date = QFont('Roboto', 40, QFont.Bold)
        font_time = QFont('Roboto', 117, QFont.Bold)
        self.container = QHBoxLayout()
        self.day_label = QLabel()
        self.day_label.setFont(font_day)
        self.container.addWidget(self.day_label, alignment=Qt.AlignCenter)
        self.date_label = QLabel()
        self.date_label.setFont(font_date)
        self.container.addWidget(self.date_label, alignment=Qt.AlignCenter)
        self.time_label = QLabel()
        self.time_label.setFont(font_time)

        if args.temp:
            font_temp = QFont('Roboto', 45, QFont.Bold)
            self.container2 = QHBoxLayout()
            self.temp_label = QLabel()
            self.temp_label.setFont(font_temp)
            self.container2.addWidget(self.temp_label, alignment=Qt.AlignCenter)
            self.humidity_label = QLabel()
            self.humidity_label.setFont(font_temp)
            self.container2.addWidget(self.humidity_label, alignment=Qt.AlignCenter)
            alignment_time = Qt.AlignHCenter | Qt.AlignBottom
        else:
            alignment_time = Qt.AlignHCenter | Qt.AlignTop

        layout.addLayout(self.container)
        layout.addWidget(self.time_label, alignment=alignment_time)
        if args.temp:
            layout.addLayout(self.container2)
        self.setLayout(layout)
        timer = QTimer(self)
        timer.timeout.connect(self.show_time)
        timer.start(1000)

        if args.temp:
            timer_slow = QTimer(self)
            timer_slow.timeout.connect(self.show_date)
            timer_slow.start(5000)

    # method called by timer
    def show_time(self):
        current_time = QTime.currentTime()
        label_day = datetime.now().strftime("%A")
        label_time = current_time.toString('hh:mm:ss')
        label_date = datetime.now().strftime("%d.%m.%Y")
        self.day_label.setText(label_day)
        self.time_label.setText(label_time)
        self.date_label.setText(label_date)

    def show_date(self):
        temp, humidity = get_temp()
        if temp is not None:
            self.temp_label.setText(temp + "°C")
        if humidity is not None:
            self.humidity_label.setText(humidity + "%")


def get_temp():
    try:
        # Print the values to the serial port
        temp = dhtDevice.temperature
        humidity = dhtDevice.humidity
        temp = str(round(temp, 2))
        humidity = str(round(humidity, 2))
        return temp, humidity
    except RuntimeError:
        return None, None


parser = argparse.ArgumentParser(description='Simple Desk-Clock (TME).')
parser.add_argument('--temp', dest='temp', action='store_true',
                    help='Activate temperature sensor.')
args = parser.parse_args()

if args.temp:
    import adafruit_dht
    import board

    # initial device
    dhtDevice = adafruit_dht.DHT22(board.D4)

# create pyqt5 app
App = QApplication(sys.argv)
window = Window()
window.show()
App.exit(App.exec_())
