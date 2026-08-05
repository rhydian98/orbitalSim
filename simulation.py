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

    def update(self, dt):
        self.apply_gravity()
        for body in self.bodies:
            body.update_position(dt)

    def to_screen_position(self, body):
        screen_center_x = self.screen.get_width() // 2
        screen_center_y = self.screen.get_height() // 2

        screen_x = screen_center_x + body.x * SCALE
        screen_y = screen_center_y - body.y * SCALE

        return int(screen_x), int(screen_y)



    def draw(self):


        self.screen.fill((0, 0, 0))
        for body in self.bodies:
            pygame.draw.circle(self.screen, body.color, self.to_screen_position(body), body.radius)
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
