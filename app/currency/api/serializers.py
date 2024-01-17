from rest_framework import serializers

from currency.models import Rate, Source


class RateSerializer(serializers.ModelSerializer):
    currency_type = serializers.CharField(source='get_currency_type_display')

    class Meta:
        model = Rate
        fields = ('id', 'created', 'currency_type', 'sell', 'buy', 'source')


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ('id', 'name', 'source_url', 'code_name')
