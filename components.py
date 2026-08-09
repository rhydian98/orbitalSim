from dataclasses import dataclass

@dataclass
class Position:
    x: float
    y: float

@dataclass
class Velocity:
    vx: float
    vy: float
@dataclass
class Acceleration:
    ax: float
    ay: float

@dataclass
class Mass:
    value: float

@dataclass
class Renderable:
    name: str
    color: tuple
    radius: int
