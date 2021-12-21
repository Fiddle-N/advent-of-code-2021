from day_21 import process, process_2


def test_practice_game():
    starting_positions = """\
Player 1 starting position: 4
Player 2 starting position: 8"""
    dd = process.DiracDice.from_str(starting_positions)
    assert dd.play() == 739_785


def test_real_game():
    starting_positions = """\
Player 1 starting position: 4
Player 2 starting position: 8"""
    wins = process_2.dirac_dice_from_str(starting_positions)
    assert wins == {'p1': 444356092776315, 'p2': 341960390180808}
    assert max(wins.values()) == 444356092776315
