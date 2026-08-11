from body import Body
from constants import AU

bodies = [
    Body("Sun", 1.989e30, (255, 255, 0), 400, 300, 12),
    Body("Mercury", mass=3.3011e23, color=(170,170,170), x=57.91e9, y=0, radius=4, vx=0, vy=47_360),
    Body("Venus", mass=4.867e24, color=(220,180,80), x=108.21e9, y=0, radius=5, vx=0, vy=35_020),
    Body("Earth", 5.972e24, (0, 0, 255), AU, 200, 5, vx=0, vy=29_780),
    Body("Mars", 6.417e23, (255, 0, 0), 1.524*AU, 400, 3, vx=0, vy=24_070),

]
