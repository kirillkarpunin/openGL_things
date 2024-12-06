from PyQt6 import QtCore
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (
    QWidget, QLabel, QSlider, QComboBox, QVBoxLayout, QHBoxLayout, )

from Canvas import Canvas, SOME_WEIRD_CONSTANT_FOR_SCISSORS
from ColorButton import ColorButton


class MainMenu(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Main Menu")
        self.setFixedSize(QSize(400, 600))
        self.setWindowFlag(Qt.WindowType.MSWindowsFixedSizeDialogHint)
        self.move(510, 5)

        self.canvas = Canvas()
        self.canvas.show()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.createSizeSlider()

        self.createPrimitiveTypeBox()

        self.createColorButtons()
        self.createAlphaSlider()

        self.createScissorsX()
        self.createScissorsY()
        self.createScissorsW()
        self.createScissorsH()

        self.createAlphaFunctionTypeBox()
        self.createAlphaFunctionValueSlider()

        self.createBlendSFactorBox()
        self.createBlendDFactorBox()

        self.layout.addStretch()

    def createSizeSlider(self):
        sizeSlider = QSlider(QtCore.Qt.Orientation.Horizontal)
        sizeSlider.setRange(1, 30)
        sizeSlider.setValue(self.canvas.size)
        sizeSlider.valueChanged.connect(self.canvas.changeSize)

        self.layout.addWidget(QLabel("Size"))
        self.layout.addWidget(sizeSlider)

    def createPrimitiveTypeBox(self):
        primitiveTypeBox = QComboBox()
        primitiveTypeBox.addItems(self.canvas.primitiveTypesStr)
        primitiveTypeBox.currentIndexChanged.connect(self.canvas.changePrimitiveType)

        self.layout.addWidget(QLabel("Primitive Type"))
        self.layout.addWidget(primitiveTypeBox)

    def createColorButtons(self):
        buttonLayout = QHBoxLayout()
        fgButton = ColorButton("Foreground")
        bgButton = ColorButton("Background")
        buttonLayout.addWidget(fgButton)
        buttonLayout.addWidget(bgButton)

        fgButton.returnColorSignal.connect(self.canvas.changeForeground)
        bgButton.returnColorSignal.connect(self.canvas.changeBackground)

        self.layout.addWidget(QLabel("Color"))
        self.layout.addLayout(buttonLayout)

    def createAlphaSlider(self):
        alphaSlider = QSlider(QtCore.Qt.Orientation.Horizontal)
        alphaSlider.setRange(0, 255)
        alphaSlider.setValue(self.canvas.alpha)
        alphaSlider.valueChanged.connect(self.canvas.changeAlpha)

        self.layout.addWidget(QLabel("Alpha channel"))
        self.layout.addWidget(alphaSlider)

    def createScissorsX(self):
        scissorsXSlider = QSlider(QtCore.Qt.Orientation.Horizontal)
        scissorsXSlider.setRange(0, SOME_WEIRD_CONSTANT_FOR_SCISSORS)
        scissorsXSlider.setValue(self.canvas.scissorsX)
        scissorsXSlider.valueChanged.connect(self.canvas.changeScissorsX)

        self.layout.addWidget(QLabel("Visible area x (Scissors)"))
        self.layout.addWidget(scissorsXSlider)

    def createScissorsY(self):
        scissorsYSlider = QSlider(QtCore.Qt.Orientation.Horizontal)
        scissorsYSlider.setRange(0, SOME_WEIRD_CONSTANT_FOR_SCISSORS)
        scissorsYSlider.setValue(self.canvas.scissorsY)
        scissorsYSlider.valueChanged.connect(self.canvas.changeScissorsY)

        self.layout.addWidget(QLabel("Visible area y (Scissors)"))
        self.layout.addWidget(scissorsYSlider)

    def createScissorsW(self):
        scissorsWSlider = QSlider(QtCore.Qt.Orientation.Horizontal)
        scissorsWSlider.setRange(0, SOME_WEIRD_CONSTANT_FOR_SCISSORS)
        scissorsWSlider.setValue(self.canvas.scissorsW)
        scissorsWSlider.valueChanged.connect(self.canvas.changeScissorsW)

        self.layout.addWidget(QLabel("Visible area width (Scissors)"))
        self.layout.addWidget(scissorsWSlider)

    def createScissorsH(self):
        scissorsHSlider = QSlider(QtCore.Qt.Orientation.Horizontal)
        scissorsHSlider.setRange(0, SOME_WEIRD_CONSTANT_FOR_SCISSORS)
        scissorsHSlider.setValue(self.canvas.scissorsH)
        scissorsHSlider.valueChanged.connect(self.canvas.changeScissorsH)

        self.layout.addWidget(QLabel("Visible area height (Scissors)"))
        self.layout.addWidget(scissorsHSlider)

    def createAlphaFunctionTypeBox(self):
        alphaFunctionTypeBox = QComboBox()
        alphaFunctionTypeBox.addItems(self.canvas.alphaFunctionTypesStr)
        alphaFunctionTypeBox.currentIndexChanged.connect(self.canvas.changeAlphaFunctionType)

        self.layout.addWidget(QLabel("Alpha function type"))
        self.layout.addWidget(alphaFunctionTypeBox)

    def createAlphaFunctionValueSlider(self):
        alphaFunctionValueSlider = QSlider(QtCore.Qt.Orientation.Horizontal)
        alphaFunctionValueSlider.setRange(0, 255)
        alphaFunctionValueSlider.setValue(self.canvas.alphaFunctionValue)
        alphaFunctionValueSlider.valueChanged.connect(self.canvas.changeAlphaFunctionValue)

        self.layout.addWidget(QLabel("Alpha function value"))
        self.layout.addWidget(alphaFunctionValueSlider)

    def createBlendSFactorBox(self):
        blendSFactorBox = QComboBox()
        blendSFactorBox.addItems(self.canvas.blendSFactorsStr)
        blendSFactorBox.currentIndexChanged.connect(self.canvas.changeBlendSFactor)

        self.layout.addWidget(QLabel("Blend sfactor"))
        self.layout.addWidget(blendSFactorBox)

    def createBlendDFactorBox(self):
        blendDFactorBox = QComboBox()
        blendDFactorBox.addItems(self.canvas.blendDFactorsStr)
        blendDFactorBox.currentIndexChanged.connect(self.canvas.changeBlendDFactor)

        self.layout.addWidget(QLabel("Blend dfactor"))
        self.layout.addWidget(blendDFactorBox)

    def closeEvent(self, event):
        self.canvas.running = False
        self.canvas.close()
