from rest_framework import serializers

from .models import Description, Category, Game, GameItem


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


class GameItemSerializer(serializers.ModelSerializer):
    game = GameResponseSerializer()

    class Meta:
        model = GameItem
        fields = '__all__'


class GameItemCreateSerializer(serializers.ModelSerializer):
    game_id = serializers.IntegerField(required=True)
    n_items = serializers.IntegerField()

    class Meta:
        model = GameItem
        fields = ['game_id', 'n_items']


class DatesCheckRequestSerializer(serializers.Serializer):
    game_id = serializers.IntegerField()
    amount = serializers.IntegerField()
    booked_dates = serializers.ListField()


class DatesCheckResponseSerializer(serializers.Serializer):
    dates_check_status = serializers.BooleanField(required=True)
    message = serializers.CharField()
    items_ids = serializers.ListField(child=serializers.UUIDField())
