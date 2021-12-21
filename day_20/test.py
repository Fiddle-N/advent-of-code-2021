from day_20 import process


def test_trench_map_enhance_twice():
    input_data = """\
..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###"""

    image_enhancer = process.ImageEnhancer(input_data)
    assert next(image_enhancer) == process.Image.from_str("""\
.##.##.
#..#.#.
##.#..#
####..#
.#..##.
..##..#
...#.#.""")
    assert next(image_enhancer) == process.Image.from_str("""\
.......#.
.#..#.#..
#.#...###
#...##.#.
#.....#.#
.#.#####.
..#.#####
...##.##.
....###..""")
    assert image_enhancer.image.pixel_count(process.Pixel.LIGHT) == 35


def test_trench_map_enhance_twice_alternating_padding():
    """
    0 = #
    511 = .
    """

    input_data = """\
#.#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#...

#..#.
#....
##..#
..#..
..###"""

    image_enhancer = process.ImageEnhancer(input_data)

    assert next(image_enhancer) == process.Image.from_str("""\
.##.###
#..#.##
##.#..#
####..#
.#..##.
####..#
##.#.#.""")

    assert next(image_enhancer) == process.Image.from_str("""\
.........
.....#...
###......
.#..###..
......#..
.#..###.#
#..#####.
...#....#
..#.....#""")
    assert image_enhancer.image.pixel_count(process.Pixel.LIGHT) == 24
