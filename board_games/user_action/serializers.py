from rest_framework import serializers

from game.serializers import GameSerializer
from user.serializers import UserResponseShortSerializer
from .models import Booking, Vote


class BookingRequestSerializer(serializers.ModelSerializer):
    game_id = serializers.IntegerField(required=True)
    user_id = serializers.IntegerField(required=True)

    class Meta:
        model = Booking
        fields = ['game_id', 'user_id', 'opening_date', 'return_period']


class BookingResponseSerializer(serializers.ModelSerializer):
    game = GameSerializer()
    user = UserResponseShortSerializer()

    class Meta:
        model = Booking
        fields = '__all__'


class VoteRequestSerializer(serializers.Serializer):
    choice_ids = serializers.ListField(child=serializers.IntegerField(required=True))
    user_id = serializers.IntegerField(required=True)


class VoteResponseSerializer(serializers.ModelSerializer):
    user = UserResponseShortSerializer()

    class Meta:
        model = Vote
        fields = '__all__'
