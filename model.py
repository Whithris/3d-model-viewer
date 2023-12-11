import taichi as ti
import matrix_functions as mf
import numpy as np


def any_func(arr, a, b) -> bool:
    return np.any(np.logical_or(arr == a, arr == b))


class Model:
    def __init__(self, render, vertexes, faces):
        super().__init__()
        self.render = render
        self.vertexes = np.array([np.array(v + [1]) for v in vertexes])
        self.faces = np.array([np.array(f) for f in faces])

    def calculate_vertices(self) -> np.ndarray:
        vertices = self.vertexes @ self.render.camera.camera_matrix()
        vertices = vertices @ self.render.projection.projection_matrix
        vertices /= vertices[:, -1].reshape(-1, 1)
        vertices[(vertices > 2) | (vertices < -2)] = 0
        vertices = vertices @ self.render.projection.to_screen_matrix
        vertices = vertices[:, :2]
        for i in range(len(vertices)):
            vertex = vertices[i]
            if not any_func(vertex, self.render.H_WIDTH, self.render.H_HEIGHT):
                vertices[i] = (vertex[0] / self.render.WIDTH, vertex[1] / self.render.HEIGHT)
        return vertices

    def calculate_polygons(self, vertices: np.ndarray) -> list[np.ndarray, np.ndarray, np.ndarray]:
        polygons_a = []
        polygons_b = []
        polygons_c = []
        for face in self.faces:
            polygon = vertices[np.array([f - 1 for f in face])]
            polygons_a.append(polygon[0])
            polygons_b.append(polygon[1])
            polygons_c.append(polygon[2])
        return [np.array(polygons_a), np.array(polygons_b), np.array(polygons_c)]

    def translate(self, pos):  # перемещения
        self.vertexes = self.vertexes @ mf.translate(pos)  # умножение матриц (вершины на матрицу перемещения)

    def scale(self, scale_to):  # масштабирование
        self.vertexes = self.vertexes @ mf.scale(scale_to)  # умножение матриц (вершины на матрицу масштабирования)

    def rotate_x(self, angle):  # поворот по оси x
        self.vertexes = self.vertexes @ mf.rotate_x(angle)  # умножение матриц (вершины на матрицу поворота по оси х)

    def rotate_y(self, angle):  # поворот по оси y
        self.vertexes = self.vertexes @ mf.rotate_y(angle)  # умножение матриц (вершины на матрицу поворота по оси y)

    def rotate_z(self, angle):  # поворот по оси z
        self.vertexes = self.vertexes @ mf.rotate_z(angle)  # умножение матриц (вершины на матрицу поворота по оси z)
