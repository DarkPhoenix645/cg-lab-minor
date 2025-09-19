from math_utils import Vector3
from typing import List, Tuple
import math

class ProjectionManager:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.center_x = width // 2
        self.center_y = height // 2
    
    def world_to_screen(self, point: Vector3) -> Tuple[int, int]:
        """Convert world coordinates to screen coordinates"""
        screen_x = int(self.center_x + point.x)
        screen_y = int(self.center_y - point.y)  # Flip Y axis
        return screen_x, screen_y

class OrthographicProjection(ProjectionManager):
    def __init__(self, width, height, scale = 100):
        super().__init__(width, height)
        self.scale = scale
    
    def project(self, vertices: List[Vector3]) -> List[Tuple[int, int]]:
        """Project 3D vertices to 2D using orthographic projection"""
        projected = []
        for vertex in vertices:
            # For orthographic projection, we simply ignore Z coordinate
            # and scale the X and Y coordinates
            x = vertex.x * self.scale
            y = vertex.y * self.scale
            screen_pos = self.world_to_screen(Vector3(x, y, 0))
            projected.append(screen_pos)
        return projected

class PerspectiveProjection(ProjectionManager):
    def __init__(self, width, height, fov = 60, near = 0.1, far = 1000):
        super().__init__(width, height)
        self.fov = math.radians(fov)
        self.near = near
        self.far = far
        self.aspect_ratio = width / height
        self.scale = min(width, height) // 3
        # Camera is positioned at a distance where objects are visible
        self.camera_z = 8.0
    
    def project(self, vertices: List[Vector3]) -> List[Tuple[int, int]]:
        """Project 3D vertices to 2D using perspective projection"""
        projected = []
        
        for vertex in vertices:
            # Position vertex relative to camera (camera is at positive Z looking towards negative Z)
            z = self.camera_z + vertex.z  # Camera at +8, objects around 0
            
            # Avoid division by zero and ensure positive depth
            if z <= 0.1:
                z = 0.1
            
            # Simple perspective projection formula: screen_coord = (world_coord / z) * distance
            perspective_factor = self.scale / z
            projected_x = vertex.x * perspective_factor
            projected_y = vertex.y * perspective_factor
            
            screen_pos = self.world_to_screen(Vector3(projected_x, projected_y, 0))
            projected.append(screen_pos)
        
        return projected

class Camera:
    def __init__(self, position: Vector3 = None):
        self.position = position or Vector3(0, 0, 8)
        self.rotation = Vector3(0, 0, 0)
    
    def move(self, dx, dy, dz):
        self.position.x += dx
        self.position.y += dy
        self.position.z += dz
    
    def rotate(self, dx, dy, dz):
        self.rotation.x += dx
        self.rotation.y += dy
        self.rotation.z += dz