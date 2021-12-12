from day_09 import process


def test_smoke_basin_lowest_points_risk_level():
    heightmap = """\
2199943210
3987894921
9856789892
8767896789
9899965678"""
    smoke_basin = process.SmokeBasin(heightmap)
    assert smoke_basin.calculate_low_point_risk_level() == 15


def test_smoke_basin_three_largest_basins_size():
    heightmap = """\
2199943210
3987894921
9856789892
8767896789
9899965678"""
    smoke_basin = process.SmokeBasin(heightmap)
    assert smoke_basin.three_largest_basins_size() == 1134