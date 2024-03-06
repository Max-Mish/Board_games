from datetime import datetime

from rest_framework import serializers


class UTCDateField(serializers.DateField):
    def to_representation(self, value):
        return value.strftime('%a, %d %b %Y')

    def to_internal_value(self, data):
        try:
            return datetime.strptime(data, "%a %b %d %Y").date()
        except ValueError:
            raise serializers.ValidationError("Invalid date format, should be YYYY-MM-DD")
