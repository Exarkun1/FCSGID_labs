"""Модель температуры и пользовательский сигнал об изменении данных"""

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

from utils import (
    MIN_CELSIUS, MAX_CELSIUS,
    celsius_to_fahrenheit, celsius_to_kelvin,
    fahrenheit_to_celsius, kelvin_to_celsius,
)


class TemperatureModel(QObject):
    # Одно событие передаёт согласованные значения во всех трёх шкалах
    temperatures_changed = pyqtSignal(float, float, float)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._celsius = 20.0

    def values(self):
        return (
            self._celsius,
            celsius_to_fahrenheit(self._celsius),
            celsius_to_kelvin(self._celsius),
        )

    def publish(self):
        self.temperatures_changed.emit(*self.values())

    def _set_temperature(self, celsius):
        self._celsius = max(MIN_CELSIUS, min(MAX_CELSIUS, celsius))
        self.publish()

    @pyqtSlot(float)
    def set_celsius(self, value):
        self._set_temperature(value)

    @pyqtSlot(float)
    def set_fahrenheit(self, value):
        self._set_temperature(fahrenheit_to_celsius(value))

    @pyqtSlot(float)
    def set_kelvin(self, value):
        self._set_temperature(kelvin_to_celsius(value))
