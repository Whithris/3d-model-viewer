from matrix_functions import *
from PySide6.QtGui import QKeyEvent
from PySide6.QtCore import Qt


class Camera(object):
    def __init__(self, render, position):  # начальная позиция камеры
        self.render = render
        self.position = np.array([*position, 1.0])
        # вектора ориаентации камеры
        self.forward = np.array([0, 0, 1, 1])
        self.up = np.array([0, 1, 0, 1])
        self.right = np.array([1, 0, 0, 1])
        # горизонтальная и вертикальная область видимости для камеры
        self.h_fov = np.pi / 3
        self.v_fov = self.h_fov * (render.HEIGHT / render.WIDTH)
        # бляжняя и дальняя область отсичения
        self.near_plane = 0.1
        self.far_plane = 100
        # self.moving_speed = 0.02 # скорость передвижения
        self.moving_speed = 10  # скорость передвижения
        self.rotation_speed = 0.01  # скорость вращения

        self.anglePitch = 0
        self.angleYaw = 0
        self.angleRoll = 0

    # усправление камерой
    def control(self, event: QKeyEvent):

        if event.key() == Qt.Key_A:
            self.position -= self.right * self.moving_speed
        if event.key() == Qt.Key_D:
            self.position += self.right * self.moving_speed
        if event.key() == Qt.Key_W:
            self.position += self.forward * self.moving_speed
        if event.key() == Qt.Key_S:
            self.position -= self.forward * self.moving_speed
        if event.key() == Qt.Key_Q:
            self.position += self.up * self.moving_speed
        if event.key() == Qt.Key_E:
            self.position -= self.up * self.moving_speed

        if event.key() == Qt.Key_Left:
            self.camera_yaw(-self.rotation_speed)
        if event.key() == Qt.Key_Right:
            self.camera_yaw(self.rotation_speed)
        if event.key() == Qt.Key_Up:
            self.camera_pitch(-self.rotation_speed)
        if event.key() == Qt.Key_Down:
            self.camera_pitch(self.rotation_speed)

    # поворот камеры фигуры по оси у
    def camera_yaw(self, angle):
        self.angleYaw += angle

    # поворот камеры фигуры по оси x
    def camera_pitch(self, angle):
        self.anglePitch += angle

    def axiiIdentity(self):
        self.forward = np.array([0, 0, 1, 1])
        self.up = np.array([0, 1, 0, 1])
        self.right = np.array([1, 0, 0, 1])

    def camera_update_axii(self):
        # rotate = rotate_y(self.angleYaw) @ rotate_x(self.anglePitch) #left
        rotate = rotate_x(self.anglePitch) @ rotate_y(self.angleYaw)  # right
        self.axiiIdentity()
        self.forward = self.forward @ rotate
        self.right = self.right @ rotate
        self.up = self.up @ rotate

    # матрица перемещения для перехода к системе координат камеры
    def translate_matrix(self):
        x, y, z, w = self.position
        return np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 1],
            [0, 0, 1, 0],
            [-x, -y, -z, 1]
        ])

    # матрица вращения для перехода к системе координат камеры
    def rotate_matrix(self):
        rx, ry, rz, w = self.right
        fx, fy, fz, w = self.forward
        ux, uy, uz, w = self.up
        return np.array([
            [rx, ux, fx, 0],
            [ry, uy, fy, 0],
            [rz, uz, fz, 0],
            [0, 0, 0, 1]
        ])

    def camera_matrix(self):
        self.camera_update_axii()
        return self.translate_matrix() @ self.rotate_matrix()