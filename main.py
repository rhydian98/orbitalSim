import pygame
from pygame.time import Clock
from simulation import Simulation

from body import Body



bodies = [
    Body("Sun", 1.989e30, (255, 255, 0), 400, 300, 10, vx=100, vy=0),
    Body("Earth", 5.972e24, (0, 0, 255), 500, 200, 2, vx=0, vy=0),
    Body("Mars", 6.417e23, (255, 0, 0), 600, 400, 2),

]

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Orbital Simulation")
    running = True
    clock = Clock()
    simulation = Simulation(bodies, screen)
    while running:
        dt = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        simulation.update(dt)

        simulation.draw()

    pygame.quit()

if __name__ == "__main__":
    main()
