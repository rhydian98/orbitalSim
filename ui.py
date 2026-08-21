import pygame
from helpers import get_speed, get_distance



class Ui:

    def __init__(self, screen):

        self.screen = screen
        self.font = pygame.font.Font(None, 18)
        self.telemetry_options = {
            "speed": True,
            "distance": True,
            "mass": True,
            "velocity": False,
            "acceleration": False
        }

        self.telemetry_rects = {}

        self.delta_v_text = ""
        self.delta_v_active = False
        self.delta_v_rect = pygame.Rect(20, 220, 100, 30)

        self.launch_rect = pygame.Rect(20, 280, 100, 30)




    def draw_info_box(self, screen_position, lines):

        box_x = screen_position[0] + 20
        box_y = screen_position[1] + 20

        box_width=220
        box_height=80

        pygame.draw.rect(self.screen, (30,30,30), (box_x, box_y, box_width, box_height))

        y=box_y +8
        for line in lines:
            text = self.font.render(line, True, (255,255,255))
            self.screen.blit(text, (box_x + 8, y))
            y +=22


    def draw_simulation_clock(self, time):
        clock_text = self.font.render(
            f"Simulation Time: {time[0]:.2f} years",
            True,
            (25,255,255)
        )

        self.screen.blit(clock_text, (10,10))

    def draw_time_warp(self, time_warp):
        time_warp_text = self.font.render(
            f"Time Warp: {time_warp}x",
            True,
            (25, 255, 255)
        )

        self.screen.blit(time_warp_text, (10, 30))


    def draw_tel_menu(self):
         options = [
             ("speed", "Speed"),
             ("mass", "Mass"),
             ("distance", "Distance"),
             ("velocity", "Velocity")
         ]

         x = 20
         y = 60

         for key, label in options:
             checkbox_rect = pygame.Rect(x,y, 18,18)

             pygame.draw.rect(self.screen, (255,255,255), checkbox_rect,2)

             if self.telemetry_options[key]:
                 pygame.draw.line(self.screen, (255,255,255), checkbox_rect.topleft, checkbox_rect.bottomright, 2)

             text = self.font.render(label, True, (255,255,255))
             self.screen.blit(text, (x+28, y - 2))

             self.telemetry_rects[key] = checkbox_rect

             y += 28

    def draw_delta_v_input(self):
        pygame.draw.rect(self.screen, (25,255,255), self.delta_v_rect, 2)
        label = self.font.render("Δv (km/s)", True, (255,255,255))
        self.screen.blit(label, (self.delta_v_rect.x, self.delta_v_rect.y-20))

        value = self.font.render(self.delta_v_text, True, (255,255,255))

        self.screen.blit(value, (self.delta_v_rect.x + 5, self.delta_v_rect.y + 6))


    def draw_launch_button(self):
        pygame.draw.rect(self.screen, (255,255,255), self.launch_rect, 2)

        text = self.font.render("Launch", True, (255,255,255))
        text_rect = text.get_rect(center=self.launch_rect.center)
        self.screen.blit(text, (text_rect))

    def toggle_telemetry(self, key):
        self.telemetry_options[key] = not self.telemetry_options[key]



    def build_info_box(self, identity, position, velocity, mass):

        lines = [identity.name]

        if self.telemetry_options["speed"]:
            speed = get_speed(velocity) / 1000
            lines.append(f"Speed: {speed:.1f} km/s")

        if self.telemetry_options["distance"]:
            distance = get_distance(position) / 1e9
            lines.append(f"Distance: {distance:.1f} million km")

        if self.telemetry_options["mass"]:
            lines.append(f"Mass: {mass.value:.2e} kg")

        if self.telemetry_options["velocity"]:
            lines.append(f"Vx: {velocity.vx / 1000:.1f} km/s")
            lines.append(f"Vy: {velocity.vy/ 1000:.1f} km/s")

        return lines


    def ui_update(self,simulation_time, time_warp):
        simulation_days = simulation_time / 86400
        simulation_years = simulation_days / 365.25

        self.draw_tel_menu()
        self.draw_delta_v_input()
        self.draw_launch_button()
        self.draw_simulation_clock(
            (simulation_years, simulation_days)
        )
        self.draw_time_warp(time_warp)
