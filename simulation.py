
from systems import MovementSystem, TrailSystem, GravitySystem
from planet_loader import load_planets
from create_spacecraft import create_spacecraft


class Simulation:
    def __init__(self):

        #Basic Variables
        self.paused = False

        self.simulation_time = 0
        self.selected_entity = None

        # System Constructors
        self.movement = MovementSystem()
        self.trail_system = TrailSystem()
        self.gravity = GravitySystem()

        #Loading in the planet data
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



        #Declaration of the Spacecraft Array
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




    def select_entity(self, entity):
        self.selected_entity = entity



    def toggle_pause(self):
        self.paused = not self.paused






    def get_simulation_time(self):
        return self.simulation_time
    def get_current_selected(self):
        return self.selected_entity

    def launch_rocket(self, delta_v):
        if self.selected_entity is None:
            return

        spacecraft = create_spacecraft(self.next_entity_id, self.selected_entity, delta_v, "prograde", self.radii, self.positions, self.velocities,
            self.accelerations, self.masses, self.trails, self.identities, self.renderables)

        self.spacecraft.append(spacecraft)
        self.next_entity_id += 1
