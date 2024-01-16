from rest_framework import serializers

from currency.models import Rate

class RateSerializer(serializers.ModelSerializer):
    currency_type = serializers.CharField(source='get_currency_type_display')

    class Meta:
        model = Rate
        fields = ('id', 'created', 'currency_type', 'sell', 'buy', 'source')
