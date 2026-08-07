import pygame
from pygame.time import Clock
from constants import SCALE
import math

class Simulation:
    def __init__(self, bodies, screen):
        self.bodies = bodies
        self.screen = screen
        self.clock = Clock()
        self.g = 6.67430e-11
        self.font = pygame.font.Font(None, 18)
        self.simulation_time = 0
        self.selected_body = None

    def update(self, dt):
        self.simulation_time += dt
        self.apply_gravity()
        for body in self.bodies:
            body.update_position(dt)

    def to_screen_position(self, x, y):
        screen_center_x = self.screen.get_width() // 2
        screen_center_y = self.screen.get_height() // 2

        screen_x = screen_center_x + x * SCALE
        screen_y = screen_center_y - y * SCALE

        return int(screen_x), int(screen_y)

    def handle_click(self, mouse_pos):
        for body in self.bodies:
            if body.label_rect and body.label_rect.collidepoint(mouse_pos):
                self.selected_body = body
                print(self.selected_body.name, self.selected_body.vy)
                break



    def draw(self):

        self.screen.fill((0, 0, 0))

        for body in self.bodies:
            body_screen_pos = self.to_screen_position(body.x, body.y)
            trail_position = [
                self.to_screen_position(x, y)
                for x, y in body.trail

            ]

            body.draw(self.screen, body_screen_pos, trail_position, self.font)

        simulation_days = self.simulation_time / 86400
        simulation_years = simulation_days / 365.25

        clock_text = self.font.render(
            f"Simulation Time: {simulation_years:.2f} years",
            True,
            (25,255,255)
        )

        self.screen.blit(clock_text, (10,10))

        pygame.display.flip()

    def apply_gravity(self):
        sun = self.bodies[0]

        sun.ax = 0
        sun.ay = 0

        for body in self.bodies[1:]:
            dx = sun.x - body.x
            dy = sun.y - body.y

            distance = math.sqrt(dx ** 2 + dy ** 2)

            if distance == 0:
                continue

            acceleration = self.g * sun.mass / distance ** 2
            body.ax = acceleration * dx / distance
            body.ay = acceleration * dy / distance
