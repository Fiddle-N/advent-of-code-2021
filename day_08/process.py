import itertools


PATTERN_LENGTHS = {
    1: 2,
    4: 4,
    7: 3,
    8: 7,
}


UNIQUE_SIGNAL_PATTERNS = [1, 4, 7, 8]


class SevenSegmentDisplay:

    def __init__(self, signal_patterns, output_value):
        self.signal_patterns = signal_patterns
        self.output_value = output_value

    def unique_patterns(self):
        return sum(
            any([len(digit) in [PATTERN_LENGTHS[pattern] for pattern in UNIQUE_SIGNAL_PATTERNS]])
            for digit in self.output_value
        )

    def decode_output(self):
        patterns = {}

        # initial unique patterns
        for digit, pattern_length in PATTERN_LENGTHS.items():
            for pattern in self.signal_patterns:
                if len(pattern) == pattern_length:
                    patterns[digit] = pattern
                    continue

        length_5_patterns = [pattern for pattern in self.signal_patterns if len(pattern) == 5]

        pattern_2_or_5 = []
        for pattern in length_5_patterns:
            if patterns[1] < pattern:
                patterns[3] = pattern
            else:
                pattern_2_or_5.append(pattern)

        length_6_patterns = [pattern for pattern in self.signal_patterns if len(pattern) == 6]

        pattern_0_or_9 = []
        for pattern in length_6_patterns:
            if not patterns[1] < pattern:
                patterns[6] = pattern
            else:
                pattern_0_or_9.append(pattern)

        for length_5_pattern, length_6_pattern in itertools.product(pattern_2_or_5, pattern_0_or_9):
            if length_5_pattern < length_6_pattern:
                patterns[5] = length_5_pattern
                patterns[9] = length_6_pattern
                break

        for pattern in pattern_2_or_5:
            if pattern != patterns[5]:
                patterns[2] = pattern
                break

        for pattern in pattern_0_or_9:
            if pattern != patterns[9]:
                patterns[0] = pattern
                break

        decoded_values = [
            digit
            for output_pattern in self.output_value
            for digit, pattern in patterns.items()
            if pattern == output_pattern
        ]

        decoded_value = int(''.join(str(value) for value in decoded_values))
        return decoded_value


class SevenSegmentSearch:

    def __init__(self, segment_data):
        self.segment_info = self._process_segment_data(segment_data)

    def _process_segment_data(self, segment_data):
        segment_info = []
        for entry in segment_data.split('\n'):
            raw_signal_patterns, raw_output_value = entry.split(' | ')
            signal_patterns = [set(pattern) for pattern in raw_signal_patterns.split()]
            output_value = [set(digit) for digit in raw_output_value.split()]
            segment_info.append(SevenSegmentDisplay(signal_patterns, output_value))
        return segment_info

    @classmethod
    def read_file(cls):
        with open('input.txt') as f:
            return cls(f.read().strip())

    def unique_patterns(self):
        return sum(display.unique_patterns() for display in self.segment_info)

    def decode_output(self):
        return sum(display.decode_output() for display in self.segment_info)


def main():
    seven_segment_search = SevenSegmentSearch.read_file()
    print('Unique patterns:', seven_segment_search.unique_patterns())
    print('All output values:', seven_segment_search.decode_output())


if __name__ == '__main__':
    import timeit
    print(timeit.timeit(main, number=1))
