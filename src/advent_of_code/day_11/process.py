import dataclasses
import typing


@dataclasses.dataclass(frozen=True)
class Coords:
    x: int
    y: int

    def __add__(self, other):
        return Coords(self.x + other.x, self.y + other.y)


@dataclasses.dataclass(frozen=True)
class Octopus:
    energy: int
    has_flashed: bool = False

    def __add__(self, other):
        return Octopus(self.energy + other, self.has_flashed)


OFFSETS = [
    Coords(0, 1),
    Coords(1, 1),
    Coords(1, 0),
    Coords(1, -1),
    Coords(0, -1),
    Coords(-1, -1),
    Coords(-1, 0),
    Coords(-1, 1),
]


class OctopusEnergyModel:

    def __init__(self, octopuses):
        octopus_grid = [
            [Octopus(int(octopus)) for octopus in row]
            for row in octopuses.split('\n')
        ]
        self.height = len(octopus_grid)
        self.width = len(octopus_grid[0])
        self.octopuses = {}
        for y, row in enumerate(octopus_grid):
            for x, octopus in enumerate(row):
                self.octopuses[Coords(x, y)] = octopus
        self.flashes = 0
        self.step = 0

    @classmethod
    def read_file(cls):
        with open('input.txt') as f:
            return cls(f.read().strip())

    def _get_neighbours(self, coord):
        neighbour_coords = []
        for offset in OFFSETS:
            neighbour_coord = coord + offset
            if neighbour_coord in self.octopuses:
                neighbour_coords.append(neighbour_coord)
        return neighbour_coords

    def _will_flash(self, octopus: Octopus):
        return octopus.energy > 9 and not octopus.has_flashed

    def _increment_energy(self):
        for octopus_coord, octopus in self.octopuses.items():
            self.octopuses[octopus_coord] = octopus + 1

    def _model_flashes(self):
        about_to_flash = {
            octopus_coord
            for octopus_coord, octopus in self.octopuses.items()
            if self._will_flash(octopus)
        }
        while True:
            if not about_to_flash:
                break
            octopus_coord = about_to_flash.pop()
            octopus = self.octopuses[octopus_coord]
            neighbour_coords = self._get_neighbours(octopus_coord)
            for neighbour_coord in neighbour_coords:
                next_octopus = self.octopuses[neighbour_coord] + 1
                self.octopuses[neighbour_coord] = next_octopus
                if self._will_flash(next_octopus) and neighbour_coord not in about_to_flash:
                    about_to_flash.add(neighbour_coord)
            self.octopuses[octopus_coord] = Octopus(energy=octopus.energy, has_flashed=True)

    def _reset_flashed_octopuses(self):
        any_octopuses_not_flashed = False
        for octopus_coord, octopus in self.octopuses.items():
            if octopus.has_flashed:
                self.octopuses[Coords(octopus_coord.x, octopus_coord.y)] = Octopus(energy=0, has_flashed=False)
                self.flashes += 1
            else:
                any_octopuses_not_flashed = True
        return any_octopuses_not_flashed

    def __iter__(self):
        return self

    def __next__(self):
        self.step += 1
        self._increment_energy()
        self._model_flashes()
        any_octopuses_not_flashed = self._reset_flashed_octopuses()
        if not any_octopuses_not_flashed:
            raise StopIteration

    def __str__(self):
        octopus_energy_grid: typing.List[typing.List[typing.Optional[int]]] = [
            [None for _ in range(self.width)]
            for _ in range(self.height)
        ]
        for x in range(self.width):
            for y in range(self.height):
                octopus_energy_grid[y][x] = self.octopuses[Coords(x, y)].energy
        return '\n'.join(
            [''.join([str(octopus_energy) for octopus_energy in row])
             for row in octopus_energy_grid]
        )


def main():
    octopus_model = OctopusEnergyModel.read_file()
    for _ in range(100):
        next(octopus_model)
    print('Octopus flashes after 100 steps:', octopus_model.flashes)
    while True:
        try:
            next(octopus_model)
        except StopIteration as e:
            break
    print('First step when all octopuses flash:', octopus_model.step)


if __name__ == '__main__':
    import timeit
    print(timeit.timeit(main, number=1))
