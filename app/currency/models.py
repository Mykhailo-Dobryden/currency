from django.db import models
from django.utils.translation import gettext_lazy as _

from currency.choices import CurrencyTypeChoices


class Rate(models.Model):
    buy = models.DecimalField(_('Buy'), max_digits=6, decimal_places=2)
    sell = models.DecimalField(_('Sell'), max_digits=6, decimal_places=2)
    created = models.DateTimeField(_('Created'), auto_now_add=True, blank=True, null=True)
    currency_type = models.SmallIntegerField(
        _('Currency Type'),
        choices=CurrencyTypeChoices.choices,
        default=CurrencyTypeChoices.USD
    )
    source = models.CharField(_('Source'), max_length=255)

    class Meta:
        verbose_name = 'Rate'
        verbose_name_plural = 'Rates'

    def __str__(self):
        return f'{self.get_currency_type_display()} - {self.created.strftime("%d.%m.%Y %H:%M")}'


class ContactUs(models.Model):
    created = models.DateTimeField(_('Created'), auto_now_add=True, blank=True, null=True)
    name = models.CharField(_('Name'), max_length=64, blank=True, null=True)
    email_from = models.EmailField(_('E-mail From'), max_length=128)
    subject = models.CharField(_('Subject'), max_length=256)
    body = models.CharField(_('Body'), max_length=250, blank=True, null=True)

    class Meta:
        verbose_name = 'Contact Us'
        verbose_name_plural = 'Contact Us'

    def __str__(self):
        return self.subject


class Source(models.Model):
    source_url = models.URLField(_('Source Url'), max_length=255)
    name = models.CharField(_('Name'), max_length=64)
    created = models.DateTimeField(_('Created'), auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.name


class RequestResponseLog(models.Model):
    created = models.DateTimeField(_('Created'), auto_now_add=True, blank=True, null=True)
    path = models.CharField(_('Path'), max_length=255)
    request_method = models.CharField(_('Request Method'), max_length=10)
    time = models.DecimalField(_('Response Time'), max_digits=10, decimal_places=7)

    class Meta:
        verbose_name = 'Request Response Log'
        verbose_name_plural = 'Request Response Logs'
