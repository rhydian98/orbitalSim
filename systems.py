class MovementSystem:
    def update(self, dt, positions, velocities, accelerations):
        for entity in positions:
            if entity in velocities and entity in accelerations:
                position = positions[entity]
                velocity = velocities[entity]
                acceleration = accelerations[entity]

                velocity.vx += acceleration.ax * dt
                velocity.vy += acceleration.ay * dt

                position.x += velocity.vx * dt
                position.y += velocity.vy * dt
