from PySide6.QtWidgets import *
from PySide6.QtGui import QIcon, QAction, QKeyEvent, QScreen
from PySide6.QtCore import *

from model_loader import read_obj_file
from camera import *
from projection import *
from math import pi


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.WIDTH, self.HEIGHT = 1600, 900
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2
        self.resize(1600, 900)
        self.camera = Camera(self, [-5, 6, -55])
        self.projection = Projection(self)
        self.init_ui()
        self.model = None
        self.filepath = "assets/start_cube.obj"
        self.init_model(self.filepath)
        self.showMaximized()

    def keyPressEvent(self, event: QKeyEvent):
        self.model.translate((0, 0, 0))
        if event.key() == Qt.Key_A:
            self.model.rotate_y(-10)
        if event.key() == Qt.Key_D:
            self.model.rotate_y(10)
        if event.key() == Qt.Key_W:
            self.model.rotate_x(-10)
        if event.key() == Qt.Key_S:
            self.model.rotate_x(10)
        if event.key() == Qt.Key_Q:
            self.model.scale(0.75)
        if event.key() == Qt.Key_E:
            self.model.scale(1.25)
        if event.key() == Qt.Key_Space:
            self.init_model(self.filepath)
        self.model.update()

    def init_ui(self) -> None:
        self.setWindowIcon(QIcon('images/smtu_logo.png'))
        self.setWindowTitle("Обзор моделей")
        self.create_actions()
        self.init_menuBar()
        screen_size = QScreen.availableGeometry(QApplication.primaryScreen())
        x = (screen_size.width() - self.width()) / 2
        y = (screen_size.height() - self.height()) / 2
        self.move(x, y)

    def create_actions(self) -> None:
        self.openFileAction = QAction('Открыть', triggered=self.open_file)

    def init_menuBar(self) -> None:
        menuBar = self.menuBar()
        menu = menuBar.addMenu('Файл')
        menu.addAction(self.openFileAction)

    def init_model(self, filepath) -> None:
        self.model = read_obj_file(filepath, self)
        self.model.rotate_y(-pi / 4)
        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.model)
        centerWidget = QWidget(None)
        centerWidget.setLayout(mainLayout)
        self.setCentralWidget(centerWidget)

    def open_file(self) -> None:
        self.filepath, filetype = \
            QFileDialog.getOpenFileName(self, "Выбрать файл", ".", "Object Files(*.obj)")
        self.init_model(self.filepath)
