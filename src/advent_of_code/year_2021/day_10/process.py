import collections
import dataclasses
import statistics
import typing


START_BRACKETS = {'(', '[', '{', '<'}
BRACKET_PAIRS = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>',
    ')': '(',
    ']': '[',
    '}': '{',
    '>': '<',
}
ILLEGAL_BRACKET_SCORE = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}
VALID_BRACKET_SCORE = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}


@dataclasses.dataclass
class ChunkResult:
    is_valid: bool
    context: typing.Any


class NavigationSubsystem:

    def __init__(self, code):
        self.code = [
            row
            for row in code.split('\n')
        ]

    @classmethod
    def read_file(cls):
        with open('input.txt') as f:
            return cls(f.read().strip())

    def _is_valid(self, chunk):
        input_ = collections.deque(chunk)
        output = collections.deque()
        while input_:
            char = input_.popleft()
            if char in START_BRACKETS:
                output.append(char)
            elif char in ILLEGAL_BRACKET_SCORE:
                try:
                    match_char = output.pop()
                except IndexError:
                    # no chars to match
                    return ChunkResult(is_valid=False, context=ILLEGAL_BRACKET_SCORE[char])
                if match_char != BRACKET_PAIRS[char]:
                    output.append(match_char)  # put char back
                    return ChunkResult(is_valid=False, context=ILLEGAL_BRACKET_SCORE[char])
        return ChunkResult(is_valid=True, context=''.join(output))    # successful chunk

    def system_error_score(self):
        scores = []
        for chunk in self.code:
            result = self._is_valid(chunk)
            if not result.is_valid:
                scores.append(result.context)
        return sum(scores)

    def _creation_str_score(self, incomplete_chars):
        close_brackets = [BRACKET_PAIRS[char] for char in reversed(incomplete_chars)]
        score = 0
        for bracket in close_brackets:
            score = score * 5 + VALID_BRACKET_SCORE[bracket]
        return score

    def middle_score(self):
        valid_chunks = []
        for chunk in self.code:
            result = self._is_valid(chunk)
            if result.is_valid:
                valid_chunks.append(result.context)
        completion_str_scores = [self._creation_str_score(chunk) for chunk in valid_chunks]
        sorted_completion_scores = sorted(completion_str_scores)
        return statistics.median(sorted_completion_scores)


def main():
    nav_subsystem = NavigationSubsystem.read_file()
    print('System error score:', nav_subsystem.system_error_score())
    print('Middle score:', nav_subsystem.middle_score())


if __name__ == '__main__':
    import timeit
    print(timeit.timeit(main, number=1))
