import argparse
import numpy as np
from matplotlib import pyplot
import trimesh


# hardcoded constants for testing
gravity = np.array([0, 0, -1])
overhang_rads = np.pi / 4

def scalar_isclose(a, b):
    """
    Returns True if the scalar inputs (a and b) are within some epsilon (1e-8)
    of one another and False otherwise.
    """
    return np.isclose(np.array(a), np.array(b)).any()

def unit_vector(v):
    """
    Returns the unit vector of the vector. See:
    https://stackoverflow.com/questions/2827393/angles-between-two-n-dimensional-vectors-in-python.
     """
    return v / np.linalg.norm(v)

def angle_between(v1, v2):
    """
    Returns the angle in radians between vectors 'v1' and 'v2'. See:
    https://stackoverflow.com/questions/2827393/angles-between-two-n-dimensional-vectors-in-python.
    """
    u1 = unit_vector(v1)
    u2 = unit_vector(v2)
    return np.arccos(np.clip(np.dot(u1, u2), -1.0, 1.0))

def points_up(v):
    return angle_between(v, gravity) >= overhang_rads

def exceeds_overhang(v):
    if all(map(lambda x: x == 0, v)):
        return False
    return not points_up(v) or not points_up(-v)

def is_on_build_plate(v):
    return scalar_isclose(np.dot(v, gravity), 0)

def face_is_supported(face_normal, face_vertices):
    return not exceeds_overhang(face_normal) or all(map(is_on_build_plate, face_vertices))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Highlight faces that exceed maximum overhand.')
    parser.add_argument('stl_file',  type=str, help='stl file to analyze')
    parser.add_argument('overhang_angle', help="maximum angle (in degrees) supported by printer")
    parser.add_argument('gravity_vector', help="3D vector representing gravitational force (comma separated, e.g. 0,0,1)")
    args = parser.parse_args()
    mesh = trimesh.load(args.stl_file)
    overhang_rads = np.deg2rad(float(args.overhang_angle))
    gravity = np.array(map(lambda x: float(x), np.array(args.gravity_vector.split(","))))

    for fdx, face in enumerate(mesh.faces):
        face_normal = mesh.face_normals[fdx]
        face_vertices = [mesh.vertices[vdx] for vdx in face]
        if not face_is_supported(face_normal, face_vertices):
            mesh.visual.face_colors[mesh.faces[fdx]] = [255, 0, 0, 255]
    mesh.show()
