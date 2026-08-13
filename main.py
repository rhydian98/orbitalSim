import pygame
from pygame.time import Clock
from simulation import Simulation
from constants import TIME_SCALE







def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Orbital Simulation")
    running = True
    clock = Clock()
    simulation = Simulation( screen)

    while running:
        dt = clock.tick(60) / 1000

        dt = min(dt, 1/30)

        simulation_dt = dt * (TIME_SCALE*10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                simulation.handle_keydown(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                simulation.handle_click(event.pos)



        simulation.update(simulation_dt)

        simulation.draw()

    pygame.quit()

if __name__ == "__main__":
    main()
