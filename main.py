import pygame
from pygame.time import Clock
class Planet:
    def __init__(self, name, mass, color, x=100 ,y=100, radius=1):
        self.name = name
        self.x = x
        self.y = y
        self.mass = mass
        self.color = color
        self.radius = radius
        self.vx = 0
        self.vy = 0


planets = [
    Planet("Sun", 1.989e30, (255, 255, 0), 400, 300, 10),
    Planet("Earth", 5.972e24, (0, 0, 255), 500, 200, 2),
    Planet("Mars", 6.417e23, (255, 0, 0), 600, 400, 2),

]

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Orbital Simulation")
    running = True
    clock = Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for planet in planets:
            pygame.draw.circle(screen, planet.color, (planet.x, planet.y), planet.radius*2)
            planet.x += planet.vx
            planet.y += planet.vy
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()
