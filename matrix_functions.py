import numpy as np
import taichi as ti


def translate(pos):  # матрица перемещения
    tx, ty, tz = pos
    return ti.Matrix([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [tx, ty, tz, 1]
    ], ti.f32)


def rotate_x(a):  # матрица поворота по оси x
    return ti.Matrix([
        [1, 0, 0, 0],
        [0, np.cos(a), np.sin(a), 0],
        [0, -np.sin(a), np.cos(a), 0],
        [0, 0, 0, 1]
    ], ti.f32)


def rotate_y(a):  # матрица поворота по оси y
    return ti.Matrix([
        [np.cos(a), 0, -np.sin(a), 0],
        [0, 1, 0, 0],
        [np.sin(a), 0, np.cos(a), 0],
        [0, 0, 0, 1]
    ], ti.f32)


def rotate_z(a):  # матрица поворота по оси z
    return ti.Matrix([
        [np.cos(a), np.sin(a), 0, 0],
        [-np.sin(a), np.cos(a), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ], ti.f32)


def scale(n):  # матрица масштабирования
    return ti.Matrix([
        [n, 0, 0, 0],
        [0, n, 0, 0],
        [0, 0, n, 0],
        [0, 0, 0, 1]
    ], ti.f32)
