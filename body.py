class Body:
    def __init__(self, name, mass, color, x=0.0 ,y=0.0, radius=1, vx=0, vy=0, ax=0, ay=0):
        self.name = name
        self.x = x
        self.y = y
        self.mass = mass
        self.color = color
        self.radius = radius
        self.vx = vx
        self.vy = vy
        self.ax = ax
        self.ay = ay


    def update_position(self, dt):
        self.vx += self.ax * dt
        self.vy += self.ay * dt

        self.x += self.vx * dt
        self.y += self.vy * dt
