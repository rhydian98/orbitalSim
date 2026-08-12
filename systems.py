import math

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


class GravitySystem:
    def update(self, star, masses, positions, accelerations):
        g = 6.67430e-11
        sun_pos_x = positions[star].x
        sun_pos_y = positions[star].y


        for body in positions:
            if body == star:
                continue
            dx = sun_pos_x - positions[body].x
            dy = sun_pos_y - positions[body].y

            distance = math.sqrt(dx ** 2 + dy ** 2)

            if distance == 0:
                continue

            acceleration = g * masses[star].value / distance ** 2
            accelerations[body].ax = acceleration * dx / distance
            accelerations[body].ay = acceleration * dy / distance
