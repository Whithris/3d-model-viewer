from model import Model

from camera import *
from projection import *


def read_obj_file(filepath: str, render) -> Model:
    vertexes = []
    normals = []
    texture_coords = []
    faces = []
    # material = []
    # mtl = None
    for line in open(filepath, "r"):
        # material = None
        if line.startswith('#'): continue
        values = line.split()
        if not values: continue
        if values[0] == 'v':
            v = [float(x) for x in values[1:4]]
            vertexes.append(v)
        elif values[0] == 'vn':
            v = [float(x) for x in values[1:4]]
            normals.append(v)
        elif values[0] == 'vt':
            v = [float(x) for x in values[1:3]]
            texture_coords.append(v)
        # elif values[0] in ('usemtl', 'usemat'):
        #     material = values[1]
        # elif values[0] == 'mtllib':
        #      mtl = [filepath, values[1]]
        elif values[0] == 'f':
            face = []
            texture_coords = []
            norms = []
            for v in values[1:]:
                w = v.split('/')
                face.append(int(w[0]))
                if len(w) >= 2 and len(w[1]) > 0:
                    texture_coords.append(int(w[1]))
                else:
                    texture_coords.append(0)
                if len(w) >= 3 and len(w[2]) > 0:
                    norms.append(int(w[2]))
                else:
                    norms.append(0)
            faces.append(face)
    return Model(render, vertexes, faces)
