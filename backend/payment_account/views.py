import rollbar
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers
from rest_framework import status, generics, viewsets
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from purchase.models import Invoice
from .models import Account, BalanceChange, PaymentCommission
from .serializers import CalculateCommissionSerializer, BalanceIncreaseSerializer, AccountSerializer, UUIDSerializer, \
    BalanceSerializer, YookassaPaymentAcceptanceSerializer, PaymentServiceSerializer
from .services import PaymentCalculation, request_balance_deposit_url, check_yookassa_response, \
    proceed_payment_response


class PaymentServicesAPIView(generics.GenericAPIView):
    @swagger_auto_schema(responses={200: PaymentServiceSerializer(many=True)})
    def get(self, request):
        queryset = PaymentCommission.objects.all().order_by('-id')
        return Response(data=PaymentServiceSerializer(queryset, many=True).data, status=status.HTTP_200_OK)


class CalculatePaymentCommissionAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
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
    permission_classes = (IsAuthenticated,)
    serializer_class = BalanceIncreaseSerializer

    @swagger_auto_schema(request_body=BalanceIncreaseSerializer(),
                         responses={201: 'Confirmation url returned'})
    def post(self, request, *args, **kwargs):
        serializer = BalanceIncreaseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        data['user_uuid'] = request.user.pk

        confirmation_url = request_balance_deposit_url(request, data)
        return Response(
            {'confirmation_url': confirmation_url},
            status=status.HTTP_201_CREATED,
        )


class UserCreateAPIView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(responses={200: AccountSerializer()})
    def post(self, request):
        user_uuid = request.user.pk
        if Account.objects.filter(user_uuid=user_uuid).exists():
            return Response(
                {'error': 'A user with this UUID already exists'},
                status=status.HTTP_409_CONFLICT,
            )
        account = Account.objects.create(user_uuid=user_uuid)
        return Response(data=AccountSerializer(account).data, status=status.HTTP_201_CREATED)


class BalancesAPIView(generics.GenericAPIView):
    permission_classes = (IsAdminUser,)

    @swagger_auto_schema(request_body=UUIDSerializer(), responses={200: BalanceSerializer(many=True)})
    def post(self, request):
        serializer = UUIDSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        uuid_list = data['uuid_list']
        balance_list = list(Account.objects.filter(user_uuid__in=uuid_list))

        return Response(BalanceSerializer(balance_list, many=True).data)


class BalanceAPIView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(responses={200: BalanceSerializer()})
    def get(self, request):
        user_uuid = request.user.pk
        account = get_object_or_404(Account, user_uuid=user_uuid)
        return Response(BalanceSerializer(account).data)


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
        rollbar.report_message(
            'Payment proceed gone wrong',
            'warning',
        )
        return Response(404)


class CallbackView(generics.GenericAPIView):
    class CallbackSerializer(serializers.Serializer):
        purchase = serializers.CharField(required=True)

    @swagger_auto_schema(responses={200: serializers.Serializer()}, query_serializer=CallbackSerializer())
    def get(self, request):
        serializer = self.CallbackSerializer(request.query_params)
        purchase = serializer.data.get('purchase')

        balance_change_id, invoice_id = purchase.split('_')

        balance_change = BalanceChange.objects.get(id=balance_change_id)
        balance_change.is_accepted = True
        balance_change.save()

        if invoice_id:
            invoice = Invoice.objects.get(invoice_id=invoice_id)
            invoice.is_paid = True
            invoice.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
