from django.urls import reverse


def test_get_rate_latest(api_client_auth):
    response = api_client_auth.get(reverse('currency_api:rate-latest'))
    assert response.status_code == 200
    assert response.json()
