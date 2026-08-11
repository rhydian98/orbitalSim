import pygame
from pygame.time import Clock
from constants import SCALE
import math
from systems import MovementSystem, TrailSystem
from ui import Ui
from helpers import get_distance, get_speed
from planet_loader import load_planets


class Simulation:
    def __init__(self, screen):

        self.screen = screen
        self.clock = Clock()
        self.g = 6.67430e-11
        self.font = pygame.font.Font(None, 18)
        self.simulation_time = 0
        self.selected_body = None
        self.movement = MovementSystem()
        self.trail_system = TrailSystem()
        self.ui = Ui()
        self.label_rects = {}


        ecs = load_planets()

        if ecs is None:
            raise RuntimeError("Failed to load planet data")

        self.positions = ecs["positions"]
        self.accelerations = ecs["accelerations"]
        self.masses = ecs["masses"]
        self.velocities = ecs["velocities"]
        self.trails = ecs["trails"]
        self.identities = ecs["identities"]
        self.renderables = ecs["renderables"]

        self.entities_by_name = ecs["entities_by_name"]
        self.next_entity_id = ecs["next_entity_id"]


        print(self.entities_by_name)
        print(self.positions[self.entities_by_name["Earth"]])


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
        self.movement.update(dt, self.positions, self.velocities, self.accelerations)
        self.trail_system.update(self.positions, self.trails)


    def to_screen_position(self, x, y):
        screen_center_x = self.screen.get_width() // 2
        screen_center_y = self.screen.get_height() // 2

        screen_x = screen_center_x + x * SCALE
        screen_y = screen_center_y - y * SCALE

        return int(screen_x), int(screen_y)

    def handle_click(self, mouse_pos):
        for entity in self.identities:
            rect = self.label_rects.get(entity)
            if rect and rect.collidepoint(mouse_pos):
                self.selected_body = entity
                break

        for key, rect in self.telemetry_menu_rects.items():
            if rect.collidepoint(mouse_pos):
                self.telemetry_options[key] = not self.telemetry_options[key]
                return



    def build_info_box(self, body):

        lines = [self.identities[body].name]

        if self.telemetry_options["speed"]:
            speed = get_speed(self.velocities[body]) / 1000
            lines.append(f"Speed: {speed:.1f} km/s")

        if self.telemetry_options["distance"]:
            distance = get_distance(self.positions[body]) / 1e9
            lines.append(f"Distance: {distance:.1f} million km")

        if self.telemetry_options["mass"]:
            lines.append(f"Mass: {self.masses[body].value:.2e} kg")

        if self.telemetry_options["velocity"]:
            lines.append(f"Vx: {self.velocities[body].vx / 1000:.1f} km/s")
            lines.append(f"Vy: {self.velocities[body].vy/ 1000:.1f} km/s")

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

        for entity in self.renderables:
            position = self.positions[entity]
            renderable = self.renderables[entity]
            identity = self.identities[entity]
            trail = self.trails.get(entity)

            body_screen_position = self.to_screen_position(position.x, position.y)
            if trail:
                trail_position = [
                    self.to_screen_position(x,y)
                    for x, y in trail.points
                ]
            else:
                trail_position = []

            for point in trail_position:
                pygame.draw.circle(self.screen, renderable.color, point, max(1, renderable.radius//2))

            pygame.draw.circle(self.screen, renderable.color,body_screen_position, renderable.radius)

            lines = self.build_info_box(entity)


            if entity ==  self.selected_body:
                 self.ui.draw_info_box(self.screen, body_screen_position, self.font, lines)

            text = self.font.render(identity.name, True, (255,255,255))

            label_pos = (
                body_screen_position[0] + renderable.radius + 5,
                body_screen_position[1]

            )

            self.label_rects[entity] = text.get_rect(topleft=label_pos)

            self.screen.blit(text, label_pos)

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
        sun = self.entities_by_name["Sun"]

        sun_pos_x = self.positions[sun].x
        sun_pos_y = self.positions[sun].y


        for body in self.positions:
            if body == sun:
                continue
            dx = sun_pos_x - self.positions[body].x
            dy = sun_pos_y - self.positions[body].y

            distance = math.sqrt(dx ** 2 + dy ** 2)

            if distance == 0:
                continue

            acceleration = self.g * self.masses[sun].value / distance ** 2
            self.accelerations[body].ax = acceleration * dx / distance
            self.accelerations[body].ay = acceleration * dy / distance
