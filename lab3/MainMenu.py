from PyQt6 import QtCore
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QWidget, QSlider, QVBoxLayout, QCheckBox

from Canvas import Canvas


class MainMenu(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Main menu")
        self.setFixedSize(QSize(40, 300))
        self.setWindowFlag(Qt.WindowType.MSWindowsFixedSizeDialogHint)
        self.move(510, 5)

        self.canvas = Canvas()
        self.canvas.show()

        self.layout = QVBoxLayout()

        iterationSlider = QSlider(QtCore.Qt.Orientation.Vertical)
        iterationSlider.setRange(1, 10)
        iterationSlider.setValue(self.canvas.maxIterations)
        iterationSlider.setTickInterval(1)
        iterationSlider.setTickPosition(QSlider.TickPosition.TicksBelow)
        iterationSlider.valueChanged.connect(self.canvas.changeMaxIterations)
        self.layout.addWidget(iterationSlider)

        typeBox = QCheckBox()
        typeBox.stateChanged.connect(self.canvas.changeType)
        self.layout.addWidget(typeBox)

        self.setLayout(self.layout)

    def closeEvent(self, event):
        self.canvas.running = False
        self.canvas.close()
