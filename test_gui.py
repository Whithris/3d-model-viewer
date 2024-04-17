from PySide6.QtCore import QTimer, Qt, QPoint
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QWidget, QGridLayout, QVBoxLayout, QLabel, \
    QPushButton, QHBoxLayout, QCheckBox, QComboBox, QToolBar
from PySide6.QtGui import QAction, QIcon

import os
from test import MyOpenGl
import settings


class AdditionalWidget(QWidget):
    def __init__(self, size_x, size_y):
        super().__init__()
        self.hide()
        self.setFixedSize(size_x, size_y)
        self.old_pos = None
        self.init_ui()

    def mousePressEvent(self, event):
        if settings.movable_widgets:
            if event.button() == Qt.MouseButton.LeftButton:
                p = event.globalPosition()
                global_pos = p.toPoint()
                self.old_pos = global_pos

    def mouseMoveEvent(self, event):
        if self.old_pos is not None:
            p = event.globalPosition()
            global_pos = p.toPoint()
            delta = global_pos - self.old_pos
            self.move(self.pos() + delta)
            self.old_pos = global_pos

    def mouseReleaseEvent(self, event):
        self.old_pos = None

    def view(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(0)
        self.setLayout(layout)

        menu_layout = QHBoxLayout()
        exit_button = QPushButton('', self)
        exit_button.setIcon(QIcon(os.path.join(settings.PATH, 'images', 'minimize.png')))
        exit_button.clicked.connect(self.view)
        menu_layout.addWidget(exit_button)
        layout.addLayout(menu_layout)
        label = QLabel('')
        layout.addWidget(label)


class Settings(QWidget):
    def __init__(self, window):
        super().__init__()
        self.hide()
        self.window = window
        self.setWindowTitle('Настройки')
        self.setWindowIcon(QIcon(os.path.join(settings.PATH, 'images', 'settings.png')))
        self.comboboxes = []
        self.checkboxes = []
        self.init_ui()

    def init_ui(self):
        resolution_change_layout = QHBoxLayout()
        resolution_change_layout.addWidget(QLabel('Разрешение экрана:'))
        resolution_combobox = QComboBox()
        self.comboboxes.append(resolution_combobox)
        resolution_combobox.addItems(['800x600', '1024x768', '1280x720', '1600x900',
                                      '1920x1080', '2560x1440', 'Полный экран'])
        resolution_combobox.currentTextChanged.connect(self.resize_window)
        resolution_change_layout.addWidget(resolution_combobox)

        movable_widgets_checkbox = QCheckBox("Движимость виджетов")
        self.checkboxes.append(movable_widgets_checkbox)
        movable_widgets_checkbox.stateChanged.connect(self.movable_widgets_checkbox_changed)

        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addLayout(resolution_change_layout)
        layout.addWidget(movable_widgets_checkbox)

    def movable_widgets_checkbox_changed(self):
        settings.movable_widgets = self.checkboxes[0].isChecked()

    def resize_window(self, resolution):
        if 'x' in resolution:
            w, h = [int(x) for x in resolution.split('x')]
            self.window.setFixedSize(w, h)
            qr = self.window.frameGeometry()
            cp = self.window.screen().availableGeometry().center()
            qr.moveCenter(cp)
            self.window.move(qr.topLeft())


class LayersWidget(AdditionalWidget):
    def __init__(self, pos):
        super().__init__(200, 250)

    def view(self):
        super().view()
        # anim = QPropertyAnimation(self, b"pos")
        # anim.setStartValue(self.pos)
        # anim.setEndValue(QPoint(500, 500))
        # anim.setDuration(15000)
        # anim.start()


class ObjectListWidget(AdditionalWidget):
    def __init__(self, pos):
        super().__init__(200, 250)

    def view(self):
        super().view()
        # anim = QPropertyAnimation(self, b"pos")
        # anim.setStartValue(self.pos)
        # anim.setEndValue(QPoint(500, 500))
        # anim.setDuration(15000)
        # anim.start()


class PropertiesWidget(AdditionalWidget):
    def __init__(self, pos):
        super().__init__(200, 250)

    def view(self):
        super().view()


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(settings.width, settings.height)
        self.setWindowTitle('SMTU 3D')
        self.setWindowIcon(QIcon(os.path.join(settings.PATH, 'images', 'smtu_logo.png')))

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_layout = QGridLayout()

        self.gl_widget = MyOpenGl(self)
        central_layout.addWidget(self.gl_widget, 0, 0, 3, 3)

        self.settings_widget = Settings(self)

        self.properties_widget = PropertiesWidget((0, 0))
        self.objectlist_widget = ObjectListWidget(QPoint(1000, 1000))
        self.layers_widget = LayersWidget(QPoint(500, 0))
        central_layout.addWidget(self.properties_widget, 0, 0)
        central_layout.addWidget(self.objectlist_widget, 0, 2)
        central_layout.addWidget(self.layers_widget, 2, 2)

        self.actions = []
        self.init_actions()
        self.init_menubar()
        self.toolbar = self.init_toolbar()
        self.statusBar()
        self.setStatusTip('Файл не выбран')
        self.timer = self.create_timer()

        central_widget.setLayout(central_layout)

    def create_menu_action(self, name, icon, shortcut, tip, connect=None):
        action = QAction(icon, f'&{name}', self)
        if shortcut != '': action.setShortcut(shortcut)
        action.setStatusTip(tip)
        action.triggered.connect(connect)
        self.actions.append(action)
        return action

    def adding_actions(self, menu, n):
        for i in range(n):
            menu.addAction(self.actions[0])
            self.actions = self.actions[1:]

    def init_actions(self):
        # FILE ACTIONS
        open_action = self.create_menu_action('Открыть', QIcon(os.path.join(settings.PATH, 'images', 'open.png')),
                                              'Ctrl+N', 'Открыть файл', self.open_file)
        save_action = self.create_menu_action('Сохранить', QIcon(os.path.join(settings.PATH, 'images', 'save.png')),
                                              'Ctrl+S', 'Сохранить файл', self.save_file)
        settings_action = self.create_menu_action('Настройки',
                                                  QIcon(os.path.join(settings.PATH, 'images', 'settings.png')),
                                                  'Ctrl+Alt+S', 'Изменение настроек', self.open_settings)
        exit_action = self.create_menu_action('Выход', QIcon(os.path.join(settings.PATH, 'images', 'exit.png')),
                                              'Ctrl+Q', 'Выход из программы', self.close)

        # EDIT ACTIONS
        open_toolbar_action = self.create_menu_action('Панель инструментов', QIcon(), 'Ctrl+T',
                                                      'Отображение панели инструментов')
        open_toolbar_action.triggered.connect(lambda: self.view_widget(open_toolbar_action,
                                                                       self.toolbar))

        # VIEW ACTIONS
        view_light_action = self.create_menu_action('Освещение', QIcon(), 'F1',
                                                    'Отображение освещения модели', None)
        view_shadow_action = self.create_menu_action('Тени', QIcon(), 'F2',
                                                     'Отображение теней модели', None)
        view_properties_action = self.create_menu_action('Настройка объекта', QIcon(), 'F3',
                                                         'Отображение настройки объекта')
        view_properties_action.triggered.connect(lambda: self.view_widget(view_properties_action,
                                                                          self.properties_widget))
        view_objectlist_action = self.create_menu_action('Список объектов', QIcon(), 'F4',
                                                         'Отображение списка объектов')
        view_objectlist_action.triggered.connect(lambda: self.view_widget(view_objectlist_action,
                                                                          self.objectlist_widget))
        view_layers_action = self.create_menu_action('Слои', QIcon(), 'F5', 'Отображение слоев')
        view_layers_action.triggered.connect(lambda: self.view_widget(view_layers_action,
                                                                      self.layers_widget))

        # HELP ACTIONS
        help_action = self.create_menu_action('Справка', QIcon(os.path.join(settings.PATH, 'images', 'help.png')),
                                              'Ctrl+H', 'Справочная информация', self.help)

        # TOOLBAR ACTIONS
        choose_object_actions = self.create_menu_action('Выбор объекта',
                                                        QIcon(os.path.join(settings.PATH, 'images', 'object.png')),
                                                        '', 'Выбор объекта для редактирования')
        move_object_actions = self.create_menu_action('Движение объекта',
                                                        QIcon(os.path.join(settings.PATH, 'images', 'move.png')),
                                                        '', 'Движение выбранного объекта')
        resize_object_actions = self.create_menu_action('Масштабирование объекта',
                                                        QIcon(os.path.join(settings.PATH, 'images', 'resize.png')),
                                                        '', 'Масштабирование выбранного объекта')
        minimize_action = self.create_menu_action('Свернуть',
                                                  QIcon(os.path.join(settings.PATH, 'images', 'minimize.png')),
                                                  '', 'Свернуть панель инструментов')
        minimize_action.triggered.connect(lambda: self.toolbar.hide())

    def init_menubar(self):
        menubar = self.menuBar()

        menu_file = menubar.addMenu('&Файл')
        self.adding_actions(menu_file, 4)

        menu_edit = menubar.addMenu('&Редактирование')
        self.adding_actions(menu_edit, 1)

        menu_view = menubar.addMenu('&Вид')
        self.adding_actions(menu_view, 5)

        menu_help = menubar.addMenu('&Справка')
        self.adding_actions(menu_help, 1)

    def init_toolbar(self):
        toolbar = self.addToolBar('Свернуть')
        toolbar.hide()
        self.adding_actions(toolbar, 4)
        return toolbar

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
                self.setStatusTip('Работа с файлом {}'.format(path))
            except OSError as err:
                self.statusBar().showMessage(err)

    def save_file(self):
        pass

    def open_settings(self):
        self.settings_widget.show()

    @staticmethod
    def view_widget(action, widget):
        if widget.isVisible():
            widget.hide()
        else:
            widget.show()
        if QIcon.isNull(action.icon()):
            action.setIcon(QIcon(os.path.join(settings.PATH, 'images', 'done.png')))
            return True
        action.setIcon(QIcon())
        return False

    def help(self):
        pass


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(settings.STYLE_SHEET)
    window = Window()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
