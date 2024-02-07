from datetime import date

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, generics
from rest_framework.response import Response

from .models import Booking, Vote
from .serializers import BookingRequestSerializer, BookingResponseSerializer, VoteRequestSerializer, \
    VoteResponseSerializer


class BookingAPIView(generics.GenericAPIView):
    @swagger_auto_schema(responses={200: BookingResponseSerializer(many=True)})
    def get(self, request):
        queryset = Booking.objects.all().order_by('-opening_date')
        return Response(data=BookingResponseSerializer(queryset, many=True).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=BookingRequestSerializer(), responses={201: BookingResponseSerializer()}
    )
    def post(self, request):
        serializer = BookingRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # data = serializer.validated_data
        #
        # booking = Booking(user_id=data['user_id'], game_id=data['game_id'], opening_date=data['opening_date'],
        #                   return_date=data['return_date'])
        # booking.save()
        return Response(
            data=serializer.data, status=status.HTTP_201_CREATED
        )


class BookingFilteredAPIView(generics.GenericAPIView):
    @swagger_auto_schema(responses={200: BookingResponseSerializer(many=True)})
    def get(self, request):
        queryset = Booking.objects.all().order_by('-opening_date')
        queryset_filtered = [booking for booking in queryset if
                             (booking.closing_date and booking.return_date < booking.closing_date) or (
                                     not booking.closing_date and booking.return_date < date.today())]

        return Response(data=BookingResponseSerializer(queryset_filtered, many=True).data, status=status.HTTP_200_OK)


class VoteAPIView(generics.GenericAPIView):
    @swagger_auto_schema(responses={200: VoteResponseSerializer(many=True)})
    def get(self, request):
        queryset = Vote.objects.all().order_by('-id')
        return Response(data=VoteResponseSerializer(queryset, many=True).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=VoteRequestSerializer(), responses={201: VoteResponseSerializer()}
    )
    def post(self, request):
        serializer = VoteRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        votes = [Vote(choice_id=choice, user_id=data['user_id']).save() for choice in data['choice_ids']]
        queryset = Vote.objects.filter(choice_id__in=data['choice_ids'], user_id=data['user_id'])

        return Response(
            data=VoteResponseSerializer(queryset, many=True).data, status=status.HTTP_201_CREATED
        )
