import collections
import fractions

import more_itertools


class ExtendedPolymerisation:

    def __init__(self, formula):
        template, rules = formula.split('\n\n')
        self.polymer_count = collections.Counter(''.join(pair) for pair in more_itertools.pairwise(template))
        self.first = template[0]
        self.last = template[-1]
        self.rules = {}
        for rule in rules.split('\n'):
            input_, output = rule.split(' -> ')
            self.rules[input_] = (input_[0] + output, output + input_[1])

    @classmethod
    def read_file(cls):
        with open('input.txt') as f:
            return cls(f.read().strip())

    def __iter__(self):
        return self

    def __next__(self):
        next_polymer = collections.Counter()
        for pair, count in self.polymer_count.items():
            result = self.rules[pair]
            for pair in result:
                next_polymer[pair] += count
        self.polymer_count = next_polymer
        return self.polymer_count

    def polymer_length(self):
        return sum(self.polymer_count.values()) + 1

    @property
    def element_count(self):
        counts = collections.Counter()
        for pair, value in self.polymer_count.items():
            for element in pair:
                counts[element] += fractions.Fraction(value, 2)
        counts[self.first] += fractions.Fraction(1, 2)
        counts[self.last] += fractions.Fraction(1, 2)
        return collections.Counter({element: int(count) for element, count in counts.items()})

    @property
    def most_common_element(self):
        return self.element_count.most_common()[0]

    @property
    def least_common_element(self):
        return self.element_count.most_common()[-1]

    def score(self):
        return self.most_common_element[1] - self.least_common_element[1]


def main():
    ep = ExtendedPolymerisation.read_file()
    for _ in range(10):
        next(ep)
    print('After 10 steps - quantity of most common element - least common element:', ep.score())
    for _ in range(40 - 10):
        next(ep)
    print('After 40 steps - quantity of most common element - least common element:', ep.score())


if __name__ == '__main__':
    import timeit
    print(timeit.timeit(main, number=1))
