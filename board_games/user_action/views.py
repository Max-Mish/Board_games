from datetime import date

from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Booking, Vote
from .serializers import BookingRequestSerializer, BookingResponseSerializer, VoteRequestSerializer, \
    VoteResponseSerializer


class BookingAPIView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    view_permissions = (
        'user_action.view_booking', 'game.view_game', 'game.view_description', 'game.view_category',
        'authentication.view_profile_info'
    )
    add_permissions = ('user_action.add_booking', *view_permissions)

    @method_decorator(permission_required(perm=view_permissions, raise_exception=True))
    @swagger_auto_schema(responses={200: BookingResponseSerializer(many=True)})
    def get(self, request):
        queryset = Booking.objects.all().order_by('-opening_date')
        return Response(data=BookingResponseSerializer(queryset, many=True).data, status=status.HTTP_200_OK)

    @method_decorator(permission_required(perm=add_permissions, raise_exception=True))
    @swagger_auto_schema(request_body=BookingRequestSerializer(), responses={201: BookingResponseSerializer()})
    def post(self, request):
        serializer = BookingRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user_id = request.user.pk
        booking = Booking(user_id=user_id, game_id=data['game_id'], return_date=data['return_date'])
        booking.save()
        return Response(
            data=BookingResponseSerializer(booking).data, status=status.HTTP_201_CREATED
        )


class BookingFilteredAPIView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    view_permissions = (
        'user_action.view_booking', 'user_action.view_filtered_booking', 'game.view_game', 'game.view_description',
        'game.view_category', 'authentication.view_profile_info'
    )

    @method_decorator(permission_required(perm=view_permissions, raise_exception=True))
    @swagger_auto_schema(responses={200: BookingResponseSerializer(many=True)})
    def get(self, request):
        queryset = Booking.objects.all().order_by('-opening_date')
        queryset_filtered = [booking for booking in queryset if
                             (booking.closing_date and booking.return_date < booking.closing_date) or (
                                     not booking.closing_date and booking.return_date < date.today())]

        return Response(data=BookingResponseSerializer(queryset_filtered, many=True).data, status=status.HTTP_200_OK)


class VoteAPIView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    view_permissions = ('user_action.view_vote', 'authentication.view_profile_info')
    add_permissions = ('user_action.add_vote', *view_permissions)

    @method_decorator(permission_required(perm=view_permissions, raise_exception=True))
    @swagger_auto_schema(responses={200: VoteResponseSerializer(many=True)})
    def get(self, request):
        queryset = Vote.objects.all().order_by('-id')
        return Response(data=VoteResponseSerializer(queryset, many=True).data, status=status.HTTP_200_OK)

    @method_decorator(permission_required(perm=add_permissions, raise_exception=True))
    @swagger_auto_schema(request_body=VoteRequestSerializer(), responses={201: VoteResponseSerializer()})
    def post(self, request):
        serializer = VoteRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        votes = [Vote(choice_id=choice, user_id=data['user_id']).save() for choice in data['choice_ids']]
        queryset = Vote.objects.filter(choice_id__in=data['choice_ids'], user_id=data['user_id'])

        return Response(
            data=VoteResponseSerializer(queryset, many=True).data, status=status.HTTP_201_CREATED
        )
