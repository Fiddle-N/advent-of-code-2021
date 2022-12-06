import collections
import copy
import dataclasses
import enum
import functools
import queue
import typing

AMPHIPODS_PER_ROW = 4


@dataclasses.dataclass(eq=True, frozen=True, order=True)
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


@dataclasses.dataclass(frozen=True)
class Location:
    coords: Coords
    distance: int


class BurrowMapSpace(enum.Enum):
    WALL = "#"
    HALLWAY = "."
    EMPTY = " "


class BurrowRoomType(enum.Enum):
    OPEN = enum.auto()
    END = enum.auto()


class BurrowHallwayType(enum.Enum):
    OUTSIDE_ROOM = enum.auto()
    AWAY_FROM_ROOM = enum.auto()


class BurrowAmphipodState(enum.Enum):
    ORIGINAL = enum.auto()
    HALLWAY = enum.auto()
    SETTLED = enum.auto()


class AmphipodType(enum.Enum):
    AMBER = "A"
    BRONZE = "B"
    COPPER = "C"
    DESERT = "D"


AMPHIPOD_ENERGY = {
    AmphipodType.AMBER: 1,
    AmphipodType.BRONZE: 10,
    AmphipodType.COPPER: 100,
    AmphipodType.DESERT: 1000,
}


class AmphipodCounterMixin:
    def __init_subclass__(cls, /, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._ids = collections.Counter()

    def __init__(self, amphipod_type: AmphipodType):
        self.id = type(self)._ids[amphipod_type]
        type(self)._ids[amphipod_type] += 1
        self.type = amphipod_type

    def __repr__(self):
        return f"<{type(self).__name__}: type={self.type.name}, id={self.id}>"


AMPHIPOD_HASH_CALLS = 0


class Amphipod(AmphipodCounterMixin):

    def __hash__(self):
        global AMPHIPOD_HASH_CALLS
        AMPHIPOD_HASH_CALLS += 1
        return hash((self.type, self.id))

    def __eq__(self, other):
        return (self.type == other.type) and (self.id == other.id)


class BurrowAmphipod:

    def __init__(self, amphipod_type: AmphipodType):
        self.amphipod: Amphipod = Amphipod(amphipod_type)
        self.state: BurrowAmphipodState = BurrowAmphipodState.ORIGINAL

    def __repr__(self):
        return f"<{type(self).__name__}: type={self.amphipod.type.name}, id={self.amphipod.id}, state={self.state}>"


class BurrowAmphipodSpace(AmphipodCounterMixin):

    def __init__(self, amphipod_type: AmphipodType, room_type: BurrowRoomType):
        super().__init__(amphipod_type)
        self.room_type: BurrowRoomType = room_type

    def __repr__(self):
        return f"<{type(self).__name__}: type={self.type.name}, id={self.id}, room_type={self.room_type}>"


@dataclasses.dataclass
class Node:
    this: typing.Union[BurrowMapSpace, BurrowAmphipodSpace]
    neighbours: list[Location]


@dataclasses.dataclass(frozen=True, eq=True)
class Move:
    amphipod: BurrowAmphipod
    location: typing.Union[BurrowMapSpace, BurrowAmphipodSpace]


@dataclasses.dataclass(frozen=True, order=True)
class AmphipodConfiguration:
    energy: int
    amphipods: dict[Coords, Amphipod] = dataclasses.field(compare=False)
    amphipods_state: dict[Amphipod, BurrowAmphipodState] = dataclasses.field(compare=False)
    history: set[tuple[Amphipod, Coords]] = dataclasses.field(default_factory=set)

    @property
    def diagram(self):
        burrow_top = """\
#############
#...........#
### # # # ###"""

        burrow_mid_row = '  # # # # #  '

        burrow_bottom_row = '  #########  '

        burrow_middle = '\n'.join([burrow_mid_row] * ((len(self.amphipods) // AMPHIPODS_PER_ROW) - 1))
        burrow = '\n'.join([burrow_top, burrow_middle, burrow_bottom_row])

        base_diagram_list = [
            list(row)
            for row in burrow.splitlines()
        ]

        for amphipod_coord, amphipod in self.amphipods.items():
            base_diagram_list[amphipod_coord.y][amphipod_coord.x] = amphipod.type.value

        return '\n'.join([''.join(row) for row in base_diagram_list])


class BurrowMap:
    def __init__(self, burrow_map):
        self.map = burrow_map
        self._amphipod_space_coords = self._calculate_amphipod_spaces()

    def _calculate_amphipod_spaces(self):
        coords = collections.defaultdict(dict)
        for coord, space in self.map.items():
            if isinstance(space.this, BurrowAmphipodSpace):
                coords[space.this.type][space.this.room_type] = coord
        return coords

    def get_amphipod_coords(self, amphipod_type: AmphipodType):
        return self._amphipod_space_coords[amphipod_type]

    def get_hallway_coords(self):
        return [coord for coord, node in self.map.items() if node.this == BurrowHallwayType.AWAY_FROM_ROOM]

    @functools.cache
    def _path_coords(self, start: Coords, end: Coords):

        def dfs(space=start, path=None):
            if path is None:
                path = []
            path.append(space)
            if space == end:
                return path
            for neighbour in self.map[space].neighbours:
                assert neighbour.distance == 1
                neighbour_space = neighbour.coords
                if neighbour_space not in path:
                    if (next_path := dfs(neighbour_space, path.copy())) is not None:
                        # only return if we have a path that ends in our destination
                        return next_path

        d = dfs()
        return d

    @functools.cache
    def path_coords(self, start: Coords, end: Coords, exclude_start=False):
        path = self._path_coords(start, end)
        return path[1:] if exclude_start else path


class BurrowMapGenerator:

    BURROW_TOP = """\
#############
#...........#
###A#B#C#D###"""

    BURROW_MID_ROW = '  #A#B#C#D#  '

    BURROW_BOTTOM_ROW = '  #########  '

    def __init__(self):
        self.height = None
        self.width = None

    def create(self, amphipod_rows):
        burrow_middle = '\n'.join([self.BURROW_MID_ROW] * (amphipod_rows - 1))
        burrow = '\n'.join([self.BURROW_TOP, burrow_middle, self.BURROW_BOTTOM_ROW])
        burrow_grid = self._generate_grid(burrow)
        self.height = len(burrow_grid)
        self.width = len(burrow_grid[0])
        burrow_map = self._generate_map(burrow_grid)
        return BurrowMap(burrow_map)

    def get_neighbours(self, coord):
        neighbour_coords = []
        for offset in OFFSETS:
            neighbour_coord = coord + offset
            if (
                0 <= neighbour_coord.x < self.width
                and 0 <= neighbour_coord.y < self.height
            ):
                neighbour_coords.append(neighbour_coord)
        return neighbour_coords

    def _generate_grid(self, burrow):
        burrow_grid = []
        for row in burrow.splitlines():
            list_row = []
            for raw_space in row:
                try:
                    space = AmphipodType(raw_space)
                except ValueError:
                    space = BurrowMapSpace(raw_space)
                list_row.append(space)
            burrow_grid.append(list_row)
        return burrow_grid

    def _generate_map(self, burrow_preprocessed):
        burrow_map = {}
        neighbour_nodes_to_side_room_types = {
            2: BurrowRoomType.OPEN,
            1: BurrowRoomType.END,
        }
        for y, row in enumerate(burrow_preprocessed):
            for x, space in enumerate(row):
                coord = Coords(x, y)
                if space in (BurrowMapSpace.WALL, BurrowMapSpace.EMPTY):
                    continue

                neighbour_coords_including_walls = self.get_neighbours(coord)
                neighbour_coords = [
                    coord
                    for coord in neighbour_coords_including_walls
                    if burrow_preprocessed[coord.y][coord.x] != BurrowMapSpace.WALL
                ]
                neighbour_nodes = [
                    Location(coord, distance=1) for coord in neighbour_coords
                ]
                if space == BurrowMapSpace.HALLWAY:
                    node_val = BurrowHallwayType.OUTSIDE_ROOM if len(neighbour_nodes) == 3 else BurrowHallwayType.AWAY_FROM_ROOM
                elif space in AmphipodType:
                    node_val = BurrowAmphipodSpace(space, neighbour_nodes_to_side_room_types[len(neighbour_nodes)])
                else:
                    raise Exception
                node = Node(node_val, neighbour_nodes)
                burrow_map[coord] = node
        return burrow_map



class AmphipodOrganiser:
    def __init__(self, burrow_start):
        amphipods = self._find_amphipods(burrow_start)
        amphipod_rows = len(amphipods) // AMPHIPODS_PER_ROW

        self.burrow_map = BurrowMapGenerator().create(amphipod_rows)

        amphipods_state = self._determine_amphipod_state(amphipods)
        self.start_state = AmphipodConfiguration(0, amphipods, amphipods_state)

        self._total_energy = None
        self._cache = None

    @classmethod
    def read_file(cls):
        with open('input.txt') as f:
            return cls(f.read().strip())

    def _find_amphipods(self, burrow_start):
        amphipods: dict[Coords, Amphipod] = {}
        for y, row in enumerate(burrow_start.splitlines()):
            for x, raw_space in enumerate(row):
                try:
                    space = AmphipodType(raw_space)
                except ValueError:
                    pass
                else:
                    amphipods[Coords(x, y)] = Amphipod(space)
        return amphipods

    def _determine_amphipod_state(self, amphipods: dict[Coords, Amphipod]):
        amphipods_state = {amphipod: BurrowAmphipodState.ORIGINAL for amphipod in amphipods.values()}

        open_neighbours_of_settled_end_amphipods = set()

        for coord, amphipod in amphipods.items():
            room = self.burrow_map.map[coord]
            if room.this.room_type == BurrowRoomType.END:    # we need to check bottom row first
                room_amphipod_type = room.this.type
                if room_amphipod_type == amphipod.type:
                    amphipods_state[amphipod] = BurrowAmphipodState.SETTLED
                    open_neighbours_of_settled_end_amphipods.add(room.neighbours[0].coords)        # assume end only has one neighbour

        # now check top row of those next to settled bottom row
        for coord in open_neighbours_of_settled_end_amphipods:
            amphipod = amphipods[coord]
            room = self.burrow_map.map[coord]
            room_amphipod_type = room.this.type
            if room_amphipod_type == amphipod.type:
                amphipods_state[amphipod] = BurrowAmphipodState.SETTLED

        return amphipods_state

    def _win_condition(self, state):
        if all(amphipod_state == BurrowAmphipodState.SETTLED for amphipod_state in state.amphipods_state.values()):
            return True
        return False

    def _free_room(self, amphipods: dict[Coords, Amphipod], amphipod: Amphipod):
        amphipod_rooms = self.burrow_map.get_amphipod_coords(amphipod.type)

        if (end_coords := amphipod_rooms[BurrowRoomType.END]) not in amphipods:
            if amphipod_rooms[BurrowRoomType.OPEN] not in amphipods:
                # both spaces are empty - move into the end room
                return end_coords
            else:
                return Exception('somehow open room is occupied and blocking off an empty end room - should not be the case')
        elif amphipods[end_coords].type == amphipod.type:
            # end room is occupied with the correct amphipod type
            if (open_coords := amphipod_rooms[BurrowRoomType.OPEN]) not in amphipods:
                # open room is empty
                return open_coords
            else:
                # open room is occupied and blocking off end room populated (with the correct amphipod type)
                return None
        else:
            return None

    def _path_details(self, state, amphipod_coord: Coords, dest_coord: Coords):
        intrapath_coords = self.burrow_map.path_coords(amphipod_coord, dest_coord, exclude_start=True)
        free_path = not any(intrapath_coord in state.amphipods for intrapath_coord in intrapath_coords)
        distance = len(intrapath_coords)
        return free_path, distance

    def _create_next_state(self, state, old_coord, new_coord, distance, amphipod_state: BurrowAmphipodState):
        next_amphipods = state.amphipods.copy()
        amphipod = next_amphipods.pop(old_coord)
        next_amphipods[new_coord] = amphipod

        next_history = state.history.copy()
        next_history.add((amphipod, new_coord))

        next_amphipods_state = state.amphipods_state.copy()
        next_amphipods_state[amphipod] = amphipod_state

        energy = AMPHIPOD_ENERGY[amphipod.type] * distance

        next_state = AmphipodConfiguration(
            energy=state.energy + energy,
            amphipods=next_amphipods,
            amphipods_state=next_amphipods_state,
            history=next_history
        )
        return next_state

    def _move_amphipod(self, state, amphipod_coord, next_coord, distance, next_amphipod_state):
        next_state = self._create_next_state(state, amphipod_coord, next_coord, distance, amphipod_state=next_amphipod_state)
        history_frozen = frozenset(x for x in next_state.history)
        if history_frozen in self._cache:
            return False
        self._cache.add(history_frozen)
        self._dfs(next_state)
        return True

    def _dfs(self, state):
        if self._total_energy is not None and state.energy >= self._total_energy:
            return
        if self._win_condition(state):
            if self._total_energy is None or state.energy < self._total_energy:
                self._total_energy = state.energy
            return
        for amphipod_coord, amphipod in state.amphipods.items():
            if (amphipod_state := state.amphipods_state[amphipod]) in (BurrowAmphipodState.HALLWAY, BurrowAmphipodState.ORIGINAL):
                if free_room_coord := self._free_room(state.amphipods, amphipod):
                    free_path, distance = self._path_details(state, amphipod_coord, free_room_coord)
                if free_room_coord and free_path:
                    # amphipod can move straight into settled room
                    is_new_state = self._move_amphipod(
                        state=state, amphipod_coord=amphipod_coord, next_coord=free_room_coord, distance=distance, next_amphipod_state=BurrowAmphipodState.SETTLED
                    )
                    if not is_new_state:
                        continue

                elif amphipod_state == BurrowAmphipodState.ORIGINAL:
                    # amphipod must move into hallway
                    hallway_coords = self.burrow_map.get_hallway_coords()
                    for hallway_coord in hallway_coords:
                        free_path, distance = self._path_details(state, amphipod_coord, hallway_coord)
                        if not free_path:
                            # spaces from amphipod to hallway room is occupied
                            continue

                        is_new_state = self._move_amphipod(
                            state=state, amphipod_coord=amphipod_coord, next_coord=hallway_coord, distance=distance, next_amphipod_state=BurrowAmphipodState.HALLWAY
                        )
                        if not is_new_state:
                            continue

    def organise(self):
        self._cache = set()
        self._dfs(self.start_state)
        return self._total_energy


def main():
    ao = AmphipodOrganiser.read_file()
    total_energy = ao.organise()
    print(f'{total_energy=}')
    print(f'{AMPHIPOD_HASH_CALLS=:,}')

if __name__ == '__main__':
    import timeit
    print(timeit.timeit(main, number=1))



# if __name__ == '__main__':
#     import cProfile
#     cProfile.run('main()')
