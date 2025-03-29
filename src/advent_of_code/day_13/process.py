import dataclasses


@dataclasses.dataclass(frozen=True)
class Coords:
    x: int
    y: int


@dataclasses.dataclass(frozen=True)
class Fold:
    axis: str
    coord: int


class TransparentOrigami:

    def __init__(self, paper):
        self.dots = set()
        self.folds = []

        raw_dots, raw_instrs = paper.split('\n\n')
        self._max_x = 0
        self._max_y = 0
        for raw_dot in raw_dots.strip().split('\n'):
            x, y = [int(dot_coord) for dot_coord in raw_dot.split(',')]
            if x > self._max_x:
                self._max_x = x
            if y > self._max_y:
                self._max_y = y
            self.dots.add(Coords(x, y))

        for raw_instr in raw_instrs.split('\n'):
            raw_fold = raw_instr.split()[-1]
            axis, coord = raw_fold.split('=')
            self.folds.append(Fold(axis, int(coord)))

    @property
    def width(self):
        return self._max_x + 1

    @property
    def height(self):
        return self._max_y + 1

    @classmethod
    def read_file(cls):
        with open('input.txt') as f:
            return cls(f.read().strip())

    def __iter__(self):
        for fold in self.folds:
            next_dots = set()
            for dot in self.dots:
                before_fold = getattr(dot, fold.axis)
                if before_fold > fold.coord:
                    next_dot = dot.__dict__.copy()
                    after_fold = (2 * fold.coord) - before_fold
                    next_dot[fold.axis] = after_fold
                    next_dots.add(Coords(**next_dot))
                else:
                    next_dots.add(dot)
            self.dots = next_dots
            setattr(self, f'_max_{fold.axis}', fold.coord - 1)
            yield self

    def __str__(self):
        grid = [
            ['.' for _ in range(self.width)]
            for _ in range(self.height)
        ]
        for dot in self.dots:
            grid[dot.y][dot.x] = '#'

        return '\n'.join([''.join(row) for row in grid])


def main():
    transparent_origami = TransparentOrigami.read_file()
    to = iter(transparent_origami)
    next(to)
    print('Number of dots after first fold:', len(transparent_origami.dots))

    while True:
        try:
            next(to)
        except StopIteration:
            break

    print(str(transparent_origami))


if __name__ == '__main__':
    import timeit
    print(timeit.timeit(main, number=1))
