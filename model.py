from PySide6.QtOpenGLWidgets import QOpenGLWidget

from OpenGL.GL import *
from OpenGL.GLU import *
from PySide6.QtGui import QPainter, QPen, QBrush
from PySide6.QtCore import Qt

import numpy as np
import matrix_functions as mf


def any_func(arr, a, b) -> bool:
    return np.any((arr == a) | (arr == b))


class Model(QOpenGLWidget):
    def __init__(self, render, vertexes: np.array, faces: np.array):
        super().__init__()
        self.render = render
        self.vertexes = np.array([np.array(v + [1]) for v in vertexes])
        self.faces = np.array([np.array(f) for f in faces])
        self.translate([0.0001, 0.0001, 0.0001])
        self.needDrawing = True
        self.resize(1600, 900)

    def paintGL(self) -> None:
        self.screen_projection()

    def screen_projection(self):
        if self.needDrawing:
            vertexes = self.update_vertexes()
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glPointSize(12)
            glBegin(GL_POINTS)
            glColor3f(0, 0, 0)
            for vertex in vertexes:
                if not any_func(vertex, self.render.H_WIDTH, self.render.H_HEIGHT):
                    glVertex4fv(vertex)
            glEnd()
            glColor3f(0.3, 0.3, 0.3)
            for face in self.faces:
                polygon = vertexes[np.array([f - 1 for f in face])]
                glBegin(GL_POLYGON)
                if not any_func(polygon, self.render.H_WIDTH, self.render.H_HEIGHT):
                    for p in polygon:
                        glVertex4fv(p)
                glEnd()
            glFlush()

    def update_vertexes(self):
        vertexes = self.vertexes @ self.render.camera.camera_matrix()
        vertexes = vertexes @ self.render.projection.projection_matrix
        vertexes /= vertexes[:, -1:].reshape(-1, 1)
        vertexes[(vertexes > 2) | (vertexes < -2)] = 0
        return vertexes

    @staticmethod
    def paintCoordsSystem() -> None:
        glLineWidth(2)
        glBegin(GL_LINES)
        for i in range(3):
            test = [0, 0, 0]
            test[i] = 1
            glColor3f(*tuple(test))
            glVertex3fv((0, 0, 0))
            glVertex3fv(tuple(test))
        glEnd()

    def initializeGL(self) -> None:
        glClearColor(120.0 / 255.0, 120.0 / 255.0, 120.0 / 255.0, 1.0)
        self.setMinimumSize(1190, 700)

    def resizeGL(self, width: int, height: int) -> None:
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = width / float(height)
        gluPerspective(45.0, aspect, 1.0, 1000.0)
        glTranslatef(0.0, 0.0, -5)
        glMatrixMode(GL_MODELVIEW)

    def translate(self, pos):  # перемещения
        self.vertexes = self.vertexes @ mf.translate(pos)  # умножение матриц (вершины на матрицу перемещения)

    def scale(self, scale_to):  # масштабирование
        self.vertexes = self.vertexes @ mf.scale(scale_to)  # умножение матриц (вершины на матрицу масштабирования)

    def rotate_x(self, angle):  # поворот по оси x
        self.vertexes = self.vertexes @ mf.rotate_x(angle)  # умножение матриц (вершины на матрицу поворота по оси х)

    def rotate_y(self, angle):  # поворот по оси y
        self.vertexes = self.vertexes @ mf.rotate_y(angle)  # умножение матриц (вершины на матрицу поворота по оси y)

    def rotate_z(self, angle):  # поворот по оси z
        self.vertexes = self.vertexes @ mf.rotate_z(angle)  # умножение матриц (вершины на матрицу поворота по оси z)
