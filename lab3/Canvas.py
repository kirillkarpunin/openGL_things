import math

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

        self.primitiveType = GL_LINE_LOOP

        self.startSize = 0.8
        self.maxIterations = 1

    def initializeGL(self):
        glClearColor(255, 255, 255, 255)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT)

        glLineWidth(1)

        self.drawFractal(Point(-0.035, 0.3), 0, self.startSize, 1)

        glFlush()

    def drawFractal(self, crownPeak, angle, size, iteration):

        crownLeftSideVec = Vector(-120 + angle)
        crownLeftSideVec.multiply(size)

        crownRightSideVec = Vector(-60 + angle)
        crownRightSideVec.multiply(size)

        crownLeftSide = crownLeftSideVec.use(crownPeak)
        crownRightSide = crownRightSideVec.use(crownPeak)

        crown = [crownPeak, crownLeftSide, crownRightSide]

        glBegin(self.primitiveType)
        glColor3f(0, 0.5, 0)
        for point in crown:
            glVertex2f(point.x, point.y)
        glEnd()

        crownLeftSideMid = Point(
            (crownPeak.x + crownLeftSide.x) / 2,
            (crownPeak.y + crownLeftSide.y) / 2
        )

        crownRightSideMid = Point(
            (crownPeak.x + crownRightSide.x) / 2,
            (crownPeak.y + crownRightSide.y) / 2
        )

        crownBottom = Point(
            (crownRightSide.x + crownLeftSide.x) / 2,
            (crownRightSide.y + crownLeftSide.y) / 2
        )

        leftBranchVec = Vector(120 + angle)
        leftBranchVec.multiply(size * 1.2)

        rightBranchVec = Vector(45 + angle)
        rightBranchVec.multiply(size * 1.1)

        leftBranchPeak = leftBranchVec.use(crownBottom)
        rightBranchPeak = rightBranchVec.use(crownBottom)

        leftBranch = [crownBottom, leftBranchPeak, crownRightSideMid]
        rightBranch = [crownBottom, rightBranchPeak, crownLeftSideMid]

        glBegin(self.primitiveType)
        glColor3f(0, 0.5, 0)
        for point in leftBranch:
            glVertex2f(point.x, point.y)
        glEnd()

        glBegin(self.primitiveType)
        glColor3f(0, 0.5, 0)
        for point in rightBranch:
            glVertex2f(point.x, point.y)
        glEnd()

        trunkLeftSideVec = Vector(-110 + angle)
        trunkLeftSideVec.multiply(size / 2 * 1.2)

        trunkRightSideVec = Vector(-70 + angle)
        trunkRightSideVec.multiply(size / 2 * 1.3)

        trunkRightSide = trunkRightSideVec.use(crownBottom)
        trunkLeftSide = trunkLeftSideVec.use(crownBottom)

        trunk = [trunkLeftSide, trunkRightSide, crownPeak]

        glBegin(self.primitiveType)
        glColor3f(0.5, 0, 0)
        for point in trunk:
            glVertex2f(point.x, point.y)
        glEnd()

        if size >= 0.01 and iteration < self.maxIterations:
            self.drawFractal(leftBranchPeak, angle + 45, size * 0.6, iteration + 1)
            self.drawFractal(rightBranchPeak, angle - 60, size * 0.6, iteration + 1)

    def changeMaxIterations(self, value):
        self.maxIterations = value
        self.update()

    def changeType(self, value):
        if value:
            self.primitiveType = GL_TRIANGLES
        else:
            self.primitiveType = GL_LINE_LOOP
        self.update()

    def closeEvent(self, event):
        if self.running:
            event.ignore()
