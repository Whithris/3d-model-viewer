from model_loader import read_obj_file
from camera import *
from projection import *
from math import pi
import taichi as ti
import time


class MainWindow:
    def __init__(self):
        super().__init__()
        self.WIDTH, self.HEIGHT = 800, 600
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2
        self.gui = ti.GUI("3D MODEL VIEWER", res=(self.WIDTH, self.HEIGHT))
        self.filepath = "assets/start_cube.obj"
        self.model = read_obj_file(self.filepath, self)
        self.model.rotate_y(-pi / 4)
        self.camera = Camera(self, [-5, 6, -55])
        self.projection = Projection(self)
        self.paint()

    def paint(self):
        while self.gui.running:
            start = time.time()
            for e in self.gui.get_events(self.gui.PRESS):
                if e.key == self.gui.ESCAPE:
                    self.gui.running = False
                if e.key in ['w', 'a', 's', 'd', 'q', 'e',
                             ti.GUI.LEFT, ti.GUI.RIGHT, ti.GUI.UP, ti.GUI.DOWN]:
                    self.camera.control(e.key)

            v = self.model.calculate_vertices()
            t = self.model.calculate_polygons(v)
            self.gui.circles(v, radius=2, color=0x068587)
            self.gui.triangles(t[0], t[1], t[2], color=0x068587)
            print((time.time() - start) * 10 ** 3)
            self.gui.show()

