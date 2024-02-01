from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, generics, status
from rest_framework import generics, mixins, permissions
from rest_framework.response import Response

from user_action.models import Booking
from .models import BoardGame
from .serialiers import GamesSerializer, BookingRequestSerializer, BookingResponseSerializer


# Create your views here.
class GamesViewSet(viewsets.ModelViewSet):
    serializer_class = GamesSerializer
    queryset = BoardGame.objects.all().order_by("-id")


class GameBookViewSet(generics.GenericAPIView, mixins.RetrieveModelMixin):
    serializer_class = BookingRequestSerializer

    @swagger_auto_schema(
        request_body=BookingRequestSerializer(), responses={201: BookingResponseSerializer()}
    )
    def post(self, request):
        serializer = BookingRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        booking = Booking(user_id=data['user_id'], game_id=data['game_id'], opening_date=data['opening_date'],
                          return_period=data['return_period'])
        booking.save()
        return Response(
            data=BookingResponseSerializer(booking).data, status=status.HTTP_201_CREATED
        )
