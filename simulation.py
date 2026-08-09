import pygame
from pygame.time import Clock
from constants import SCALE
import math

class Simulation:
    def __init__(self, bodies, screen):
        self.bodies = bodies
        self.screen = screen
        self.clock = Clock()
        self.g = 6.67430e-11
        self.font = pygame.font.Font(None, 18)
        self.simulation_time = 0
        self.selected_body = None


        self.telemetry_options = {
            "speed": True,
            "distance": True,
            "mass": True,
            "velocity": False,
            "acceleration": False
        }

        self.telemetry_menu_rects = {}

    def update(self, dt):
        self.simulation_time += dt
        self.apply_gravity()
        for body in self.bodies:
            body.update_position(dt)

    def to_screen_position(self, x, y):
        screen_center_x = self.screen.get_width() // 2
        screen_center_y = self.screen.get_height() // 2

        screen_x = screen_center_x + x * SCALE
        screen_y = screen_center_y - y * SCALE

        return int(screen_x), int(screen_y)

    def handle_click(self, mouse_pos):
        for body in self.bodies:
            if body.label_rect and body.label_rect.collidepoint(mouse_pos):
                self.selected_body = body
                break

        for key, rect in self.telemetry_menu_rects.items():
            if rect.collidepoint(mouse_pos):
                self.telemetry_options[key] = not self.telemetry_options[key]
                return



    def build_info_box(self, body):

        lines = [body.name]

        if self.telemetry_options["speed"]:
            speed = body.get_speed() / 1000
            lines.append(f"Speed: {speed:.1f} km/s")

        if self.telemetry_options["distance"]:
            distance = body.get_distance() / 1e9
            lines.append(f"Distance: {distance:.1f} million km")

        if self.telemetry_options["mass"]:
            lines.append(f"Mass: {body.mass:.2e} kg")

        if self.telemetry_options["velocity"]:
            lines.append(f"Vx: {body.vx / 1000:.1f} km/s")
            lines.append(f"Vy: {body.vy / 1000:.1f} km/s")

        return lines


    def draw_tel_menu(self,screen):
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

            pygame.draw.rect(screen, (255,255,255), checkbox_rect,2)

            if self.telemetry_options[key]:
                pygame.draw.line(screen, (255,255,255), checkbox_rect.topleft, checkbox_rect.bottomright, 2)

            text = self.font.render(label, True, (255,255,255))
            screen.blit(text, (x+28, y - 2))

            self.telemetry_menu_rects[key] = checkbox_rect

            y += 28



    def draw(self):

        self.screen.fill((0, 0, 0))

        for body in self.bodies:
            body_screen_pos = self.to_screen_position(body.x, body.y)
            trail_position = [
                self.to_screen_position(x, y)
                for x, y in body.trail

            ]

            body.draw(self.screen, body_screen_pos, trail_position, self.font)

            lines = self.build_info_box(body)


            if body ==  self.selected_body:
                body.draw_info_box(self.screen, body_screen_pos, self.font, lines)

        simulation_days = self.simulation_time / 86400
        simulation_years = simulation_days / 365.25
        self.draw_tel_menu(self.screen)
        clock_text = self.font.render(
            f"Simulation Time: {simulation_years:.2f} years",
            True,
            (25,255,255)
        )

        self.screen.blit(clock_text, (10,10))

        pygame.display.flip()

    def apply_gravity(self):
        sun = self.bodies[0]

        sun.ax = 0
        sun.ay = 0

        for body in self.bodies[1:]:
            dx = sun.x - body.x
            dy = sun.y - body.y

            distance = math.sqrt(dx ** 2 + dy ** 2)

            if distance == 0:
                continue

            acceleration = self.g * sun.mass / distance ** 2
            body.ax = acceleration * dx / distance
            body.ay = acceleration * dy / distance
