import sys

from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import *
from PyQt5.QtOpenGL import *

from OpenGL.GL import *
from OpenGL.GLU import *


class MainWindow(QMainWindow):
    def __init__(self, filepath):
        super().__init__(None)
        if filepath:
            self.initUI()
            self.initMenuBar()
            self.objWidget = ObjWidget(filepath)
            self.initObjWidget()
        else:
            self.newFile()
            self.close()

    def initUI(self) -> None:
        self.setWindowIcon(QIcon('smtu1.png'))
        self.setWindowTitle("Обзор моделей")
        frameGeometry = self.frameGeometry()
        windowFrameGeometry = self.frameGeometry()
        x = int(frameGeometry.center().x() - windowFrameGeometry.center().x())
        y = int(frameGeometry.center().y() - windowFrameGeometry.center().y())
        self.move(x, y)

    def initObjWidget(self) -> None:
        xSlider = self.createSlider(self.objWidget.xRotationChanged,
                                    self.objWidget.setXRotation)
        ySlider = self.createSlider(self.objWidget.yRotationChanged,
                                    self.objWidget.setYRotation)
        zSlider = self.createSlider(self.objWidget.zRotationChanged,
                                    self.objWidget.setZRotation)
        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.objWidget)
        mainLayout.addWidget(xSlider)
        mainLayout.addWidget(ySlider)
        mainLayout.addWidget(zSlider)
        centerWidget = QWidget(None)
        centerWidget.setLayout(mainLayout)
        self.setCentralWidget(centerWidget)

    def initMenuBar(self) -> None:
        menuBar = self.menuBar()
        menu = menuBar.addMenu('Файл')
        self.openFile = QAction('Открыть')
        menu.addAction(self.openFile)
        self.openFile.triggered.connect(self.newFile)

    @staticmethod
    def createSlider(changedSignal, setterSlot) -> QSlider:
        slider = QSlider(Qt.Vertical)
        slider.setRange(0, 360*4)
        slider.setSingleStep(1)
        slider.setPageStep(15)
        slider.setTickInterval(15)
        slider.setTickPosition(QSlider.TicksRight)
        slider.valueChanged.connect(setterSlot)
        changedSignal.connect(slider.setValue)
        return slider

    def newFile(self) -> None:
        filepath, filetype = \
            QFileDialog.getOpenFileName(self, "Выбрать файл", ".", "Object Files(*.obj)")
        self.mw = MainWindow(filepath)
        self.mw.show()
        self.close()


class ObjWidget(QGLWidget):
    xRotationChanged = pyqtSignal(int)
    yRotationChanged = pyqtSignal(int)
    zRotationChanged = pyqtSignal(int)

    def __init__(self, filepath):
        super().__init__()
        self.vertices = []
        self.normals = []
        self.texturecoords = []
        self.faces = []
        self.mtl = None
        self.lastpos = None
        self.xRot = 0
        self.zRot = 0
        self.yRot = 0
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
        self.qglClearColor(QColor(120, 120, 120))
        self.setMinimumSize(1190, 700)

    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = width / float(height)
        gluPerspective(45.0, aspect, 1.0, 1000.0)
        glTranslatef(0.0, 0.0, -5)
        glMatrixMode(GL_MODELVIEW)

    def mousePressEvent(self, event):
        self.lastPos = event.pos()

    def mouseMoveEvent(self, event):
        print(self.xRot, self.yRot, self.zRot)
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()
        if event.buttons() & Qt.LeftButton:
            self.setXRotation(self.xRot + 1*dy)
            self.setYRotation(self.yRot + 1*dx)
        elif event.buttons() & Qt.RightButton:
            self.setXRotation(self.xRot + 1*dy)
            self.setZRotation(self.zRot + 1*dx)
        self.lastPos = event.pos()

    def setXRotation(self, angle):
        self.normalizeAngle(angle)
        if angle != self.xRot:
            self.xRot = angle
            self.xRotationChanged.emit(angle)
            glRotated(angle, 1.0, 0.0, 0.0)
            self.update()

    def setYRotation(self, angle):
        self.normalizeAngle(angle)
        if angle != self.yRot:
            self.yRot = angle
            self.yRotationChanged.emit(angle)
            glRotated(angle, 0.0, 1.0, 0.0)
            self.update()

    def setZRotation(self, angle):
        self.normalizeAngle(angle)
        if angle != self.zRot:
            self.zRot = angle
            self.zRotationChanged.emit(angle)
            glRotated(angle, 0.0, 0.0, 1.0)
            self.update()

    @staticmethod
    def normalizeAngle(angle):
        while angle < 0:
            angle += 360 * 4

        while angle > 360 * 4:
            angle -= 360 * 4


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow(None)
    window.show()
    sys.exit(app.exec_())
