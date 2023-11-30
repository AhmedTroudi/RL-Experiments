from enum import Enum


class CellType(Enum):
    VOID = 0
    ROBOT = 1
    WALL = 2
    GOAL = 3
    PATH = 4
    MUD = 5
    IN_MUD = 6
