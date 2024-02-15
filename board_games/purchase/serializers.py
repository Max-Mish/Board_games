from django.core.validators import MinValueValidator
from rest_framework import serializers


class ItemPaymentData(serializers.Serializer):
    booking_id = serializers.IntegerField()
    price = serializers.DecimalField(min_value=0,
                                     max_digits=11,
                                     decimal_places=2,
                                     validators=[MinValueValidator(0, message='Insufficient Funds')],
                                     )

    def to_internal_value(self, data):
        if 'offer_uuid' in data.keys():
            data['item_uuid'] = data['offer_uuid']
            del data['offer_uuid']
        return super().to_internal_value(data)


class PurchaseItemsSerializer(serializers.Serializer):
    payment_types = ('bank_card', 'yoo_money', 'sberbank', 'qiwi', 'from_balance')
    payment_services = ('yookassa', 'from_balance')

    payment_type = serializers.ChoiceField(choices=payment_types)
    payment_service = serializers.ChoiceField(choices=payment_services)
    user_uuid_to = serializers.UUIDField(required=False)
    items_payment_data = ItemPaymentData(many=True)
    return_url = serializers.URLField()

    supported_currencies = ('RUB',)
    currency = serializers.ChoiceField(choices=supported_currencies)
    price_with_commission = serializers.DecimalField(min_value=0,
                                                     max_digits=11,
                                                     decimal_places=2,
                                                     validators=[MinValueValidator(0, message='Insufficient Funds')],
                                                     )
