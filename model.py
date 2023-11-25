from PySide6.QtOpenGLWidgets import QOpenGLWidget

from OpenGL.GL import *
from OpenGL.GLU import *
from PySide6.QtGui import QPainter, QPen, QBrush
from PySide6.QtCore import Qt
import time

import numpy as np
import matrix_functions as mf


def any_func(arr, a, b) -> bool:
    return np.any(np.logical_or(arr == a, arr == b))


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
        self.rotate_y(1)

    def screen_projection(self):
        if self.needDrawing:
            vertexes = self.update_vertexes()
            start = time.time()
            anyfunctime = 0
            glvertex4fvtime = 0
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glPointSize(12)
            glBegin(GL_POINTS)
            glColor3f(0, 0, 0)
            for vertex in vertexes:
                start_anyfunc = time.time()
                if not any_func(vertex, self.render.H_WIDTH, self.render.H_HEIGHT):
                    end_anyfunc = time.time()
                    anyfunctime += (end_anyfunc - start_anyfunc) * 10 ** 3
                    start_glvertex4fv = time.time()
                    glVertex4fv(vertex)
                    end_glvertex4fv = time.time()
                    glvertex4fvtime +=  (end_glvertex4fv - start_glvertex4fv) * 10 ** 3
            glEnd()
            glColor3f(0.3, 0.3, 0.3)
            for face in self.faces:
                polygon = vertexes[np.array([f - 1 for f in face])]

                glBegin(GL_POLYGON)
                start_anyfunc = time.time()
                if not any_func(polygon, self.render.H_WIDTH, self.render.H_HEIGHT):
                    end_anyfunc = time.time()
                    anyfunctime += (end_anyfunc - start_anyfunc) * 10 ** 3
                    for p in polygon:
                        start_glvertex4fv = time.time()
                        glVertex4fv(p)
                        end_glvertex4fv = time.time()
                        glvertex4fvtime += (end_glvertex4fv - start_glvertex4fv) * 10 ** 3
                glEnd()
            end = time.time()
            print("glvertex4fv time is ", glvertex4fvtime, " ms")
            print("Anyfunc time is ", anyfunctime, " ms")
            if (end - start) * 10 ** 3 > 0.1:
                print("The time of OpenGL is",
                      (end - start) * 10 ** 3, "ms")
            glFlush()

    def update_vertexes(self):
        start = time.time()
        vertexes = self.vertexes @ self.render.camera.camera_matrix()
        vertexes = vertexes @ self.render.projection.projection_matrix
        vertexes /= vertexes[:, -1:].reshape(-1, 1)
        vertexes[(vertexes > 2) | (vertexes < -2)] = 0
        end = time.time()
        if (end - start) * 10 ** 3 > 0.1:
            print("The time of vertex calculations is",
                  (end - start) * 10 ** 3, "ms")
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
