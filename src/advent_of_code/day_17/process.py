import dataclasses
import math
import parse


@dataclasses.dataclass
class TargetArea:
    x_start: int
    x_end: int
    y_start: int
    y_end: int


class TrickShot:

    def __init__(self, target_area):
        result = parse.parse('target area: x={x_start:d}..{x_end:d}, y={y_start:d}..{y_end:d}', target_area)
        self.target = TargetArea(result['x_start'], result['x_end'], result['y_start'], result['y_end'])
        if self.target.x_start < 0:
            raise NotImplementedError('not thinking about firing backwards yet')

    @classmethod
    def read_file(cls):
        with open('input.txt') as f:
            return cls(f.read().strip())

    def y_peak(self):
        # probe must shoot upwards to get height
        # probe goes upwards, dropping 1 from its y velocity each time until it hits its peak at y velocity = 0
        # probe then falls down
        # each time it drops 1 from its y velocity it has the exact same y values as when it went up
        # probe will fall straight back to exactly y = 0
        # at y = 0, probe will have exactly negative initial y velocity
        # the fastest probe lands right at the lowest possible negative y in the zone
        # so initial y velocity of the fastest probe must be
        # one minus the absolute value of the lowest possible negative y
        initial_velocity = abs(self.target.y_start) - 1

        # the highest peak is then sum of velocities from 0 to initial velocity - use triangle number formula
        return initial_velocity * (initial_velocity + 1) // 2

    def initial_velocities(self):
        xs = range(self._calculate_lowest_possible_x(), self.target.x_end + 1)
        ys = range(self.target.y_start, -self.target.y_start)
        xys = set((x, y) for x in xs for y in ys if self._check_xy_velocity(x, y))
        return xys

    def _calculate_lowest_possible_x(self):
        # calculate x that corresponds to triangle number within range
        # (x (x + 1 )) / 2 = t, where t is lowest x value in target range
        # rearranged, that's x^2 + x - 2t = 0
        # use reverse triangle formula
        # (-b +- sqrt(b^2 - 4ac)) / 2a
        # a = 1, b = 1, c = 2t
        # only need + in +- as we don't care about negative x
        result = (-1 + math.sqrt(1**2 + 4 * 1 * 2 * self.target.x_start)) / 2 * 1

        # round result upwards once we have it to get lowest integer within range
        return math.ceil(result)

    def _check_xy_velocity(self, x, y):
        x_pos = x
        y_pos = y
        while True:
            if self.target.x_start <= x_pos <= self.target.x_end and self.target.y_start <= y_pos <= self.target.y_end:
                return True
            elif x_pos > self.target.x_end or y_pos < self.target.y_start:
                return False
            if x > 0:
                x -= 1
                x_pos += x
            y -= 1
            y_pos += y


def main():
    trick_shot = TrickShot.read_file()
    print('Highest peak:', trick_shot.y_peak())
    print('Distinct initial velocities:', len(trick_shot.initial_velocities()))


if __name__ == '__main__':
    import timeit
    print(timeit.timeit(main, number=1))
