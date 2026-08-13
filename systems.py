import math

class MovementSystem:
    def update(self, dt, positions, velocities, accelerations):
        for body in positions:
            if body in velocities and body in accelerations:
                position = positions[body]
                velocity = velocities[body]
                acceleration = accelerations[body]
                #print (f"Before {position.x},{ position.y}")
                velocity.vx += acceleration.ax * dt
                velocity.vy += acceleration.ay * dt

                position.x += velocity.vx * dt
                position.y += velocity.vy * dt
                #print(f"After {position.x}, {position.y}")




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


class GravitySystem:
    def update(self, masses, positions, accelerations):
        g = 6.67430e-11
        for entity in positions:
            accelerations[entity].ax = 0
            accelerations[entity].ay = 0

            for other in positions:
                if entity == other:
                    continue


                dx = positions[other].x - positions[entity].x
                dy = positions[other].y - positions[entity].y

                distance = math.hypot(dx,dy)

                if distance == 0:
                    continue

                acceleration = (g * masses[other].value) / distance ** 2

                accelerations[entity].ax +=(
                    acceleration * dx / distance
                )

                accelerations[entity].ay += (
                    acceleration * dy / distance
                )
