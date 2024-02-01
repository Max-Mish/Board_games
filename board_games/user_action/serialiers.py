from rest_framework import serializers

from .models import Booking
from game.serialiers import GamesSerializer


class BookingRequestSerializer(serializers.Serializer):
    game_id = serializers.IntegerField(required=True)
    user_id = serializers.IntegerField(required=True)
    opening_date = serializers.DateField(required=True)
    return_period = serializers.DateField(required=True)


class BookingResponseSerializer(serializers.ModelSerializer):
    game = GamesSerializer()

    class Meta:
        model = Booking
        fields = "__all__"
