from enum import Enum


class Direction(Enum):
    LEFT = (-1, 0)
    DOWN = (0, 1)
    UP = (0, -1)
    RIGHT = (1, 0)
