from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QWidget, QCheckBox, QVBoxLayout, QLabel, QSlider

from Canvas import Canvas


class MainMenu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Main menu")

        self.setFixedSize(QSize(250, 450))
        self.setWindowFlag(Qt.WindowType.MSWindowsFixedSizeDialogHint)
        self.move(510, 5)

        self.canvas = Canvas()
        self.canvas.show()

        self.layout = QVBoxLayout()
        self.layout.addStretch()

        scaleSlider = QSlider(Qt.Orientation.Horizontal)
        scaleSlider.setMinimum(1)
        scaleSlider.setMaximum(200)
        scaleSlider.setValue(self.canvas.scale * 100)
        scaleSlider.valueChanged.connect(self.canvas.scaleChange)

        self.layout.addWidget(QLabel("Масштаб"))
        self.layout.addWidget(scaleSlider)

        rotateSlider = QSlider(Qt.Orientation.Horizontal)
        rotateSlider.setMinimum(30)
        rotateSlider.setMaximum(5000)
        rotateSlider.setValue(int(self.canvas.rotateAngle * 100))
        rotateSlider.valueChanged.connect(self.canvas.rotationChange)

        self.layout.addWidget(QLabel("Поворот"))
        self.layout.addWidget(rotateSlider)

        self.layout.addStretch()

        effectCheckBox = QCheckBox("Включить эффект")
        effectCheckBox.setChecked(self.canvas.effectEnabled)
        effectCheckBox.toggled.connect(self.canvas.effectChackBoxChange)

        self.layout.addWidget(effectCheckBox)

        self.layout.addStretch()

        self.setLayout(self.layout)

    def closeEvent(self, event):
        self.canvas.running = False
        self.canvas.close()
