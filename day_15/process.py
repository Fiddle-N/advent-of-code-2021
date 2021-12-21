import dataclasses

import networkx as nx


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

        self._chiton_graph = nx.DiGraph()

        for y, row in enumerate(self._chiton_map):
            for x, _ in enumerate(row):
                coord = Coords(x, y)
                neighbour_coords = self._get_neighbours(coord)
                for neighbour_coord in neighbour_coords:
                    self._chiton_graph.add_edge(
                        coord,
                        neighbour_coord,
                        weight=self._chiton_map[neighbour_coord.y][neighbour_coord.x]
                    )

    def _get_neighbours(self, coord):
        neighbour_coords = []
        for offset in OFFSETS:
            neighbour_coord = coord + offset
            if 0 <= neighbour_coord.x < self._width and 0 <= neighbour_coord.y < self._height:
                neighbour_coords.append(neighbour_coord)
        return neighbour_coords

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

    def shortest_path_length(self):
        return nx.shortest_path_length(
            self._chiton_graph,
            source=Coords(0, 0),
            target=Coords(self._width - 1, self._height - 1),
            weight='weight',
        )


def main():
    chiton = Chiton.read_file()
    print('Lowest risk level:', chiton.shortest_path_length())
    chiton_exp = Chiton.read_file(let_the_expansion_begin=True)
    print('Lowest risk level:', chiton_exp.shortest_path_length())


if __name__ == '__main__':
    import timeit
    print(timeit.timeit(main, number=1))
