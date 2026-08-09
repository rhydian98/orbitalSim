

from components import Position, Velocity, Acceleration
from systems import MovementSystem

earth = 1

positions = {

    earth : Position(0,0)

}

velocities = {

    earth: Velocity(10,0)

}

accelerations = {

    earth: Acceleration(2,0)

}

movement_system = MovementSystem()



for i in range(10):
    movement_system.update(
        1,
        positions,
        velocities,
        accelerations

    )
    print(positions[earth])
