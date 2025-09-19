import pygame
import sys
from objects import create_object
from transformations import Transform, TransformManager
from renderer import Renderer3D

class GUI:
    def __init__(self, width: int = 1024, height: int = 768):
        pygame.init()

        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(
            "Nilanjan Mitra's (2023BCS-501) Submission for CG Lab Exam"
        )

        self.clock = pygame.time.Clock()
        self.running = True

        # Initialize components
        self.renderer = Renderer3D(width, height)
        self.transform_manager = TransformManager()
        self.current_object = create_object("cube", size=2.0)

        # Create transform for the object
        self.object_transform = Transform()
        self.transform_manager.add_transform(self.object_transform)

        # Control variables
        self.rotation_speed = 1.0
        self.auto_rotate = True
        self.keys_pressed = set()

        # Initialize font
        pygame.font.init()
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                self.keys_pressed.add(event.key)
                self.handle_key_press(event.key)

            elif event.type == pygame.KEYUP:
                self.keys_pressed.discard(event.key)

    def handle_key_press(self, key):
        # Projection switching
        if key == pygame.K_o:
            self.renderer.set_projection("orthographic")
        elif key == pygame.K_p:
            self.renderer.set_projection("perspective")

        # Object switching
        elif key == pygame.K_1:
            self.current_object = create_object("cube", size=2.0)
        elif key == pygame.K_2:
            self.current_object = create_object("pyramid", base_size=2.0, height=2.0)
        elif key == pygame.K_3:
            self.current_object = create_object("tetrahedron", size=1.5)
        elif key == pygame.K_4:
            self.current_object = create_object("octahedron", size=1.5)

        # Toggle features
        elif key == pygame.K_v:
            self.renderer.toggle_vertices()
        elif key == pygame.K_SPACE:
            self.auto_rotate = not self.auto_rotate
        elif key == pygame.K_r:
            # Reset transformations
            self.object_transform = Transform()
            self.transform_manager.clear_transforms()
            self.transform_manager.add_transform(self.object_transform)

        # Line width adjustment
        elif key == pygame.K_PLUS or key == pygame.K_EQUALS:
            self.renderer.set_line_width(self.renderer.line_width + 1)
        elif key == pygame.K_MINUS:
            self.renderer.set_line_width(self.renderer.line_width - 1)

    def handle_continuous_input(self):
        """Handle keys that should be processed continuously"""
        # Manual rotation controls
        if pygame.K_LEFT in self.keys_pressed:
            current_rot = self.object_transform.rotation
            self.object_transform.set_rotation(
                current_rot.x, current_rot.y - 2, current_rot.z
            )
        if pygame.K_RIGHT in self.keys_pressed:
            current_rot = self.object_transform.rotation
            self.object_transform.set_rotation(
                current_rot.x, current_rot.y + 2, current_rot.z
            )
        if pygame.K_UP in self.keys_pressed:
            current_rot = self.object_transform.rotation
            self.object_transform.set_rotation(
                current_rot.x - 2, current_rot.y, current_rot.z
            )
        if pygame.K_DOWN in self.keys_pressed:
            current_rot = self.object_transform.rotation
            self.object_transform.set_rotation(
                current_rot.x + 2, current_rot.y, current_rot.z
            )

        # Translation controls
        if pygame.K_w in self.keys_pressed:
            current_trans = self.object_transform.translation
            self.object_transform.set_translation(
                current_trans.x, current_trans.y + 0.1, current_trans.z
            )
        if pygame.K_s in self.keys_pressed:
            current_trans = self.object_transform.translation
            self.object_transform.set_translation(
                current_trans.x, current_trans.y - 0.1, current_trans.z
            )
        if pygame.K_a in self.keys_pressed:
            current_trans = self.object_transform.translation
            self.object_transform.set_translation(
                current_trans.x - 0.1, current_trans.y, current_trans.z
            )
        if pygame.K_d in self.keys_pressed:
            current_trans = self.object_transform.translation
            self.object_transform.set_translation(
                current_trans.x + 0.1, current_trans.y, current_trans.z
            )

        # Scaling controls
        if pygame.K_z in self.keys_pressed:
            current_scale = self.object_transform.scale
            scale_factor = 1.02
            self.object_transform.set_scale(
                current_scale.x * scale_factor,
                current_scale.y * scale_factor,
                current_scale.z * scale_factor,
            )
        if pygame.K_x in self.keys_pressed:
            current_scale = self.object_transform.scale
            scale_factor = 0.98
            self.object_transform.set_scale(
                current_scale.x * scale_factor,
                current_scale.y * scale_factor,
                current_scale.z * scale_factor,
            )

    def update(self):
        """Update the application state"""
        # Auto rotation
        if self.auto_rotate:
            current_rot = self.object_transform.rotation
            self.object_transform.set_rotation(
                current_rot.x + self.rotation_speed * 0.5,
                current_rot.y + self.rotation_speed,
                current_rot.z,
            )

        # Handle continuous input
        self.handle_continuous_input()

    def draw_ui(self):
        # Current projection
        projection_text = f"Projection: {self.renderer.current_projection}"
        text_surface = self.font.render(projection_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (10, 10))

        # Current object
        object_text = f"Object: {self.current_object.name}"
        text_surface = self.font.render(object_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (10, 35))

        # Controls
        help_texts = [
            "Controls:",
            "O - Orthographic projection",
            "P - Perspective projection",
            "1-4 - Switch objects",
            "Arrow Keys - Manual rotation",
            "WASD - Move object",
            "Z/X - Scale object",
            "V - Toggle vertices",
            "Space - Toggle auto-rotation",
            "R - Reset transform",
            "+/- - Line width",
        ]

        y_offset = self.height - len(help_texts) * 20 - 10
        for i, text in enumerate(help_texts):
            color = (255, 255, 255) if i == 0 else (200, 200, 200)
            text_surface = self.small_font.render(text, True, color)
            self.screen.blit(text_surface, (10, y_offset + i * 18))

    def render(self):
        """Render the current frame"""
        self.renderer.clear_screen(self.screen)

        self.renderer.render_object(
            self.screen, self.current_object, self.transform_manager
        )

        self.draw_ui()
        pygame.display.flip()

    def run(self):
        """Main application loop (runs at 60FPS)"""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()
