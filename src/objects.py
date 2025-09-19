from math_utils import Vector3
from typing import List, Tuple
import math

class Object3D:
    def __init__(self, name: str = "Object"):
        self.name = name
        self.vertices: List[Vector3] = []
        self.edges: List[Tuple[int, int]] = []  # Pairs of vertex indices
        self.faces: List[List[int]] = []  # Lists of vertex indices for faces

    def add_vertex(self, x, y, z):
        """Add a vertex and return its index"""
        self.vertices.append(Vector3(x, y, z))
        return len(self.vertices) - 1

    def add_edge(self, v1_idx, v2_idx):
        """Add an edge between two vertices"""
        if 0 <= v1_idx < len(self.vertices) and 0 <= v2_idx < len(self.vertices):
            self.edges.append((v1_idx, v2_idx))

    def add_face(self, vertex_indices: List[int]):
        """Add a face defined by vertex indices"""
        self.faces.append(vertex_indices)


def create_cube(size = 1.0) -> Object3D:
    """Create a cube centered at origin"""
    cube = Object3D("Cube")
    half_size = size / 2

    # Origin is at center of the cube
    # Define vertices
    vertices = [
        (-half_size, -half_size, -half_size), 
        (half_size, -half_size, -half_size),  
        (half_size, half_size, -half_size),  
        (-half_size, half_size, -half_size), 
        (-half_size, -half_size, half_size), 
        (half_size, -half_size, half_size),  
        (half_size, half_size, half_size),   
        (-half_size, half_size, half_size), 
    ]

    for x, y, z in vertices:
        cube.add_vertex(x, y, z)

    # Define edges
    edges = [
        # Back face
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 0),
        # Front face
        (4, 5),
        (5, 6),
        (6, 7),
        (7, 4),
        # Connecting edges
        (0, 4),
        (1, 5),
        (2, 6),
        (3, 7),
    ]

    for v1, v2 in edges:
        cube.add_edge(v1, v2)

    return cube


def create_pyramid(base_size = 1.0, height = 1.0) -> Object3D:
    """Create a pyramid with square base"""
    pyramid = Object3D("Pyramid")
    half_base = base_size / 2

    # Origin is at center of the pyramid
    # Base vertices
    pyramid.add_vertex(-half_base, -height / 2, -half_base) 
    pyramid.add_vertex(half_base, -height / 2, -half_base) 
    pyramid.add_vertex(half_base, -height / 2, half_base)  
    pyramid.add_vertex(-half_base, -height / 2, half_base) 
    # Apex vertex
    pyramid.add_vertex(0, height / 2, 0)  
    
    # Base edges
    pyramid.add_edge(0, 1)
    pyramid.add_edge(1, 2)
    pyramid.add_edge(2, 3)
    pyramid.add_edge(3, 0)

    # Edges to apex
    pyramid.add_edge(0, 4)
    pyramid.add_edge(1, 4)
    pyramid.add_edge(2, 4)
    pyramid.add_edge(3, 4)

    return pyramid


def create_tetrahedron(size = 1.0) -> Object3D:
    """Create a regular tetrahedron"""
    tetrahedron = Object3D("Tetrahedron")

    # Origin is at center of the tetrahedron
    # Regular tetrahedron vertices
    a = size / math.sqrt(2)
    vertices = [
        (a, a, a),  
        (-a, -a, a), 
        (-a, a, -a), 
        (a, -a, -a), 
    ]

    for x, y, z in vertices:
        tetrahedron.add_vertex(x, y, z)

    # All edges (every vertex connects to every other vertex)
    edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    for v1, v2 in edges:
        tetrahedron.add_edge(v1, v2)

    return tetrahedron


def create_octahedron(size = 1.0) -> Object3D:
    """Create a regular octahedron"""
    octahedron = Object3D("Octahedron")

    # Origin is at center of the octahedron
    # Octahedron vertices (6 vertices at unit distance from center)
    octahedron.add_vertex(size, 0, 0)
    octahedron.add_vertex(-size, 0, 0)
    octahedron.add_vertex(0, size, 0) 
    octahedron.add_vertex(0, -size, 0)
    octahedron.add_vertex(0, 0, size) 
    octahedron.add_vertex(0, 0, -size)

    # Edges connecting vertices
    edges = [
        # From +X
        (0, 2),
        (0, 3),
        (0, 4),
        (0, 5),
        # From -X
        (1, 2),
        (1, 3),
        (1, 4),
        (1, 5),
        # Between Y vertices and Z vertices
        (2, 4),
        (2, 5),
        (3, 4),
        (3, 5),
    ]

    for v1, v2 in edges:
        octahedron.add_edge(v1, v2)

    return octahedron


# Factory function
def create_object(object_type: str, **kwargs) -> Object3D:
    """Factory function to create different types of 3D objects"""
    if object_type.lower() == "cube":
        return create_cube(kwargs.get("size", 1.0))
    elif object_type.lower() == "pyramid":
        return create_pyramid(kwargs.get("base_size", 1.0), kwargs.get("height", 1.0))
    elif object_type.lower() == "tetrahedron":
        return create_tetrahedron(kwargs.get("size", 1.0))
    elif object_type.lower() == "octahedron":
        return create_octahedron(kwargs.get("size", 1.0))
    else:
        return create_cube()
