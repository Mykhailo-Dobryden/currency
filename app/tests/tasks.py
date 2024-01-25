from unittest.mock import MagicMock

from currency.choices import CurrencyTypeChoices
from currency.constants import (PRIVATBANK_CODE_NAME,
                                MONOBANK_CODE_NAME,
                                NBU_CODE_NAME)
from currency.tasks import (parse_privatbank,
                            parse_monobank,
                            parse_nbu)
from currency.models import Rate, Source


def test_parse_privatbank(mocker):
    initial_count = Rate.objects.count()

    privatbank_data = [
        {"ccy": "EUR", "base_ccy": "UAH", "buy": "40.70000", "sale": "41.70000"},
        {"ccy": "USD", "base_ccy": "UAH", "buy": "37.40000", "sale": "38.00000"},
        {"ccy": "PLN", "base_ccy": "UAH", "buy": "15.40000", "sale": "16.00000"}
    ]
    request_get_mock = mocker.patch(
        'requests.get',
        return_value=MagicMock(json=lambda: privatbank_data),
    )
    parse_privatbank()

    assert Rate.objects.count() == initial_count + 2
    assert request_get_mock.call_count == 1
    assert request_get_mock.call_args[0][0] == 'https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=5'


def test_parse_privatbank_prevent_duplicates(mocker):
    privatbank_data = [
        {"ccy": "EUR", "base_ccy": "UAH", "buy": "40.80000", "sale": "41.80000"},
        {"ccy": "USD", "base_ccy": "UAH", "buy": "37.50000", "sale": "38.10000"},
        {"ccy": "PLN", "base_ccy": "UAH", "buy": "37.50000", "sale": "38.10000"},
    ]
    requests_get_mock = mocker.patch(
        'requests.get',
        return_value=MagicMock(json=lambda: privatbank_data)
    )
    source = Source.objects.get(code_name=PRIVATBANK_CODE_NAME)
    Rate.objects.create(source=source, buy="40.80", sell="41.80", currency_type=CurrencyTypeChoices.EUR)
    Rate.objects.create(source=source, buy="37.50", sell="38.10", currency_type=CurrencyTypeChoices.USD)
    initial_count = Rate.objects.count()

    parse_privatbank()

    assert Rate.objects.count() == initial_count
    assert requests_get_mock.call_count == 1


def test_parse_monobank(mocker):
    initial_count = Rate.objects.count()

    monobank_data = [
        {"currencyCodeA": 840, "currencyCodeB": 980, "date": 1706108173, "rateBuy": 37.43, "rateSell": 38.01},
        {"currencyCodeA": 978, "currencyCodeB": 980, "date": 1706108173, "rateBuy": 40.73, "rateSell": 41.50},
        {"currencyCodeA": 978, "currencyCodeB": 840, "date": 1706108173, "rateBuy": 1.08, "rateSell": 1.09},
    ]

    request_get_mock = mocker.patch(
        'requests.get',
        return_value=MagicMock(json=lambda: monobank_data)
    )

    parse_monobank()

    assert Rate.objects.count() == initial_count + 2
    assert request_get_mock.call_count == 1
    assert request_get_mock.call_args[0][0] == 'https://api.monobank.ua/bank/currency'


def test_parse_monobank_prevent_duplicates(mocker):
    monobank_data = [
        {"currencyCodeA": 840, "currencyCodeB": 980, "date": 1706108173, "rateBuy": 37.43, "rateSell": 38.01},
        {"currencyCodeA": 978, "currencyCodeB": 980, "date": 1706108173, "rateBuy": 40.73, "rateSell": 41.50},
    ]

    request_get_mock = mocker.patch(
        'requests.get',
        return_value=MagicMock(json=lambda: monobank_data)
    )

    source = Source.objects.get(code_name=MONOBANK_CODE_NAME)
    Rate.objects.create(source=source, buy="37.43", sell="38.01", currency_type=CurrencyTypeChoices.USD)
    Rate.objects.create(source=source, buy="40.73", sell="41.50", currency_type=CurrencyTypeChoices.EUR)
    initial_count = Rate.objects.count()

    parse_monobank()

    assert request_get_mock.call_count == 1
    assert Rate.objects.count() == initial_count


def test_parse_nbu(mocker):
    initial_count = Rate.objects.count()

    nbu_data = [
        {"r030": 840, "txt": "Долар США", "rate": 37.5252, "cc": "USD", "exchangedate": "25.01.2024"},
        {"r030": 978, "txt": "Євро", "rate": 40.8837, "cc": "EUR", "exchangedate": "25.01.2024"},
        {"r030": 975, "txt": "Болгарський лев", "rate": 20.9042, "cc": "BGN", "exchangedate": "25.01.2024"},
    ]

    request_get_mock = mocker.patch(
        'requests.get',
        return_value=MagicMock(json=lambda: nbu_data)
    )

    parse_nbu()
    assert Rate.objects.count() == initial_count + 2
    assert request_get_mock.call_count == 1


def test_parse_nbu_prevent_duplicates(mocker):
    nbu_data = [
        {"r030": 840, "txt": "Долар США", "rate": 37.5252, "cc": "USD", "exchangedate": "25.01.2024"},
        {"r030": 978, "txt": "Євро", "rate": 40.8837, "cc": "EUR", "exchangedate": "25.01.2024"},
    ]

    request_get_mock = mocker.patch(
        'requests.get',
        return_value=MagicMock(json=lambda: nbu_data)
    )

    source = Source.objects.get(code_name=NBU_CODE_NAME)
    Rate.objects.create(source=source, buy="37.52", sell="37.52", currency_type=CurrencyTypeChoices.USD)
    Rate.objects.create(source=source, buy="40.88", sell="40.88", currency_type=CurrencyTypeChoices.EUR)
    initial_count = Rate.objects.count()

    parse_nbu()

    assert request_get_mock.call_count == 1
    assert Rate.objects.count() == initial_count
