from unittest import mock
from django.test import TestCase

# Create your tests here.

from games.minesweeper_board import Minesweeper


class MinesweeperTest(TestCase):
    """ Test minesweeper board generation
    """

    def test_one_mine(self):
        _b = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 1, 1, 1, 0, 0, 0],
              [0, 0, 0, 1, "M", 1, 0, 0, 0],
              [0, 0, 0, 1, 1, 1, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0]
              ]
        _board = []
        for row in _b:
            cols = []
            for c in row:
                cols.append(Minesweeper._convert_to_cell(c))
            _board.append(cols)
        ins = Minesweeper()
        ins.get_point = mock.Mock(return_value=(4, 4))
        board = ins.create_game_board(mines=1)
        # print("-"*30)
        # Minesweeper.display_traslated_board(_board)
        # print("*"*30)
        # Minesweeper.display_traslated_board(board)
        self.assertEqual(board, _board)

    def test_corners_mines(self):
        mines = ((0, 0), (0, 8), (8, 0), (8, 8))
        # # board
        _b = [["M", 1, 0, 0, 0, 0, 0, 1, "M"],
              [1, 1, 0, 0, 0, 0, 0, 1, 1],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [1, 1, 0, 0, 0, 0, 0, 1, 1],
              ["M", 1, 0, 0, 0, 0, 0, 1, "M"]
              ]
        _board = []
        for row in _b:
            cols = []
            for c in row:
                cols.append(Minesweeper.convert_to_cell(c))
            _board.append(cols)
        ins = Minesweeper()
        ins.get_point = mock.Mock(side_effect=mines)
        board = ins.create_game_board(mines=4)
        # print("-"*30)
        # Minesweeper.display_traslated_board(_board)
        # print("*"*30)
        # Minesweeper.display_traslated_board(board)
        self.assertEqual(board, _board)

    def test_adjacents_mines(self):
        mines = ((1, 1), (2, 2), (3, 2), (5, 5))
        # # board
        _b = [[1, 1, 1, 0, 0, 0, 0, 0, 0],
              [1, "M", 2, 1, 0, 0, 0, 0, 0],
              [1, 3, "M", 2, 0, 0, 0, 0, 0],
              [0, 2, "M", 2, 0, 0, 0, 0, 0],
              [0, 1, 1, 1, 1, 1, 1, 0, 0],
              [0, 0, 0, 0, 1, "M", 1, 0, 0],
              [0, 0, 0, 0, 1, 1, 1, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0]
              ]
        _board = []
        for row in _b:
            cols = []
            for c in row:
                cols.append(Minesweeper.convert_to_cell(c))
            _board.append(cols)
        ins = Minesweeper()
        ins.get_point = mock.Mock(side_effect=mines)
        board = ins.create_game_board(mines=4)
        # print("-"*30)
        # Minesweeper.display_traslated_board(_board)
        # print("*"*30)
        # Minesweeper.display_traslated_board(board)
        self.assertEqual(board, _board)
