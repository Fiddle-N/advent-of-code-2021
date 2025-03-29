import dataclasses
import enum
import itertools

import parse


@dataclasses.dataclass(frozen=True)
class Coords:
    x: int
    y: int
    z: int


class StepSwitch(enum.Enum):
    ON = "on"
    OFF = "off"


@dataclasses.dataclass
class CoordRange:
    start: int
    end: int


@dataclasses.dataclass
class Step:
    x: CoordRange
    y: CoordRange
    z: CoordRange
    switch: StepSwitch


class ReactorReboot:

    SET_OPS = {
        StepSwitch.ON: set.add,
        StepSwitch.OFF: set.discard,
    }

    INIT_RANGE = CoordRange(-50, 50)

    def __init__(self, steps, enable_full=False):
        step_template = "{switch} x={x_start:d}..{x_end:d},y={y_start:d}..{y_end:d},z={z_start:d}..{z_end:d}"
        self.steps = []
        for raw_step in steps.splitlines():
            parsed_step = parse.parse(step_template, raw_step)
            self.steps.append(
                Step(
                    CoordRange(parsed_step["x_start"], parsed_step["x_end"]),
                    CoordRange(parsed_step["y_start"], parsed_step["y_end"]),
                    CoordRange(parsed_step["z_start"], parsed_step["z_end"]),
                    switch=StepSwitch(parsed_step["switch"]),
                )
            )
        self.enable_full = enable_full

    @classmethod
    def from_file(cls):
        with open("input.txt") as f:
            return cls(f.read().strip())

    def __iter__(self):
        cubes = set()
        for step in self.steps:
            lower = {axis: getattr(step, axis).start for axis in ("x", "y", "z")}
            upper = {axis: getattr(step, axis).end for axis in ("x", "y", "z")}

            check = any(val < self.INIT_RANGE.start for val in lower.values()) or any(
                val > self.INIT_RANGE.end for val in upper.values())

            if not self.enable_full and check:
                continue

            for x, y, z in itertools.product(
                range(lower["x"], upper["x"] + 1),
                range(lower["y"], upper["y"] + 1),
                range(lower["z"], upper["z"] + 1),
            ):
                self.SET_OPS[step.switch](cubes, Coords(x, y, z))
            yield cubes


def main():
    rr = ReactorReboot.from_file()
    rr_iter = iter(rr)
    while True:
        try:
            cubes = next(rr_iter)
        except StopIteration:
            break
    print('On cubes:', len(cubes))


if __name__ == '__main__':
    import timeit
    print(timeit.timeit(main, number=1))
