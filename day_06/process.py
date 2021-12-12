import collections


class LanternfishSimulator:

    def __init__(self, lanternfish):
        self.lanternfish = collections.Counter(lanternfish)

    @classmethod
    def read_file(cls):
        with open('input.txt') as f:
            return cls([int(fish) for fish in f.read().strip().split(',')])

    def __iter__(self):
        return self

    def __next__(self):
        next_lanternfish = collections.Counter()
        for fish in range(1, 9):
            next_lanternfish[fish - 1] = self.lanternfish[fish]
        next_lanternfish[6] += self.lanternfish[0]
        next_lanternfish[8] = self.lanternfish[0]
        self.lanternfish = next_lanternfish
        return self.lanternfish


def main():
    lanternfish_simulation = LanternfishSimulator.read_file()
    for _ in range(80):
        result = next(lanternfish_simulation)
    print('Lanternfish after 80 days:', sum(result.values()))
    for _ in range(256 - 80):
        result = next(lanternfish_simulation)
    print('Lanternfish after 256 days:', sum(result.values()))


if __name__ == '__main__':
    import timeit
    print(timeit.timeit(main, number=1))
