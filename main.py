import Adafruit_DHT
import sys
from PyQt5.QtCore import QTimer, QDateTime
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QFont

class DHT22GUI(QWidget):
    def __init__(self):
        super().__init()

        self.sensor = Adafruit_DHT.DHT22
        self.sensor_pin = 4

        self.init_ui()

        # Create a QTimer for automatic updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.read_sensor_data)
        self.timer.start(60000)  # 60,000 milliseconds = 60 seconds

    def init_ui(self):
        self.setStyleSheet("background-color: black; color: white;")

        self.result_label = QLabel(self)
        self.result_label.setFont(QFont("Helvetica", 16))

        layout = QVBoxLayout()
        layout.addWidget(self.result_label)
        # No need to add the buttons here

        self.setLayout(layout)

        self.read_sensor_data()

        self.setWindowTitle("DHT22-GUI")
        self.setGeometry(100, 100, 400, 200)

    def read_sensor_data(self):
        humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.sensor_pin)
        if humidity is not None and temperature is not None:
            current_time = QDateTime.currentDateTime().toString("HH:mm:ss")
            data = "Last update: {}\nTemperature: {:.1f}°C\nHumidity: {:.1f}%".format(current_time, temperature, humidity)
            self.result_label.setText(data)
        else:
            self.result_label.setText("Sensor failure.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DHT22GUI()
    window.show()
    sys.exit(app.exec_())
