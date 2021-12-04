import dataclasses
import timeit


@dataclasses.dataclass
class Coords:
    x: int = 0
    y: int = 0

    def __add__(self, other):
        return Coords(self.x + other.x, self.y + other.y)


def course_calc_part_1(course_text):
    movements = {
        'forward': (lambda val: Coords(val, 0)),
        'down': (lambda val: Coords(0, val)),
        'up': (lambda val: Coords(0, -val)),
    }
    course = []
    for course_line in course_text.splitlines():
        direction, raw_unit = course_line.split()
        unit = int(raw_unit)
        course.append((direction, unit))
    position = Coords()
    for instr in course:
        direction, unit = instr
        change = movements[direction](unit)
        position += change
    return position


def course_calc_part_2(course_text):
    aim = 0
    course = []
    for course_line in course_text.splitlines():
        direction, raw_unit = course_line.split()
        unit = int(raw_unit)
        course.append((direction, unit))
    position = Coords()
    for instr in course:
        direction, unit = instr
        if direction == 'forward':
            position += Coords(unit, unit * aim)
        elif direction == 'down':
            aim += unit
        elif direction == 'up':
            aim -= unit
        else:
            raise Exception
    return position


def main():
    with open('input.txt') as f:
        course_text = f.read()
        position_1 = course_calc_part_1(course_text)
        print('Course part 1:', position_1.x * position_1.y)
        position_2 = course_calc_part_2(course_text)
        print('Course part 2:', position_2.x * position_2.y)


if __name__ == '__main__':
    print(timeit.timeit(main, number=1))
