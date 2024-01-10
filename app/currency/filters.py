
import django_filters
from django.utils.translation import gettext_lazy as _

from currency.models import Rate, ContactUs, Source


from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Row, Column, Field


class RateFilter(django_filters.FilterSet):
    class Meta:
        model = Rate
        fields = {
            'buy': ['exact', 'gt', 'gte', 'lt', 'lte'],
            'sell': ['exact', 'gt', 'gte', 'lt', 'lte'],
            'currency_type': ['exact'],
            'source': ['exact'],
        }


class ContactUsFilter(django_filters.FilterSet):
    class Meta:
        model = ContactUs
        fields = {
            'name': ['iexact'],
            'email_from': ['iexact'],
            'subject': ['iexact'],
        }


class SourceFilter(django_filters.FilterSet):

    class Meta:
        model = Source
        fields = {
            'name': ['iexact'],
            'source_url': ['icontains'],
        }