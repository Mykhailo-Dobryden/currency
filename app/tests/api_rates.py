from django.urls import reverse

from currency.models import Source, Rate


def test_get_rate_list(api_client_auth):
    response = api_client_auth.get(reverse('currency_api:rate-list'))
    assert response.status_code == 200
    assert response.json()


def test_get_rate_by_id_200(api_client_auth):
    rate = Rate.objects.create(buy=37.00, sell=38.00, source=Source.objects.first())
    response = api_client_auth.get(reverse('currency_api:rate-detail', args=(rate.id,)))
    assert response.status_code == 200
    assert response.json() == {
        'id': rate.id,
        'buy': '37.00',
        'sell': '38.00',
        'source': rate.source.id,
        'currency_type': 'USD',
        'created': rate.created.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    }


def test_post_rate_list_empty_body(api_client_auth):
    response = api_client_auth.post(reverse('currency_api:rate-list'))
    assert response.status_code == 400
    assert response.json() == {
        'sell': ['This field is required.'],
        'buy': ['This field is required.'],
        'source': ['This field is required.']}


def test_post_rate_list_valid_data(api_client_auth):
    initial_count = Rate.objects.count()
    source = Source.objects.create(name='Test', code_name='test')
    payload = {
        'buy': '37.00',
        'sell': '38.00',
        'source': source.id
    }
    response = api_client_auth.post(reverse('currency_api:rate-list'), data=payload)
    assert response.status_code == 201
    assert Rate.objects.count() == initial_count + 1


def test_post_rate_list_invalid_data(api_client_auth):
    source = Source.objects.create(name='Test', code_name='test')
    payload = {
        'buy': '37.000',
        'sell': '38.00',
        'source': source.id,
    }
    response = api_client_auth.post(reverse('currency_api:rate-list'), data=payload)
    assert response.status_code == 400
    assert response.json() == {
        'buy': ['Ensure that there are no more than 2 decimal places.']
    }
