from PySide6.QtCore import QTimer
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QWidget, QGridLayout
from PySide6.QtGui import QAction, QIcon
from pathlib import Path
import os
from test import MyOpenGl


class LayersWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(150, 200)
        self.setWindowTitle('Layers')


class ObjectListWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(150, 200)
        self.setWindowTitle('Layers')


class PropertiesWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(150, 200)
        self.setWindowTitle('Layers')


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.path = Path(__file__).resolve().parent
        self.resize(1920, 1080)
        self.setWindowTitle('SMTU 3D Engine')
        self.setWindowIcon(QIcon(os.path.join(self.path, 'images', 'smtu_logo.png')))

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_layout = QGridLayout()

        self.gl_widget = MyOpenGl(self)
        central_layout.addWidget(self.gl_widget, 0, 1, 2, 2)

        self.layers_widget = LayersWidget()
        central_layout.addWidget(self.layers_widget, 0, 0)
        self.objectlist_widget = ObjectListWidget()
        central_layout.addWidget(self.layers_widget, 0, 3)
        self.properties_widget = PropertiesWidget()
        central_layout.addWidget(self.layers_widget, 1, 3)

        self.actions = self.init_actions()
        self.init_menubar()
        self.statusBar()
        self.timer = self.create_timer()

        central_widget.setLayout(central_layout)

    def create_menu_action(self, name, icon, shortcut, tip, connect):
        action = QAction(icon, f'&{name}', self)
        action.setShortcut(shortcut)
        action.setStatusTip(tip)
        action.triggered.connect(connect)
        return action

    def init_actions(self):
        open_action = self.create_menu_action('Открыть', QIcon(os.path.join(self.path, 'images', 'open.png')),
                                              'Ctrl+N', 'Открыть файл', self.open_file)
        exit_action = self.create_menu_action('Выход', QIcon(os.path.join(self.path, 'images', 'exit.png')),
                                              'Ctrl+Q', 'Выход из программы', self.close)
        view_light_action = self.create_menu_action('Освещение', QIcon(), 'F3',
                                                    'Отображение освещения модели', self.view_light)
        view_shadow_action = self.create_menu_action('Тени', QIcon(), 'F4',
                                                     'Отображение теней модели', self.view_shadows)
        view_properties_action = self.create_menu_action('Настройка объекта', QIcon(), 'F5',
                                                         'Отображение настройки объекта', self.view_properties)
        view_objectlist_action = self.create_menu_action('Список объектов', QIcon(), 'F6',
                                                         'Отображение списка объектов', self.view_objectlist)
        view_layers_action = self.create_menu_action('Слои', QIcon(), 'F7',
                                                     'Отображение слоев', self.view_layers)
        return [open_action, exit_action, view_light_action, view_shadow_action, view_properties_action,
                view_objectlist_action, view_layers_action]

    def init_menubar(self):
        menubar = self.menuBar()
        menu_file = menubar.addMenu('&Файл')
        menu_file.addAction(self.actions[0])
        menu_file.addAction(self.actions[1])
        menu_edit = menubar.addMenu('&Редактирование')
        menu_view = menubar.addMenu('&Вид')
        menu_view.addAction(self.actions[2])
        menu_view.addAction(self.actions[3])
        menu_view.addAction(self.actions[4])
        menu_view.addAction(self.actions[5])
        menu_view.addAction(self.actions[6])
        menu_help = menubar.addMenu('&Справка')

    def create_timer(self):
        timer = QTimer(self)
        timer.timeout.connect(self.gl_widget.update_texture)
        timer.start(10)
        return timer

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(self, 'Выбор файла')
        if not path:
            self.statusBar().showMessage('Файл не выбран'.format())
        elif not os.path.exists(path):
            self.statusBar().showMessage('Файл {} не найден'.format(path))
        else:
            try:
                self.statusBar().showMessage('Файл {} открыт'.format(path))
            except OSError as err:
                self.statusBar().showMessage(err)

    def change_action_status(self, action):
        if QIcon.isNull(action.icon()):
            action.setIcon(QIcon(os.path.join(self.path, 'images', 'done.png')))
            return True
        action.setIcon(QIcon())
        return False

    def view_light(self):
        # status = self.change_action_status(self.view_light_action)
        pass

    def view_shadows(self):
        # status = self.change_action_status(self.view_shadow_action)
        pass

    def view_properties(self):
        # status = self.change_action_status(self.view_properties_action)
        pass

    def view_objectlist(self):
        # status = self.change_action_status(self.view_objectlist_action)
        pass

    def view_layers(self):
        # status = self.change_action_status(self.view_layers_action)
        pass


STYLE_SHEET = """
QMainWindow {
        background-color: #282828
}
QMenuBar, QMenu{
        background-color: #404040;
        color: #FFFFFF;
        font-family: Roboto;
        font-size: 14px;
}
QMenuBar::item:selected, QMenu::item:selected{
        background-color: #505050;
}
QStatusBar {
        color: #FFFFFF
}
"""


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLE_SHEET)
    window = Window()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
