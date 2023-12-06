from django import forms
from currency.models import Source, Rate, ContactUs


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


class ContactUsCreateForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ('email_from', 'name', 'subject', 'body', )

        labels = {
            'email_from': 'E-mail',
            'name': 'Name',
            'subject': 'Subject',
            'body': 'Message',
        }
