from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QPushButton, QColorDialog


class ColorButton(QPushButton):
    returnColorSignal = pyqtSignal(QColor)

    def __init__(self, text):
        super().__init__(text)

        self.pressed.connect(self.createColorDialog)

    def createColorDialog(self):
        colorDialog = QColorDialog(self)

        if colorDialog.exec():
            self.returnColorSignal.emit(colorDialog.currentColor())
