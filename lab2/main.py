"""Запуск приложения и соединение сигналов со слотами"""

import sys

from PyQt5.QtWidgets import QApplication

from cl1 import TemperatureModel
from cl2 import WeatherWindow


class MainWindow(WeatherWindow):
    def __init__(self):
        super().__init__()
        self.model = TemperatureModel(self)
        self.celsius.valueChanged.connect(self.model.set_celsius)
        self.fahrenheit.valueChanged.connect(self.model.set_fahrenheit)
        self.kelvin.valueChanged.connect(self.model.set_kelvin)
        self.model.temperatures_changed.connect(self.update_temperatures)
        self.reset_button.clicked.connect(self.reset_temperature)
        self.model.publish()

    def reset_temperature(self):
        self.model.set_celsius(20.0)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())
