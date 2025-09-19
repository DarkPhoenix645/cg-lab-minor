import pygame
from objects import Object3D
from transformations import TransformManager
from projections import OrthographicProjection, PerspectiveProjection
from typing import Tuple
import math

class LineRenderer:
    @staticmethod
    def dda_line(surface, start: Tuple[int, int], end: Tuple[int, int], 
                 color: Tuple[int, int, int] = (255, 255, 255)):
        """
        DDA (Digital Differential Analyzer) Line Drawing Algorithm
        """
        x1, y1 = start
        x2, y2 = end
        
        dx = x2 - x1
        dy = y2 - y1
        
        # Calculate steps required for generating pixels
        steps = abs(dx) if abs(dx) > abs(dy) else abs(dy)
        
        # Calculate increment in x & y for each steps
        if steps == 0:
            return  # Avoid division by zero
            
        x_inc = float(dx) / steps
        y_inc = float(dy) / steps
        
        # Put pixel for each step
        x = float(x1)
        y = float(y1)
        
        for i in range(steps + 1):
            # Check bounds before drawing
            px, py = int(round(x)), int(round(y))
            if (0 <= px < surface.get_width() and 
                0 <= py < surface.get_height()):
                surface.set_at((px, py), color)
            
            x += x_inc
            y += y_inc
    
    @staticmethod
    def dda_line_thick(surface, start, end, color = (255, 255, 255), width = 1):
        """
        DDA Line Drawing Algorithm with thickness support
        """
        if width <= 1:
            LineRenderer.dda_line(surface, start, end, color)
            return
        
        x1, y1 = start
        x2, y2 = end
        
        # Calculate perpendicular offset for thickness
        dx = x2 - x1
        dy = y2 - y1
        length = math.sqrt(dx*dx + dy*dy)
        
        if length == 0:
            return
        
        # Normalize and perpendicular vector
        ux = -dy / length
        uy = dx / length
        
        # Draw multiple parallel lines for thickness
        for i in range(width):
            offset = (i - width//2)
            offset_x = int(ux * offset)
            offset_y = int(uy * offset)
            
            new_start = (x1 + offset_x, y1 + offset_y)
            new_end = (x2 + offset_x, y2 + offset_y)
            
            LineRenderer.dda_line(surface, new_start, new_end, color)
    
    def draw_line(self, surface, start, end, color = (255, 255, 255), width = 1):
        # Check if points are reasonable (not too far off-screen)
        screen_width = surface.get_width()
        screen_height = surface.get_height()
        
        # Simple clipping - skip lines that are off screen
        if (max(start[0], end[0]) < -100 or min(start[0], end[0]) > screen_width + 100 or
            max(start[1], end[1]) < -100 or min(start[1], end[1]) > screen_height + 100):
            return
        
        self.dda_line_thick(surface, start, end, color, width)

class Renderer3D:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.orthographic = OrthographicProjection(width, height)
        self.perspective = PerspectiveProjection(width, height)
        self.current_projection = "orthographic"
        self.line_renderer = LineRenderer()
        
        # Rendering options
        self.wireframe_color = (255, 255, 255)
        self.background_color = (0, 0, 0)
        self.line_width = 1
        self.show_vertices = True
        self.vertex_color = (255, 0, 0)
        self.vertex_size = 3
    
    def set_projection(self, projection_type: str):
        if projection_type in ["orthographic", "perspective"]:
            self.current_projection = projection_type
    
    def get_current_projection(self):
        if self.current_projection == "orthographic":
            return self.orthographic
        else:
            return self.perspective
    
    def render_object(self, surface, obj: Object3D, transform_manager: TransformManager):
        if not obj.vertices:
            return
        
        # Apply transformations
        transformed_vertices = transform_manager.apply_to_vertices(obj.vertices)
        
        # Project to 2D
        projection = self.get_current_projection()
        projected_points = projection.project(transformed_vertices)
        
        # Draw edges using DDA algorithm
        for v1_idx, v2_idx in obj.edges:
            if (v1_idx < len(projected_points) and v2_idx < len(projected_points)):
                start_point = projected_points[v1_idx]
                end_point = projected_points[v2_idx]
                
                # Skip off-screen points (marked with -1000, -1000)
                if (start_point[0] != -1000 and end_point[0] != -1000):
                    self.line_renderer.draw_line(
                        surface, start_point, end_point, 
                        self.wireframe_color, self.line_width
                    )
        
        # Draw vertices if enabled
        if self.show_vertices:
            for point in projected_points:
                # Skip off-screen points
                if point[0] != -1000:
                    pygame.draw.circle(surface, self.vertex_color, 
                                     point, self.vertex_size)
    
    def clear_screen(self, surface):
        """Clear the screen with background color"""
        surface.fill(self.background_color)
    
    def set_wireframe_color(self, color):
        self.wireframe_color = color
    
    def set_vertex_color(self, color):
        self.vertex_color = color
    
    def set_background_color(self, color):
        self.background_color = color
    
    def toggle_vertices(self):
        self.show_vertices = not self.show_vertices
    
    def set_line_width(self, width):
        self.line_width = max(1, width)