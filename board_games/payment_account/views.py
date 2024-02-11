import json

import rollbar
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, generics, viewsets
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.response import Response

from .models import Account
from .serializers import CalculateCommissionSerializer, BalanceIncreaseSerializer, AccountSerializer, UUIDSerializer, \
    BalanceSerializer, YookassaPaymentAcceptanceSerializer
from .services import payment_acceptance, PaymentCalculation, request_balance_deposit_url, check_yookassa_response, \
    proceed_payment_response


class CreatePaymentAcceptanceAPIView(CreateAPIView):

    @swagger_auto_schema(
        responses={200: 'Payment succeeded', 404: 'Payment canceled'})
    def post(self, request, *args, **kwargs):
        response = json.loads(request.body)

        if payment_acceptance(response):
            return Response(200)
        return Response(404)


class CalculatePaymentCommissionAPIView(CreateAPIView):
    serializer_class = CalculateCommissionSerializer

    @swagger_auto_schema(request_body=CalculateCommissionSerializer(),
                         responses={201: 'Amount with commission returned'})
    def post(self, request, *args, **kwargs):
        serializer = CalculateCommissionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        amount_with_commission = PaymentCalculation(
            payment_type=data['payment_type'],
            payment_service=data['payment_service'],
            payment_amount=data['payment_amount'],
        ).calculate_payment_with_commission()

        return Response({'amount with commission': amount_with_commission})


class BalanceIncreaseAPIView(CreateAPIView):
    serializer_class = BalanceIncreaseSerializer

    @swagger_auto_schema(request_body=BalanceIncreaseSerializer(),
                         responses={201: 'Confirmation url returned'})
    def post(self, request, *args, **kwargs):
        serializer = BalanceIncreaseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        confirmation_url = request_balance_deposit_url(data)
        return Response(
            {'confirmation_url': confirmation_url},
            status=status.HTTP_201_CREATED,
        )


class UserCreateAPIView(generics.GenericAPIView):
    @swagger_auto_schema(request_body=AccountSerializer(), responses={200: AccountSerializer()})
    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        uuid = data.get('user_uuid')
        if Account.objects.filter(user_uuid=uuid).exists():
            return Response(
                {'error': 'A user with this UUID already exists'},
                status=status.HTTP_409_CONFLICT,
            )
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class BalanceViewSet(viewsets.ViewSet):
    @swagger_auto_schema(responses={200: BalanceSerializer()})
    def retrieve(self, request, user_uuid=None):
        account = get_object_or_404(Account, user_uuid=user_uuid)
        return Response(BalanceSerializer(account).data)

    @swagger_auto_schema(request_body=UUIDSerializer(), responses={200: BalanceSerializer(many=True)})
    def list(self, request):
        serializer = UUIDSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        uuid_list = data['uuid_list']
        balance_list = list(Account.objects.filter(user_uuid__in=uuid_list))

        return Response(BalanceSerializer(balance_list, many=True).data)


class YookassaPaymentAcceptanceView(viewsets.GenericViewSet):
    serializer_class = YookassaPaymentAcceptanceSerializer

    def create(self, request):
        serializer = YookassaPaymentAcceptanceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        yookassa_data = serializer.validated_data
        yookassa_object = yookassa_data.get('object_')
        yookassa_event = yookassa_data.get('event')

        if yookassa_object is None or not check_yookassa_response(yookassa_object, yookassa_event):
            rollbar.report_message(
                'Response not from yookassa.',
                'warning',
            )
            return Response(404)

        if yookassa_event == 'succeeded':
            payment_status = proceed_payment_response(
                yookassa_data,
                'yookassa',
            )
            if payment_status is True:
                return Response(200)
        return Response(404)
