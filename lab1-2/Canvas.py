from OpenGL.GL import *
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtOpenGLWidgets import QOpenGLWidget

from Point import Point

SOME_WEIRD_CONSTANT_FOR_SCISSORS = 630


class Canvas(QOpenGLWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Canvas")
        self.setWindowFlag(Qt.WindowType.MSWindowsFixedSizeDialogHint)

        self.width, self.height = 500, 500
        self.resize(self.width, self.height)
        self.move(5, 5)

        self.primitiveTypes = [
            GL_POINTS, GL_LINES, GL_LINE_LOOP, GL_LINE_STRIP,
            GL_TRIANGLES, GL_TRIANGLE_FAN, GL_TRIANGLE_STRIP,
            GL_QUADS, GL_QUAD_STRIP, GL_POLYGON
        ]
        self.primitiveTypesStr = [str(t).split()[0] for t in self.primitiveTypes]

        self.alphaFunctionTypes = [
            GL_ALWAYS, GL_LESS, GL_EQUAL, GL_LEQUAL,
            GL_GREATER, GL_NOTEQUAL, GL_GEQUAL, GL_NEVER
        ]
        self.alphaFunctionTypesStr = [str(t).split()[0] for t in self.alphaFunctionTypes]

        self.blendSFactors = [
            GL_ONE, GL_ZERO, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA,
            GL_DST_ALPHA, GL_ONE_MINUS_DST_ALPHA, GL_DST_COLOR,
            GL_ONE_MINUS_DST_COLOR, GL_SRC_ALPHA_SATURATE
        ]
        self.blendSFactorsStr = [str(f).split()[0] for f in self.blendSFactors]

        self.blendDFactors = [
            GL_ZERO, GL_ONE, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA,
            GL_DST_ALPHA, GL_ONE_MINUS_DST_ALPHA, GL_DST_COLOR,
            GL_ONE_MINUS_DST_COLOR, GL_SRC_ALPHA_SATURATE
        ]
        self.blendDFactorsStr = [str(f).split()[0] for f in self.blendDFactors]

        self.running = True

        self.scissorsX = 0
        self.scissorsY = 0
        self.scissorsW = SOME_WEIRD_CONSTANT_FOR_SCISSORS
        self.scissorsH = SOME_WEIRD_CONSTANT_FOR_SCISSORS

        self.primitiveType = self.primitiveTypes[0]
        self.size = 10

        self.color = QColor(0, 0, 0)
        self.alpha = 255
        self.backgroundColor = QColor(255, 255, 255)

        self.alphaFunctionType = self.alphaFunctionTypes[0]
        self.alphaFunctionValue = 255

        self.blendSFactor = self.blendSFactors[0]
        self.blendDFactor = self.blendDFactors[0]

        self.points = []

    def initializeGL(self):
        glClearColor(self.backgroundColor.redF(),
                     self.backgroundColor.greenF(),
                     self.backgroundColor.blueF(), 255)

    def paintGL(self):
        glClearColor(self.backgroundColor.redF(),
                     self.backgroundColor.greenF(),
                     self.backgroundColor.blueF(), 255)

        glClear(GL_COLOR_BUFFER_BIT)

        glEnable(GL_SCISSOR_TEST)
        glScissor(self.scissorsX, self.scissorsY, self.scissorsW, self.scissorsH)

        glEnable(GL_BLEND)
        glBlendFunc(self.blendSFactor, self.blendDFactor)

        glEnable(GL_ALPHA_TEST)
        glAlphaFunc(self.alphaFunctionType, self.alphaFunctionValue / 255)

        glPointSize(self.size)
        glLineWidth(self.size)

        glBegin(self.primitiveType)
        for point in self.points:
            glColor4f(point.r, point.g, point.b, point.a)
            glVertex2f(point.x, point.y)
        glEnd()

        glDisable(GL_BLEND)
        glDisable(GL_ALPHA_TEST)
        glDisable(GL_SCISSOR_TEST)

        glFlush()

    def mouseCoordToGLCoord(self, coord):
        return 2 * coord / self.width - 1

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            x = self.mouseCoordToGLCoord(event.position().x())
            y = -self.mouseCoordToGLCoord(event.position().y())
            r = self.color.redF()
            g = self.color.greenF()
            b = self.color.blueF()

            self.points.append(Point(x, y, r, g, b, self.alpha / 255))

        elif event.button() == Qt.MouseButton.RightButton and len(self.points) > 0:
            self.points.pop()

        self.update()

    def changeSize(self, size):
        self.size = size
        self.update()

    def changePrimitiveType(self, index):
        self.primitiveType = self.primitiveTypes[index]
        self.update()

    def changeForeground(self, color):
        self.color = color
        self.update()

    def changeBackground(self, color):
        self.backgroundColor = color
        self.update()

    def changeAlpha(self, alpha):
        self.alpha = alpha
        self.update()

    def changeScissorsX(self, x):
        self.scissorsX = x
        self.update()

    def changeScissorsY(self, y):
        self.scissorsY = y
        self.update()

    def changeScissorsW(self, w):
        self.scissorsW = w
        self.update()

    def changeScissorsH(self, h):
        self.scissorsH = h
        self.update()

    def changeAlphaFunctionType(self, index):
        self.alphaFunctionType = self.alphaFunctionTypes[index]
        self.update()

    def changeAlphaFunctionValue(self, value):
        self.alphaFunctionValue = value
        self.update()

    def changeBlendSFactor(self, index):
        self.blendSFactor = self.blendSFactors[index]
        self.update()

    def changeBlendDFactor(self, index):
        self.blendDFactor = self.blendDFactors[index]
        self.update()

    def closeEvent(self, event):
        if self.running:
            event.ignore()
