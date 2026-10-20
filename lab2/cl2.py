"""Представление: три связанных поля и слот обновления интерфейса"""

from PyQt5.QtCore import QSignalBlocker, pyqtSlot
from PyQt5.QtWidgets import (
    QDoubleSpinBox, QFormLayout, QLabel, QMainWindow, QPushButton,
    QVBoxLayout, QWidget,
)

from utils import (
    MIN_CELSIUS, MAX_CELSIUS,
    celsius_to_fahrenheit, celsius_to_kelvin,
)


class WeatherWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Метеостанция")
        self.resize(580, 380)
        self.setMinimumSize(480, 340)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(16)

        title = QLabel("Температура воздуха")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)

        self.celsius = self.make_field(MIN_CELSIUS, MAX_CELSIUS, " °C")
        self.fahrenheit = self.make_field(
            celsius_to_fahrenheit(MIN_CELSIUS), celsius_to_fahrenheit(MAX_CELSIUS), " °F"
        )
        self.kelvin = self.make_field(
            celsius_to_kelvin(MIN_CELSIUS), celsius_to_kelvin(MAX_CELSIUS), " K"
        )
        form = QFormLayout()
        form.setSpacing(12)
        form.addRow("По &Цельсию", self.celsius)
        form.addRow("По &Фаренгейту", self.fahrenheit)
        form.addRow("По &Кельвину", self.kelvin)
        layout.addLayout(form)

        formulas = QLabel("°F = °C × 9 / 5 + 32          K = °C + 273,15")
        formulas.setWordWrap(True)
        layout.addWidget(formulas)
        note = QLabel(f"Диапазон модели в °C: от {MIN_CELSIUS} до {MAX_CELSIUS} °C. Точность полей: 0,01.")
        note.setWordWrap(True)
        layout.addWidget(note)
        layout.addStretch()
        self.reset_button = QPushButton("Сбросить к 20 °C")
        layout.addWidget(self.reset_button)

    @staticmethod
    def make_field(minimum, maximum, suffix):
        field = QDoubleSpinBox()
        field.setRange(minimum, maximum)
        field.setDecimals(2)
        field.setSingleStep(1.0)
        field.setSuffix(suffix)
        # Ввод подтверждается Enter или выходом из поля, стрелки работают сразу
        field.setKeyboardTracking(False)
        field.setMinimumHeight(34)
        return field

    @pyqtSlot(float, float, float)
    def update_temperatures(self, celsius, fahrenheit, kelvin):
        # Программное обновление не должно снова запускать valueChanged
        fields = (
            (self.celsius, celsius),
            (self.fahrenheit, fahrenheit),
            (self.kelvin, kelvin),
        )

        for field, value in fields:
            blocker = QSignalBlocker(field)
            field.setValue(value)
            del blocker
