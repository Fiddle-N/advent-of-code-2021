import dataclasses
import heapq


@dataclasses.dataclass(frozen=True)
class Coords:
    x: int
    y: int

    def __add__(self, other):
        return Coords(self.x + other.x, self.y + other.y)


@dataclasses.dataclass(frozen=True, order=True)
class PrioritisedItem:
    total_risk: int
    location: Coords = dataclasses.field(compare=False)


OFFSETS = [
    Coords(0, 1),
    Coords(1, 0),
    Coords(0, -1),
    Coords(-1, 0),
]


class Chiton:

    def __init__(self, chiton_map, let_the_expansion_begin=False):
        self._chiton_map = [
            [int(risk) for risk in row]
            for row in chiton_map.split('\n')
        ]

        if let_the_expansion_begin:
            self._expand()

        self._height = len(self._chiton_map)
        self._width = len(self._chiton_map[0])

        self._chiton_graph = {}

        for y, row in enumerate(self._chiton_map):
            for x, risk in enumerate(row):
                coord = Coords(x, y)
                self._chiton_graph[coord] = risk

        self.source = Coords(0, 0)
        self.target = Coords(self._width - 1, self._height - 1)

    def _add_risks(self, num1, num2):
        val = num1 + num2
        while val > 9:
            val -= 9
        return val

    def _expand_1d(self, grid):
        ext = []
        for row in grid:
            next_row = []
            for mul in range(5):
                next_chunk = [self._add_risks(num, mul) for num in row]
                next_row.extend(next_chunk)
            ext.append(next_row)
        return ext

    def _expand(self):
        horizontal_ext = self._expand_1d(self._chiton_map)
        horizontal_ext_t = zip(*horizontal_ext)
        ext_t = self._expand_1d(horizontal_ext_t)
        ext = [list(row) for row in zip(*ext_t)]
        self._chiton_map = ext

    @classmethod
    def read_file(cls, let_the_expansion_begin=False):
        with open('input.txt') as f:
            return cls(f.read().strip(), let_the_expansion_begin)

    def _get_neighbours(self, coord):
        neighbour_coords = []
        for offset in OFFSETS:
            neighbour_coord = coord + offset
            if 0 <= neighbour_coord.x < self._width and 0 <= neighbour_coord.y < self._height:
                neighbour_coords.append(neighbour_coord)
        return neighbour_coords

    def shortest_path_length(self):
        visited: set[Coords] = set()
        costs: dict[Coords, int] = {self.source: 0}
        q: list[PrioritisedItem] = []

        heapq.heappush(q, PrioritisedItem(0, self.source))

        while q:
            item = heapq.heappop(q)
            if (location := item.location) in visited:
                continue
            visited.add(location)
            if location == self.target:
                break
            for neighbour in self._get_neighbours(location):
                if neighbour in visited:
                    continue
                risk_level = self._chiton_graph[neighbour]
                old_cost = costs.get(neighbour)
                new_cost = costs[location] + risk_level
                if old_cost is None or new_cost < old_cost:
                    heapq.heappush(q, PrioritisedItem(new_cost, neighbour))
                    costs[neighbour] = new_cost

        return costs[self.target]


def main():
    chiton = Chiton.read_file()
    print('Lowest risk level:', chiton.shortest_path_length())
    chiton_exp = Chiton.read_file(let_the_expansion_begin=True)
    print('Lowest risk level:', chiton_exp.shortest_path_length())


if __name__ == '__main__':
    import timeit
    print(timeit.timeit(main, number=1))
