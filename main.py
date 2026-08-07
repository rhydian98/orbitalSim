import pygame
from pygame.time import Clock
from simulation import Simulation
from constants import AU,TIME_SCALE

from body import Body



bodies = [
    Body("Sun", 1.989e30, (255, 255, 0), 400, 300, 12),
    Body("Mercury", mass=3.3011e23, color=(170,170,170), x=57.91e9, y=0, radius=4, vx=0, vy=47_360),
    Body("Venus", mass=4.867e24, color=(220,180,80), x=108.21e9, y=0, radius=5, vx=0, vy=35_020),
    Body("Earth", 5.972e24, (0, 0, 255), AU, 200, 5, vx=0, vy=29_780),
    Body("Mars", 6.417e23, (255, 0, 0), 1.524*AU, 400, 3, vx=0, vy=24_070),

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

        dt = min(dt, 1/30)

        simulation_dt = dt * (TIME_SCALE*10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                simulation.handle_click(event.pos)



        simulation.update(simulation_dt)

        simulation.draw()

    pygame.quit()

if __name__ == "__main__":
    main()
