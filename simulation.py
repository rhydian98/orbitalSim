import pygame
from pygame.time import Clock


class Simulation:
    def __init__(self, bodies, screen):
        self.bodies = bodies
        self.screen = screen
        self.clock = Clock()

    def update(self, dt):
        for body in self.bodies:
            body.update_position(dt)


    def draw(self):
        self.screen.fill((0, 0, 0))
        for body in self.bodies:
            pygame.draw.circle(self.screen, body.color, (body.x, body.y), body.radius)
        pygame.display.flip()
