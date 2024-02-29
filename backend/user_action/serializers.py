from datetime import datetime

from rest_framework import serializers

from authentication.serializers import ProfileInfoSerializer
from game.serializers import GameResponseSerializer
from .models import Booking, Vote


class UTCDateField(serializers.DateField):
    def to_representation(self, value):
        return value.strftime('%a, %d %b %Y %H:%M:%S UTC')

    def to_internal_value(self, data):
        try:
            return datetime.strptime(data, "%a, %d %b %Y %H:%M:%S %Z").date()
        except ValueError:
            raise serializers.ValidationError("Invalid date format, should be YYYY-MM-DD")


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
