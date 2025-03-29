from src.advent_of_code.year_2021.day_15 import process


def test_chiton():
    chiton_map = """\
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"""
    chiton = process.Chiton(chiton_map, let_the_expansion_begin=False)
    assert chiton.shortest_path_length() == 40


def test_chiton_expanded():
    chiton_map = """\
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"""
    chiton = process.Chiton(chiton_map, let_the_expansion_begin=True)
    assert chiton.shortest_path_length() == 315
