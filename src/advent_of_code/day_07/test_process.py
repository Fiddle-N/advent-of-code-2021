from src.advent_of_code.day_07 import process


def test_crab_alignment_linear():
    assert process.crab_alignment_linear([16, 1, 2, 0, 4, 2, 7, 1, 2, 14]) == 37


def test_crab_alignment_triangular():
    assert process.crab_alignment_triangular([16, 1, 2, 0, 4, 2, 7, 1, 2, 14]) == 168
