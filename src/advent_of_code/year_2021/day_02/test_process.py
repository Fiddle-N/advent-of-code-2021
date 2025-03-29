from advent_of_code.year_2021.day_02 import process


def test_course_calc():
    input_course = """\
forward 5
down 5
forward 8
up 3
down 8
forward 2"""
    assert process.course_calc_part_1(input_course) == process.Coords(15, 10)


def test_course_calc_part_2():
    input_course = """\
forward 5
down 5
forward 8
up 3
down 8
forward 2"""
    assert process.course_calc_part_2(input_course) == process.Coords(15, 60)