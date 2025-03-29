from src.advent_of_code.year_2021.day_05 import process


def test_hydrothermal_venture():
    vent_data = """\
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"""
    hydrothermal_venture = process.HydrothermalVenture(vent_data)
    assert hydrothermal_venture.horizontal_vertical_overlaps() == 5


def test_hydrothermal_venture_include_diagonals():
    vent_data = """\
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"""
    hydrothermal_venture = process.HydrothermalVenture(vent_data)
    assert hydrothermal_venture.horizontal_vertical_diagonal_overlaps() == 12