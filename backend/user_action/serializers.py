from rest_framework import serializers

from game.serializers import GameRequestSerializer, GameResponseSerializer
from authentication.serializers import ProfileInfoSerializer
from .models import Booking, Vote


class BookingRequestSerializer(serializers.ModelSerializer):
    game_id = serializers.IntegerField()

    class Meta:
        model = Booking
        fields = ['game_id', 'return_date']


class BookingResponseSerializer(serializers.ModelSerializer):
    game = GameResponseSerializer()
    user = ProfileInfoSerializer()

    class Meta:
        model = Booking
        fields = '__all__'


class VoteRequestSerializer(serializers.Serializer):
    choice_ids = serializers.ListField(child=serializers.IntegerField())
    user_id = serializers.IntegerField()


class VoteResponseSerializer(serializers.ModelSerializer):
    user = ProfileInfoSerializer()

    class Meta:
        model = Vote
        fields = '__all__'
