from time import sleep
import requests

from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task

from currency.choices import CurrencyTypeChoices
from currency.constants import PRIVATBANK_CODE_NAME, MONOBANK_CODE_NAME
from currency.models import Source, Rate
from currency.utils import to_2_places_decimal


@shared_task(autoretry_for=(ConnectionError,), retry_kwargs={
    'max_retries': 5
})
def send_email_in_background(subject, body):

    sleep(10)
    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [settings.DEFAULT_FROM_EMAIL],
        fail_silently=False,
    )


@shared_task
def parse_privatbank():
    url = 'https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=5'
    response = requests.get(url)
    response.raise_for_status()  # raise exception if status code is not 200

    source, _ = Source.objects.get_or_create(code_name=PRIVATBANK_CODE_NAME,
                                             defaults={'name': 'PrivatBank',
                                                       'source_url': url})

    rates = response.json()

    available_currency_types = {
        'USD': CurrencyTypeChoices.USD,
        'EUR': CurrencyTypeChoices.EUR
    }

    for rate in rates:
        currency_type = rate['ccy']

        if currency_type not in available_currency_types:
            continue

        buy = to_2_places_decimal(rate['buy'])
        sell = to_2_places_decimal(rate['sale'])

        currency_type = available_currency_types[currency_type]

        last_rate = Rate.objects.filter(source=source, currency_type=currency_type).order_by('-created').first()

        if last_rate is None or last_rate.buy != buy or last_rate.sell != sell:
            Rate.objects.create(
                buy=buy,
                sell=sell,
                currency_type=currency_type,
                source=source
            )


@shared_task
def parse_monobank():
    url = 'https://api.monobank.ua/bank/currency'
    response = requests.get(url)
    response.raise_for_status()  # raise exception if status code is not 200

    source, _ = Source.objects.get_or_create(code_name=MONOBANK_CODE_NAME,
                                             defaults={'name': 'MonoBank',
                                                       'source_url': url})

    rates = response.json()

    available_currency_types = {
        840: CurrencyTypeChoices.USD,
        978: CurrencyTypeChoices.EUR
    }

    for rate in rates:
        currency_type = rate['currencyCodeA']

        if currency_type not in available_currency_types or rate['currencyCodeB'] != 980:
            continue

        buy = to_2_places_decimal(rate['rateBuy'])
        sell = to_2_places_decimal(rate['rateSell'])



        currency_type = available_currency_types[currency_type]

        last_rate = Rate.objects.filter(source=source, currency_type=currency_type).order_by('-created').first()

        if last_rate is None or last_rate.buy != buy or last_rate.sell != sell:
            Rate.objects.create(
                buy=buy,
                sell=sell,
                currency_type=currency_type,
                source=source
            )


@shared_task
def parse_nbu():
    url = 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json'
    response = requests.get(url)
    response.raise_for_status()

    source, _ = Source.objects.get_or_create(code_name='nbu',
                                             defaults={'name': 'NBU',
                                                       'source_url': url})

    rates = response.json()

    available_currency_types = {
        'USD': CurrencyTypeChoices.USD,
        'EUR': CurrencyTypeChoices.EUR
    }

    for rate in rates:
        currency_type = rate['cc']

        if currency_type not in available_currency_types:
            continue

        buy = to_2_places_decimal(rate['rate'])
        sell = to_2_places_decimal(rate['rate'])

        currency_type = available_currency_types[currency_type]

        last_rate = Rate.objects.filter(source=source, currency_type=currency_type).order_by('-created').first()

        if last_rate is None or last_rate.buy != buy or last_rate.sell != sell:
            Rate.objects.create(
                buy=buy,
                sell=sell,
                currency_type=currency_type,
                source=source
            )

