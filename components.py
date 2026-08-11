from dataclasses import dataclass, field
import string
from tokenize import String

@dataclass
class Identity:
    name: str


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
    color: tuple
    radius: int

@dataclass
class Trail:
    points: list = field(default_factory=list)
    maxLength: int = 200
