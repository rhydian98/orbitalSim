from components import Position, Velocity, Identity, Acceleration, Mass, Trail, Renderable
import math
def create_spacecraft( entity, launch_entity, delta_v, direction,
    positions, velocities, accelerations, masses, trails, identities, renderables):
        position = positions[launch_entity]
        velocity = velocities[launch_entity]

        speed = math.hypot(velocity.vx, velocity.vy)

        direction_x = velocity.vx / speed
        direction_y = velocity.vy / speed

        if direction == "retrograde":
            direction_x *= -1
            direction_y *= -1


        identities[entity] = Identity(name="")


        positions[entity] = Position(
            position.x,
            position.y
        )


        velocities[entity] = Velocity(
            velocity.vx + direction_x * delta_v,
            velocity.vy + direction_y * delta_v
        )

        accelerations[entity] = Acceleration(0,0)

        masses[entity] = Mass(10_000)

        trails[entity] = Trail()

        renderables[entity] = Renderable((128,128,128), 3)

        return entity
