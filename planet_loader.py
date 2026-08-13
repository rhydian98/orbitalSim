import json
from json.decoder import JSONDecodeError

from components import Identity, Velocity, Acceleration, Position, Renderable, Mass, Trail, Radius

def load_planets(path="planets.json"):
    try:
        with open(path, "r") as file:
            planet_data = json.load(file)

    except FileNotFoundError:
        print("Error: file not found")
        return None

    except JSONDecodeError:
        print(f"Error: invalid json in {path}")
        return None

    positions = {}
    velocities = {}
    accelerations = {}
    masses = {}
    renderables = {}
    radii = {}
    trails = {}
    identities = {}

    entity_by_name = {}

    next_entity_id = 0

    for planet in planet_data:
        entity = next_entity_id
        next_entity_id += 1

        identities[entity] = Identity(planet["name"])

        positions[entity] = Position(
            planet["x"],
            planet["y"]
        )

        velocities[entity] = Velocity(
            planet["vx"],
            planet["vy"]
        )

        accelerations[entity] = Acceleration(
            planet["ax"],
            planet["ay"]
        )

        masses[entity] = Mass(
            planet["mass"]
        )

        radii[entity] = Radius(
            planet["physical_radius"]
        )

        renderables[entity] = Renderable(
            planet["color"],
            planet["radius"]
        )
        trails[entity] = Trail()

        entity_by_name[planet["name"]] = entity

    return {
       "positions": positions,
       "velocities": velocities,
       "accelerations": accelerations,
       "masses": masses,
       "radii": radii,
       "renderables": renderables,
       "trails": trails,
       "identities": identities,
       "entities_by_name": entity_by_name,
       "next_entity_id": next_entity_id

        }
