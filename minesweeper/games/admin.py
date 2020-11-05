from django.contrib import admin

# Register your models here.
from .models import MinesweeperGame


@admin.register(MinesweeperGame)
class MinesweeperGameAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'board', 'rows', 'columns',
                    'mines', 'start_at', 'finish_at', 'status', 'result')
