from PySide6.QtOpenGLWidgets import QOpenGLWidget

from OpenGL.GL import *
from OpenGL.GLU import *


class Model(QOpenGLWidget):
    def __init__(self, vertices: list, normals: list, texture_coords: list, faces: list):
        super().__init__()
        self.vertices = vertices
        self.normals = normals
        self.texture_coords = texture_coords
        self.faces = faces

    def paintGL(self) -> None:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPointSize(12)
        self.paintCoordsSystem()
        glBegin(GL_POINTS)
        glColor3f(0, 0, 0)
        for v in self.vertices:
            glVertex3fv(v)
        glEnd()
        glBegin(GL_TRIANGLES)
        for edge in self.faces[:-2]:
            for vertex in edge:
                glColor3f(0.3, 0.3, 0.3)
                glVertex3fv(self.vertices[vertex - 1])
        glEnd()
        glFlush()

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
        glClearColor(120.0/255.0, 120.0/255.0, 120.0/255.0, 1.0)
        self.setMinimumSize(1190, 700)

    def resizeGL(self, width: int, height: int):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = width / float(height)
        gluPerspective(45.0, aspect, 1.0, 1000.0)
        glTranslatef(0.0, 0.0, -5)
        glMatrixMode(GL_MODELVIEW)
