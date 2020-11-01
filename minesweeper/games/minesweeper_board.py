import random


class Minesweeper:

    @staticmethod
    def _display_board(board):
        for row in board:
            print(" ".join(str(cell) for cell in row))
            print("")

    def get_point(self, max_x, max_y):
        """ Detemine a X, Y point in a random way
            point value from 0 to max-1
        """
        return (random.randrange(0, max_x-1),
                random.randrange(0, max_y-1))

    def _update_neighbor(self, x, y, board):
        """ update mine neighbor counter
            if the square is not a mine
        """
        if board[x][y] != 'M':
            board[x][y] += 1
        return

    def create_game_board(self, rows=9, columns=9, mines=10):
        """ Create a board for minesweeper game 
            according to args received

            The board is generated based on `rows` and `columns` args, 
            at the begining the board is filled with 0
            based on `mines` argument, each one is inserted in the board 
            ensuring that only one mine is in a square, when a mine is inserted 
            all its neigbors are updated addinng 1 to the counter (every square is a counter) 
            in every square if it is not a mine.

            A mine can have up to 8 neighbors
            \ | /
            - M -
            / | \ 

        """
        # create zeroised board
        board = [[0 for i in range(rows)] for i in range(columns)]
        # mines setup
        _mines = []
        while len(_mines) < mines:
            r, c = self.get_point(rows, columns)
            if (r, c) in _mines:
                continue
            _mines.append((r, c))
            board[r][c] = 'M'
            # left
            if c > 0:
                self._update_neighbor(r, c-1, board)
                if r > 0:
                    # upper
                    self._update_neighbor(r-1, c, board)
                    # left upper
                    self._update_neighbor(r-1, c-1, board)
                if r < rows-1:
                    # lower
                    self._update_neighbor(r+1, c, board)
                    # left lower
                    self._update_neighbor(r+1, c-1, board)
            # right
            if c < columns-1:
                self._update_neighbor(r, c+1, board)
                if r > 0:
                    # right upper
                    self._update_neighbor(r-1, c+1, board)
                if r < rows-1:
                    # right lower
                    self._update_neighbor(r+1, c+1, board)
            # colum 0
            if c == 0:
                if r > 0:
                    # upper
                    self._update_neighbor(r-1, c, board)
                if r < rows-1:
                    # lower
                    self._update_neighbor(r+1, c, board)

        return board


if __name__ == '__main__':
    board = Minesweeper().create_game_board()
    Minesweeper._display_board(board)
