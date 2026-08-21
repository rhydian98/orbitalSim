from time import time

import pygame
from simulation import Simulation
from draw import Rendering
from pygame.time import Clock
from event_handlers import EventHandler
from simulation import Simulation
from systems import ThrustVectorSystem, TimeSystem
from ui import Ui
from camera import Camera

class Application:
    def __init__(self, screen):
        #Basic constructors
        self.clock = Clock()
        self.camera = Camera(screen)
        self.simulation = Simulation()
        self.time_system = TimeSystem()
        self.screen = screen
        self.running = True
        self.font = pygame.font.Font(None, 18)
        self.running = True
        self.thrust_vector_controller = ThrustVectorSystem()
        self.renderer = Rendering(screen, self.camera,self.font)
        self.ui = Ui(self.screen)
        self.event_handler = EventHandler(self.simulation, self.camera, self.ui, self.renderer, self.thrust_vector_controller, self.time_system)


        self.label_rects = {}


    def run(self):

        while self.running:
            dt = self.clock.tick(60) / 1000
            dt = min(dt, 1/30)
            time_warp = self.time_system.get_warp()
            simulation_dt  = dt * (time_warp)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.event_handler.handle_event(event)

            self.update(simulation_dt, time_warp)

    def update(self,dt, time_warp):
        selected_body = self.simulation.get_current_selected()

        simulation_time = self.simulation.get_simulation_time()

        self.simulation.update(dt)
        self.camera.update(self.simulation.positions)
        self.label_rects = self.renderer.update(
            self.simulation.renderables,
            self.simulation.positions,
            self.simulation.identities,
            self.simulation.trails
        )
        self.event_handler.set_label_rects(self.label_rects)
        self.ui.ui_update( simulation_time, time_warp)
        if selected_body is not None:
            lines = self.ui.build_info_box(
                self.simulation.identities[selected_body],
                self.simulation.positions[selected_body],
                self.simulation.velocities[selected_body],
                self.simulation.masses[selected_body]
            )
            screen_position = self.renderer.to_screen_position(
                self.simulation.positions[selected_body].x,
                self.simulation.positions[selected_body].y
            )
            self.ui.draw_info_box(screen_position, lines)
        pygame.display.flip()
