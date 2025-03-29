import collections

from src.advent_of_code.year_2021.day_06 import process


def test_lanternfish():
    lanternfish_input = [3, 4, 3, 1, 2]
    lanternfish_simulation = process.LanternfishSimulator(lanternfish_input)

    for _ in range(18):
        result = next(lanternfish_simulation)

    assert result == collections.Counter(
        [6, 0, 6, 4, 5, 6, 0, 1, 1, 2, 6, 0, 1, 1, 1, 2, 2, 3, 3, 4, 6, 7, 8, 8, 8, 8]
    )

    assert sum(result.values()) == 26

    for _ in range(62):
        result = next(lanternfish_simulation)

    assert sum(result.values()) == 5934
