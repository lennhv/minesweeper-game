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
        if instance.status == instance.FINISHED:
            return instance
        # 
        board = json.loads(instance.board)
        lost = False
        flagged = kwargs["square"]
        log.debug("flagged: %s", flagged)
        data = Minesweeper.property_to_numbers(board[flagged[1]][flagged[0]])
        data[0] = 1
        # update board
        board[flagged[1]][flagged[0]] = Minesweeper.numbers_to_property(data)
        instance.board = json.dumps(board)
        instance.save(using=self._db)
        return instance

    def update_game(self, **kwargs):
        """ Update game if is not 
            finished and is user is owner
        """
        instance = kwargs["instance"]
        if instance.status == instance.FINISHED:
            return instance
        # 
        # log.debug("instance.board %s", instance.board)
        board = json.loads(instance.board)
        lost = False
        opens = kwargs["opens"]
        for sq in opens:
            data = Minesweeper.property_to_numbers(board[sq[1]][sq[0]])
            data[1] = 1
            if data[2] == 1:
                lost = True
            # update board
            board[sq[1]][sq[0]] = Minesweeper.numbers_to_property(data)
        instance.board = json.dumps(board)
        finish = False
        if lost:
            finish = True
            instance.result = instance.LOST
        else:
            # validate if all not mine square are open
            # if so win and finish
            all_open = True
            for i, row in enumerate(board):
                for j, column in enumerate(row):
                    data = Minesweeper.property_to_numbers(column)
                    # open square or mine
                    if data[1] == 1 or data[2] == 1:  
                        continue
                    all_open = False
                    break
                if not all_open:
                    break
            if all_open:
                finish = True
                instance.result = instance.WIN
        if finish:
            instance.status = instance.FINISHED
            instance.finish_at = timezone.now()
        #
        instance.save(using=self._db)
        return instance
