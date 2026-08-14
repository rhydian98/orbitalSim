import pygame
from pygame.time import Clock
from simulation import Simulation
from constants import TIME_SCALE
from event_handlers import EventHandler
from camera import Camera




def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Orbital Simulation")
    running = True
    clock = Clock()
    camera = Camera(screen)
    simulation = Simulation( screen, camera)
    event_handler = EventHandler(simulation, camera)

    while running:
        dt = clock.tick(60) / 1000

        dt = min(dt, 1/30)

        simulation_dt = dt * (TIME_SCALE*10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            event_handler.handle_event(event)



        simulation.update(simulation_dt)

        simulation.draw()

    pygame.quit()

if __name__ == "__main__":
    main()
