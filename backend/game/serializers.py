from rest_framework import serializers

from .models import Description, Category, Game


class DescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Description
        fields = '__all__'


class CategoryRequestSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Category
        fields = ['id']


class CategoryResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class GameRequestSerializer(serializers.ModelSerializer):
    description = DescriptionSerializer()
    category_ids = CategoryRequestSerializer(many=True)

    class Meta:
        model = Game
        fields = ['name', 'publisher', 'cost', 'cover_photo', 'description', 'category_ids']


class GameResponseSerializer(serializers.ModelSerializer):
    description = DescriptionSerializer()
    category = CategoryResponseSerializer(many=True)

    class Meta:
        model = Game
        fields = '__all__'


class GameQuerySerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
