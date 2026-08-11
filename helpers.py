import math

def get_speed( velocity):
    return math.hypot(velocity.vx, velocity.vy)

def get_distance(position):
    return math.hypot(position.x, position.y)
