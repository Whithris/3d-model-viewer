import numpy as np

from matrix_functions import *
import pygame as pg
from numba import njit


@njit(fastmath=True, cache=True)
def any_func(arr, a, b)->bool:
    return np.any((arr == a) | (arr == b))

class Object3D(object):
    def __init__(self, render,vertexes, faces):
        self.render = render
        self.vertexes = np.array([np.array(v) for v in vertexes])
        self.faces = np.array([np.array(f) for f in faces])
        self.translate([0.0001, 0.0001, 0.0001])

        self.font = pg.font.SysFont("Arial", 30, bold=True)
        self.color_face = [(pg.Color('lightgray'), face) for face in self.faces]
        self.movement_flag, self.draw_vertexes = True, True
        self.label = ''


    def draw(self):
        self.screen_projection()
        self.movement()

    def movement(self):
        if self.movement_flag:
            self.rotate_y(-(pg.time.get_ticks() % 0.005))



        """!
            @ 
        """
    def screen_projection(self):
        vertexes = self.vertexes @ self.render.camera.camera_matrix()  # перенос вершины обьекта в пространство камеры
        vertexes = vertexes @ self.render.projection.projection_matrix  # перенос в пространство отсечения
        # нормализация вершин и необходиом избавиться от координат значения которых >1 <-1, так как эти координаты не
        # будут влезатьв видимую область экрана и их нету смысла отрисовывать
        vertexes /= vertexes[:, -1:].reshape(-1, 1)
        # vertexes[(vertexes > 1) | (vertexes < -1)] = 0
        vertexes[(vertexes > 2) | (vertexes < -2)] = 0  # если хотим, чтобы отсичение было за экарном
        vertexes = vertexes @ self.render.projection.to_screen_matrix  # вывод на экран вершин с преобразованными
        # вершинами
        vertexes = vertexes[:, :2]

        # отображение объекта
        # прохождение по всем граням объекта


        for index, color_face in enumerate(self.color_face):
            color, face = color_face
            polygon = vertexes[face]
            if not any_func(polygon, self.render.H_WIDTH, self.render.H_HEIGHT):
                pg.draw.polygon(self.render.screen, color, polygon, 1)
                if self.label:
                    text = self.font.render(self.label[index], True,pg.Color("white"))
                    self.render.screen.blit(text, polygon[-1])
        if self.draw_vertexes:
            for vertex in vertexes:
                if not any_func(vertex, self.render.H_WIDTH, self.render.H_HEIGHT):
                    pg.draw.circle(self.render.screen, pg.Color('white'), vertex, 2)

    # методы изменения обьекта в пространстве
    def translate(self, pos):  # перемещения
        self.vertexes = self.vertexes @ translate(pos)  # умножение матриц (вершины на матрицу перемещения)

    def scale(self, scale_to):  # масштабирование
        self.vertexes = self.vertexes @ scale(scale_to)  # умножение матриц (вершины на матрицу масштабирования)

    def rotate_x(self, angle):  # поворот по оси x
        self.vertexes = self.vertexes @ rotate_x(angle)  # умножение матриц (вершины на матрицу поворота по оси х)

    def rotate_y(self, angle):  # поворот по оси y
        self.vertexes = self.vertexes @ rotate_y(angle)  # умножение матриц (вершины на матрицу поворота по оси y)

    def rotate_z(self, angle):  # поворот по оси z
        self.vertexes = self.vertexes @ rotate_z(angle)  # умножение матриц (вершины на матрицу поворота по оси z)

# Нарисовка осей
class Axes(Object3D):
    def __init__(self, render,vertexes,faces):
        super().__init__(render,vertexes, faces)
        self.vertexes = np.array([(0, 0, 0, 1),(1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1)])
        self.faces = np.array([(0,1), (0,2), (0,3)])
        self.colors = [pg.Color('red'),pg.Color('green'), pg.Color('blue')]
        self.color_face = [(color, face) for color, face in zip(self.colors, self.faces)]
        self.draw_vertexes = False
        self.label = 'XYZ'

