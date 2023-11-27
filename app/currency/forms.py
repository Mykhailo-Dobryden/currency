from django import forms
from currency.models import Source, Rate


class SourceCreateForm(forms.ModelForm):
    class Meta:
        model = Source
        fields = ('name', 'source_url')


class RateCreateForm(forms.ModelForm):
    class Meta:
        model = Rate
        fields = ('buy', 'sell', 'currency_type', 'source')

        labels = {
            'source': 'Currency Supplier'
        }
