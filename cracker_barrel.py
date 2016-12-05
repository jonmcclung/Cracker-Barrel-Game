# -*-coding:utf8;-*-
# qpy:3
# qpy:console
from collections import namedtuple, Counter
from copy import deepcopy
from numbers import Number
from typing import Iterable

Move = namedtuple('Move', 'row column direction')


class Direction:
    def __init__(self, x: int, y: int, name=''):
        self.x = x
        self.y = y
        self.name = name

    def __mul__(self, rhs: Number) -> 'Direction':
        return Direction(self.x * rhs, self.y * rhs)

    def __str__(self):
        return self.name or '<' + __name__ + '(x: ' + str(self.x) + ', y: ' + str(self.y) + ')>'

    def __repr__(self):
        return str(self)


class Puzzle:
    directions = tuple(
        Direction(x, y, name)
        for (x, y, name) in [
            (0, -1, 'up'),
            (0, 1, 'down'),
            (-1, 0, 'left'),
            (1, 0, 'right'),
            (1, -1, 'up_right'),
            (-1, 1, 'down_left'),
            (0, 0, 'zero'),
        ]
    )

    up, down, left, right, up_right, down_left, zero = directions
    directions = directions[:-1]

    def __str__(self):
        rows = []
        for row in self.board:
            rows.append(' '.join(str(int(val)) for val in row))
        return '\n'.join(rows)

    def __repr__(self):
        return self.__str__()

    def get(self, move: Move, direction: Direction) -> bool:
        if move.row + direction.y < 0 or move.column + direction.x < 0:
            raise IndexError
        return self.board[move.row + direction.y][move.column + direction.x]

    def set(self, move: Move, direction: Direction, val: bool):
        if move.row + direction.y < 0 or move.column + direction.x < 0:
            raise IndexError
        self.board[move.row + direction.y][move.column + direction.x] = val

    def board_hash(self) -> int:
        res = 0
        i = 0
        for row in self.board:
            for val in row:
                res += val << i
                i += 1
        return res

    def __init__(self, board: Iterable[Iterable[bool]] = None, moves: Iterable[Move] = None):
        self.board = board or [
            [True, True, True, True, True],
            [True, True, True, True],
            [True, False, True],
            [True, True],
            [True]]
        self.moves = moves or self.all_moves()
        self.solution = []

    def solve(self, memory={}) -> bool:
        if self.is_solved():
            return True
        elif self.board_hash() in memory:
            return False
        for move in self.moves:
            puzzle = Puzzle(deepcopy(self.board), self.moves)
            if puzzle.hop(move) and puzzle.solve():
                self.solution = [move] + puzzle.solution
                return True
        memory[self.board_hash()] = True
        return False

    def is_solved(self) -> bool:
        left = 0
        for row in self.board:
            for column in row:
                left += column
        if left == 1:
            return True
        return False

    def hop(self, move: Move) -> bool:
        if not (self.get(move, move.direction) and self.get(move, move.direction * 2) and
                    not self.get(move, Puzzle.zero)):
            return False
        self.set(move, Puzzle.zero, True)
        self.set(move, move.direction, False)
        self.set(move, move.direction * 2, False)
        return True

    def all_moves(self):
        res = []
        for direction in Puzzle.directions:
            for row in range(5):
                for column in range(5 - row):
                    move = Move(row, column, direction)
                    try:
                        # self.get(move, move.direction)
                        self.get(move, move.direction * 2)
                        res.append(move)
                    except IndexError:
                        pass
        return res


def main():
    solved = Puzzle()
    display_puzzle = Puzzle()
    if solved.solve():
        print('solution:')
        print(display_puzzle)
        for move in solved.solution:
            display_puzzle.hop(move)
            print(move, display_puzzle, sep='\n')


if __name__ == '__main__':
    main()
