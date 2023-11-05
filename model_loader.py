from PySide6.QtGui import QColor
from PySide6.QtOpenGLWidgets import QOpenGLWidget

from OpenGL.GL import *
from OpenGL.GLU import *


class ObjWidget(QOpenGLWidget):
    def __init__(self, filepath):
        super().__init__()
        self.vertices = []
        self.normals = []
        self.texturecoords = []
        self.faces = []
        self.mtl = None
        self.lastpos = None
        self.readFile(filepath)

    def readFile(self, filepath) -> None:
        for line in open(filepath, "r"):
            material = None
            if line.startswith('#'): continue
            values = line.split()
            if not values: continue
            if values[0] == 'v':
                v = [float(x) for x in values[1:4]]
                self.vertices.append(v)
            elif values[0] == 'vn':
                v = [float(x) for x in values[1:4]]
                self.normals.append(v)
            elif values[0] == 'vt':
                v = [float(x) for x in values[1:3]]
                self.texturecoords.append(v)
            elif values[0] in ('usemtl', 'usemat'):
                material = values[1]
            elif values[0] == 'mtllib':
                self.mtl = [filepath, values[1]]
            elif values[0] == 'f':
                face = []
                texturecoords = []
                norms = []
                for v in values[1:]:
                    w = v.split('/')
                    face.append(int(w[0]))
                    if len(w) >= 2 and len(w[1]) > 0:
                        texturecoords.append(int(w[1]))
                    else:
                        texturecoords.append(0)
                    if len(w) >= 3 and len(w[2]) > 0:
                        norms.append(int(w[2]))
                    else:
                        norms.append(0)
                self.faces.append(face)

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
    def paintCoordsSystem():
        glLineWidth(2)
        glBegin(GL_LINES)
        for i in range(3):
            test = [0, 0, 0]
            test[i] = 1
            glColor3f(*tuple(test))
            glVertex3fv((0, 0, 0))
            glVertex3fv(tuple(test))
        glEnd()

    def initializeGL(self):
        glClearColor(120.0/255.0, 120.0/255.0, 120.0/255.0, 1.0)
        self.setMinimumSize(1190, 700)

    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = width / float(height)
        gluPerspective(45.0, aspect, 1.0, 1000.0)
        glTranslatef(0.0, 0.0, -5)
        glMatrixMode(GL_MODELVIEW)
