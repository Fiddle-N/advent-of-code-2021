import collections
import dataclasses
import enum
import itertools

import parse


class State(enum.Enum):
    ON = "on"
    OFF = "off"


@dataclasses.dataclass(frozen=True, eq=True)
class Coords3D:
    x: int
    y: int
    z: int


@dataclasses.dataclass(frozen=True, eq=True)
class Cube:
    start: Coords3D
    end: Coords3D
    state: State


class ReactorReboot:
    def __init__(self, steps):
        step_template = "{state} x={x_start:d}..{x_end:d},y={y_start:d}..{y_end:d},z={z_start:d}..{z_end:d}"
        self.cubes = []
        for cube in steps.splitlines():
            parsed_cube = parse.parse(step_template, cube)
            self.cubes.append(
                Cube(
                    start=Coords3D(
                        parsed_cube["x_start"],
                        parsed_cube["y_start"],
                        parsed_cube["z_start"],
                    ),
                    end=Coords3D(
                        parsed_cube["x_end"], parsed_cube["y_end"], parsed_cube["z_end"]
                    ),
                    state=State(parsed_cube["state"]),
                )
            )

    @classmethod
    def from_file(cls):
        with open("input.txt") as f:
            return cls(f.read().strip())

    def cube_contains_other_cube(self, larger_cube, smaller_cube):
        assert larger_cube.state == State.ON and smaller_cube.state == State.OFF

        x_ranges, middle_x_range = self._get_ranges(larger_cube, smaller_cube, "x")
        y_ranges, middle_y_range = self._get_ranges(larger_cube, smaller_cube, "y")
        z_ranges, middle_z_range = self._get_ranges(larger_cube, smaller_cube, "z")

        cubes = []

        for x_range, y_range, z_range in itertools.product(
            x_ranges, y_ranges, z_ranges
        ):
            if not (
                x_range == middle_x_range
                and y_range == middle_y_range
                and z_range == middle_z_range
            ):
                # add all cuboids except the middle one
                x_start, x_end = x_range
                y_start, y_end = y_range
                z_start, z_end = z_range
                cubes.append(
                    Cube(
                        start=Coords3D(x_start, y_start, z_start),
                        end=Coords3D(x_end, y_end, z_end),
                        state=State.ON,
                    )
                )

        return cubes

    def _get_ranges(self, larger_cube, smaller_cube, axis):
        left_range = [
            getattr(larger_cube.start, axis),
            getattr(smaller_cube.start, axis) - 1,
        ]
        middle_range = [
            getattr(smaller_cube.start, axis),
            getattr(smaller_cube.end, axis),
        ]
        right_range = [
            getattr(smaller_cube.end, axis) + 1,
            getattr(larger_cube.end, axis),
        ]

        if getattr(larger_cube.start, axis) == getattr(smaller_cube.start, axis):
            left_range = None

        elif middle_range[0] < left_range[0]:
            middle_range[0] = left_range[0]
            left_range = None

        if getattr(larger_cube.end, axis) == getattr(smaller_cube.end, axis):
            right_range = None

        elif middle_range[1] > right_range[1]:
            middle_range[1] = right_range[1]
            right_range = None

        ranges = (left_range, middle_range, right_range)

        ranges = [range_ for range_ in ranges if range_ is not None]

        return ranges, middle_range

    def cube_contains_other_cube_2_eb(self, larger_cube, smaller_cube):
        x_ranges, middle_x_range = self._get_ranges(larger_cube, smaller_cube, "x")
        y_ranges, middle_y_range = self._get_ranges(larger_cube, smaller_cube, "y")
        z_ranges, middle_z_range = self._get_ranges(larger_cube, smaller_cube, "z")

        cubes = []

        for x_range, y_range, z_range in itertools.product(
            x_ranges, y_ranges, z_ranges
        ):
            if not (
                x_range == middle_x_range
                and y_range == middle_y_range
                and z_range == middle_z_range
            ):

                # add all cuboids except the middle one
                x_start, x_end = x_range
                y_start, y_end = y_range
                z_start, z_end = z_range
                cubes.append(
                    Cube(
                        start=Coords3D(x_start, y_start, z_start),
                        end=Coords3D(x_end, y_end, z_end),
                        state=State.ON,
                    )
                )

        return cubes

    def volume(self, cubes):
        vol = 0
        for cube in cubes:
            assert cube.end.x >= cube.start.x
            assert cube.end.y >= cube.start.y
            assert cube.end.z >= cube.start.z
            vol += (
                (cube.end.x - cube.start.x + 1)
                * (cube.end.y - cube.start.y + 1)
                * (cube.end.z - cube.start.z + 1)
            )
        return vol

    def do_cubes_overlap_in_one_direction(self, left_cube, right_cube):
        for right_cube_corner in itertools.product(
            (right_cube.start.x, right_cube.end.x),
            (right_cube.start.y, right_cube.end.y),
            (right_cube.start.z, right_cube.end.z),
        ):
            right_cube_x, right_cube_y, right_cube_z = right_cube_corner
            if (
                (left_cube.start.x <= right_cube_x <= left_cube.end.x)
                and (left_cube.start.y <= right_cube_y <= left_cube.end.y)
                and (left_cube.start.z <= right_cube_z <= left_cube.end.z)
            ):
                return True
        return False

    def do_cubes_overlap(self, cube_1, cube_2):
        if self.do_cubes_overlap_in_one_direction(cube_1, cube_2):
            return True
        elif self.do_cubes_overlap_in_one_direction(cube_2, cube_1):
            return True
        else:
            return False

    def is_cube_contained_inside_another(self, container_cube, containee_cube):
        for containee_cube_corner in itertools.product(
            (containee_cube.start.x, containee_cube.end.x),
            (containee_cube.start.y, containee_cube.end.y),
            (containee_cube.start.z, containee_cube.end.z),
        ):
            containee_cube_x, containee_cube_y, containee_cube_z = containee_cube_corner
            if not (
                (container_cube.start.x <= containee_cube_x <= container_cube.end.x)
                and (container_cube.start.y <= containee_cube_y <= container_cube.end.y)
                and (container_cube.start.z <= containee_cube_z <= container_cube.end.z)
            ):
                return False
        return True

    def process(self):
        distinct_cubes = set()
        cube_q = collections.deque(self.cubes)
        while cube_q:
            next_cube = cube_q.popleft()

            if not distinct_cubes:
                distinct_cubes.add(next_cube)
                # print()
                # print(self.volume(distinct_cubes))
                continue

            overlapping_distinct_cubes = set(distinct_cubes)
            non_overlapping_distinct_cubes = set()

            # for distinct_cube in distinct_cubes:
            #     if self.do_cubes_overlap(distinct_cube, next_cube):
            #         overlapping_distinct_cubes.add(distinct_cube)
            #     else:
            #         non_overlapping_distinct_cubes.add(distinct_cube)
            #
            # if not overlapping_distinct_cubes:
            #     distinct_cubes = non_overlapping_distinct_cubes
            #     if next_cube.state == State.ON:
            #         distinct_cubes.add(next_cube)
            #     # print(self.volume(distinct_cubes))
            #     continue

            new_overlapping_distinct_cubes = set()

            for distinct_cube in overlapping_distinct_cubes:
                # if self.is_cube_contained_inside_another(
                #     container_cube=distinct_cube, containee_cube=next_cube
                # ):
                #     # next cube is contained wholly within the distinct cube
                #     if next_cube.state == State.ON:
                #         new_overlapping_distinct_cubes.add(distinct_cube)
                #     elif next_cube.state == State.OFF:
                #         new_distinct_cubes = self.cube_contains_other_cube(
                #             distinct_cube, next_cube
                #         )
                #         new_overlapping_distinct_cubes.update(new_distinct_cubes)
                # elif self.is_cube_contained_inside_another(
                #     container_cube=next_cube, containee_cube=distinct_cube
                # ):
                #     # next cube engulfs wholly distinct cube
                #     if next_cube.state == State.ON:
                #         # next cube replaces distinct cube
                #         new_overlapping_distinct_cubes.add(next_cube)
                #     elif next_cube.state == State.OFF:
                #         # distinct cube disappears completely
                #         pass
                #
                # else:
                #     # partial overlap
                new_distinct_cubes = self.cube_contains_other_cube_2_eb(
                    distinct_cube, next_cube
                )
                new_overlapping_distinct_cubes.update(new_distinct_cubes)
                if next_cube.state == State.ON:
                    # new cube is added whole as distinct cube is split up
                    new_overlapping_distinct_cubes.add(next_cube)
                else:
                    pass

            distinct_cubes = set()
            distinct_cubes.update(non_overlapping_distinct_cubes)
            distinct_cubes.update(new_overlapping_distinct_cubes)
            # print(self.volume(distinct_cubes))

        vol = self.volume(distinct_cubes)

        return vol


def main():
    rr = ReactorReboot.from_file()
    print(rr.process())


if __name__ == "__main__":
    import timeit

    print(timeit.timeit(main, number=1))
