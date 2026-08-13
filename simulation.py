import pygame
from pygame.time import Clock
from constants import SCALE
import math
from systems import MovementSystem, TrailSystem, GravitySystem
from ui import Ui
from helpers import get_distance, get_speed
from planet_loader import load_planets
from create_spacecraft import create_spacecraft
from draw import Rendering
class Simulation:
    def __init__(self, screen):
        self.paused = False
        self.screen = screen
        self.clock = Clock()

        self.font = pygame.font.Font(None, 18)
        self.simulation_time = 0
        self.selected_body = None
        self.movement = MovementSystem()
        self.trail_system = TrailSystem()
        self.gravity = GravitySystem()
        self.ui = Ui()
        self.label_rects = {}
        self.rendering = Rendering()

        ecs = load_planets()

        if ecs is None:
            raise RuntimeError("Failed to load planet data")

        self.positions = ecs["positions"]
        self.accelerations = ecs["accelerations"]
        self.masses = ecs["masses"]
        self.velocities = ecs["velocities"]
        self.radii = ecs["radii"]
        self.trails = ecs["trails"]
        self.identities = ecs["identities"]
        self.renderables = ecs["renderables"]

        self.entities_by_name = ecs["entities_by_name"]
        self.next_entity_id = ecs["next_entity_id"]


        self.telemetry_options = {
            "speed": True,
            "distance": True,
            "mass": True,
            "velocity": False,
            "acceleration": False
        }

        self.telemetry_menu_rects = {}
        self.launch_rect=pygame.Rect(20,280,100,30)

        self.delta_v_text = ""
        self.delta_v_active = False
        self.delta_v_rect = pygame.Rect(20,220,100,30)

        self.spacecraft = []
        self.next_entity_id += 1




    def update(self, dt):
        if self.paused:
            return
        self.simulation_time += dt


        max_step = 60

        remaining = dt
        while remaining > 0:

            step= min(max_step, remaining)
            self.gravity.update(self.masses, self.positions, self.accelerations)
            self.movement.update(step, self.positions, self.velocities, self.accelerations)


            remaining -= step

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

        if self.delta_v_rect.collidepoint(mouse_pos):
            self.delta_v_active = True
        else:
            self.delta_v_active = False

        if self.launch_rect.collidepoint(mouse_pos):
            self.launch_rocket()


    def handle_keydown(self, event):
        if event.key == pygame.K_SPACE:
            self.paused = not self.paused

        if not self.delta_v_active:
            return

        if event.key == pygame.K_BACKSPACE:
            self.delta_v_text = self.delta_v_text[:-1]
        elif event.key == pygame.K_RETURN:
            self.delta_v_active = False
        elif event.unicode.isdigit() or event.unicode == ".":
            self.delta_v_text += event.unicode




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

            lines = self.build_info_box(entity)

            if entity ==  self.selected_body:
                 self.ui.draw_info_box(self.screen, body_screen_position, self.font, lines)

            self.label_rects[entity] = self.rendering.draw_entity(self.screen, body_screen_position, renderable, identity, trail_position, self.font )

        simulation_days = self.simulation_time / 86400
        simulation_years = simulation_days / 365.25
        self.ui.draw_tel_menu(self.screen, self.telemetry_menu_rects, self.telemetry_options, self.font)
        self.ui.draw_delta_v_input(self.screen, self.font, self.delta_v_rect, self.delta_v_text, self.delta_v_active)
        self.ui.draw_launch_button(self.screen, self.font, self.launch_rect)
        self.ui.draw_simulation_clock(self.screen, self.font, (simulation_years, simulation_days))



        pygame.display.flip()

    def launch_rocket(self):
        if self.selected_body is None:
            return

        if not self.delta_v_text:
            return

        delta_v = float(self.delta_v_text)*1000

        spacecraft = create_spacecraft(self.next_entity_id, self.selected_body, delta_v, "prograde", self.radii, self.positions, self.velocities,
            self.accelerations, self.masses, self.trails, self.identities, self.renderables)

        self.spacecraft.append(spacecraft)
        self.next_entity_id += 1
