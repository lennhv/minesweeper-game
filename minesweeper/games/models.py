import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from .managers import MinesweeperGameManager


class MinesweeperGame(models.Model):
    """
    """
    
    WIN = 1
    LOST = 2
    RESULTS = (
        (WIN, _('WIN')),
        (LOST, _('LOST')),
    )
    
    STARTED = 1
    FINISHED = 2
    STATUSES = (
        (STARTED, _('STARTED')),
        (FINISHED, _('FINISHED')),
    )
    
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    board = models.TextField(_('board'))
    rows = models.SmallIntegerField(_('rows'))
    columns = models.SmallIntegerField(_('columns'))
    mines = models.SmallIntegerField(_('mines'))
    start_at = models.DateTimeField(_('start_at'),auto_now=True)
    finish_at = models.DateTimeField(_('finish_at'), null=True)
    status = models.SmallIntegerField(_('status'), choices=STATUSES, default=STARTED)
    result = models.SmallIntegerField(_('result'), choices=RESULTS, null=True)

    objects = MinesweeperGameManager()

    class Meta:
        verbose_name = _('minesweeper game')
        verbose_name_plural = _('minesweeper games')

    def __str__(self):
        return str(id)

