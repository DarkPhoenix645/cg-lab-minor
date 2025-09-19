import numpy as np
import math

class Vector3:
    def __init__(self, x = 0, y = 0, z = 0):
        self.x = x
        self.y = y
        self.z = z

    def to_numpy(self):
        return np.array([self.x, self.y, self.z, 1])

    def from_numpy(self, arr):
        if len(arr) >= 3:
            self.x = arr[0]
            self.y = arr[1]
            self.z = arr[2]
        return self

    def __str__(self):
        return f"Vector3({self.x:.2f}, {self.y:.2f}, {self.z:.2f})"


class Matrix4x4:
    def __init__(self, matrix = None):
        if matrix is None:
            self.matrix = np.identity(4)
        else:
            self.matrix = matrix

    @staticmethod
    def identity():
        return Matrix4x4()

    @staticmethod
    def translation(x, y, z):
        mat = np.identity(4)
        mat[0, 3] = x
        mat[1, 3] = y
        mat[2, 3] = z
        return Matrix4x4(mat)

    @staticmethod
    def rotation_x(angle):
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        mat = np.array(
            [[1, 0, 0, 0], [0, cos_a, -sin_a, 0], [0, sin_a, cos_a, 0], [0, 0, 0, 1]]
        )
        return Matrix4x4(mat)

    @staticmethod
    def rotation_y(angle):
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        mat = np.array(
            [[cos_a, 0, sin_a, 0], [0, 1, 0, 0], [-sin_a, 0, cos_a, 0], [0, 0, 0, 1]]
        )
        return Matrix4x4(mat)

    @staticmethod
    def rotation_z(angle):
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        mat = np.array(
            [[cos_a, -sin_a, 0, 0], [sin_a, cos_a, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
        )
        return Matrix4x4(mat)

    @staticmethod
    def scaling(sx, sy, sz):
        mat = np.array([[sx, 0, 0, 0], [0, sy, 0, 0], [0, 0, sz, 0], [0, 0, 0, 1]])
        return Matrix4x4(mat)

    def multiply(self, other):
        if isinstance(other, Matrix4x4):
            return Matrix4x4(np.dot(self.matrix, other.matrix))
        elif isinstance(other, Vector3):
            vec4 = other.to_numpy()
            result = np.dot(self.matrix, vec4)
            return Vector3().from_numpy(result)
        return None


def degrees_to_radians(degrees):
    return degrees * math.pi / 180


def radians_to_degrees(radians):
    return radians * 180 / math.pi
