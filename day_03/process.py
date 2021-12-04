import enum
import statistics
import timeit


def twos_complement(x, num_bits):
    if x < 0:
        return x + (1 << num_bits)
    return x


def power_rating(report):
    numbers = report.splitlines()
    numbers_t = zip(*numbers)
    gamma_str = ''.join(statistics.mode(pos) for pos in numbers_t)
    gamma = int(gamma_str, base=2)
    epsilon = twos_complement(~gamma, len(gamma_str))
    return gamma * epsilon


class Ratings(enum.Enum):
    OXYGEN_GENERATOR = enum.auto()
    CO2_SCRUBBER = enum.auto()


def rating_search(numbers, bit_criteria: Ratings):
    pos = 0
    while True:
        numbers_t = list(zip(*numbers))
        bit_values = statistics.multimode(numbers_t[pos])
        match bit_values:
            case (_, _):
                if bit_criteria == Ratings.OXYGEN_GENERATOR:
                    bit_value = '1'
                elif bit_criteria == Ratings.CO2_SCRUBBER:
                    bit_value = '0'
                else:
                    raise Exception
            case (x,):
                if bit_criteria == Ratings.OXYGEN_GENERATOR:
                    bit_value = x
                elif bit_criteria == Ratings.CO2_SCRUBBER:
                    bit_value = {'0': '1', '1': '0'}[x]
                else:
                    raise Exception
            case _:
                raise Exception
        numbers = [number for number in numbers if number[pos] == bit_value]
        if len(numbers) == 1:
            result, = numbers
            return int(result, base=2)
        pos += 1


def life_support_rating(report):
    numbers = report.splitlines()
    return rating_search(numbers.copy(), Ratings.OXYGEN_GENERATOR) * rating_search(numbers.copy(), Ratings.CO2_SCRUBBER)


def main():
    with open('input.txt') as f:
        report = f.read()
        power = power_rating(report)
        print(f'{power=}')
        life_support = life_support_rating(report)
        print(f'{life_support=}')


if __name__ == '__main__':
    print(timeit.timeit(main, number=1))