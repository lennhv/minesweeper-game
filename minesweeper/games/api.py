from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import (RetrieveUpdateAPIView,
                                     ListCreateAPIView, UpdateAPIView)

from .models import MinesweeperGame

from .serializers import (
    MinesweeperGameSerializer,
    MinesweeperGameUpdateSerializer,
    FlagSquareBoarSerializer)


class ListMinesweperApiView(ListCreateAPIView):
    serializer_class = MinesweeperGameSerializer
    queryset = MinesweeperGame.objects.all()
    lookup_field = "id"


class RetrieveUpdateDestroyApiView(RetrieveUpdateAPIView):
    serializer_class = MinesweeperGameUpdateSerializer
    queryset = MinesweeperGame.objects.all()
    lookup_field = "id"


class FlagSquareBoardApiView(UpdateAPIView):
    serializer_class = FlagSquareBoarSerializer
    queryset = MinesweeperGame.objects.all()
    lookup_field = "id"
