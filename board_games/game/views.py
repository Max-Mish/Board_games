from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework import generics, mixins, permissions
from .models import BoardGame
from .serialiers import GamesSerializer, BookingRequestSerializer


# Create your views here.
class GamesViewSet(viewsets.ModelViewSet):
    serializer_class = GamesSerializer
    queryset = BoardGame.objects.all().order_by("-id")



class GameBookViewSet(generics.GenericAPIView, mixins.RetrieveModelMixin):
    serializer_class = BookingRequestSerializer

    def create_booking(self, request):
        pass
