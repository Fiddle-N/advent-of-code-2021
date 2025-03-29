import functools
import statistics


@functools.cache
def triangle(num):
    return (num * (num+1)) // 2


def crab_alignment_linear(positions):
    median_pos = statistics.median_low(positions)
    return sum(abs(pos - median_pos) for pos in positions)


def crab_alignment_triangular(positions):
    alignments = []
    for alignment in range(min(positions), max(positions) + 1):
        alignments.append(sum(triangle(abs(pos - alignment)) for pos in positions))
    return min(alignments)


def main():
    with open('input.txt') as f:
        raw_positions = f.read().strip()
    positions = [int(pos) for pos in raw_positions.split(',')]
    print(f'{crab_alignment_linear(positions)}')
    print(f'{crab_alignment_triangular(positions)}')


if __name__ == '__main__':
    import timeit
    print(timeit.timeit(main, number=1))
