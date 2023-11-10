import numpy as np
import pygame as pg

from object_3d import *
from camera import *
from projection import *
np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)

class SoftwareRender(object):
    def __init__(self):
        pg.init()
        self.RES = self.WIDTH, self.HEIGHT = 800, 450
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2  # поверхность для отривоски
        self.FPS = 60
        self.screen = pg.display.set_mode(self.RES)  # размер дисплея
        self.clock = pg.time.Clock()
        self.create_object()

    def create_object(self):
        # прошлая сцена
        self.camera = Camera(self, [0.5, 1, -4])
        #self.camera = Camera(self, [10, -90, 90])
        self.projection = Projection(self)
        self.object = self.get_object('2344.obj')
        self.object.draw_vertexes = False
        #self.object.translate([500, 500, 500])
        #self.object.rotate_x(45*np.pi/180)
        self.object.movement_flag =False


    def get_object(self, filename):
        vertex, faces = [], []
        with open(filename) as f:
            for line in f:
                if line.startswith('v '):
                    vertex.append([float(i)*(-1.) for i in line.split()[1:]]+[1])

                elif line.startswith('f '):
                    faces_ = line.split()[1:]
                    faces.append([int(face_.split('/')[0])-1 for face_ in faces_])
        return Object3D(self, vertex, faces)


    def draw(self):  # функция отрисовки
        self.screen.fill(pg.Color('black'))  # цвет фигуры
        self.object.draw()

    def run(self):
        while True:
            self.draw()  # отрисовка
            self.camera.control()
            [exit() for i in pg.event.get() if i.type == pg.QUIT]  # проверка на выход из приложения
            pg.display.set_caption(str(self.clock.get_fps()))  # в заголовке выводим текущее количество кадров
            pg.display.flip()  # обновление дисплея
            self.clock.tick(self.FPS)  # обновление кадров


if __name__ == "__main__":
    app = SoftwareRender()
    app.run()

