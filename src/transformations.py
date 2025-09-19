from math_utils import Matrix4x4, Vector3, degrees_to_radians
from typing import List


class Transform:
    def __init__(self):
        self.translation = Vector3(0, 0, 0)
        self.rotation = Vector3(0, 0, 0)  # Euler angles in degrees
        self.scale = Vector3(1, 1, 1)
        self._matrix = None
        self._needs_update = True

    def set_translation(self, x, y, z):
        self.translation = Vector3(x, y, z)
        self._needs_update = True

    def set_rotation(self, x, y, z):
        self.rotation = Vector3(x, y, z)
        self._needs_update = True

    def set_scale(self, x, y, z):
        self.scale = Vector3(x, y, z)
        self._needs_update = True

    def get_matrix(self) -> Matrix4x4:
        if self._needs_update or self._matrix is None:
            self._update_matrix()
        return self._matrix

    def _update_matrix(self):
        # Create transformation matrices
        scale_matrix = Matrix4x4.scaling(self.scale.x, self.scale.y, self.scale.z)

        rot_x = Matrix4x4.rotation_x(degrees_to_radians(self.rotation.x))
        rot_y = Matrix4x4.rotation_y(degrees_to_radians(self.rotation.y))
        rot_z = Matrix4x4.rotation_z(degrees_to_radians(self.rotation.z))

        # Combine rotations (Z * Y * X order)
        rotation_matrix = rot_z.multiply(rot_y.multiply(rot_x))

        translation_matrix = Matrix4x4.translation(
            self.translation.x, self.translation.y, self.translation.z
        )

        # Combine transformations: T * R * S
        self._matrix = translation_matrix.multiply(
            rotation_matrix.multiply(scale_matrix)
        )
        self._needs_update = False


class TransformManager:
    def __init__(self):
        self.transforms = []

    def add_transform(self, transform: Transform):
        self.transforms.append(transform)

    def clear_transforms(self):
        self.transforms.clear()

    def get_combined_matrix(self) -> Matrix4x4:
        if not self.transforms:
            return Matrix4x4.identity()

        result = self.transforms[0].get_matrix()
        for i in range(1, len(self.transforms)):
            result = result.multiply(self.transforms[i].get_matrix())

        return result

    def apply_to_vertices(self, vertices: List[Vector3]) -> List[Vector3]:
        matrix = self.get_combined_matrix()
        return [matrix.multiply(vertex) for vertex in vertices]
