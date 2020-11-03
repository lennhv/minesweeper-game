from rest_framework import serializers
from drf_yasg import openapi

from .models import MinesweeperGame


class MinesweeperGameSerializer(serializers.ModelSerializer):

    class Meta:
        model = MinesweeperGame
        fields = ('id', 'board', 'rows', 'columns', 'mines',
                  'start_at', 'finish_at', 'status', 'result',)
        read_only_fields = ('board', 'finish_at',
                            'start_at', 'status', 'result')


class SquareSerializer(serializers.ListField):
    """ Serializer to determine the location 
        of the square on the game board
    """
    max_length = 2
    min_length = 2
    child = serializers.IntegerField()


class MinesweeperGameUpdateSerializer(serializers.ModelSerializer):

    picked = SquareSerializer(write_only=True)
    squares = serializers.ListField(
        child=SquareSerializer(write_only=True), min_length=1, write_only=True)
    mine = serializers.BooleanField(write_only=True)

    class Meta:
        model = MinesweeperGame
        fields = ('id', 'board', 'start_at', 'finish_at',
                  'status', 'result', 'picked', 'squares', 'mine',)
        read_only_fields = ('board', 'finish_at',
                            'start_at', 'status', 'result')


class FlagSquareBoarSerializer(serializers.ModelSerializer):
    square = SquareSerializer(write_only=True)

    class Meta:
        model = MinesweeperGame
        fields = ('id', 'board', 'square')
        read_only_fields = ('board', )
