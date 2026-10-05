import sys
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPainter, QPixmap
from PyQt5.QtWidgets import (
    QApplication, QHBoxLayout, QLabel, QMessageBox, QPushButton,
    QVBoxLayout, QWidget,
)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Лабораторная работа №1")
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(540, 370)
        self.background = QPixmap()
        self.drag_position = None
        self.click_count = 0

        self.label = QLabel("Надпись")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("color: #202020; font-size: 18px;")
        self.button1 = QPushButton("Кнопка 1")
        self.button1.setToolTip("Изменить надпись")
        self.button1.clicked.connect(self.change_text)
        self.button2 = QPushButton("Кнопка 2")
        self.button2.setToolTip("Изменить форму окна с помощью PNG")
        self.button2.clicked.connect(self.change_shape)
        self.button3 = QPushButton("Кнопка 3")
        self.button3.setToolTip("Показать image.jpg вместо надписи")
        self.button3.clicked.connect(self.show_image)
        for button in (self.button1, self.button2, self.button3):
            button.setMinimumHeight(36)

        self.close_button = QPushButton("×")
        self.close_button.setToolTip("Закрыть (Esc)")
        self.close_button.setAccessibleName("Закрыть окно")
        self.close_button.setFixedSize(28, 28)
        self.close_button.clicked.connect(self.close)
        title_row = QHBoxLayout()
        title_row.addStretch()
        title_row.addWidget(self.close_button)
        buttons = QHBoxLayout()
        buttons.setSpacing(16)
        buttons.addWidget(self.button1)
        buttons.addWidget(self.button2)
        buttons.addWidget(self.button3)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(64, 40, 64, 64)
        layout.addLayout(title_row)
        layout.addStretch()
        layout.addWidget(self.label)
        layout.addSpacing(48)
        layout.addLayout(buttons)
        layout.addStretch()

    def change_text(self):
        self.click_count += 1
        self.label.setText(f"Надпись изменена! Нажатий: {self.click_count}")

    def show_image(self):
        image_path = Path(__file__).with_name("image.jpg")
        image = QPixmap(str(image_path))
        if image.isNull():
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить изображение:\n{image_path}")
            return
        self.label.setPixmap(image.scaled(360, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def change_shape(self):
        if not self.background.isNull():
            self.background = QPixmap()
            self.button2.setToolTip("Изменить форму окна с помощью PNG")
        else:
            path = Path(__file__).with_name("window_shape.png")
            pixmap = QPixmap(str(path))
            if pixmap.isNull():
                QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить PNG:\n{path}")
                return
            self.background = pixmap
            self.button2.setToolTip("Вернуть прямоугольную форму окна")
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        if self.background.isNull():
            painter.fillRect(self.rect(), Qt.white)
            painter.setPen(QColor("#202020"))
            painter.drawRect(self.rect().adjusted(1, 1, -2, -2))
        else:
            # Альфа-канал PNG сохраняет прозрачность и полупрозрачность краёв.
            painter.drawPixmap(self.rect(), self.background)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.drag_position is not None and event.buttons() & Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.drag_position = None

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
