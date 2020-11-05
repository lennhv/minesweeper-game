import random
import logging

log = logging.getLogger(__name__)


class Minesweeper:

    @staticmethod
    def _traslate_cell(cell):
        """ traslate cell  into a:
            - number if is not a mine
            - 'M' if is a mine
        """
        prop = Minesweeper.property_to_numbers(cell)
        if prop[2] == 1:
            return 'M'
        return prop[3]

    @staticmethod
    def convert_to_cell(cell):
        """ convert a cell value into a string cell
            NOTE: not take in account flagged and open properties
        """
        if cell == 'M':
            return '0010'
        return '000' + str(cell)

    @staticmethod
    def display_board(board):
        """ display a board with all properties
        """
        log.debug("+"*60)
        _board = [""]
        for row in board:
            _board.append(" ".join(cell for cell in row))
            _board.append("")
        log.debug("%s", '\n'.join(_board))
        log.debug("+"*60)

    @staticmethod
    def display_traslated_board(board):
        """ display a board in a simple way
         'M' for mines and number for counters
        """
        log.debug("+"*60)
        _board = [""]
        for row in board:
            _board.append(" ".join(str(Minesweeper._traslate_cell(cell))
                                for cell in row))
            _board.append("")
        log.debug("%s", '\n'.join(_board))
        log.debug("+"*60)

    @staticmethod
    def property_to_numbers(s):
        """ Convert numeric string into a list numbers
        """
        return [int(i) for i in list(s)]

    @staticmethod
    def numbers_to_property(n):
        """ convert list numbers to numeric string
        """
        return ''.join([str(i) for i in n])

    def get_point(self, col, row):
        """ Detemine a X, Y point in a random way
            point value from 0 to max-1
        """
        return (random.randrange(0, col-1),
                random.randrange(0, row-1))

    def _update_neighbor(self, c, r, board):
        """ update mine neighbor counter
            if the square is not a mine
        """
        prop = Minesweeper.property_to_numbers(board[r][c])
        if prop[2] == 0:
            prop[3] += 1
        board[r][c] = Minesweeper.numbers_to_property(prop)
        return

    def create_game_board(self, rows=9, columns=9, mines=10, **kwargs):
        """ Create a board for minesweeper game 
            according to args received

            The board is generated based on `rows` and `columns` args, 
            at the begining the board is filled '0000' string number
            based on `mines` argument, each one is inserted in the board 
            ensuring that only one mine is in a square, when a mine is inserted 
            all its neigbors are updated addinng 1 to the counter in every square 
            if it is not a mine.

            A mine can have up to 8 neighbors
            \ | /
            - M -
            / | \ 

            Each number '0000' is the initial properties of the square
            from the left to right
            0 -> flagged 
            1 -> open
            2 -> mine
            3-> counter

            For flags(flagged, open, mine)
                0 -> false
                1 -> true

        """
        log.debug("create board cols: %s rows: %s mines: %s",
                  columns, rows, mines)
        # create `zeroised` board
        board = [['0000' for i in range(columns)] for i in range(rows)]
        # mines setup
        _mines = []
        while len(_mines) < mines:
            c, r = self.get_point(columns, rows)
            if (c, r) in _mines:
                continue
            _mines.append((c, r))
            try:
                prop = Minesweeper.property_to_numbers(board[r][c])
                prop[2] = 1
                prop[3] = 0
                board[r][c] = Minesweeper.numbers_to_property(prop)
            except:
                log.exception("Setup mine row:%s column:%s", r, c)
                log.exception("Setup mine row:%s column:%s" % (r, c))
                Minesweeper.display_board(board)
                raise
            # left
            if c > 0:
                self._update_neighbor(c-1, r, board)
                if r > 0:
                    # upper
                    self._update_neighbor(c, r-1, board)
                    # left upper
                    self._update_neighbor(c-1, r-1, board)
                if r < rows-1:
                    # lower
                    self._update_neighbor(c, r+1, board)
                    # left lower
                    self._update_neighbor(c-1, r+1, board)
            # right
            if c < columns-1:
                self._update_neighbor(c+1, r, board)
                if r > 0:
                    # right upper
                    self._update_neighbor(c+1, r-1, board)
                if r < rows-1:
                    # right lower
                    self._update_neighbor(c+1, r+1, board)
            # colum 0
            if c == 0:
                if r > 0:
                    # upper
                    self._update_neighbor(c, r-1, board)
                if r < rows-1:
                    # lower
                    self._update_neighbor(c, r+1, board)
        return board


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    rows = random.randrange(9, 30)
    cols = random.randrange(9, 30)
    mines = random.randrange(9, 30)
    board = Minesweeper().\
        create_game_board(rows=rows, columns=cols, mines=mines)
    Minesweeper.display_board(board)
    Minesweeper.display_traslated_board(board)
