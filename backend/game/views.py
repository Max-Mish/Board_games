from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, generics
from rest_framework.response import Response

from .models import Game, Category, Description, GameItem
from .serializers import GameRequestSerializer, GameResponseSerializer, CategoryResponseSerializer, GameQuerySerializer, \
    DatesCheckRequestSerializer, DatesCheckResponseSerializer, GameItemCreateSerializer, GameItemSerializer
from .services import get_all_dates, get_available_game_items, pack_response_serializer


class RelatedGamesAPIView(generics.ListAPIView):
    @swagger_auto_schema(responses={200: GameResponseSerializer(many=True)}, query_serializer=GameQuerySerializer())
    def get(self, request):
        serializer = GameQuerySerializer(request.query_params)
        game_id = serializer.data.get('id')
        game = Game.objects.get(id=game_id)

        category_ids = [category.id for category in game.category.all()]
        games = Game.objects.filter(category__id__in=category_ids).distinct()
        games = games.exclude(id=game_id)

        return Response(data=GameResponseSerializer(games, many=True).data,
                        status=status.HTTP_200_OK)


class GamesAPIView(generics.ListAPIView):
    @swagger_auto_schema(responses={200: GameResponseSerializer(many=True)})
    def get(self, request):
        queryset = Game.objects.all().order_by('-id')
        return Response(data=GameResponseSerializer(queryset, many=True).data,
                        status=status.HTTP_200_OK)


class GameAPIView(generics.GenericAPIView):
    # permission_classes = (IsAuthenticated,)
    view_permissions = ('game.view_game', 'game.view_description', 'game.view_category')
    add_permissions = ('game.add_game', 'game.add_description', *view_permissions)

    # @method_decorator(permission_required(perm=view_permissions, raise_exception=True))
    @swagger_auto_schema(responses={200: GameResponseSerializer(many=True)}, query_serializer=GameQuerySerializer())
    def get(self, request):
        serializer = GameQuerySerializer(request.query_params)
        game_id = serializer.data.get('id')

        game = Game.objects.get(id=game_id)
        return Response(data=GameResponseSerializer(game).data,
                        status=status.HTTP_200_OK)

    @method_decorator(permission_required(perm=add_permissions, raise_exception=True))
    @swagger_auto_schema(request_body=GameRequestSerializer(), responses={201: GameResponseSerializer()})
    def post(self, request):
        serializer = GameRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        description = Description.objects.create(**data['description'])
        description.save()
        description_id = description.pk

        game = Game(name=data['name'], publisher=data['publisher'], cost=data['cost'],
                    description_id=description_id)
        game.save()

        game_id = game.pk

        ThroughModel = Game.category.through

        category_ids = [category['id'] for category in data.pop('category_ids')]
        categories = Category.objects.filter(pk__in=category_ids)

        ThroughModel.objects.bulk_create([
            ThroughModel(game_id=game_id, category_id=category_id.pk) for category_id in categories
        ])

        return Response(
            data=GameResponseSerializer(game).data, status=status.HTTP_201_CREATED
        )


class CategoryAPIView(generics.GenericAPIView):
    # permission_classes = (IsAuthenticated,)
    view_permissions = ('game.view_category',)
    add_permissions = ('game.add_game', 'game.add_description', *view_permissions)

    # @method_decorator(permission_required(perm=view_permissions, raise_exception=True))
    @swagger_auto_schema(responses={200: CategoryResponseSerializer(many=True)})
    def get(self, request):
        queryset = Category.objects.all().order_by('-id')
        return Response(data=CategoryResponseSerializer(queryset, many=True).data, status=status.HTTP_200_OK)

    @method_decorator(permission_required(perm=add_permissions, raise_exception=True))
    @swagger_auto_schema(request_body=CategoryResponseSerializer(), responses={201: CategoryResponseSerializer()})
    def post(self, request):
        serializer = CategoryResponseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data=serializer.data, status=status.HTTP_201_CREATED
        )


class GameItemCreateAPIView(generics.GenericAPIView):
    @swagger_auto_schema(request_body=GameItemCreateSerializer(), responses={201: GameItemSerializer(many=True)})
    def post(self, request):
        serializer = GameItemCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        game_item_data = serializer.validated_data
        game_id = game_item_data.get('game_id')
        n_items = game_item_data.get('n_items')

        items = [GameItem.objects.create(game_id=game_id) for _ in range(n_items)]

        return Response(
            data=GameItemSerializer(items, many=True).data, status=status.HTTP_201_CREATED
        )


class DatesCheckAPIView(generics.GenericAPIView):
    @swagger_auto_schema(request_body=DatesCheckRequestSerializer(), responses={201: DatesCheckResponseSerializer()})
    def post(self, request):
        serializer = DatesCheckRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        game_item_data = serializer.validated_data
        game_id = game_item_data.get('game_id')
        amount = game_item_data.get('amount')

        booked_dates = get_all_dates(game_item_data.get('booked_dates'))
        available_items = get_available_game_items(game_id, booked_dates)
        response_serializer_data = pack_response_serializer(available_items, amount)
        return Response(data=response_serializer_data, status=status.HTTP_200_OK)
