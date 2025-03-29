import collections
import dataclasses
import functools
import itertools

import parse


@dataclasses.dataclass(frozen=True)
class PlayerState:
    score: int
    square: int


@dataclasses.dataclass(frozen=True)
class GameState:
    p1: PlayerState
    p2: PlayerState


@functools.cache
def dice_rolls():
    return collections.Counter(
        sum(die_no) for die_no in itertools.product(range(1, 4), repeat=3)
    )


@functools.cache
def board_move(start, roll):
    return (start - 1 + roll) % 10 + 1


@functools.cache
def board_moves(start):
    rolls = dice_rolls()
    return collections.Counter(
        {board_move(start, roll): count for roll, count in rolls.items()}
    )


@functools.cache
def simulate_states(state: PlayerState):
    moves = board_moves(state.square)
    return collections.Counter(
        {
            PlayerState(score=state.score + move, square=move): count
            for move, count in moves.items()
        }
    )


@functools.cache
def generate_state(p1, p2):
    return GameState(p1, p2)


def dirac_dice(p1, p2):
    start_state = GameState(p1=PlayerState(0, p1), p2=PlayerState(0, p2))
    non_winning_states = collections.Counter([start_state])
    wins = collections.Counter({'p1': 0, 'p2': 0})
    player = None

    while non_winning_states:
        if player is None:
            player = 'p1'
        else:
            player = {'p2': 'p1', 'p1': 'p2'}[player]
        sitter = {'p2': 'p1', 'p1': 'p2'}[player]
        next_non_winning_states = collections.Counter()
        for state, count in non_winning_states.items():
            player_state = getattr(state, player)
            next_states = simulate_states(player_state)
            for next_state, next_count in next_states.items():
                total_count = count * next_count
                if next_state.score >= 21:
                    wins[player] += total_count
                else:
                    gs_details = {player: next_state, sitter: getattr(state, sitter)}
                    next_non_winning_states[generate_state(**gs_details)] += total_count
        non_winning_states = next_non_winning_states
    return wins


def dirac_dice_from_str(str_):
    template = """\
Player 1 starting position: {p1:d}
Player 2 starting position: {p2:d}"""
    parsed = parse.parse(template, str_)
    return dirac_dice(parsed['p1'], parsed['p2'])


def dirac_dice_from_file():
    with open("input.txt") as f:
        wins = dirac_dice_from_str(f.read().strip())
    print('Player with more wins - number of wins:', max(wins.values()))


def main():
    dirac_dice_from_file()


if __name__ == '__main__':
    import timeit
    print(timeit.timeit(main, number=1))
