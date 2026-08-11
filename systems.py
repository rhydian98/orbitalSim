class MovementSystem:
    def update(self, dt, positions, velocities, accelerations):
        for body in positions:
            if body in velocities and body in accelerations:
                position = positions[body]
                velocity = velocities[body]
                acceleration = accelerations[body]
                print (f"Before {position.x},{ position.y}")
                velocity.vx += acceleration.ax * dt
                velocity.vy += acceleration.ay * dt

                position.x += velocity.vx * dt
                position.y += velocity.vy * dt
                print(f"After {position.x}, {position.y}")




class TrailSystem:
    def update(self, positions, trails):
        for entity in trails:
            if entity in trails:
                if entity in positions:
                    position = positions[entity]
                    trail = trails[entity]


                    trail.points.append(
                        (position.x, position.y)
                    )

                    if len(trail.points) > trail.maxLength:
                        trail.points.pop(0)
