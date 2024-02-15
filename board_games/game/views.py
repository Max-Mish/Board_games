from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Game, Category, Description
from .serializers import GameRequestSerializer, GameResponseSerializer, CategoryResponseSerializer


class GameAPIView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    view_permissions = ('game.view_game', 'game.view_description', 'game.view_category')
    add_permissions = ('game.add_game', 'game.add_description', *view_permissions)

    @method_decorator(permission_required(perm=view_permissions, raise_exception=True))
    @swagger_auto_schema(responses={200: GameResponseSerializer(many=True)})
    def get(self, request):
        queryset = Game.objects.all().order_by('-id')
        return Response(data=GameResponseSerializer(queryset, many=True).data,
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
    permission_classes = (IsAuthenticated,)
    view_permissions = ('game.view_category',)
    add_permissions = ('game.add_game', 'game.add_description', *view_permissions)

    @method_decorator(permission_required(perm=view_permissions, raise_exception=True))
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
