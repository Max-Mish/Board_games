from rest_framework import serializers

from .models import Description, Category, Game


class DescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Description
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class GameSerializer(serializers.ModelSerializer):
    description = DescriptionSerializer()
    category = CategorySerializer(many=True)

    class Meta:
        model = Game
        fields = '__all__'
