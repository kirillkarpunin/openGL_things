from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QRadioButton, QSlider, QLabel, QCheckBox

from Canvas import Canvas


class MainMenu(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Main menu")
        self.setFixedSize(QSize(400, 450))
        self.setWindowFlag(Qt.WindowType.MSWindowsFixedSizeDialogHint)
        self.move(510, 5)

        self.canvas = Canvas()
        self.canvas.show()

        self.layout = QVBoxLayout()
        self.layout.addStretch()

        radioButton1 = QRadioButton("1-я точка")
        radioButton1.pressed.connect(self.canvas.choosePoint1)

        self.layout.addWidget(radioButton1)

        radioButton2 = QRadioButton("2-я точка")
        radioButton2.pressed.connect(self.canvas.choosePoint2)

        self.layout.addWidget(radioButton2)

        radioButton3 = QRadioButton("3-я точка")
        radioButton3.pressed.connect(self.canvas.choosePoint3)

        self.layout.addWidget(radioButton3)

        self.layout.addStretch()

        stretchSlider1 = QSlider(Qt.Orientation.Horizontal)
        stretchSlider1.setRange(0, 360)
        stretchSlider1.setValue(self.canvas.angle1)
        stretchSlider1.valueChanged.connect(self.canvas.changeAngle1)

        self.layout.addWidget(QLabel("Наклон 1-й производной"))
        self.layout.addWidget(stretchSlider1)

        angleSlider2 = QSlider(Qt.Orientation.Horizontal)
        angleSlider2.setRange(0, 360)
        angleSlider2.setValue(self.canvas.angle2)
        angleSlider2.valueChanged.connect(self.canvas.changeAngle2)

        self.layout.addWidget(QLabel("Наклон 2-й производной"))
        self.layout.addWidget(angleSlider2)

        self.layout.addStretch()

        stretchSlider1 = QSlider(Qt.Orientation.Horizontal)
        stretchSlider1.setRange(1, 5)
        stretchSlider1.setValue(self.canvas.stretch1)
        stretchSlider1.valueChanged.connect(self.canvas.changeStretch1)

        self.layout.addWidget(QLabel("Натяжение 1-й производной"))
        self.layout.addWidget(stretchSlider1)

        stretchSlider2 = QSlider(Qt.Orientation.Horizontal)
        stretchSlider2.setRange(1, 5)
        stretchSlider2.setValue(self.canvas.stretch2)
        stretchSlider2.valueChanged.connect(self.canvas.changeStretch2)

        self.layout.addWidget(QLabel("Натяжение 2-й производной"))
        self.layout.addWidget(stretchSlider2)

        self.layout.addStretch()

        checkBox = QCheckBox("Показывать направления производных")
        checkBox.setChecked(self.canvas.visibleDerivatives)
        checkBox.stateChanged.connect(self.canvas.changeDerVisibility)

        self.layout.addWidget(checkBox)

        self.layout.addStretch()

        self.setLayout(self.layout)

    def closeEvent(self, event):
        self.canvas.running = False
        self.canvas.close()
