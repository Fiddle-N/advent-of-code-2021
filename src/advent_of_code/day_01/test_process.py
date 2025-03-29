from src.advent_of_code.day_01 import process


def test_depth_count():
    input_report = """\
199
200
208
210
200
207
240
269
260
263"""
    assert process.count_depth(input_report) == 7


def test_depth_count_window():
    input_report = """\
199
200
208
210
200
207
240
269
260
263"""
    assert process.count_depth(input_report, window=3) == 5
