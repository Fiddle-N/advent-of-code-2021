import collections


Coords = collections.namedtuple('Coords', 'x y')


class HydrothermalVenture:

    def __init__(self, vent_data):
        self._vents = self._process_vent_data(vent_data)

    @classmethod
    def read_file(cls):
        with open('input.txt') as f:
            return cls(f.read())

    def _process_vent_data(self, vent_data):
        vents = []
        for vent in vent_data.splitlines():
            raw_vent_start, raw_vent_end = vent.split(' -> ')
            vent_start = Coords(*[int(point) for point in raw_vent_start.split(',')])
            vent_end = Coords(*[int(point) for point in raw_vent_end.split(',')])
            vents.append((vent_start, vent_end))
        return vents

    def _get_vent_range(self, start_pos, end_pos):
        if start_pos < end_pos:
            step = offset = 1
        elif start_pos > end_pos:
            step = offset = -1
        else:
            raise Exception
        range_vals = range(start_pos, end_pos + offset, step)
        return range_vals

    def _vent_calculation(self, include_diagonals=False):
        expanded_vents = collections.Counter()
        for vent_start, vent_end in self._vents:
            is_x_same = (vent_start.x == vent_end.x)
            is_y_same = (vent_start.y == vent_end.y)
            if is_x_same:
                ys = self._get_vent_range(vent_start.y, vent_end.y)
                for y in ys:
                    expanded_vents[Coords(vent_start.x, y)] += 1
            elif is_y_same:
                xs = self._get_vent_range(vent_start.x, vent_end.x)
                for x in xs:
                    expanded_vents[Coords(x, vent_start.y)] += 1
            elif not is_x_same and not is_y_same:
                if not include_diagonals:
                    continue
                xs = self._get_vent_range(vent_start.x, vent_end.x)
                ys = self._get_vent_range(vent_start.y, vent_end.y)
                for x, y in zip(xs, ys):
                    expanded_vents[Coords(x, y)] += 1
            else:
                raise Exception
        return expanded_vents

    def _overlaps(self, include_diagonals):
        expanded_vents = self._vent_calculation(include_diagonals)
        overlaps = sum(points >= 2 for points in expanded_vents.values())
        return overlaps

    def horizontal_vertical_overlaps(self):
        return self._overlaps(include_diagonals=False)

    def horizontal_vertical_diagonal_overlaps(self):
        return self._overlaps(include_diagonals=True)


def main():
    hydrothermal_venture = HydrothermalVenture.read_file()
    print(f'{hydrothermal_venture.horizontal_vertical_overlaps()=}')
    print(f'{hydrothermal_venture.horizontal_vertical_diagonal_overlaps()=}')


if __name__ == '__main__':
    import timeit
    print(timeit.timeit(main, number=1))
