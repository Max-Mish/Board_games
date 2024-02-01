from rest_framework import serializers

from user_action.models import Booking
from .models import BoardGame


class GamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardGame
        fields = "__all__"


class BookingRequestSerializer(serializers.Serializer):
    game_id = serializers.IntegerField(required=True)
    user_id = serializers.IntegerField(required=True)
    opening_date = serializers.DateField(required=True)
    return_period = serializers.DateField(required=True)


class BookingResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"
