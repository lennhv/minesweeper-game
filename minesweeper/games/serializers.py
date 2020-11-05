import json
from rest_framework import serializers

from .models import MinesweeperGame


class MinesweeperGameSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    board = serializers.SerializerMethodField(source='board')

    class Meta:
        model = MinesweeperGame
        fields = ('id', 'board', 'rows', 'columns', 'mines', 'user',
                  'start_at', 'finish_at', 'status', 'result',)
        read_only_fields = ('board', 'finish_at',
                            'start_at', 'status', 'result')

    def create(self, validated_data):
        return self.Meta.model.\
            objects.create_game(**validated_data)

    def get_board(self, obj):
        if isinstance(obj.board, str):
            return json.loads(obj.board)
        return obj.board


class SquareSerializer(serializers.ListField):
    """ Serializer to determine the location 
        of the square on the game board
        [column, row]
    """
    max_length = 2
    min_length = 2
    child = serializers.IntegerField()


class MinesweeperGameUpdateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    opens = serializers.ListField(
        child=SquareSerializer(write_only=True), min_length=1, write_only=True)
    board = serializers.SerializerMethodField(source='board')

    class Meta:
        model = MinesweeperGame
        fields = ('id', 'board', 'start_at', 'finish_at', 'user',
                  'status', 'result', 'opens', )
        read_only_fields = ('board', 'finish_at',
                            'start_at', 'status', 'result')

    def update(self, instance, validated_data):
        validated_data["instance"] = instance
        return self.Meta.model.\
            objects.update_game(**validated_data)

    def get_board(self, obj):
        if isinstance(obj.board, str):
            return json.loads(obj.board)
        return obj.board


class FlagSquareBoarSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    square = SquareSerializer(write_only=True)
    board = serializers.SerializerMethodField(source='board')

    class Meta:
        model = MinesweeperGame
        fields = ('id', 'board', 'square', 'user',)
        read_only_fields = ('board', )

    def update(self, instance, validated_data):
        validated_data["instance"] = instance
        return self.Meta.model.\
            objects.flag_square(**validated_data)

    def get_board(self, obj):
        if isinstance(obj.board, str):
            return json.loads(obj.board)
        return obj.board
