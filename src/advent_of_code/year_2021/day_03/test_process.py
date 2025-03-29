from src.advent_of_code.year_2021.day_03 import process


def test_power_rates():
    report = """\
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010"""
    assert process.power_rating(report) == 198


def test_life_support_rating():
    report = """\
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010"""
    assert process.life_support_rating(report) == 230