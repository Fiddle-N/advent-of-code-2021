import dataclasses
import enum

import parse


class State(enum.Enum):
    ON = 1
    OFF = -1

    @property
    def opposite(self):
        if self == State.ON:
            return State.OFF
        elif self == State.OFF:
            return State.ON


@dataclasses.dataclass(frozen=True, eq=True)
class Coords3D:
    x: int
    y: int
    z: int


@dataclasses.dataclass(frozen=True, eq=True)
class Cube:
    start: Coords3D
    end: Coords3D


class ReactorReboot:
    def __init__(self, steps):
        step_template = "{state} x={x_start:d}..{x_end:d},y={y_start:d}..{y_end:d},z={z_start:d}..{z_end:d}"
        self.cubes = []
        for cube in steps.splitlines():
            parsed_cube = parse.parse(step_template, cube)
            self.cubes.append(
                (
                    Cube(
                        start=Coords3D(
                            parsed_cube["x_start"],
                            parsed_cube["y_start"],
                            parsed_cube["z_start"],
                        ),
                        end=Coords3D(
                            parsed_cube["x_end"],
                            parsed_cube["y_end"],
                            parsed_cube["z_end"],
                        ),
                    ),
                    getattr(State, parsed_cube["state"].upper()),
                )
            )

    @classmethod
    def from_file(cls):
        with open("input.txt") as f:
            return cls(f.read().strip())

    def volume(self, distinct_cubes):
        return sum(
            (
                (cube.end.x - cube.start.x + 1)
                * (cube.end.y - cube.start.y + 1)
                * (cube.end.z - cube.start.z + 1)
                * state.value
            )
            for cube, state in distinct_cubes.items()
        )

    def process(self):
        previous_cubes = {}
        for current_cube, state in self.cubes:

            previous_cubes_copy = previous_cubes.copy()
            for previous_cube, previous_cube_state in previous_cubes.items():
                x_lower = max(previous_cube.start.x, current_cube.start.x)
                x_upper = min(previous_cube.end.x, current_cube.end.x)
                y_lower = max(previous_cube.start.y, current_cube.start.y)
                y_upper = min(previous_cube.end.y, current_cube.end.y)
                z_lower = max(previous_cube.start.z, current_cube.start.z)
                z_upper = min(previous_cube.end.z, current_cube.end.z)
                if x_lower <= x_upper and y_lower <= y_upper and z_lower <= z_upper:
                    overlap_cube = Cube(
                        start=Coords3D(x_lower, y_lower, z_lower),
                        end=Coords3D(x_upper, y_upper, z_upper),
                    )
                    if overlap_cube not in previous_cubes_copy:
                        # if this overlap cube isn't in our cache
                        # either we haven't seen it before
                        # or we have but we are now dealing with the second cube in the overlap
                        if previous_cube_state == State.ON:
                            # negate the overlapping volume from the previous cube
                            # if the current cube state is off, this is all we need to do.
                            # if the current cube state is on, after the negation,
                            # we need to add an ON cube for our current cube state - this will be done in code below
                            previous_cubes_copy[overlap_cube] = State.OFF
                        elif previous_cube_state == State.OFF:
                            # complex state
                            # we are overlapping with an off state cube generated from a previous overlap
                            # where the overlap with the previous overlap
                            # is different from the overlap with the first cube
                            # when we overlap with the first cube, that will generate another off state cube
                            # however we need to fill in the overlap between the two off state cubes
                            # to ensure we don't double count
                            previous_cubes_copy[overlap_cube] = State.ON

                    else:
                        # there must be already be an overlap
                        # Previous state = ON
                        #   current state = ON -> remove cube as we will turn it back on later
                        #   current state = OFF -> remove in order to turn off the cube
                        # Previous state = OFF
                        # complex case
                        # two previous cubes overlapped that generated an off overlap
                        # this current cube completely contains the overlap without being exactly equal to it
                        # in which case we want to remove the smaller overlap cube so that we don't double count
                        previous_cubes_copy.pop(overlap_cube)
            if state == State.ON:
                if current_cube not in previous_cubes_copy:
                    # all required negations have been performed and there are no complications
                    # so we just add the new cube in
                    previous_cubes_copy[current_cube] = State.ON
                else:
                    # do nothing if the cubes are already on
                    # however, if this exact cube has been negated from an unrelated overlap
                    # then just rectify that state
                    if previous_cubes_copy[current_cube] == State.OFF:
                        previous_cubes_copy.pop(current_cube)

            previous_cubes = previous_cubes_copy

        vol = self.volume(previous_cubes)

        return vol


def main():
    rr = ReactorReboot.from_file()
    print(rr.process())


if __name__ == "__main__":
    import timeit

    print(timeit.timeit(main, number=1))
