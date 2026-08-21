from sqlite3.dbapi2 import Time

import pygame
from systems import ThrustVectorSystem, TimeSystem

class EventHandler:

    def __init__(self, simulation, camera, ui, renderer, thrust_vector, time_system):
        self.simulation = simulation
        self.camera = camera
        self.ui = ui
        self.renderer = renderer
        self.time_system = time_system
        self.thrust_control = thrust_vector
        self.label_rects = {}


    def set_label_rects(self, label_rects):
        self.label_rects = label_rects

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:
            self.handle_keydown(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.handle_click(event.pos)
        elif event.type == pygame.MOUSEWHEEL:
            self.handle_zoom(event.y)


    def handle_click(self, mousepos):
        self.handle_entity_click(mousepos)
        self.handle_telemetry_click(mousepos)
        self.handle_delta_v_click(mousepos)
        self.handle_launch_click(mousepos)
        #self.handle_thurst_vector_click(mousepos)



    def handle_entity_click(self, mousepos):
        for entity, rect in self.label_rects.items():
            if rect and rect.collidepoint(mousepos):
                self.simulation.select_entity(entity)
                self.camera.focus_on(entity)
                return


    def handle_telemetry_click(self, mousepos):
        for key, rect in self.ui.telemetry_rects.items():
            if rect.collidepoint(mousepos):
                self.ui.toggle_telemetry(key)
                return

    def handle_launch_click(self, mousepos):
        if self.ui.launch_rect.collidepoint(mousepos):
            delta_v = float(self.ui.delta_v_text) * 1000
            self.simulation.launch_rocket(delta_v)

    def handle_delta_v_click(self, mousepos):
        if self.ui.delta_v_rect.collidepoint(mousepos):
            self.ui.delta_v_active = not self.ui.delta_v_active

    def handlethrust_vector_click(self, mousepos):
        position = self.simulation.positions[self.simulation.selected_entity]
        ship_screen_pos = self.renderer.to_screen_position(position.x, position.y)
        if self.thrust_control.dragging:
            self.thrust_control.update_drag(mousepos, ship_screen_pos)


    def handle_keydown(self, event):
        if event.key == pygame.K_SPACE:
            self.simulation.toggle_pause()
            return

        if event.key == pygame.K_PERIOD:
            if not self.ui.delta_v_active:
                self.time_system.increase()
                return
        elif event.key == pygame.K_COMMA:
            self.time_system.decrease()


        if not self.ui.delta_v_active:
            return

        if event.key == pygame.K_BACKSPACE:
            self.ui.delta_v_text = self.ui.delta_v_text[:-1]
        elif event.key == pygame.K_RETURN:
            self.ui.delta_v_active = False
        elif event.unicode.isdigit() or event.unicode == ".":
            self.ui.delta_v_text += event.unicode



    def handle_zoom(self,scroll):
        if scroll > 0:
            self.camera.zoom_in()
        elif scroll < 0:
            self.camera.zoom_out()
