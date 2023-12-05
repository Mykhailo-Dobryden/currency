from django.db import models
from currency.choices import CurrencyTypeChoices


class Rate(models.Model):
    buy = models.DecimalField(max_digits=6, decimal_places=2)
    sell = models.DecimalField(max_digits=6, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    currency_type = models.SmallIntegerField(
        choices=CurrencyTypeChoices.choices,
        default=CurrencyTypeChoices.USD
    )
    source = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.get_currency_type_display()} - {self.created.strftime("%d.%m.%Y %H:%M")}'


class ContactUs(models.Model):
    email_from = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.subject


class Source(models.Model):
    source_url = models.URLField(max_length=255)
    name = models.CharField(max_length=64)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.name
