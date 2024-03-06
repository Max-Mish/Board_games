from rest_framework import serializers

from store.models import Store


class StoreRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['address', 'open_hours', 'email', 'phone_number', 'manager']


class StoreResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'
