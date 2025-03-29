from src.advent_of_code.day_13 import process


def test_transparent_origami():
    paper = """\
6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"""
    transparent_origami = process.TransparentOrigami(paper)
    to = iter(transparent_origami)

    next(to)

    assert str(to) == """\
#.##..#..#.
#...#......
......#...#
#...#......
.#.#..#.###
...........
..........."""
#     assert len(transparent_origami.dots) == 17
#
#     while True:
#         try:
#             next(to)
#         except StopIteration:
#             break
#
#     assert str(transparent_origami) == """\
# #####
# #...#
# #...#
# #...#
# #####
# .....
# ....."""