from pathlib import Path

STYLE_SHEET = """
QMenuBar, QMenu, QPushButton, QLabel, QCheckBox{
        background-color: #404040;
        color: #FFFFFF;
        font-family: Roboto;
        font-size: 14px;
        border-radius: 0px;
}
QMainWindow, Settings {
        background-color: #282828
}
QToolButton, QPushButton {
        background-color: #282828
} 
QMenuBar::item:selected, QMenu::item:selected, QPushButton::item:selected {
        background-color: #505050;
}
QStatusBar {
        color: #FFFFFF;
        font-family: Roboto;
        font-size: 14px;
}
QToolButton:pressed, QPushButton:pressed {
        background-color: #404040
}
QToolBar {
        background-color: #404040;
        color: #FFFFFF;
        font-family: Roboto;
        font-size: 14px;
        border-radius: 2px;
}
"""
PATH = Path(__file__).resolve().parent
width, height = 800, 600
