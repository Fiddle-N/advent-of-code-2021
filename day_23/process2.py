import collections
import dataclasses
import enum
import queue
import typing


@dataclasses.dataclass(frozen=True, order=True)
class Coords:
    x: int
    y: int

    def __add__(self, other):
        return Coords(self.x + other.x, self.y + other.y)


OFFSETS = [
    Coords(0, 1),
    Coords(1, 0),
    Coords(0, -1),
    Coords(-1, 0),
]


class AmphipodType(enum.Enum):
    AMBER = "A"
    BRONZE = "B"
    COPPER = "C"
    DESERT = "D"


class MapSpace(enum.Enum):
    WALL = "#"
    HALLWAY = "."
    EMPTY = " "


AMPHIPOD_ENERGY = {
    AmphipodType.AMBER: 1,
    AmphipodType.BRONZE: 10,
    AmphipodType.COPPER: 100,
    AmphipodType.DESERT: 1000,
}
