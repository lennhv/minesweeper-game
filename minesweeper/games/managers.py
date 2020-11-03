import logging
from django.db import models

from .minesweeper_board import Minesweeper


log = logging.getLogger(__name__)


class MinesweeperGameManager(models.Manager):

    def create_game(self, **kwargs):
        """ Crea game
        """
        log.debug("create_game kwargs %s", kwargs)
        board = Minesweeper().create_game_board(**kwargs)
        kwargs['board'] = board
        game = self.model(**kwargs)
        game.save(using=self._db)
        return game

    def update_game(self, **kwargs):
        """ Update game if is not 
            finished and is user is owner
        """
        self.model.filter(
            id=kwargs[id], status=self.model.STARTED,
            user=kwargs['user']).update(**kwargs)
