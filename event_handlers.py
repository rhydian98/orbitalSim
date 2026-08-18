import pygame

class EventHandler:

    def __init__(self, simulation, camera):
        self.simulation = simulation
        self.camera = camera
        self.time_warps = [1, 10, 100, 1000, 10_000, 100_000, 1_000_000]
        self.time_warp_index = 0

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:
            self.handle_keydown(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_click(event.pos)
        elif event.type == pygame.MOUSEWHEEL:
            self.handle_zoom(event.y)


    def handle_click(self, mousepos):
        self.handle_entity_click(mousepos)
        self.handle_telemetry_click(mousepos)
        self.handle_delta_v_click(mousepos)
        self.handle_launch_click(mousepos)



    def handle_entity_click(self, mousepos):
        for entity in self.simulation.identities:
            rect = self.simulation.label_rects.get(entity)

            if rect and rect.collidepoint(mousepos):
                self.simulation.select_entity(entity)
                self.camera.focus_on(entity)


    def handle_telemetry_click(self, mousepos):
        for key, rect in self.simulation.telemetry_menu_rects.items():
            if rect.collidepoint(mousepos):
                self.simulation.toggle_telemetry(key)
                return

    def handle_launch_click(self, mousepos):
        if self.simulation.launch_rect.collidepoint(mousepos):
            self.simulation.launch_rocket()

    def handle_delta_v_click(self, mousepos):
        if self.simulation.delta_v_rect.collidepoint(mousepos):
            self.simulation.delta_v_active = not self.simulation.delta_v_active


    def handle_keydown(self, event):
        if event.key == pygame.K_SPACE:
            self.simulation.toggle_pause()
            return

        if event.key == pygame.K_PERIOD:
            if not self.simulation.delta_v_active:
                self.increase_time_warp()
                return
        elif event.key == pygame.K_COMMA:
            self.decrease_time_warp()


        if not self.simulation.delta_v_active:
            return

        if event.key == pygame.K_BACKSPACE:
            self.simulation.delta_v_text = self.simulation.delta_v_text[:-1]
        elif event.key == pygame.K_RETURN:
            self.simulation.delta_v_active = False
        elif event.unicode.isdigit() or event.unicode == ".":
            self.simulation.delta_v_text += event.unicode



    def handle_zoom(self,scroll):
        if scroll > 0:
            self.camera.zoom_in()
        elif scroll < 0:
            self.camera.zoom_out()

    def increase_time_warp(self):
        if self.time_warp_index < len(self.time_warps) - 1:
            self.time_warp_index += 1
        else:
            return
    def decrease_time_warp(self):
        if self.time_warp_index > 0:
            self.time_warp_index -= 1
        else:
            return
    def get_time_warp(self):
        return self.time_warps[self.time_warp_index]
