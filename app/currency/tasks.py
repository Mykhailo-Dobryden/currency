from time import sleep
import requests
from bs4 import BeautifulSoup

from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task

from currency.choices import CurrencyTypeChoices
from currency.constants import (PRIVATBANK_CODE_NAME, MONOBANK_CODE_NAME,
                                NBU_CODE_NAME, SENSEBANK_CODE_NAME, currency_codes_iso4217)
from currency.models import Source, Rate
from currency.utils import to_2_places_decimal


@shared_task(autoretry_for=(ConnectionError,), retry_kwargs={
    'max_retries': 5
})
def send_email_in_background(subject, body):

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
        currency_codes_iso4217['USD']: CurrencyTypeChoices.USD,
        currency_codes_iso4217['EUR']: CurrencyTypeChoices.EUR
    }

    for rate in rates:
        currency_type = rate['currencyCodeA']

        # we need only UAH to USD and UAH to EUR, otherwise we'll receive an EUR to USD rate also and vice versa
        # look at api.monobank.ua/bank/currency
        if currency_type not in available_currency_types or rate['currencyCodeB'] != currency_codes_iso4217['UAH']:
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

    source, _ = Source.objects.get_or_create(code_name=NBU_CODE_NAME,
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


@shared_task
def parse_sensebank():
    sensebank_url = 'https://sensebank.ua/currency-exchange'

    request_headers = {"Accept": "*/*",
                       "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 "
                                     "(KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"}

    web_response = requests.get(sensebank_url, headers=request_headers)
    web_response.raise_for_status()

    html_content = web_response.text

    # Parse html content with BeautifulSoup
    parsed_html = BeautifulSoup(html_content, 'html.parser')

    # Find the exchange rate items in the parsed HTML
    sensebank_exchange_rate_items = parsed_html.find(
        'div', class_="exchange-rate-tabs__items").find_all(
        'div', "exchange-rate-tabs__item"
    )

    # Get or create the Source
    source, _ = Source.objects.get_or_create(code_name=SENSEBANK_CODE_NAME,
                                             defaults={'name': 'SenseBank',
                                                       'source_url': sensebank_url})

    available_currency_types = {
        'USD': CurrencyTypeChoices.USD,
        'EUR': CurrencyTypeChoices.EUR
    }

    # Initialize an empty list to store the dictionaries of parsed rates
    rates = []

    # Iterate over the exchange rate items  and parse the rate for each currency_type
    for rate_item in sensebank_exchange_rate_items:

        # Initialize an empty dictionary to store the parsed rate for each single currency_type
        rate = {}

        currency_type = rate_item.find('h2').text.split('/')[0].strip()

        # Get buy/sell values for specific currency_type of the rate_item
        rate_tab_info = rate_item.find_all('div', class_="exchange-rate-tabs__info-item")

        # Iterate over the rate_tab_info and parse the buy/sell values from item
        for info in rate_tab_info:
            rate['currency_type'] = currency_type
            parsed_info_list = info.text.replace('\n', ' ').strip().split()

            if parsed_info_list[0] == 'Купівля':
                buy_rate = parsed_info_list[1]
                rate['buy'] = buy_rate

            elif parsed_info_list[0] == 'Продаж':
                sell_rate = parsed_info_list[1]
                rate['sell'] = sell_rate

        rates.append(rate)

        # Iterate over the parsed rates and create the Rate object if it doesn't exist
        for rate in rates:
            currency_type = rate['currency_type']

            if currency_type not in available_currency_types:
                continue

            # Convert buy/sell values to Decimal with 2 places
            buy = to_2_places_decimal(rate['buy'])
            sell = to_2_places_decimal(rate['sell'])

            # Convert currency_type to the CurrencyTypeChoices
            currency_type = available_currency_types[currency_type]

            # Get the last Rate object for specific currency_type and source
            last_rate = Rate.objects.filter(source=source, currency_type=currency_type).order_by('-created').first()

            # Create the Rate object if it doesn't exist or if the buy/sell values are different
            if last_rate is None or last_rate.buy != buy or last_rate.sell != sell:
                Rate.objects.create(
                    buy=buy,
                    sell=sell,
                    currency_type=currency_type,
                    source=source
                )
