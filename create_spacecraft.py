from components import Position, Velocity, Identity, Acceleration, Mass, Trail, Renderable
import math
def create_spacecraft( entity, launch_entity, delta_v, direction,radii,
    positions, velocities, accelerations, masses, trails, identities, renderables):
        position = positions[launch_entity]
        velocity = velocities[launch_entity]

        speed = math.hypot(velocity.vx, velocity.vy)

        #direction_x = velocity.vx / speed
        #direction_y = velocity.vy / speed

        #if direction == "retrograde":
         #   direction_x *= -1
         #   direction_y *= -1


        identities[entity] = Identity(name="")
        launch_distance = float(radii[launch_entity].radius) + 400_000.0

        positions[entity] = Position(
            position.x + launch_distance,
            position.y
        )


        velocities[entity] = Velocity(
            velocity.vx ,
            velocity.vy + delta_v
        )

        accelerations[entity] = Acceleration(0,0)

        masses[entity] = Mass(10_000)

        trails[entity] = Trail()

        renderables[entity] = Renderable((128,128,128), 3)

        print("delta_v:", delta_v)
        print("planet radius:", radii[launch_entity].radius)
        print("launch distance:", launch_distance)

        print(
            "relative position:",
            positions[entity].x - positions[launch_entity].x,
            positions[entity].y - positions[launch_entity].y
        )

        print(
            "relative velocity:",
            velocities[entity].vx - velocities[launch_entity].vx,
            velocities[entity].vy - velocities[launch_entity].vy
        )

        return entity
