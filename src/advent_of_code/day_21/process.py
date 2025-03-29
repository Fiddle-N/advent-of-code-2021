import itertools

import more_itertools
import parse


class DiracDice:

    def __init__(self, p1_start, p2_start):
        self.p1_start = p1_start
        self.p2_start = p2_start

    @classmethod
    def from_str(cls, starting_positions):
        template = """\
Player 1 starting position: {p1:d}
Player 2 starting position: {p2:d}"""
        parsed = parse.parse(template, starting_positions)
        return cls(parsed['p1'], parsed['p2'])

    @classmethod
    def from_file(cls):
        with open("input.txt") as f:
            return cls.from_str(f.read().strip())

    def play(self):
        p1_pos = self.p1_start
        p2_pos = self.p2_start
        p1_score = 0
        p2_score = 0
        die = (sum(roll) for roll in more_itertools.chunked(itertools.cycle(range(1, 101)), 3))
        die_roll = 0
        while True:
            die_roll += 3
            jump = next(die)
            p1_pos = (p1_pos - 1 + jump) % 10 + 1
            p1_score += p1_pos
            if p1_score >= 1000:
                return p2_score * die_roll

            die_roll += 3
            jump = next(die)
            p2_pos = (p2_pos - 1 + jump) % 10 + 1
            p2_score += p2_pos
            if p2_score >= 1000:
                return p1_score * die_roll


def main():
    dd = DiracDice.from_file()
    print('Game result:', dd.play())


if __name__ == '__main__':
    import timeit
    print(timeit.timeit(main, number=1))
