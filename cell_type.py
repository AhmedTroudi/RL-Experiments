from enum import Enum


class CellType(Enum):
    VOID: int = 0
    ROBOT: int = 1
    WALL: int = 2
    GOAL: int = 3
    PATH: int = 4
    MUD: int = 5
    IN_MUD: int = 6
