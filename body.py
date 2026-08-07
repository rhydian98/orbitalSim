from collections import deque

import pygame
class Body:
    def __init__(self, name, mass, color, x=0.0 ,y=0.0, radius=1, vx=0, vy=0, ax=0, ay=0):
        self.name = name
        self.x = x
        self.y = y
        self.mass = mass
        self.color = color
        self.radius = radius
        self.vx = vx
        self.vy = vy
        self.ax = ax
        self.ay = ay
        self.trail = deque(maxlen=200)
        self.label_rect = None


    def update_position(self, dt):
        self.vx += self.ax * dt
        self.vy += self.ay * dt

        self.x += self.vx * dt
        self.y += self.vy * dt

        self.trail.append((self.x, self.y))


    def draw(self, screen, screen_position, trail_screen_pos, font):
        #print(self.name, len(self.trail), len(trail_screen_pos))


        for trailpos in trail_screen_pos:
            pygame.draw.circle(screen, self.color, trailpos, max(1,self.radius//2))

        pygame.draw.circle(screen, self.color, (screen_position), self.radius)

        label = font.render(self.name, True, self.color)

        label_position = [
            screen_position[0] + self.radius + 5,
            screen_position[1] - self.radius
        ]

        self.label_rect = label.get_rect(topleft=label_position)

        screen.blit(label, label_position)
