from django.urls import path


from .api import (
    ListMinesweperApiView,
    RetrieveUpdateDestroyApiView,
    FlagSquareBoardApiView)


app_name = 'games'
urlpatterns = [
    path('games/', ListMinesweperApiView.as_view(), name='api-minesweeper'),
    path('games/<uuid:id>/', RetrieveUpdateDestroyApiView.as_view(),
         name='api-minesweeper-detail'),
    path('games/<uuid:id>/flag/', FlagSquareBoardApiView.as_view(),
         name='api-minesweeper-flag'),
]
