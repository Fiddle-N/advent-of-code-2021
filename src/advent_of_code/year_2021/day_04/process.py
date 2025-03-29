import timeit

import numpy as np


class BingoBoard:

    def __init__(self, board_data, height, width):
        self.board_data = board_data
        self._board = np.full((height, width), False)

    def mark(self, number):
        if number in self.board_data:
            self._board[self.board_data[number]] = True

    @property
    def win_condition(self):
        won_cols = np.all(self._board, axis=0)
        won_rows = np.all(self._board, axis=1)
        wins = np.append(won_cols, won_rows)
        win_condition = np.any(wins)
        return win_condition

    def score(self, called_num):
        unmarked_nums = [num for num, pos in self.board_data.items() if not self._board[pos]]
        return sum(unmarked_nums) * called_num


class BingoSubsystem:

    def __init__(self, bingo_data):
        self._bingo_data = bingo_data
        self.numbers = None
        self.boards = None

    @classmethod
    def read_file(cls):
        with open('input.txt') as f:
            return cls(f.read())

    def _process_data(self, bingo_data):
        raw_numbers, *raw_boards = bingo_data.split('\n\n')
        numbers = [int(number) for number in raw_numbers.split(',')]
        boards = []
        for raw_board in raw_boards:
            board_data = {}
            split_board = [
                [int(val) for val in row.split()]
                for row in raw_board.split('\n')
            ]
            height = len(split_board)
            width = len(split_board[0])
            for y, row in enumerate(split_board):
                for x, val in enumerate(row):
                    board_data[val] = (y, x)
            board = BingoBoard(board_data, height, width)
            boards.append(board)
        return numbers, boards

    def win(self):
        self.numbers, self.boards = self._process_data(self._bingo_data)
        for number in self.numbers:
            for board in self.boards:
                board.mark(number)
                if board.win_condition:
                    return board.score(number)

    def wookie_win(self):
        self.numbers, self.boards = self._process_data(self._bingo_data)
        won_boards = []
        number_of_boards = len(self.boards)
        number_of_won_boards = 0
        for number in self.numbers:
            for board_no, board in enumerate(self.boards):
                if board_no in won_boards:
                    continue
                board.mark(number)
                if board.win_condition:
                    won_boards.append(board_no)
                    number_of_won_boards += 1
                    last_board = board
                if number_of_boards == number_of_won_boards:
                    # all boards are won before all numbers called
                    return board.score(number)
        # all numbers are called before all boards are won
        return last_board.score(number)


def main():
    bingo_subsystem = BingoSubsystem.read_file()
    print('Win score:', bingo_subsystem.win())
    print('Wookie win score:', bingo_subsystem.wookie_win())


if __name__ == '__main__':
    print(timeit.timeit(main, number=1))