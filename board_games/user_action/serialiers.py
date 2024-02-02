from rest_framework import serializers

from .models import Booking, Vote
from game.serialiers import GamesSerializer


class BookingRequestSerializer(serializers.ModelSerializer):
    game_id = serializers.IntegerField(required=True)
    user_id = serializers.IntegerField(required=True)

    class Meta:
        model = Booking
        fields = ['game_id', 'user_id', 'opening_date', 'return_period']


class BookingResponseSerializer(serializers.ModelSerializer):
    game = GamesSerializer()

    class Meta:
        model = Booking
        fields = "__all__"


class VoteRequestSerializer(serializers.Serializer):
    choice_id = serializers.IntegerField(required=True)
    user_id = serializers.IntegerField(required=True)


class VoteResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = "__all__"
