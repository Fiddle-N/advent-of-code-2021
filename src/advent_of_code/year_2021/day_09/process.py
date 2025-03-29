import collections
import dataclasses
import math


@dataclasses.dataclass(frozen=True)
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


class SmokeBasin:

    def __init__(self, heightmap):
        self.heightmap = [
            [int(point) for point in row]
            for row in heightmap.split('\n')
        ]
        self.height = len(self.heightmap)
        self.width = len(self.heightmap[0])

    @classmethod
    def read_file(cls):
        with open('input.txt') as f:
            return cls(f.read().strip())

    def _get_neighbours(self, coord):
        neighbour_coords = []
        for offset in OFFSETS:
            neighbour_coord = coord + offset
            if 0 <= neighbour_coord.x < self.width and 0 <= neighbour_coord.y < self.height:
                neighbour_coords.append(neighbour_coord)
        return neighbour_coords

    def _get_low_points(self):
        low_points = []
        for y, row in enumerate(self.heightmap):
            for x, point in enumerate(row):
                coord = Coords(x, y)
                neighbour_coords = self._get_neighbours(coord)
                neighbours = [self.heightmap[coord.y][coord.x] for coord in neighbour_coords]
                if all(point < neighbour for neighbour in neighbours):
                    low_points.append(coord)
        return low_points

    def calculate_low_point_risk_level(self):
        low_point_coords = self._get_low_points()
        low_point_values = [self.heightmap[coord.y][coord.x] for coord in low_point_coords]
        return sum(low_point_values) + len(low_point_values)

    def _get_basin_size(self, low_point):
        seen = set()
        coords_queue = collections.deque([low_point])
        while coords_queue:
            coord = coords_queue.popleft()
            seen.add(coord)
            neighbour_coords = self._get_neighbours(coord)
            for neighbour_coord in neighbour_coords:
                if neighbour_coord not in seen and self.heightmap[neighbour_coord.y][neighbour_coord.x] != 9:
                    coords_queue.append(neighbour_coord)
        return len(seen)

    def three_largest_basins_size(self):
        low_point_coords = self._get_low_points()
        basin_sizes = [self._get_basin_size(low_point) for low_point in low_point_coords]
        sorted_basin_sizes = sorted(basin_sizes, reverse=True)
        return math.prod(sorted_basin_sizes[:3])


def main():
    smoke_basin = SmokeBasin.read_file()
    print('Low points risk level:', smoke_basin.calculate_low_point_risk_level())
    print('Size of largest three basins:', smoke_basin.three_largest_basins_size())


if __name__ == '__main__':
    import timeit
    print(timeit.timeit(main, number=1))
