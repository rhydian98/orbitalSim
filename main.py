import pygame
from pygame.time import Clock
from simulation import Simulation
from constants import TIME_SCALE
from event_handlers import EventHandler
from camera import Camera
from systems import ThrustVectorSystem
from application import Application



def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    app = Application(screen)

    app.run()

    pygame.quit()

if __name__ == "__main__":
    main()
