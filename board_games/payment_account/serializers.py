from decimal import Decimal

from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework import serializers

from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    user_uuid = serializers.UUIDField()

    class Meta:
        model = Account
        fields = ('user_uuid',)


class CalculateCommissionSerializer(serializers.Serializer):
    payment_types = ('bank_card', 'yoo_money', 'sberbank', 'qiwi', 'from_balance')
    payment_services = ('yookassa', 'from_balance')

    payment_type = serializers.ChoiceField(choices=payment_types)
    payment_service = serializers.ChoiceField(choices=payment_services)
    payment_amount = serializers.DecimalField(min_value=0,
                                              max_digits=11,
                                              decimal_places=2,
                                              validators=[MinValueValidator(0, message='Insufficient Funds')],
                                              )


class YookassaMoneySerializer(serializers.Serializer):
    supported_currencies = ('RUB',)
    currency = serializers.ChoiceField(choices=supported_currencies)
    value = serializers.DecimalField(min_value=0,
                                     max_digits=11,
                                     decimal_places=2,
                                     validators=[MinValueValidator(0, message='Insufficient Funds')],
                                     )


class BalanceIncreaseSerializer(serializers.Serializer):
    payment_types = ('bank_card', 'yoo_money', 'sberbank', 'qiwi', 'from_balance')
    payment_services = ('yookassa', 'from_balance')

    payment_type = serializers.ChoiceField(choices=payment_types)
    payment_service = serializers.ChoiceField(choices=payment_services)
    user_uuid = serializers.UUIDField()
    return_url = serializers.URLField()
    amount = YookassaMoneySerializer()


class WithdrawSerializer(serializers.Serializer):
    user_uuid = serializers.UUIDField()
    supported_currencies = ('RUB',)
    currency = serializers.ChoiceField(choices=supported_currencies)
    value = serializers.DecimalField(min_value=0,
                                     max_digits=11,
                                     decimal_places=2,
                                     validators=[
                                         MinValueValidator(
                                             Decimal(500),
                                             message=f'Should be more then {Decimal(500)}',
                                         ),
                                         MaxValueValidator(
                                             Decimal(500000),
                                             message=f'Payout service limit exceeded {Decimal(500000)}',
                                         ),
                                     ],
                                     )


class UUIDSerializer(serializers.Serializer):
    uuid_list = serializers.ListField(child=serializers.UUIDField())


class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('user_uuid', 'balance', 'balance_currency')


class YookassaPaymentBodySerializer(serializers.Serializer):
    payment_types = ('bank_card', 'yoo_money', 'sberbank', 'qiwi', 'from_balance')

    id_ = serializers.UUIDField()
    income_amount = YookassaMoneySerializer()
    amount = YookassaMoneySerializer()
    description = serializers.CharField()
    metadata = serializers.DictField()  # account_id, balance_change_id, invoice_id=None (из item_purchases)
    payment_method = serializers.ChoiceField(choices=payment_types)


class YookassaPaymentAcceptanceSerializer(serializers.Serializer):
    yookassa_payment_statuses = ['payment.succeeded', 'payment.canceled', 'payment.waiting_for_capture',
                                 'refund.succeeded', 'succeeded']

    event = serializers.ChoiceField(choices=yookassa_payment_statuses)
    object_ = YookassaPaymentBodySerializer()
