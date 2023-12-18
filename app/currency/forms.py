from django import forms
from currency.models import Source, Rate, ContactUs
from django.utils.translation import gettext_lazy as _


class SourceCreateForm(forms.ModelForm):
    class Meta:
        model = Source
        fields = ('name', 'source_url')

        labels = {
            'name': _('Name'),
            'source_url': _('Source URL'),
        }


class RateCreateForm(forms.ModelForm):
    class Meta:
        model = Rate
        fields = ('buy', 'sell', 'currency_type', 'source')

        labels = {
            'buy': _('Buy'),
            'sell': _('Sell'),
            'currency_type': _('Currency Type'),
            'source': _('Currency Supplier'),
        }


class ContactUsCreateForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ('email_from', 'name', 'subject', 'body', )

        labels = {
            'email_from': _('E-mail'),
            'name': _('Name'),
            'subject': _('Subject'),
            'body': _('Message'),
        }
