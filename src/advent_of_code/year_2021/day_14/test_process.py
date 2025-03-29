import collections

import more_itertools

from advent_of_code.year_2021.day_14 import process


def test_polymer():
    formula = """\
NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""
    ep = process.ExtendedPolymerisation(formula)

    step_1 = 'NCNBCHB'
    assert next(ep) == collections.Counter(''.join(pair) for pair in more_itertools.pairwise(step_1))
    assert ep.polymer_length() == len(step_1)

    step_2 = 'NBCCNBBBCBHCB'
    assert next(ep) == collections.Counter(''.join(pair) for pair in more_itertools.pairwise(step_2))
    assert ep.polymer_length() == len(step_2)

    step_3 = 'NBBBCNCCNBBNBNBBCHBHHBCHB'
    assert next(ep) == collections.Counter(''.join(pair) for pair in more_itertools.pairwise(step_3))
    assert ep.polymer_length() == len(step_3)

    step_4 = 'NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB'
    assert next(ep) == collections.Counter(''.join(pair) for pair in more_itertools.pairwise(step_4))
    assert ep.polymer_length() == len(step_4)

    next(ep)
    assert ep.polymer_length() == 97

    for _ in range(5):
        next(ep)
    assert ep.polymer_length() == 3073
    assert ep.element_count == {
        'B': 1749,
        'C': 298,
        'H': 161,
        'N': 865,
    }
    assert ep.most_common_element == ('B', 1749)
    assert ep.least_common_element == ('H', 161)
    assert ep.score() == 1588

    for _ in range(30):
        next(ep)

    assert ep.most_common_element == ('B', 2_192_039_569_602)
    assert ep.least_common_element == ('H', 3_849_876_073)
    assert ep.score() == 2_188_189_693_529
