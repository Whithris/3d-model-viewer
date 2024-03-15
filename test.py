from PySide6.QtCore import QTimer
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from OpenGL.GL import *
import numpy as np
import sys
import t

from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PySide6.QtGui import QAction, QIcon
from pathlib import Path
import os


class MyOpenGl(QOpenGLWidget):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.texture_id = None
        self.t = 0

    def initializeGL(self) -> None:
        glEnable(GL_TEXTURE_2D)
        self.texture_id = glGenTextures(1)

    def paintGL(self) -> None:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        t.render(self.t)
        img = (255 * t.pixels.to_numpy()).astype(np.uint8)
        img = np.transpose(img, (1, 0, 2))

        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.shape[1], img.shape[0], 0, GL_RGB, GL_UNSIGNED_BYTE, img)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glBegin(GL_QUADS)
        glTexCoord2f(0, 0);
        glVertex2f(-1, -1)
        glTexCoord2f(0, 1);
        glVertex2f(-1, 1)
        glTexCoord2f(1, 1);
        glVertex2f(1, 1)
        glTexCoord2f(1, 0);
        glVertex2f(1, -1)
        glEnd()

        glBindTexture(GL_TEXTURE_2D, 0)

    def resizeGL(self, w: int, h: int) -> None:
        glViewport(0, 0, w, h)

    def update_texture(self):
        self.t += 0.1
        self.update()


