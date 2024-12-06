import numpy as np
from OpenGL import GL as gl
from PyQt6.QtCore import Qt
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
import time

import shaders
from drawing import lagrange_surface

class Canvas(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Canvas")
        self.setWindowFlag(Qt.WindowType.MSWindowsFixedSizeDialogHint)

        self.width, self.height = 500, 500
        self.resize(self.width, self.height)
        self.move(5, 5)

        self.running = True

        self.function = self.renderFunction
        self.shader_program = None
        self.model_loc = None
        self.view_loc = None
        self.proj_loc = None
        self.time_loc = None
        self.wave_enabled_loc = None
        self.freq_loc = None
        self.amplitude_loc = None
        self.mode_loc = None

        # Инициализация контрольных точек (можете изменить по необходимости)
        self.x_points = np.array([1, 5.0, -4.0, 3.0])
        self.y_points = np.array([5.0, 2.0, -2.0, 9.0])

        self.selected_point = None  # Для обработки выбора точек

        # Инициализация параметров
        self.scale = 1
        self.rotateAngle = 0.3
        self.effectEnabled = False

        # Запоминаем время старта для анимации
        self.startTime = time.time()

        # Запуск таймера для анимации (60 FPS)
        self.timer = self.startTimer(int(1000 / 60))  # 60 FPS

    def getElapsedTime(self):
        return (time.time() - self.startTime) * 5

    def renderFunction(self):
        gl.glUseProgram(self.shader_program)

        # Передача времени в шейдер
        currentTime = self.getElapsedTime()
        gl.glUniform1f(self.time_loc, currentTime)

        # Передача флага включения волнового эффекта
        gl.glUniform1i(self.wave_enabled_loc, int(self.effectEnabled))

        # # Получение локаций униформ-переменных
        # model_loc = self.canvas.model_loc
        # view_loc = self.canvas.view_loc
        # proj_loc = self.canvas.proj_loc

        # Углы для изометрической проекции
        angle_x = np.radians(0)  # Примерно arctan(sqrt(1/2))
        angle_y = np.radians(self.rotateAngle)  # 45 градусов

        # # Матрица поворота вокруг оси X
        # rotate_x = np.array([
        #     [1, 0, 0, 0],
        #     [0, np.cos(angle_x), -np.sin(angle_x), 0],
        #     [0, np.sin(angle_x), np.cos(angle_x), 0],
        #     [0, 0, 0, 1]
        # ], dtype=np.float32)

        # Матрица поворота вокруг оси Y
        rotate_y = np.array([
            [np.cos(angle_y), 0, np.sin(angle_y), 0],
            [0, 1, 0, 0],
            [-np.sin(angle_y), 0, np.cos(angle_y), 0],
            [0, 0, 0, 1]
        ], dtype=np.float32)

        # Матрица масштабирования
        scale_matrix = np.array([
            [self.scale, 0, 0, 0],
            [0, self.scale, 0, 0],
            [0, 0, self.scale, 0],
            [0, 0, 0, 1]
        ], dtype=np.float32)

        # Матрица модели: масштабирование и повороты
        model = scale_matrix @ rotate_y

        # Матрица вида (камера)
        view = np.identity(4, dtype=np.float32)  # Камера в начале координат

        # Ортографическая проекция
        left, right = -10, 10
        bottom, top = -10, 10
        near, far = -10, 10
        projection = np.array([
            [2 / (right - left), 0, 0, -(right + left) / (right - left)],
            [0, 2 / (top - bottom), 0, -(top + bottom) / (top - bottom)],
            [0, 0, -2 / (far - near), -(far + near) / (far - near)],
            [0, 0, 0, 1]
        ], dtype=np.float32)

        # Передача матриц в шейдеры
        gl.glUniformMatrix4fv(self.model_loc, 1, gl.GL_FALSE, model.flatten())
        gl.glUniformMatrix4fv(self.view_loc, 1, gl.GL_FALSE, view.flatten())
        gl.glUniformMatrix4fv(self.proj_loc, 1, gl.GL_FALSE, projection.flatten())

        # Генерация вершин и индексов поверхности
        vertices, indices = lagrange_surface(self.x_points, self.y_points)

        # Создание и привязка VBO для поверхности
        vbo = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, vertices.nbytes, vertices, gl.GL_STATIC_DRAW)

        # Создание и привязка EBO для поверхности
        ebo = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, ebo)
        gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, gl.GL_STATIC_DRAW)

        # Настройка атрибута позиции
        position = gl.glGetAttribLocation(self.shader_program, 'aPos')
        gl.glEnableVertexAttribArray(position)
        gl.glVertexAttribPointer(position, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, None)

        color = np.array([0, 0, 1, 1.0], dtype=np.float32)
        gl.glUniform4fv(gl.glGetUniformLocation(self.shader_program, "color"), 1, color)

        # Отрисовка поверхности
        gl.glDrawElements(gl.GL_TRIANGLES, len(indices), gl.GL_UNSIGNED_INT, None)

        # Отключение атрибута позиции и буферов
        gl.glDisableVertexAttribArray(position)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, 0)
        gl.glDeleteBuffers(1, [vbo])
        gl.glDeleteBuffers(1, [ebo])

        # Рисование контрольных точек
        control_points_vertices = np.zeros((len(self.x_points), 3), dtype=np.float32)
        control_points_vertices[:, 0] = self.x_points
        control_points_vertices[:, 1] = self.y_points
        control_points_vertices[:, 2] = 0.0  # Контрольные точки на плоскости Z=0

        cp_vbo = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, cp_vbo)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, control_points_vertices.nbytes, control_points_vertices, gl.GL_STATIC_DRAW)

        # Установка цвета для контрольных точек (красный)
        cp_color = np.array([1.0, 0.0, 0.0, 1.0], dtype=np.float32)
        gl.glUniform4fv(gl.glGetUniformLocation(self.shader_program, "color"), 1, cp_color)

        # Настройка атрибута позиции
        gl.glEnableVertexAttribArray(position)
        gl.glVertexAttribPointer(position, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, None)

        # Отрисовка контрольных точек
        gl.glDrawArrays(gl.GL_POINTS, 0, len(control_points_vertices))

        # Отключение атрибута позиции и буфера
        gl.glDisableVertexAttribArray(position)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
        gl.glDeleteBuffers(1, [cp_vbo])

        # Отключение шейдерной программы
        gl.glUseProgram(0)

    def initializeGL(self):
        # Установка цвета очистки экрана (белый)
        gl.glClearColor(1.0, 1.0, 1.0, 1.0)
        gl.glEnable(gl.GL_DEPTH_TEST)  # Включение теста глубины

        self.shader_program = shaders.createShaderProgram()
        gl.glUseProgram(self.shader_program)

        # Получение локаций униформ-переменных
        self.model_loc = gl.glGetUniformLocation(self.shader_program, 'model')
        self.view_loc = gl.glGetUniformLocation(self.shader_program, 'view')
        self.proj_loc = gl.glGetUniformLocation(self.shader_program, 'projection')
        self.time_loc = gl.glGetUniformLocation(self.shader_program, 'time')
        self.wave_enabled_loc = gl.glGetUniformLocation(self.shader_program, 'waveEnabled')
        self.freq_loc = gl.glGetUniformLocation(self.shader_program, 'freq')
        self.amplitude_loc = gl.glGetUniformLocation(self.shader_program, 'amplitude')
        self.mode_loc = gl.glGetUniformLocation(self.shader_program, 'mode')

    def paintGL(self):
        # Очистка буферов цвета и глубины
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        if self.function is not None:
            self.function()

    def resizeGL(self, w, h):
        # Установка области просмотра
        gl.glViewport(0, 0, w, h)

    def timerEvent(self, event):
        self.update()

    def rotationChange(self, value):
        self.rotateAngle = value / 100
        self.startTime = time.time()
        self.update()

    def effectChackBoxChange(self, value):
        self.effectEnabled = value
        self.startTime = time.time()
        self.update()

    def scaleChange(self, value):
        self.scale = value / 100
        self.update()

    def closeEvent(self, event):
        if self.running:
            event.ignore()
