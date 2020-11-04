import logging
import json
from django.db import models
from django.utils import timezone

from .minesweeper_board import Minesweeper


log = logging.getLogger(__name__)


class MinesweeperGameManager(models.Manager):

    def create_game(self, **kwargs):
        """ Crea game
        """
        log.debug("create_game kwargs %s", kwargs)
        board = Minesweeper().create_game_board(**kwargs)
        kwargs['board'] = json.dumps(board)
        game = self.model(**kwargs)
        game.save(using=self._db)
        return game

    def flag_square(self, **kwargs):
        """ Update game if is not 
            finished and is user is owner
        """
        instance = kwargs["instance"]
        if instance.finished == instance.STARTED:
            return instance
        # 
        board = json.loads(instance.board)
        lost = False
        flagged = kwargs["square"]
        data = Minesweeper.property_to_numbers(board[flagged[1]][flagged[0]])
        data[0] = 1
        # update board
        board[flagged[1]][flagged[0]] = Minesweeper.numbers_to_property(data)
        #
        isinstance.board = json.dumps(board)
        #
        isinstance.save(using=self._db)
        return instance.refresh_from_db()

    def update_game(self, **kwargs):
        """ Update game if is not 
            finished and is user is owner
        """
        instance = kwargs["instance"]
        if instance.finished == instance.STARTED:
            return instance
        # 
        board = json.loads(instance.board)
        lost = False
        s_open = kwargs["open"]
        for sq in s_open:
            data = Minesweeper.property_to_numbers(board[sq[1]][sq[0]])
            data[1] = 1
            if data[2] == 1:
                lost = True
            # update board
            board[sq[1]][sq[0]] = Minesweeper.numbers_to_property(data)
        #
        isinstance.board = json.dumps(board)
        # 
        finish = False
        if lost:
            isinstance.result = instance.LOST
            finish = True
        else:
            # validate if all not mine square are open
            # if so win and finish
            all_open = True
            for row in board:
                for column in row:
                    data = Minesweeper.numbers_to_property(column)
                    if data[1] == 1:  # open square
                        continue
                    all_open = False
                    break
                if not all_open:
                    break
            if all_open:
                finish = True
                isinstance.result = instance.WIN
        if finish:
            isinstance.status = instance.FINISHED
            isinstance.finish_at = timezone.now()
        #
        isinstance.save(using=self._db)
        return instance.refresh_from_db()
