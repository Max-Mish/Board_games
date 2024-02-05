from rest_framework import viewsets

from .models import Game
from .serialiers import GameSerializer


class GameListViewSet(viewsets.ModelViewSet):
    serializer_class = GameSerializer
    queryset = Game.objects.all().order_by('-id')
