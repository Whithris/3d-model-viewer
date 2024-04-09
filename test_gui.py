from PySide6.QtCore import QTimer, Qt, Slot
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QWidget, QGridLayout, QVBoxLayout, QLabel
from PySide6.QtGui import QAction, QIcon, QFont
from pathlib import Path
import os
from test import MyOpenGl
from settings import STYLE_SHEET


class AdditionalWidget(QWidget):
    def __init__(self, size_x, size_y):
        super().__init__()
        self.hide()
        self.resize(size_x, size_y)
        self.old_pos = None
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.label = QLabel('')
        layout.addWidget(self.label)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.old_pos is not None:
            delta = event.globalPos() - self.old_pos
            self.move(self.pos() + delta)
            self.old_pos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.old_pos = None

    def view(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()


class LayersWidget(AdditionalWidget):
    def __init__(self):
        super().__init__(150, 200)


class ObjectListWidget(AdditionalWidget):
    def __init__(self):
        super().__init__(150, 200)


class PropertiesWidget(AdditionalWidget):
    def __init__(self):
        super().__init__(150, 200)


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

        self.properties_widget = PropertiesWidget()
        self.objectlist_widget = ObjectListWidget()
        self.layers_widget = LayersWidget()
        central_layout.addWidget(self.properties_widget, 0, 0)
        central_layout.addWidget(self.objectlist_widget, 0, 3)
        central_layout.addWidget(self.layers_widget, 1, 3)

        self.actions = self.init_actions()
        self.init_menubar()
        self.statusBar()
        self.timer = self.create_timer()

        central_widget.setLayout(central_layout)

    def create_menu_action(self, name, icon, shortcut, tip, connect=None):
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
                                                    'Отображение освещения модели', None)
        view_shadow_action = self.create_menu_action('Тени', QIcon(), 'F4',
                                                     'Отображение теней модели', None)
        view_properties_action = self.create_menu_action('Настройка объекта', QIcon(), 'F5',
                                                         'Отображение настройки объекта')
        view_properties_action.triggered.connect(lambda: self.view_widget(view_properties_action,
                                                                          self.properties_widget))
        view_objectlist_action = self.create_menu_action('Список объектов', QIcon(), 'F6',
                                                         'Отображение списка объектов')
        view_objectlist_action.triggered.connect(lambda: self.view_widget(view_objectlist_action,
                                                                          self.objectlist_widget))
        view_layers_action = self.create_menu_action('Слои', QIcon(), 'F7', 'Отображение слоев')
        view_layers_action.triggered.connect(lambda: self.view_widget(view_layers_action,
                                                                      self.layers_widget))
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

    def view_widget(self, action, widget):
        widget.view()
        if QIcon.isNull(action.icon()):
            action.setIcon(QIcon(os.path.join(self.path, 'images', 'done.png')))
            return True
        action.setIcon(QIcon())
        return False


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLE_SHEET)
    window = Window()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
