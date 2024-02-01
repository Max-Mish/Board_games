from rest_framework import viewsets, generics, status

from .models import BoardGame
from .serialiers import GamesSerializer


class GamesViewSet(viewsets.ModelViewSet):
    serializer_class = GamesSerializer
    queryset = BoardGame.objects.all().order_by("-id")
