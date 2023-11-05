from PySide6.QtWidgets import *
from PySide6.QtGui import QIcon, QAction, QGuiApplication
from PySide6.QtCore import *

from model_loader import ObjWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.objWidget = ObjWidget("assets/cube.obj")
        self.init_objWidget()

    def init_ui(self) -> None:
        self.setWindowIcon(QIcon('images/smtu1.png'))
        self.setWindowTitle("Обзор моделей")
        self.create_actions()
        self.init_menuBar()

        frameGeometry = self.frameGeometry()
        windowFrameGeometry = self.frameGeometry()
        x = int(frameGeometry.center().x() - windowFrameGeometry.center().x())
        y = int(frameGeometry.center().y() - windowFrameGeometry.center().y())
        self.move(x, y)

    def create_actions(self):
        self.openFileAction = QAction('Открыть', triggered=self.open_file)

    def init_menuBar(self) -> None:
        menuBar = self.menuBar()
        menu = menuBar.addMenu('Файл')
        menu.addAction(self.openFileAction)

    def init_objWidget(self) -> None:
        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.objWidget)
        centerWidget = QWidget(None)
        centerWidget.setLayout(mainLayout)
        self.setCentralWidget(centerWidget)

    def open_file(self) -> None:
        filepath, filetype = \
             QFileDialog.getOpenFileName(self, "Выбрать файл", ".", "Object Files(*.obj)")
        self.objWidget = ObjWidget(filepath)
        self.init_objWidget()
