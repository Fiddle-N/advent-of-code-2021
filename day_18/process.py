import ast
import collections
import dataclasses
import itertools
import math
import typing


@dataclasses.dataclass(frozen=True)
class SnailfishElement:
    no: typing.Union[int , list]
    lvl: int

    def __add__(self, other: int):
        assert isinstance(other, int)
        return SnailfishElement(self.no + other, self.lvl)



class SnailfishNumber:

    def __init__(self, number):
        self._number = number
        self._next_number = collections.deque()
        self._reduce()

    @classmethod
    def _flatten(cls, list_):
        sf_number = collections.deque()

        def _flatten_lvl(list_, level):
            for element in list_:
                if isinstance(element, int):
                    sf_number.append(SnailfishElement(element, level))
                elif isinstance(element, list):
                    _flatten_lvl(element, level + 1)
                else:
                    raise Exception('unexpected element')

        _flatten_lvl(list_, level=0)
        return sf_number

    @classmethod
    def from_list(cls, list_):
        return cls(cls._flatten(list_))

    def _explode(self):
        while self._number:
            if self._number[0].lvl == 4:
                left = self._number.popleft()
                right = self._number.popleft()
                assert left.lvl == right.lvl == 4
                if self._number:
                    right_regular = self._number.popleft()
                    right_result = right_regular + right.no
                    self._number.appendleft(right_result)
                self._number.appendleft(SnailfishElement(no=0, lvl=3))
                if self._next_number:
                    left_regular = self._next_number.pop()
                    left_result = left_regular + left.no
                    self._number.appendleft(left_result)
                break
            else:
                self._next_number.append(self._number.popleft())

    def _split(self):
        while self._number:
            if self._number[0].no > 9:
                large = self._number.popleft()
                assert large.no > 9
                self._number.appendleft(SnailfishElement(math.ceil(large.no / 2), large.lvl + 1))
                self._number.appendleft(SnailfishElement(math.floor(large.no / 2), large.lvl + 1))
                break
            else:
                self._next_number.append(self._number.popleft())

    def _reduce(self):
        self._next_number = collections.deque()
        while True:
            if any(element.lvl == 4 for element in self._number):
                self._explode()
                self._reset()
            elif any(element.no > 9 for element in self._number):
                self._split()
                self._reset()
            else:
                break

    def _reset(self):
        self._number = self._next_number + self._number
        self._next_number = collections.deque()

    def magnitude(self):
        number = self._number.copy()
        next_number = collections.deque()
        while len(number) > 1:
            max_lvl = max(element.lvl for element in number)
            if number[0].lvl == max_lvl:
                left = number.popleft()
                right = number.popleft()
                assert left.lvl == right.lvl
                number.appendleft(SnailfishElement(no=3 * left.no + 2 * right.no, lvl=left.lvl - 1))
                number = next_number + number
                next_number = collections.deque()
                continue
            else:
                next_number.append(number.popleft())
        assert len(number) == 1
        return number[0].no

    def __add__(self, other: 'SnailfishNumber'):
        result = collections.deque(
            SnailfishElement(element.no, element.lvl + 1)
            for element in itertools.chain(self._number, other._number)
        )
        return SnailfishNumber(result)

    def __eq__(self, other: 'SnailfishNumber'):
        return self._number == other._number


def sf_homework_part_1(homework):
    result = None
    for line in homework.split():
        sf_number = SnailfishNumber.from_list(ast.literal_eval(line))
        if result is None:
            result = sf_number
        else:
            result += sf_number
            yield result
    return result


def sf_homework_part_2(homework):
    lists = [SnailfishNumber.from_list(ast.literal_eval(line)) for line in homework.split()]
    max_val = 0
    for sn1, sn2 in itertools.permutations(lists, 2):
        result = sn1 + sn2
        if (magnitude := result.magnitude()) > max_val:
            max_val = magnitude
    return max_val


def main():
    with open('input.txt') as f:
        homework = f.read().strip()
    sf_homework_gen = sf_homework_part_1(homework)
    while True:
        try:
            next(sf_homework_gen)
        except StopIteration as e:
            result = e.value
            break

    print('Magnitude of final sum:', result.magnitude())
    print('Largest magnitude from any 2 numbers:', sf_homework_part_2(homework))


if __name__ == '__main__':
    import timeit
    print(timeit.timeit(main, number=1))
