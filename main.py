import pygame
from pygame.time import Clock
from simulation import Simulation
from constants import AU,TIME_SCALE

from body import Body



bodies = [
    Body("Sun", 1.989e30, (255, 255, 0), 400, 300, 10),
    Body("Earth", 5.972e24, (0, 0, 255), AU, 200, 3, vx=0, vy=29_780),
    #Body("Mars", 6.417e23, (255, 0, 0), 600, 400, 2, vx=0, vy=0),

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
        simulation_dt = dt * (TIME_SCALE*10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        simulation.update(simulation_dt)

        simulation.draw()

    pygame.quit()

if __name__ == "__main__":
    main()
