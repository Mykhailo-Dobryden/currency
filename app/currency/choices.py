from django.db import models


class CurrencyTypeChoices(models.IntegerChoices):
    USD = 1, 'USD'
    EUR = 2, 'EUR'
