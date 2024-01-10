from django import forms
from currency.models import Source, Rate, ContactUs
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field


class SourceCreateForm(forms.ModelForm):
    class Meta:
        model = Source
        fields = ('name', 'source_url', 'logo')

        labels = {
            'name': _('Name'),
            'source_url': _('Source URL'),
            'logo': _('Logo'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(Field('name', placeholder='Name'), css_class='form-group col-md-4'),
                Column(Field('source_url', placeholder='Source URL'), css_class='form-group col-md-4'),
                css_class='form-row'),
            Row(
                Column(Field('logo', placeholder='Logo'), css_class='form-group col-md-6'),
                css_class='form-row'),
        )
        self.helper.add_input(Submit('submit', _('Submit')))


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(Field('buy', placeholder='Buy'),
                       css_class='form-group col-md-6'),
                Column(Field('sell', placeholder='Sell'),
                       css_class='form-group col-md-6'),
                css_class='form-row'),
            Row(
                Column(Field('currency_type', placeholder='Currency Type'),
                       css_class='form-group col-md-6'),
                Column(Field('source', placeholder='Currency Supplier'),
                       css_class='form-group col-md-6'),
                css_class='form-row'),
        )
        self.helper.add_input(Submit('submit', _('Submit')))


class ContactUsCreateForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ('email_from', 'name', 'subject', 'body',)

        labels = {
            'email_from': _('E-mail'),
            'name': _('Name'),
            'subject': _('Subject'),
            'body': _('Message'),
        }

        widgets = {
            'body': forms.Textarea(attrs={'rows': 5, 'maxlength': 250}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(Field('email_from', placeholder='E-mail'), css_class='form-group col-md-4'),
                Column(Field('name', placeholder='Name'), css_class='form-group col-md-4'),
                Column(Field('subject', placeholder='Subject'), css_class='form-group col-md-4'),
                css_class='form-row'),
            Row(
                Column(Field('body', placeholder='Message'), css_class='form-group col-md-12'),
                css_class='form-row'),
        )
        self.helper.add_input(Submit('submit', _('Submit')))


# class RateFilterFormHelper(FormHelper):
#     form_method = "GET"
#     layout = Layout(
#         Row(
#             Column('buy', css_class='form-group col-md-3 mb-0'), css_class='form-row'
#         ),
#         Row(
#             Column('sell', css_class='form-group col-md-3 mb-0'), css_class='form-row'
#         ),
#         Row(Column('currency_type', css_class='form-group col-md-3 mb-0'),
#             Column('source', css_class='form-group col-md-3 mb-0'), css_class='form-row'
#             ),
#         Submit('submit', _('Search'))
#     )


# class SourceFilterFormHelper(FormHelper):
#     form_method = 'GET'
#
#     layout = Layout(
#         Row(Column('name', css_class='form-group col-md-3 mb-0'),
#             Column('source_url', css_class='form-group col-md-3 mb-0'), css_class='form-row'
#             ),
#     )
#     submit = Submit('submit', _('Search'), css_class='btn btn-primary')
