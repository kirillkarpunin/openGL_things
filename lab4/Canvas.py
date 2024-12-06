import numpy as np
from OpenGL.GL import *
from PyQt6.QtCore import Qt
from PyQt6.QtOpenGLWidgets import QOpenGLWidget

from Point import Point
from Vector import Vector


class Canvas(QOpenGLWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Canvas")
        self.setWindowFlag(Qt.WindowType.MSWindowsFixedSizeDialogHint)

        self.width, self.height = 500, 500
        self.resize(self.width, self.height)
        self.move(5, 5)

        self.running = True

        self.currentPoint = -1

        self.points = [Point(-0.8, -0.8), Point(0.0, 0.8), Point(0.8, -0.8)]

        self.angle1 = 0
        self.angle2 = 0

        self.derivatives = [Vector(self.angle1), Vector(0), Vector(self.angle2)]
        self.updateDerivatives()

        self.stretch1 = 1
        self.stretch2 = 1

        self.visibleDerivatives = True

    def initializeGL(self):
        glClearColor(255, 255, 255, 255)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT)

        glLineWidth(2)
        glPointSize(8)

        self.drawHermiteSpline()

    def drawHermiteSpline(self):
        glBegin(GL_LINE_STRIP)
        glColor3f(0, 0, 255)

        for t in np.linspace(0, 1, 100):
            point = self.hermiteSplineFunc(t, 0)
            glVertex2f(point.x, point.y)

        for t in np.linspace(0, 1, 100):
            point = self.hermiteSplineFunc(t, 1)
            glVertex2f(point.x, point.y)

        glEnd()

        if self.visibleDerivatives:
            glBegin(GL_LINES)
            glColor3f(0, 255, 0)

            for i, point in enumerate(self.points):
                glVertex2f(point.x - self.derivatives[i].x / 10, point.y - self.derivatives[i].y / 10)
                glVertex2f(point.x + self.derivatives[i].x / 10, point.y + self.derivatives[i].y / 10)

            glEnd()

        glBegin(GL_POINTS)
        glColor3f(255, 0, 0)

        for point in self.points:
            glVertex2f(point.x, point.y)

        glEnd()

    def hermiteSplineFunc(self, t, segment):
        point1 = self.points[segment]
        point2 = self.points[segment + 1]
        deriv1 = self.derivatives[segment]
        deriv2 = self.derivatives[segment + 1]

        h00 = (2 * t ** 3) - (3 * t ** 2) + 1
        h10 = (t ** 3) - (2 * t ** 2) + t
        h01 = (-2 * t ** 3) + (3 * t ** 2)
        h11 = (t ** 3) - (t ** 2)

        return Point(
            (point1.x * h00) + (deriv1.x * h10) + (point2.x * h01) + (deriv2.x * h11),
            (point1.y * h00) + (deriv1.y * h10) + (point2.y * h01) + (deriv2.y * h11)
        )

    def updateDerivatives(self):
        self.derivatives[1] = Vector(
            (self.angle1 + self.angle2) / 2
        )

    def mouseCoordToGLCoord(self, coord):
        return 2 * coord / self.width - 1

    def mousePressEvent(self, event):
        if self.currentPoint == -1:
            return

        if event.button() == Qt.MouseButton.LeftButton:
            x = self.mouseCoordToGLCoord(event.position().x())
            y = -self.mouseCoordToGLCoord(event.position().y())

            self.points[self.currentPoint] = Point(x, y)

            self.update()

    def changeAngle1(self, angle):
        self.angle1 = angle
        self.derivatives[0] = Vector(self.angle1)
        self.derivatives[0].multiply(self.stretch1)

        # self.updateDerivatives()
        self.update()

    def changeAngle2(self, angle):
        self.angle2 = angle
        self.derivatives[2] = Vector(self.angle2)
        self.derivatives[2].multiply(self.stretch2)

        # self.updateDerivatives()
        self.update()

    def choosePoint1(self):
        self.currentPoint = 0

    def choosePoint2(self):
        self.currentPoint = 1

    def choosePoint3(self):
        self.currentPoint = 2

    def changeStretch1(self, stretch):
        self.derivatives[0].multiply(1 / self.stretch1)
        self.derivatives[0].multiply(stretch)
        self.stretch1 = stretch

        # self.updateDerivatives()
        self.update()

    def changeStretch2(self, stretch):
        self.derivatives[2].multiply(1 / self.stretch2)
        self.derivatives[2].multiply(stretch)
        self.stretch2 = stretch

        # self.updateDerivatives()
        self.update()

    def changeDerVisibility(self, state):
        if state:
            self.visibleDerivatives = True
        else:
            self.visibleDerivatives = False

        self.update()

    def closeEvent(self, event):
        if self.running:
            event.ignore()
