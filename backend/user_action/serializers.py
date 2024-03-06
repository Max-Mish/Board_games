from rest_framework import serializers

from authentication.serializers import ProfileInfoSerializer
from core.fields import UTCDateField
from game.serializers import GameResponseSerializer
from .models import Booking, Vote


class BookingRequestSerializer(serializers.ModelSerializer):
    game_id = serializers.IntegerField()
    game_item_id = serializers.UUIDField()
    opening_date = UTCDateField()
    return_date = UTCDateField()

    class Meta:
        model = Booking
        fields = ['game_id', 'game_item_id', 'opening_date', 'return_date']


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
