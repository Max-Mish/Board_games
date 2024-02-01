from rest_framework import serializers

from .models import BoardGame


class GamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardGame
        fields = "__all__"
