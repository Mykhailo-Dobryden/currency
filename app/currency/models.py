from django.db import models
from django.utils.translation import gettext_lazy as _
from django.templatetags.static import static
from currency.choices import CurrencyTypeChoices


def source_directory_path(instance, filename):
    return f'logos_source/{instance.name}/{filename}'


class Rate(models.Model):
    buy = models.DecimalField(_('Buy'), max_digits=6, decimal_places=2)
    sell = models.DecimalField(_('Sell'), max_digits=6, decimal_places=2)
    created = models.DateTimeField(_('Created'), auto_now_add=True, blank=True, null=True)
    currency_type = models.SmallIntegerField(
        _('Currency Type'),
        choices=CurrencyTypeChoices.choices,
        default=CurrencyTypeChoices.USD
    )
    source = models.ForeignKey('currency.Source',
                               on_delete=models.CASCADE,
                               verbose_name=_('Source'),
                               related_name='rates', )

    class Meta:
        verbose_name = _('Rate')
        verbose_name_plural = _('Rates')

    def __str__(self):
        return (f'{self.source}: {self.get_currency_type_display()}, {self.buy}/{self.sell} '
                f'{self.created.strftime("%d.%m.%Y %H:%M")}')


class ContactUs(models.Model):
    created = models.DateTimeField(_('Created'), auto_now_add=True, blank=False, null=True)
    name = models.CharField(_('Name'), max_length=64, blank=False, null=True)
    email_from = models.EmailField(_('E-mail From'), max_length=128)
    subject = models.CharField(_('Subject'), max_length=256)
    body = models.CharField(_('Body'), max_length=250, blank=False, null=True)

    class Meta:
        verbose_name = _('Contact Us')
        verbose_name_plural = _('Contact Us')

    def __str__(self):
        return self.subject


class Source(models.Model):
    source_url = models.URLField(_('Source Url'), max_length=255)
    name = models.CharField(_('Name'), max_length=64)
    created = models.DateTimeField(_('Created'), auto_now_add=True, blank=True, null=True)
    logo = models.FileField(_('Logo'), upload_to=source_directory_path, blank=True, null=True)
    code_name = models.CharField(_('Code name'), max_length=64, unique=True)

    class Meta:
        verbose_name = _('Source')
        verbose_name_plural = _('Sources')

    def __str__(self):
        return self.name

    @property
    def logo_url(self):
        if self.logo:
            return self.logo.url
        return static('img/default_source_logo.png')


class RequestResponseLog(models.Model):
    created = models.DateTimeField(_('Created'), auto_now_add=True, blank=True, null=True)
    path = models.CharField(_('Path'), max_length=255)
    request_method = models.CharField(_('Request Method'), max_length=10)
    time = models.DecimalField(_('Response Time'), max_digits=10, decimal_places=7)

    class Meta:
        verbose_name = _('Request Response Log')
        verbose_name_plural = _('Request Response Logs')
