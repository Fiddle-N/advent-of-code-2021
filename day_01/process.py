import itertools
import timeit

import more_itertools


def count_depth(depths, window=None):
    depths = [int(depth) for depth in depths.splitlines()]
    if window is not None:
        depths = [sum(window) for window in more_itertools.windowed(depths, 3)]
    increasing = sum(
        depth_pair[1] > depth_pair[0]
        for depth_pair in itertools.pairwise(depths)
    )
    return increasing


def main():
    with open('input.txt') as f:
        depths = f.read()
        print('Increasing depths:', count_depth(depths))
        print('Increasing depths with window 3:', count_depth(depths, window=3))


if __name__ == '__main__':
    print(timeit.timeit(main, number=1))
