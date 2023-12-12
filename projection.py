import numpy as np
import taichi as ti


class Projection(object):
    def __init__(self, render):
        NEAR = render.camera.near_plane
        FAR = render.camera.far_plane
        RIGHT = np.tan(render.camera.h_fov / 2)
        LEFT = -RIGHT
        TOP = np.tan(render.camera.v_fov / 2)
        BOTTOM = -TOP

        # элементы матрицы проекции
        m00 = 2 / (RIGHT - LEFT)
        m11 = 2 / (TOP - BOTTOM)
        m22 = (FAR + NEAR) / (FAR - NEAR)
        m32 = -2 * NEAR * FAR / (FAR - NEAR)
        # матрица проекции
        self.projection_matrix = ti.Matrix([
            [m00, 0, 0, 0],
            [0, m11, 0, 0],
            [0, 0, m22, 1],
            [0, 0, m32, 0]
        ], ti.f32)

        # матрица преобразования вершин для нашего разрешения экрана
        HW, HH = render.H_WIDTH, render.H_HEIGHT
        self.to_screen_matrix = ti.Matrix([
            [HW, 0, 0, 0],
            [0, -HH, 0, 0],
            [0, 0, 1, 0],
            [HW, HH, 0, 1]
        ], ti.f32)
